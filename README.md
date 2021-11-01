# LSP-terraform

A convenience package to take advantage of the [Terraform Language Server](https://github.com/hashicorp/terraform-ls).

## Prerequisites 

To use this package, you must have:

- The [LSP](https://packagecontrol.io/packages/LSP) package.
- [Terraform Syntax](https://packagecontrol.io/packages/Terraform)
- `Optional` [Terraform CLI](https://learn.hashicorp.com/tutorials/terraform/install-cli) installed for `validateOnSave`

## Installation

1. Install LSP and LSP-terraform from Package Control.
1. Restart Sublime.

## Applicable Selectors

The Terraform language server operates on the following base scopes:

- `source.terraform`
- `source.terraform-vars`

## Configuration

You may edit the default settings by running `Preferences: LSP-terraform Settings` from the _Command Palette_.
