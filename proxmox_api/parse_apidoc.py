"""Parser tool for Proxmox VE API documentation.

Can read from a local apidoc.json file or download the schema directly
from the Proxmox documentation site (apidoc.js).
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests

APIDOC_JS_URL = "https://pve.proxmox.com/pve-docs/api-viewer/apidoc.js"


@dataclass
class Parameter:
    name: str
    type: str
    description: str
    optional: bool = True
    default: Any = None
    enum: list[str] | None = None
    minimum: int | float | None = None
    maximum: int | float | None = None
    pattern: str | None = None
    format: str | None = None
    is_path_param: bool = False

    @property
    def python_name(self) -> str:
        """Convert parameter name to valid Python identifier."""
        return self.name.replace("-", "_")

    @property
    def python_type(self) -> str:
        """Map JSON-schema type to Python type hint."""
        mapping = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "list",
            "object": "dict",
            "null": "None",
        }
        return mapping.get(self.type, "Any")


@dataclass
class Endpoint:
    path: str
    method: str
    name: str
    description: str
    parameters: list[Parameter] = field(default_factory=list)
    returns_type: str = "Any"
    protected: bool = False
    proxyto: str | None = None

    @property
    def path_params(self) -> list[Parameter]:
        return [p for p in self.parameters if p.is_path_param]

    @property
    def query_or_body_params(self) -> list[Parameter]:
        return [p for p in self.parameters if not p.is_path_param]

    @property
    def required_params(self) -> list[Parameter]:
        return [p for p in self.parameters if not p.optional]

    @property
    def optional_params(self) -> list[Parameter]:
        return [p for p in self.parameters if p.optional]


def _extract_path_param_names(path: str) -> set[str]:
    """Extract parameter names from URL path template like /nodes/{node}."""
    return set(re.findall(r"\{(\w+)\}", path))


def _parse_parameter(name: str, spec: dict, path_params: set[str]) -> Parameter:
    return Parameter(
        name=name,
        type=spec.get("type", "string"),
        description=spec.get("description", ""),
        optional=bool(spec.get("optional", 0)) and name not in path_params,
        default=spec.get("default"),
        enum=spec.get("enum"),
        minimum=spec.get("minimum"),
        maximum=spec.get("maximum"),
        pattern=spec.get("pattern"),
        format=spec.get("format") if isinstance(spec.get("format"), str) else None,
        is_path_param=name in path_params,
    )


def _parse_endpoint(path: str, method: str, info: dict) -> Endpoint:
    path_param_names = _extract_path_param_names(path)
    properties = info.get("parameters", {}).get("properties", {})

    params = [
        _parse_parameter(name, spec, path_param_names)
        for name, spec in properties.items()
    ]
    # Sort: path params first (in path order), then required, then optional
    path_order = re.findall(r"\{(\w+)\}", path)
    path_index = {name: i for i, name in enumerate(path_order)}

    def sort_key(p: Parameter) -> tuple:
        if p.is_path_param:
            return (0, path_index.get(p.name, 99))
        if not p.optional:
            return (1, p.name)
        return (2, p.name)

    params.sort(key=sort_key)

    returns_type = info.get("returns", {}).get("type", "Any")

    return Endpoint(
        path=path,
        method=method,
        name=info.get("name", ""),
        description=info.get("description", ""),
        parameters=params,
        returns_type=returns_type,
        protected=bool(info.get("protected", 0)),
        proxyto=info.get("proxyto"),
    )


def _walk_tree(node: dict, endpoints: list[Endpoint]) -> None:
    """Recursively walk the API doc tree and collect endpoints."""
    path = node.get("path", "")
    info = node.get("info", {})

    for method, method_info in info.items():
        if method in ("GET", "POST", "PUT", "DELETE"):
            endpoints.append(_parse_endpoint(path, method, method_info))

    for child in node.get("children", []):
        _walk_tree(child, endpoints)


def _extract_json_from_js(js_content: str) -> str:
    """Extract the JSON array from the apidoc.js JavaScript source.

    The file has the form: ``const apiSchema = [ ... ];`` followed by
    additional JavaScript code. We use incremental JSON parsing to
    extract just the array.
    """
    match = re.search(r"=\s*(\[)", js_content)
    if not match:
        raise ValueError("Could not find JSON array in apidoc.js content")

    # Use raw_decode to parse only the JSON array, ignoring trailing JS code
    decoder = json.JSONDecoder()
    json_start = match.start(1)
    _, end_idx = decoder.raw_decode(js_content, json_start)
    return js_content[json_start:end_idx]


def download_apidoc(
    url: str = APIDOC_JS_URL,
    save_to: str | Path | None = None,
) -> list[dict]:
    """Download apidoc.js from the Proxmox docs and extract the schema.

    Args:
        url: URL to the apidoc.js file.
        save_to: If provided, save the extracted JSON to this path.

    Returns:
        The parsed API schema as a list of dicts.
    """
    print(f"Downloading {url} ...")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    json_text = _extract_json_from_js(resp.text)
    data = json.loads(json_text)

    if save_to:
        save_path = Path(save_to)
        save_path.write_text(json_text, encoding="utf-8")
        print(f"Saved schema to {save_path}")

    return data


def _load_schema(source: str | Path) -> list[dict]:
    """Load the API schema from a file path or URL.

    Supports:
    - Local .json file (apidoc.json format)
    - Local .js file (apidoc.js format)
    - HTTP/HTTPS URL to apidoc.js
    """
    source_str = str(source)

    if source_str.startswith(("http://", "https://")):
        return download_apidoc(source_str)

    filepath = Path(source)
    content = filepath.read_text(encoding="utf-8").strip()

    if filepath.suffix == ".js":
        json_text = _extract_json_from_js(content)
        return json.loads(json_text)

    # Legacy apidoc.json format: comma-separated objects without outer brackets
    if not content.startswith("["):
        content = "[" + content + "]"
    return json.loads(content)


def parse_apidoc(source: str | Path) -> list[Endpoint]:
    """Parse an API doc source and return a list of all API endpoints.

    Args:
        source: Path to apidoc.json, apidoc.js, or a URL to apidoc.js.
    """
    data = _load_schema(source)

    endpoints: list[Endpoint] = []
    for root_node in data:
        _walk_tree(root_node, endpoints)

    return endpoints


def group_by_section(endpoints: list[Endpoint]) -> dict[str, list[Endpoint]]:
    """Group endpoints by top-level API section (cluster, nodes, etc.)."""
    groups: dict[str, list[Endpoint]] = {}
    for ep in endpoints:
        parts = ep.path.strip("/").split("/")
        section = parts[0] if parts else "root"
        groups.setdefault(section, []).append(ep)
    return groups


def print_summary(endpoints: list[Endpoint]) -> None:
    """Print a human-readable summary of all endpoints."""
    groups = group_by_section(endpoints)
    total = len(endpoints)
    print(f"Proxmox VE API - {total} endpoints\n")
    for section, eps in sorted(groups.items()):
        print(f"/{section} ({len(eps)} endpoints)")
        for ep in eps[:5]:
            req = [p.name for p in ep.required_params if not p.is_path_param]
            opt_count = len(ep.optional_params)
            print(
                f"  {ep.method:6s} {ep.path}"
                + (f"  required={req}" if req else "")
                + (f"  +{opt_count} optional" if opt_count else "")
            )
        if len(eps) > 5:
            print(f"  ... and {len(eps) - 5} more")
        print()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Parse and summarize the Proxmox VE API documentation."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default=None,
        help=(
            "Path to apidoc.json or apidoc.js, or a URL. "
            "Defaults to downloading from the Proxmox docs site."
        ),
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the latest apidoc.js from the Proxmox docs site.",
    )
    parser.add_argument(
        "--save",
        metavar="PATH",
        default=None,
        help="Save the downloaded schema to a local JSON file.",
    )
    args = parser.parse_args()

    if args.download or args.source is None:
        source = APIDOC_JS_URL
    else:
        source = args.source
        if not str(source).startswith(("http://", "https://")):
            path = Path(source)
            if not path.exists():
                print(f"Error: {path} not found", file=sys.stderr)
                sys.exit(1)

    if args.save and (args.download or args.source is None):
        download_apidoc(save_to=args.save)

    endpoints = parse_apidoc(source)
    print_summary(endpoints)


if __name__ == "__main__":
    main()
