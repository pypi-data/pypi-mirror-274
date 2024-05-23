#!/usr/bin/env python
"""
Project class.
"""

import logging

import spdx_matcher
from spdx_license_list import LICENSES as SPDX_LICENSES

from .citation import Citation
from .common import choose
from .codemeta.codemeta import CodeMeta
from .codemeta.pyproject import PyprojectCodeMeta
from .config import Config
from .gitlab.ci import GitlabCI
from .gitlab.repo import GitlabRepo
from .python.common import update_pyproject_toml, get_version
from .readme import ReadmeInserter


LOGGER = logging.getLogger(__name__)


class Project:
    """
    Project class.
    """

    def __init__(self, path, **config_kwargs):
        """
        Args:
            path:
                The path to the project.

            **config_kwargs:
                Keyword arguments passed through to Config.
        """
        self.git_repo = GitlabRepo(path)
        self.gitlab_ci = GitlabCI(self)
        self.config = Config(self.git_repo.path, **config_kwargs)
        self.codemeta = CodeMeta(self)

    @property
    def readme_md_path(self):
        """
        The README.md path.
        """
        return self.git_repo.path / "README.md"

    @property
    def pyproject_toml_path(self):
        """
        The pyproject.toml path.
        """
        return self.git_repo.path / "pyproject.toml"

    @property
    def license_txt_path(self):
        """
        The path to the LICENSE.txt file.
        """
        return self.git_repo.path / "LICENSE.txt"

    @property
    def spdx_license(self):
        """
        The detected SPDX license name.
        """
        config_license = self.config.get("license")
        if config_license:
            LOGGER.info("Using license from configuration file: %s", config_license)
            if config_license not in SPDX_LICENSES:
                LOGGER.warning('"%s" is not a recognized SPDX license', config_license)
            return config_license
        path = self.license_txt_path
        LOGGER.info("Attempting to detect license from %s", path)
        try:
            detected, percent = spdx_matcher.analyse_license_text(
                path.read_text(encoding="utf-8")
            )
        except FileNotFoundError:
            LOGGER.error("No license file found at %s", path)
            return None
        licenses = list(detected["licenses"])
        if not licenses:
            LOGGER.error("Failed to detect license in %s", path)
            return None
        lic = choose(licenses)
        if percent < 0.9:
            LOGGER.warning(
                "Detected %s license in %s but certainty is only %(0.0f) %",
                lic,
                path,
                percent * 100.0,
            )
        return lic

    @property
    def codemeta_json_path(self):
        """
        The path to the codemeta.json file.
        """
        return self.git_repo.path / "codemeta.json"

    @property
    def citation_cff_path(self):
        """
        The path to the CITATION.cff file.
        """
        return self.git_repo.path / "CITATION.cff"

    @property
    def urls(self):
        """
        A dict of URLs for the project.
        """
        host, namespace, name = self.git_repo.parsed_origin
        homepage = f"https://{host}/{namespace}/{name}"

        urls = {}
        urls["Homepage"] = homepage
        urls["Source"] = f"{homepage}.git"
        if self.gitlab_ci.data.get("pages"):
            pages_fmt = self.config.get("gitlab", "pages_urls", host)
            if pages_fmt:
                urls["Documentation"] = pages_fmt.format(namespace=namespace, name=name)
        urls["Issues"] = f"{homepage}/-/issues"
        return urls

    def update(self):
        """
        Update project metadata.
        """
        if self.pyproject_toml_path.exists():
            # TODO
            # Find a better way to automate version management while updating
            # the files. The issue is that prometa has to modify several files
            # but these modifications are visible to the VCS. This causes tools
            # such as setuptools-scm to miscalculate the version because it
            # doesn't know that the changes will be merged into the previous
            # commit.
            version = get_version(self.git_repo.path)
            update_pyproject_toml(self)
            PyprojectCodeMeta(self).update(version=version)

        if self.codemeta_json_path.exists():
            Citation(self).update()

        readme_inserter = ReadmeInserter(self)
        readme_inserter.update(self.readme_md_path)

        self.gitlab_ci.update()

    @property
    def name(self):
        """
        The project name. It will use the value in codemeta.name if it exists,
        otherwise it will use the name of the project's directory.
        """
        name = self.codemeta.name
        if name is not None:
            return name
        return self.git_repo.path.name
