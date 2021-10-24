# Packages/LSP-terraform/plugin.py

import sublime

from LSP.plugin import AbstractPlugin, register_plugin, unregister_plugin
from LSP.plugin.core.typing import Any

import os
import sys
import shutil
import gzip
import urllib.request
import json

TAG = 'v0.23.0'
GITHUB_RELEASE_API = 'https://api.github.com/repos/hashicorp/terraform-ls/releases'
GITHUB_RELEASE_DOWNLOAD_BASE = 'https://github.com/hashicorp/terraform-ls/releases/download/{tag}/terraform-ls_{tag}_{platform}_{arch}.zip'


def platform() -> str:
    os_platform = sys.platform
    if os_platform == "windows":
        return "windows"
    elif os_platform == "darwin":
        return "darwin"
    elif os_platform == "linux":
        return "linux"
    elif os_platform == "freebsd8":
        return "freebsd8"
    else:
        return "unknown-platform"


def arch() -> str:
    if sublime.arch() == "x32":
        return "x32"
    elif sublime.arch() == "x64":
        return "x64"
    elif sublime.arch() == "arm64":
        return "arm64"
    else:
        return "unknown-arch"


class Terraform(AbstractPlugin):

    @classmethod
    def name(cls):
        return "terraform"

    @classmethod
    def basedir(cls) -> str:
        return os.path.join(cls.storage_path(), __package__)

    @classmethod
    def server_version(cls):
        return TAG

    @classmethod
    def current_server_version(cls) -> str:
        with open(os.path.join(cls.basedir(), "VERSION"), "r") as fp:
            return fp.read()

    @classmethod
    def _is_terraform_ls_installed(cls) -> bool:
        terraform_ls_binary = get_setting(
            'command', [os.path.join(cls.basedir(), 'terraform-ls')])
        return _is_binary_available(terraform_ls_binary[0])

    @classmethod
    def needs_update_or_installation(cls) -> bool:
        try:
            return not cls._is_terraform_ls_installed() or (cls.current_server_version() != cls.server_version())
        except OSError:
            return True

    @classmethod
    def install_or_update(cls) -> None:
        try:
            if os.path.isdir(cls.basedir()):
                shutil.rmtree(cls.basedir())
            os.makedirs(cls.basedir(), exist_ok=True)
            version = cls.server_version()
            url = GITHUB_RELEASE_DOWNLOAD_BASE.format(
                tag=TAG, arch=arch(), platform=platform())
            gzipfile = os.path.join(cls.basedir(), "terraform-ls.gz")
            serverfile = os.path.join(
                cls.basedir(),
                "terraform-ls.exe" if sublime.platform() == "windows" else "terraform-ls"
            )
            with urllib.request.urlopen(url) as fp:
                with open(gzipfile, "wb") as f:
                    f.write(fp.read())

            with gzip.open(gzipfile, "rb") as fp:
                with open(serverfile, "wb") as f:
                    f.write(fp.read())

            os.remove(gzipfile)
            os.chmod(serverfile, 0o744)

            with open(os.path.join(cls.basedir(), "VERSION"), "w") as fp:
                fp.write(version)
        except Exception:
            shutil.rmtree(cls.basedir(), ignore_errors=True)
            raise

def _is_binary_available(path) -> bool:
    return bool(shutil.which(path))


def get_setting(key: str, default=None) -> Any:
    settings = sublime.load_settings(
        'LSP-terraform.sublime-settings').get("settings", {})
    return settings.get(key, default)


def plugin_loaded():
    register_plugin(Terraform)


def plugin_unloaded():
    unregister_plugin(Terraform)
