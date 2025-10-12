# OpenProject Management

This repository is a management wrapper for the OpenProject application.

## Getting Started

Clone this repository with submodules to get the full OpenProject source code:

```bash
git clone --recurse-submodules https://github.com/brokerkitapps/openproject.git
```

Or if you've already cloned without submodules:

```bash
git clone https://github.com/brokerkitapps/openproject.git
cd openproject
git submodule init
git submodule update
```

## Structure

- `openproject/` - The OpenProject repository (tracked as a git submodule)
- `claude.md` - This documentation file
- Root level contains management scripts and documentation

## OpenProject Repository

The OpenProject source code is tracked as a git submodule from: https://github.com/opf/openproject

This approach keeps the management repository lightweight while providing access to the full OpenProject codebase for analysis and development.

## Management

This wrapper repository allows you to manage and customize the OpenProject installation while keeping the original source separate.

## Usage

Add your management scripts, configuration files, and documentation at the root level.

## Updating OpenProject

To update the OpenProject submodule to the latest version:

```bash
cd openproject
git pull origin dev
cd ..
git add openproject
git commit -m "Update OpenProject submodule"
git push
```
