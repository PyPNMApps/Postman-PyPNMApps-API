# Postman PyPNMApps API Collections

[![Python CI (Ubuntu)](https://github.com/PyPNMApps/Postman-PyPNMApps-API/actions/workflows/python-ci.yml/badge.svg)](https://github.com/PyPNMApps/Postman-PyPNMApps-API/actions/workflows/python-ci.yml)
[![MkDocs Site Build](https://github.com/PyPNMApps/Postman-PyPNMApps-API/actions/workflows/mkdocs-site-build.yml/badge.svg)](https://github.com/PyPNMApps/Postman-PyPNMApps-API/actions/workflows/mkdocs-site-build.yml)
[![MkDocs Pages Deploy](https://github.com/PyPNMApps/Postman-PyPNMApps-API/actions/workflows/mkdocs-pages-deploy.yml/badge.svg)](https://github.com/PyPNMApps/Postman-PyPNMApps-API/actions/workflows/mkdocs-pages-deploy.yml)
[![MkDocs](https://img.shields.io/badge/docs-MkDocs-526CFE?logo=materialformkdocs&logoColor=white)](https://www.mkdocs.org/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-0A66C2)](https://pypnmapps.github.io/Postman-PyPNMApps-API/)

This repository contains Postman collections, environment/globals files, and example visualizers for PyPNM API workflows.

It includes:
- Postman collections (`PyPNM`, `PyPNM-CMTS`)
- environment and globals exports
- `visual/` example Postman Visualizer HTML + JSON fixtures

## Basic Setup

1. Install Postman Desktop (Ubuntu/Windows): `docs/postman-install.md`
2. Clone this repository:

```bash
git clone https://github.com/PyPNMApps/Postman-PyPNMApps-API.git
cd Postman-PyPNMApps-API
```

3. Import collections/environment/globals and configure `pypnm_url`:
   - `docs/postman-import-and-navigation.md`

## Install (Local Tooling + Docs)

```bash
./install.sh
```

`install.sh` now prints Windows (PowerShell) command examples by default.
Use Linux/macOS examples instead:

```bash
./install.sh --os-linux
```

Run the local MkDocs site (default local docs port for this repo: `8030`):

```bash
source .venv/bin/activate
tools/docs/build_visual_docs.py
mkdocs serve -a 127.0.0.1:8030
```

Open:
- `http://127.0.0.1:8030/`

## Start Here

- [Docs Home](docs/docs-index.md)
- [Postman Install (Ubuntu/Windows)](docs/postman-install.md)
- [Postman Import and Navigation](docs/postman-import-and-navigation.md)
