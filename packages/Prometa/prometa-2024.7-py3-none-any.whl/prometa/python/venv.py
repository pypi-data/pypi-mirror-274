#!/usr/bin/env python
"""
Virtual environment functions.
"""

import contextlib
import logging
import pathlib
import sysconfig
import tempfile
import subprocess
import sys


LOGGER = logging.getLogger(__name__)


class VirtualEnvironment(contextlib.ExitStack):
    """
    Context manager for temporary Python virtual environments.
    """
    def __init__(self, update_pip=False, inherit=False):
        """
        Args:
            update_pip:
                If True, update pip in the virtual environment.

            inherit:
                If True, create a .pth file to inherit packages from the parent
                environment.
        """
        super().__init__()

        self.update_pip = update_pip
        self.inherit = inherit

        self.tmp_dir = None
        self.venv_exe = None
        self.venv_dir = None

    @property
    def sys_exe(self):
        """
        The system Python executable.
        """
        return pathlib.Path(sys.executable).resolve()

    def run_python_in_venv(self, args, **kwargs):
        """
        Run a Python command in the virtual environment.

        Args:
            args:
                The arguments to pass to the Python interpretter.

            **kwargs:
                Keyword arguments passed through to subprocess.run.

        Returns:
            The return value of subprocess.run.
        """
        cmd = [str(self.venv_exe), *args]
        kwargs.setdefault("check", True)
        LOGGER.debug("Running command: %s", cmd)
        return subprocess.run(cmd, **kwargs)  # pylint: disable=subprocess-run-check

    def run_pip_in_venv(self, args, **kwargs):
        """
        Run a pip command in the virtual environment. This is a wrapper around
        run_python_in_venv().

        Args:
            args:
                The arguments to pass to pip.

            **kwargs:
                Keyword arguments passed through to run_python_in_venv().

        Returns:
            The return value of run_python_in_venv().
        """
        return self.run_python_in_venv(["-m", "pip", *args], **kwargs)

    def __enter__(self):
        self.tmp_dir = pathlib.Path(
            self.enter_context(tempfile.TemporaryDirectory())
        )
        sys_exe = self.sys_exe
        self.venv_dir = self.tmp_dir / "venv"
        self.venv_exe = self.venv_dir / "bin" / sys_exe.name

        cmd = [str(sys_exe), "-m", "venv", str(self.venv_dir)]
        LOGGER.debug("Creating temporary virtual environment: %s", cmd)
        subprocess.run(cmd, check=True)

        if self.update_pip:
            LOGGER.debug("Updating pip in virtual environment: %s", cmd)
            self.run_pip_in_venv(["install", "-U", "pip"])

        if self.inherit:
            LOGGER.debug("Locating virtual environment's purelib directory.")
            child_purelib = (
                self.run_python_in_venv(
                    [
                        "-c",
                        'import sysconfig; print(sysconfig.get_paths()["purelib"])',
                    ],
                    stdout=subprocess.PIPE
                ).stdout.decode().strip()
            )
            parent_purelib = sysconfig.get_paths()["purelib"]
            pth_path = pathlib.Path(child_purelib) / "parent.pth"
            pth_path.write_text(parent_purelib, encoding="utf-8")

        return self
