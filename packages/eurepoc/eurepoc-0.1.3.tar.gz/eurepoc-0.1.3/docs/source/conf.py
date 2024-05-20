import os
import sys

# Add the project root directory to the PYTHONPATH
sys.path.insert(0, os.path.abspath('../..'))

# Verify the added path (optional for debugging)
print("Project root added to PYTHONPATH:", os.path.abspath('../..'))

# Project information
project = 'EuRepoC'
author = 'Camille Borrett'
release = '0.1.2'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx_autodoc_typehints',
]

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'special-members': True,
    'inherited-members': True,
    'show-inheritance': True,
    'exclude-members': '__dict__,__weakref__,__module__, __init__',
}

templates_path = ['_templates']
exclude_patterns = []

# HTML output options
html_theme = 'python_docs_theme'
html_static_path = ['_static']
