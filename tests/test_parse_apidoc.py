"""Tests for the apidoc parser."""

import json
import tempfile
from pathlib import Path

import pytest

from proxmox_api.parse_apidoc import (
    Endpoint,
    Parameter,
    _extract_json_from_js,
    group_by_section,
    parse_apidoc,
)

SAMPLE_APIDOC = """
{
  "children": [
    {
      "info": {
        "DELETE": {
          "description": "Delete replication job.",
          "method": "DELETE",
          "name": "delete",
          "parameters": {
            "additionalProperties": 0,
            "properties": {
              "id": {
                "description": "Replication Job ID.",
                "type": "string"
              },
              "force": {
                "default": 0,
                "description": "Force removal.",
                "optional": 1,
                "type": "boolean"
              }
            }
          },
          "returns": { "type": "null" }
        },
        "GET": {
          "description": "Read replication job config.",
          "method": "GET",
          "name": "read",
          "parameters": {
            "additionalProperties": 0,
            "properties": {
              "id": {
                "description": "Replication Job ID.",
                "type": "string"
              }
            }
          },
          "returns": { "type": "object" }
        }
      },
      "leaf": 1,
      "path": "/cluster/replication/{id}",
      "text": "{id}"
    }
  ],
  "info": {
    "GET": {
      "description": "List replication jobs.",
      "method": "GET",
      "name": "index",
      "parameters": { "additionalProperties": 0, "properties": {} },
      "returns": { "type": "array" }
    },
    "POST": {
      "description": "Create replication job.",
      "method": "POST",
      "name": "create",
      "parameters": {
        "additionalProperties": 0,
        "properties": {
          "id": {
            "description": "Replication Job ID.",
            "type": "string"
          },
          "target": {
            "description": "Target node.",
            "type": "string"
          },
          "type": {
            "description": "Section type.",
            "enum": ["local"],
            "type": "string"
          },
          "comment": {
            "description": "Comment.",
            "optional": 1,
            "type": "string"
          }
        }
      },
      "returns": { "type": "null" }
    }
  },
  "leaf": 0,
  "path": "/cluster/replication",
  "text": "replication"
},
{
  "info": {
    "GET": {
      "description": "API version details.",
      "method": "GET",
      "name": "version",
      "parameters": { "additionalProperties": 0, "properties": {} },
      "returns": { "type": "object" }
    }
  },
  "leaf": 1,
  "path": "/version",
  "text": "version"
}
"""


@pytest.fixture
def sample_file(tmp_path: Path) -> Path:
    p = tmp_path / "apidoc.json"
    p.write_text(SAMPLE_APIDOC.strip(), encoding="utf-8")
    return p


def test_parse_returns_all_endpoints(sample_file: Path) -> None:
    endpoints = parse_apidoc(sample_file)
    # 2 on /cluster/replication + 2 on /cluster/replication/{id} + 1 on /version
    assert len(endpoints) == 5


def test_parse_endpoint_methods(sample_file: Path) -> None:
    endpoints = parse_apidoc(sample_file)
    methods = {(ep.path, ep.method) for ep in endpoints}
    assert ("/cluster/replication", "GET") in methods
    assert ("/cluster/replication", "POST") in methods
    assert ("/cluster/replication/{id}", "GET") in methods
    assert ("/cluster/replication/{id}", "DELETE") in methods
    assert ("/version", "GET") in methods


def test_path_params_detected(sample_file: Path) -> None:
    endpoints = parse_apidoc(sample_file)
    ep = next(
        e for e in endpoints
        if e.path == "/cluster/replication/{id}" and e.method == "GET"
    )
    assert len(ep.path_params) == 1
    assert ep.path_params[0].name == "id"
    assert ep.path_params[0].is_path_param is True
    assert ep.path_params[0].optional is False


def test_optional_params(sample_file: Path) -> None:
    endpoints = parse_apidoc(sample_file)
    ep = next(
        e for e in endpoints
        if e.path == "/cluster/replication/{id}" and e.method == "DELETE"
    )
    opt = [p for p in ep.parameters if p.optional]
    assert any(p.name == "force" for p in opt)


def test_required_params(sample_file: Path) -> None:
    endpoints = parse_apidoc(sample_file)
    ep = next(
        e for e in endpoints
        if e.path == "/cluster/replication" and e.method == "POST"
    )
    required_names = {p.name for p in ep.required_params}
    assert "id" in required_names
    assert "target" in required_names
    assert "type" in required_names
    assert "comment" not in required_names


def test_enum_param(sample_file: Path) -> None:
    endpoints = parse_apidoc(sample_file)
    ep = next(
        e for e in endpoints
        if e.path == "/cluster/replication" and e.method == "POST"
    )
    type_param = next(p for p in ep.parameters if p.name == "type")
    assert type_param.enum == ["local"]


def test_group_by_section(sample_file: Path) -> None:
    endpoints = parse_apidoc(sample_file)
    groups = group_by_section(endpoints)
    assert "cluster" in groups
    assert "version" in groups
    assert len(groups["cluster"]) == 4
    assert len(groups["version"]) == 1


def test_parameter_python_name() -> None:
    p = Parameter(
        name="force-cpu",
        type="string",
        description="Override CPU.",
    )
    assert p.python_name == "force_cpu"


def test_parameter_python_type() -> None:
    assert Parameter(name="x", type="string", description="").python_type == "str"
    assert Parameter(name="x", type="integer", description="").python_type == "int"
    assert Parameter(name="x", type="boolean", description="").python_type == "bool"
    assert Parameter(name="x", type="number", description="").python_type == "float"


def test_returns_type(sample_file: Path) -> None:
    endpoints = parse_apidoc(sample_file)
    ep = next(e for e in endpoints if e.path == "/version")
    assert ep.returns_type == "object"


# --- JS extraction tests ---

SAMPLE_JS = 'const apiSchema = [{"path": "/version", "info": {"GET": {"description": "Version", "method": "GET", "name": "version", "parameters": {"properties": {}}, "returns": {"type": "object"}}}, "leaf": 1, "text": "version"}];'


def test_extract_json_from_js() -> None:
    json_text = _extract_json_from_js(SAMPLE_JS)
    data = json.loads(json_text)
    assert isinstance(data, list)
    assert data[0]["path"] == "/version"


def test_extract_json_from_js_no_semicolon() -> None:
    js = 'const apiSchema = [{"path": "/test"}]'
    json_text = _extract_json_from_js(js)
    data = json.loads(json_text)
    assert data[0]["path"] == "/test"


def test_parse_apidoc_js_file(tmp_path: Path) -> None:
    p = tmp_path / "apidoc.js"
    p.write_text(SAMPLE_JS, encoding="utf-8")
    endpoints = parse_apidoc(p)
    assert len(endpoints) == 1
    assert endpoints[0].path == "/version"
    assert endpoints[0].method == "GET"


def test_extract_json_from_js_invalid() -> None:
    with pytest.raises(ValueError, match="Could not find JSON array"):
        _extract_json_from_js("var x = 42;")
