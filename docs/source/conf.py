# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import inspect

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import subprocess
import sys

sys.path.insert(0, "..")


# -- Project information -----------------------------------------------------

project = "wearipedia"
copyright = "2022, Rodrigo Castellon"
author = "Rodrigo Castellon"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.linkcode",
    "sphinx.ext.mathjax",
    "numpydoc",
    "sphinx_reredirects",
    "sphinx_copybutton",
    "sphinx.ext.graphviz",
    "matplotlib.sphinxext.plot_directive",
    "myst_parser",
    "sphinx.ext.intersphinx",
    "sphinx.ext.doctest",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "alabaster"
# html_theme = "insegel"
html_permalinks_icon = "§"
html_theme = "insipid"
# html_theme = 'bizstyle'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]
html_static_path = []
commit_hash_filepath = "../commit_hash.txt"

commit_hash = None
if os.path.isfile(commit_hash_filepath):
    with open(commit_hash_filepath) as f:
        commit_hash = f.readline()

# Get commit hash from the external file.
if not commit_hash:
    try:
        commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"])
        commit_hash = commit_hash.decode("ascii")
        commit_hash = commit_hash.rstrip()
    except:
        import warnings

        warnings.warn(
            "Failed to get the git commit hash as the command "
            "'git rev-parse HEAD' is not working. The commit hash will be "
            "assumed as the Wearipedia master, but the lines may be misleading "
            "or nonexistent as it is not the correct branch the doc is "
            "built with. Check your installation of 'git' if you want to "
            "resolve this warning."
        )
        commit_hash = "master"

fork = "Stanford-Health"
blobpath = f"https://github.com/{fork}/wearipedia/blob/{commit_hash}/wearipedia/"

root_doc = "source/index"


def linkcode_resolve(domain, info):
    """Determine the URL corresponding to Python object."""
    if domain != "py":
        return

    modname = info["module"]
    fullname = info["fullname"]

    submod = sys.modules.get(modname)
    if submod is None:
        return

    obj = submod
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except Exception:
            return

    # strip decorators, which would resolve to the source of the decorator
    # possibly an upstream bug in getsourcefile, bpo-1764286
    try:
        unwrap = inspect.unwrap
    except AttributeError:
        pass
    else:
        obj = unwrap(obj)

    try:
        fn = inspect.getsourcefile(obj)
    except Exception:
        fn = None
    if not fn:
        return

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""

    # fn = os.path.relpath(fn, start=os.path.dirname(sympy.__file__))
    fn = os.path.relpath(fn)
    return blobpath + fn + linespec
