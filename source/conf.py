from datetime import date

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Zhaocheng Che's Blog"
copyright = '2025, Zhaocheng Che, chezhaocheng[AT]outlook.com'
author = 'Zhaocheng Che'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "ablog", 
    "myst_parser", 
    "sphinx_rtd_theme"
]

myst_enable_extensions = [
    "dollarmath",
    "colon_fence"
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# Automatically insert today's date
release = date.today().strftime("%Y-%m-%d")
version = release  # optional, same as release

# Ablog configuration

blog_title = "Zhaocheng Che's Blog"
blog_path = "blog"
blog_post_pattern = "posts/*"

html_sidebars = {
    "**": [
        "about.html",
        "recentposts.html",
        "archives.html",
        "tagcloud.html",
        "categories.html",
    ]
}
