from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

docs_require = [
    "markdown==3.3.7",
    "markdown-include==0.7.0",
    "mkdocs==1.3.1",
    "mkdocs-material==8.5.3",
    "mkdocstrings-python==0.7.1",
    "mkdocs-include-markdown-plugin==3.8.1",
    "mkdocs-git-revision-date-localized-plugin==1.1.0",
    "griffe==0.29.1",
]

tests_require = [
    "mypy==0.971",
    "pylint==2.15.3",
    "pytest==7.1.3",
    "pytest-cov==3.0.0",
    "coverage==6.4.4",
    "coverage-badge==1.1.0",
    "flake8==5.0.4",
]

build_require = [
    "setuptools==65.3.0"
]

all_requirements = required + docs_require + tests_require + build_require

setup(
    name="fiqus",
    version="2024.5.2",
    author="STEAM Team",
    author_email="steam-team@cern.ch",
    description="Source code for STEAM FiQuS tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/steam/fiqus",
    keywords=["STEAM", "FiQuS", "CERN"],
    install_requires=required,
    extras_require={
        "all": all_requirements,
        "docs": docs_require,
        "tests": tests_require,
        "build": build_require,
    },
    python_requires=">=3.11",
    packages=find_packages(),
    package_data={
        "fiqus": [
            "**/*.pro",
        ]
    },
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3.11"],
)
