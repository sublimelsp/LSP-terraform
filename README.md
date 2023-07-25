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

## Formatting

The server supports formatting for the terraform files (equivalent to running `terraform fmt`). You can either trigger it manually from the _Command Palette_ using the `LSP: Format File` command or automatically run it on saving the file. To enable formatting on save, open `Preferences: LSP Settings` from the _Command Palette_ and add or modify the following setting:

```js
{
    "lsp_code_actions_on_save": {
      "source.formatAll.terraform": true,
    },
}
```
