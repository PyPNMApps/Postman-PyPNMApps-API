# Postman PyPNMApps API Collections

This repository contains Postman collections, environments, and globals for working with the PyPNM API.

## 1. Download and Install Postman

1. Go to the Postman downloads page: https://www.postman.com/downloads/
2. Download the Postman Desktop App for your operating system.
3. Install and open Postman.

## 2. Clone This Repository Locally

Open a terminal and run:

```bash
git clone https://github.com/PyPNMApps/Postman-PyPNMApps-API.git
cd Postman-PyPNMApps-API
```

If you are using an existing local copy, use that path instead.

## 3. Import the Repo Files into Postman

In Postman:

1. Click `Import` (top left).
2. Choose `Files` (or drag and drop files).
3. Import these files from this repo:

- `postman/collections/PyPNM.postman_collection.json`
- `postman/collections/PyPNM-CMTS.postman_collection.json`
- `postman/environments/PyPNM Remote Server.postman_environment.json`
- `postman/globals/workspace.postman_globals.json`

## 4. Select the Environment

1. In Postman, open the environment selector (top right).
2. Select `PyPNM Remote Server`.
3. Confirm `base_url` points to your PyPNM API server.

Example:

```text
http://127.0.0.1:8000
```

## 5. Set Required Variables (Globals)

Open `Globals` in Postman and fill in values used by requests, for example:

- `cm_ip_address`
- `cm_mac_address`
- `cm_snmp_community_rw` (or `snmp_v2_community_rw`)
- `tftp_server_ipv4` / `tftp_server_ipv6`
- `pypnm_url` (if used by your requests/scripts)

Only set the variables required for the requests you plan to run.

## 6. Run a Request

1. Open the imported `PyPNM` collection.
2. Expand `SingleCapture`.
3. Choose a request (for example `Ofdma-PreEq-GetCapture`).
4. Review the request body/variables.
5. Click `Send`.

## Notes

- `PyPNM.postman_collection.json` contains PyPNM API requests.
- `PyPNM-CMTS.postman_collection.json` is included for CMTS-related workflows.
- If a request fails, verify `base_url` and required globals first.
