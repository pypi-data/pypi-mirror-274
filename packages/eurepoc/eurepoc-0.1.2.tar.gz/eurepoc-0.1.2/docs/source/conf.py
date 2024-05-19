import os
import sys

# Add the project root directory to the PYTHONPATH
sys.path.insert(0, os.path.abspath('../..'))

# Verify the added path (optional for debugging)
print("Project root added to PYTHONPATH:", os.path.abspath('../..'))

# Project information
project = 'EuRepoC'
author = 'Camille Borrett'
release = '0.1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary'
]

templates_path = ['_templates']
exclude_patterns = []

# HTML output options
html_theme = 'python_docs_theme'
html_static_path = ['_static']

"""# Ensure the theme is available
try:
    import sphinx_rtd_theme
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
except ImportError:
    html_theme = 'default'
    html_theme_path = []
"""