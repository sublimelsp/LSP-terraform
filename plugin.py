# Packages/LSP-terraform/plugin.py

from LSP.plugin import AbstractPlugin
from LSP.plugin import register_plugin
from LSP.plugin import unregister_plugin


SETTINGS_FILE = "LSP-terraform.sublime-settings"


class Terraform(AbstractPlugin):

    @classmethod
    def name(cls):
        return "terraform"

def plugin_loaded():
    register_plugin(Terraform)


def plugin_unloaded():
    unregister_plugin(Terraform)
