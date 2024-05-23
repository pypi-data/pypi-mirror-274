#!/usr/bin/env python
"""
All things specific to Python (pyproject.toml, PyPI, etc.)
"""

import difflib
import logging
import pathlib
import subprocess
import tomllib
from urllib.parse import quote as urlquote

import requests
import tomli_w
import tomli_w._writer
from spdx_license_list import LICENSES as SPDX_LICENSES
from trove_classifiers import classifiers as py_classifiers

from ..file import update_content
from .venv import VirtualEnvironment

LOGGER = logging.getLogger(__name__)


def get_pypi_url(name):
    """
    Get the URL to the project's page on PyPI if it exists.

    Args:
        name:
            The project name.

    Returns:
        The project URL, or None if it does not exist.
    """
    timeout = 5
    url = f"https://pypi.org/pypi/{urlquote(name)}/json"
    LOGGER.debug("Querying %s", url)
    resp = requests.get(url, timeout=timeout).json()
    try:
        return resp["info"]["package_url"]
    except KeyError:
        return None


def get_license_classifier(spdx_id):
    """
    Get the Python license classifier for the given SPDX license ID.

    Args:
        spdx_id:
            The SPXD license ID.

    Returns:
        The corresponding Python trove classifier if found, else None.
    """
    spdx_data = SPDX_LICENSES.get(spdx_id)
    if not spdx_data:
        LOGGER.warning("%s is not a recognized SPDX license ID.", spdx_id)
        return None
    name = spdx_data.name
    if spdx_data.osi_approved:
        expected = f"License :: OSI Approved :: {name}"
    else:
        expected = "License :: {name}"
    if expected in py_classifiers:
        return expected
    closest = difflib.get_close_matches(expected, py_classifiers)
    if not closest:
        LOGGER.warning(
            "Failed to map SPDX license ID %s to a Python trove classifier.", spdx_id
        )
        return None
    return closest[0]


def _join_names(given_names, family_names):
    """
    Join given and family names to a single string.

    Args:
        given_names:
            The given names.

        family_names:
            The family names.

    Returns:
        A string with the joined names.
    """
    if given_names and family_names:
        return f"{given_names} {family_names}"
    if given_names:
        return str(given_names)
    if family_names:
        return str(family_names)
    return None


def update_pyproject_toml(project):
    """
    Update the URLs in a pyproject.toml file.

    Args:
        project:
            The Project instance.
    """
    path = project.pyproject_toml_path
    data = tomllib.loads(path.read_text(encoding="utf-8"))

    urls = data["project"]["urls"]
    #  urls.clear()
    urls.update(project.urls)

    data["project"]["authors"] = [
        {
            "name": _join_names(author["given-names"], author["family-names"]),
            "email": author["email"],
        }
        for author in project.config.config["authors"]
    ]

    classifiers = set(
        classifier
        for classifier in data["project"].get("classifiers", [])
        if not classifier.startswith("License :: ")
    )

    spdx_id = project.spdx_license
    if spdx_id:
        license_classifier = get_license_classifier(spdx_id)
        if license_classifier:
            classifiers.add(license_classifier)
    else:
        LOGGER.warning("No license detected for project.")

    data["project"]["classifiers"] = sorted(classifiers)

    content = tomli_w.dumps(data, multiline_strings=True)
    update_content(content, path)
    return urls


def get_version(project_dir):
    """
    Get the version of a project from its directory.

    This will create a temporary virtual environment and install the project in
    it to get the version. This ensures that VCS-versions are correctly handled.

    This should not be necessary but at the time or writing the current version
    of CodeMetaPy fails to detect versions.
    """
    project_dir = pathlib.Path(project_dir).resolve()
    with VirtualEnvironment() as venv:
        venv.run_pip_in_venv(["install", "--no-deps", "-U", str(project_dir)])

        data = tomllib.loads(
            (project_dir / "pyproject.toml").read_text(encoding="utf-8")
        )
        name = data["project"]["name"]
        return venv.run_python_in_venv(
            [
                "-c",
                f'from importlib.metadata import version; print(version("{name}"))'
            ],
            capture_output=True
        ).stdout.decode().strip()
