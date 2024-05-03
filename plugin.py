# Packages/LSP-terraform/plugin.py

import sublime

from LSP.plugin import AbstractPlugin, register_plugin, unregister_plugin
from LSP.plugin.core.typing import cast, Any, List, Optional

import os
import sys
import shutil
import zipfile
import urllib.request
import platform
import hashlib

USER_AGENT = 'Sublime Text LSP'

TAG = '0.33.1'

# GitHub releases page: https://github.com/hashicorp/terraform-ls/releases
HASHICORP_RELEASES_BASE = 'https://releases.hashicorp.com/terraform-ls/{tag}/terraform-ls_{tag}_{platform}_{arch}.zip'
HASHICORP_SHA256_BASE = 'https://releases.hashicorp.com/terraform-ls/{tag}/terraform-ls_{tag}_SHA256SUMS'
HASHICORP_FILENAME_BASE = 'terraform-ls_{tag}_{platform}_{arch}.zip'


def plat() -> Optional[str]:
    '''
    Returns the user friendly platform version that
    sublime is running on.
    '''
    if sublime.platform() == 'osx':
        return 'darwin'
    elif sublime.platform() == 'windows':
        return 'windows'
    elif sublime.platform() == 'linux':
        if platform.system() == 'Linux':
            return 'linux'
        elif sys.platform.startswith('freebsd'):
            return 'freebsd'
        elif sys.platform.startswith('openbsd'):
            return 'openbsd'
        else:
            return None
    else:
        return None


def arch() -> Optional[str]:
    '''
    Returns the user friendly architecture version that
    sublime is running on.
    '''
    if sublime.arch() == "x32":
        return "386"
    elif sublime.arch() == "x64":
        return "amd64"
    elif sublime.arch() == "arm64":
        return "arm64"
    else:
        return None


class Terraform(AbstractPlugin):
    '''
    Terraform is an AbstractPlugin implementation that provides
    the required functions to act as a helper package for the
    Terraform Language Server (terraform-ls)
    '''

    @classmethod
    def name(cls) -> str:
        return "terraform"

    @classmethod
    def basedir(cls) -> str:
        return os.path.join(cls.storage_path(), __package__)

    @classmethod
    def server_version(cls) -> str:
        return TAG

    @classmethod
    def current_server_version(cls) -> Optional[str]:
        try:
            with open(os.path.join(cls.basedir(), "VERSION"), "r") as fp:
                return fp.read()
        except:
            return None

    @classmethod
    def _is_terraform_ls_installed(cls) -> bool:
        return bool(cls._get_terraform_ls_path())

    @classmethod
    def _get_terraform_ls_path(cls) -> Optional[str]:
        terraform_ls_binary = cast(List[str], get_setting('command', [os.path.join(cls.basedir(), 'terraform-ls')]))
        return shutil.which(terraform_ls_binary[0]) if len(terraform_ls_binary) else None

    @classmethod
    def needs_update_or_installation(cls) -> bool:
        return not cls._is_terraform_ls_installed() or (cls.current_server_version() != cls.server_version())

    @classmethod
    def install_or_update(cls) -> None:
        if plat() is None:
            raise ValueError('System platform not detected or supported')

        if arch() is None:
            raise ValueError('System architecture not detected or supported')

        terraform_ls_path = cls._get_terraform_ls_path()
        if terraform_ls_path:
            os.remove(terraform_ls_path)

        os.makedirs(cls.basedir(), exist_ok=True)

        zip_url = HASHICORP_RELEASES_BASE.format(
            tag=cls.server_version(), arch=arch(), platform=plat())
        zip_file = os.path.join(cls.basedir(), HASHICORP_FILENAME_BASE.format(
            tag=cls.server_version(), platform=plat(), arch=arch()))
        sha_url = HASHICORP_SHA256_BASE.format(tag=cls.server_version())

        sha_file = os.path.join(cls.basedir(), 'terraform-ls.sha')

        req = urllib.request.Request(
            zip_url,
            data=None,
            headers={
                'User-Agent': USER_AGENT
            }
        )
        with urllib.request.urlopen(req) as fp:
            with open(zip_file, "wb") as f:
                f.write(fp.read())

        req = urllib.request.Request(
            sha_url,
            data=None,
            headers={
                'User-Agent': USER_AGENT
            }
        )
        with urllib.request.urlopen(req) as fp:
            with open(sha_file, "wb") as f:
                f.write(fp.read())

        sha256_hash_computed = None
        with open(zip_file, "rb") as f:
            file_bytes = f.read()
            sha256_hash_computed = hashlib.sha256(file_bytes).hexdigest()

        with open(sha_file) as fp:
            for line in fp:
                sha256sum, filename = line.split('  ')
                if filename.strip() != HASHICORP_FILENAME_BASE.format(tag=TAG, platform=plat(), arch=arch()):
                    continue

                if sha256sum.strip() != sha256_hash_computed:
                    raise ValueError(
                        'sha256 mismatch', 'original hash:', sha256sum, 'computed hash:', sha256_hash_computed)
                break

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(cls.basedir())

        os.remove(zip_file)
        os.remove(sha_file)

        terraform_ls = 'terraform-ls' if plat() != 'windows' else 'terraform-ls.exe'
        os.chmod(os.path.join(cls.basedir(), terraform_ls), 0o700)

        with open(os.path.join(cls.basedir(), 'VERSION'), 'w') as fp:
            fp.write(cls.server_version())


def get_setting(key: str, default=None) -> Any:
    settings = sublime.load_settings(
        'LSP-terraform.sublime-settings').get("settings", {})
    return settings.get(key, default)


def plugin_loaded():
    register_plugin(Terraform)


def plugin_unloaded():
    unregister_plugin(Terraform)
