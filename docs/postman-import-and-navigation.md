# Postman Import and Navigation

Use this guide after installing Postman and cloning the repository.

Required Postman version: **Postman Desktop v12+**.

## Local-Mode Source of Truth

This repository uses Postman local-mode file artifacts:

- Collections: `postman/collections/<collection>/.../*.request.yaml`
- Environments: `postman/environments/*.environment.yaml`
- Globals: `postman/globals/*.globals.yaml`

Do not expect a single `*.postman_collection.json` export as the primary source.

## Open In Postman

Recommended flow:

1. Open Postman Desktop
2. Use local mode / open workspace from your cloned repository
3. Point Postman to this repository root so it can read `postman/` YAML artifacts

## Configure Base URL / Variables

Set `pypnm_url` in globals (or equivalent environment variable if your workspace uses environment scope).

Example:

- `http://127.0.0.1:8000`

Important:

- Request URLs in this repo use `{{pypnm_url}}` by default.
- Keep variable syntax in Postman form (`{{var}}`).

## Navigate Main Collections

- `postman/collections/PyPNM/`
- `postman/collections/PyPNM-CMTS/`

## Good First Request

Use a simple health check first:

1. Open collection `PyPNM`
2. Open folder `Health`
3. Open request `Health.request.yaml` (`name: Health`)
4. Confirm `pypnm_url` is set
5. Click `Send`

## Common Next Areas

- `SingleCapture` for single-capture workflows and visualizers
- `MultiCapture` for multi-capture operations and analysis flows
- `PNM/Files` for file workflow endpoints
- `System` / `Health` for service checks and system actions

## Troubleshooting

- If variables appear unresolved, confirm globals/environment YAML loaded in local mode.
- If requests fail immediately, verify `pypnm_url` and authentication-related variables.
- If visual output looks stale, run:

```bash
source .venv/bin/activate
tools/postman/sync_visualizers.py --check
```
