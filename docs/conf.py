# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add the project root so autodoc can find the package.
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "proxmox_api"
copyright = "2025, proxmox_api contributors"
author = "proxmox_api contributors"
release = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Autodoc settings --------------------------------------------------------

autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# -- Napoleon settings (Google / NumPy docstrings) ---------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True

# -- Intersphinx mapping -----------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
