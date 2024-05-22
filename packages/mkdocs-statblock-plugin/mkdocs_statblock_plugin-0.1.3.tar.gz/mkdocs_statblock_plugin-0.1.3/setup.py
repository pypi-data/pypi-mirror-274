from setuptools import setup, find_packages

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mkdocs_statblock_plugin",
    version="0.1.3",
    description="MkDocs plugin to format YAML within statblock superfences as HTML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johannes-z/mkdocs-statblock-plugin.git",
    author="Johannes Zwirchmayr",
    author_email="johannes.zwirchmayr@gmail.com",
    packages=find_packages(),
    package_data={"mkdocs_statblock_plugin": ["template.html"]},
    install_requires=[
        "mkdocs>=1.6.0",
        "pyyaml",
    ],
    python_requires=">=3.6",
    entry_points={
        "mkdocs.plugins": [
            "statblocks = mkdocs_statblock_plugin.mkdocs_statblock_plugin:StatBlockPlugin"
        ]
    },
)
