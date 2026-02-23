# Postman Import and Navigation

Use this guide after installing Postman and cloning the repository.

## Import Files Into Postman

In Postman, import the following files:

- [`postman/collections/PyPNM.postman_collection.json`](https://github.com/PyPNMApps/Postman-PyPNMApps-API/blob/main/postman/collections/PyPNM.postman_collection.json)
- [`postman/collections/PyPNM-CMTS.postman_collection.json`](https://github.com/PyPNMApps/Postman-PyPNMApps-API/blob/main/postman/collections/PyPNM-CMTS.postman_collection.json)
- [`postman/environments/PyPNM Remote Server.postman_environment.json`](https://github.com/PyPNMApps/Postman-PyPNMApps-API/blob/main/postman/environments/PyPNM%20Remote%20Server.postman_environment.json)
- [`postman/globals/workspace.postman_globals.json`](https://github.com/PyPNMApps/Postman-PyPNMApps-API/blob/main/postman/globals/workspace.postman_globals.json)

Recommended import flow:

1. Open Postman Desktop
2. Click `Import`
3. Select `Files`
4. Choose the files listed above
5. Confirm import

## Configure Base URL / Globals

Set `pypnm_url` in Postman Globals.

Example:

- `http://127.0.0.1:8000`

Important:

- Collection requests use `{{pypnm_url}}` (global variable)
- The provided environment file includes `base_url`
- If you prefer environment-only configuration, update the collection requests to use `{{base_url}}`

## Navigate the Imported Content

### Collections

- `PyPNM` (primary collection)
- `PyPNM-CMTS` (placeholder shell)

### Good First Request

Use a simple health check first:

1. Open [`PyPNM` collection](https://github.com/PyPNMApps/Postman-PyPNMApps-API/blob/main/postman/collections/PyPNM.postman_collection.json)
2. Open `Health` folder
3. Open `Health` request
4. Confirm `pypnm_url` is set
5. Click `Send`

### Common Next Areas

- `SingleCapture` for single-capture workflows and visualizers
- `MultiCapture` for multi-capture operations and analysis flows
- `FileManager` for file workflow endpoints
- `System` / `Health` for service checks and system actions

## Troubleshooting Import Setup

- If requests fail immediately, confirm `pypnm_url` is set in [Globals (`workspace.postman_globals.json`)](https://github.com/PyPNMApps/Postman-PyPNMApps-API/blob/main/postman/globals/workspace.postman_globals.json)
- If variables appear unresolved, verify [`workspace.postman_globals.json`](https://github.com/PyPNMApps/Postman-PyPNMApps-API/blob/main/postman/globals/workspace.postman_globals.json) imported successfully
- If you use the environment value (`base_url`) instead, verify the imported environment [`PyPNM Remote Server.postman_environment.json`](https://github.com/PyPNMApps/Postman-PyPNMApps-API/blob/main/postman/environments/PyPNM%20Remote%20Server.postman_environment.json) and ensure request URLs in [`PyPNM.postman_collection.json`](https://github.com/PyPNMApps/Postman-PyPNMApps-API/blob/main/postman/collections/PyPNM.postman_collection.json) were updated from `{{pypnm_url}}`
