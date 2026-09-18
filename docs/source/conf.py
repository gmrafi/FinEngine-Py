import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

project = "FinEngine"
copyright = "2026, Md Golam Mubasshir Rafi / CFSBR"
author = "Md Golam Mubasshir Rafi"
release = "0.1.1"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
