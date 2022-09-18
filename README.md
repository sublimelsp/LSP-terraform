# LSP-terraform

A convenience package to take advantage of the [Terraform Language Server](https://github.com/hashicorp/terraform-ls).

## Installation

1. Install [LSP](https://packagecontrol.io/packages/LSP), [LSP-terraform](https://packagecontrol.io/packages/LSP-terraform) and [Terraform Syntax](https://packagecontrol.io/packages/Terraform) from Package Control.
2. Restart Sublime Text.
3. (Optional but recommended) Install the [LSP-file-watcher-chokidar](https://github.com/sublimelsp/LSP-file-watcher-chokidar) via Package Control to enable functionality to notify the server about new files.

Optionally install the [Terraform CLI](https://learn.hashicorp.com/tutorials/terraform/install-cli) for the `validateOnSave` and formatting functionality.

## Configuration

You may edit the default settings by running `Preferences: LSP-terraform Settings` from the _Command Palette_.

Optionally you can view `terraform-ls` settings at Hashicorps [repo](https://github.com/hashicorp/terraform-ls/blob/main/docs/SETTINGS.md)
