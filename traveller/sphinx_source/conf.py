# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# import sphinx_rtd_theme

# sys.path.insert(0, os.path.abspath('.'))
import pathlib


# -- Project information -----------------------------------------------------

project = 'Traveller'
copyright = '2021, FlaskCon'
author = 'FlaskCon'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
]


source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
html_context = {
    "project_links": [
        "Source Code",
        "https://github.com/<name>/<project>",
        "Issue Tracker",
        "https://github.com/<name>/<project>/issues",
    ]
}
html_logo = "icon.png"

# html_sidebars = {
#     "**": ["about.html", "relations.html", "navigation.html", "searchbox.html"]
# }

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
html_theme_options = {
    "github_repo": "<name>/<project>",
    "fixed_sidebar": "true",
}
# html_theme = 'sphinx_rtd_theme'
# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

pygments_style = 'sphinx'

# Custom codes
def restructure_readme():
    """
    Include README.md in Sphinx documentation

Restructures existing README.md file and creates a new readme.md file in sphinx_source folder.
"""
    # The Path to README.md that already exists in root folder
    readme_path = pathlib.Path(__file__).parent.parent.parent.resolve() / "README.md"
    # We copy a modified version here
    readme_target = pathlib.Path(__file__).parent / "readme.md"

    with readme_target.open("w") as outf:
        # Change the title to "Readme"
        outf.write(
            "\n\n".join(["# Readme",])
        )
        lines = []
        for line in readme_path.read_text().split("\n"):
            if line.startswith(r"![](icon.png)") or line.startswith("# "):
                # Skip traveller's icon image, because we have the same image on the docs
                # Skip title, because we now use "Readme"
                continue

            lines.append(line)
        outf.write("\n".join(lines))
    
    pass
restructure_readme()
