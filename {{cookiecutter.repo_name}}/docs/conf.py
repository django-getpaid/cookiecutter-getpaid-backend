"""Sphinx configuration for {{ cookiecutter.repo_name }}."""

project = "{{ cookiecutter.repo_name }}"
author = "{{ cookiecutter.full_name }}"
project_copyright = "{% now 'local', '%Y' %}, {{ cookiecutter.full_name }}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

autodoc_typehints = "description"
autodoc_member_order = "bysource"
autosummary_generate = True

html_theme = "furo"
html_title = "{{ cookiecutter.repo_name }}"

myst_enable_extensions = [
    "colon_fence",
    "fieldlist",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
