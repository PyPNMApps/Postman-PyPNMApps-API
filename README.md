# Postman PyPNMApps API Collections

This repository contains Postman collections, environment, and globals for PyPNM API workflows.

The main collection (`PyPNM`) includes requests for:

- Single-capture PNM workflows
- Multi-capture start/status/results/stop/analysis flows
- File manager endpoints
- Interface and DOCSIS endpoints
- System and health endpoints

## 1. Download and Install Postman

1. Go to https://www.postman.com/downloads/
2. Download the Postman Desktop App for your OS.
3. Install and open Postman.

## 2. Clone This Repository

```bash
git clone https://github.com/PyPNMApps/Postman-PyPNMApps-API.git
cd Postman-PyPNMApps-API
```

## 3. Import Files into Postman

In Postman:

1. Click `Import`.
2. Choose `Files` (or drag and drop).
3. Import the following files:

- `postman/collections/PyPNM.postman_collection.json`
- `postman/collections/PyPNM-CMTS.postman_collection.json`
- `postman/environments/PyPNM Remote Server.postman_environment.json`
- `postman/globals/workspace.postman_globals.json`

## 4. Select Environment and Set Base URL

1. Select `PyPNM Remote Server` in the environment dropdown.
2. Update `base_url` in that environment to your PyPNM server (if needed).

Example:

```text
http://127.0.0.1:8000
```

Important:

- The collection requests currently use `{{pypnm_url}}` (a global variable), not `{{base_url}}`.
- You must set `pypnm_url` in Globals (recommended) or update the collection to use `base_url`.

## 5. Configure Required Global Variables

Open Postman `Globals` and populate the values used by requests.

Minimum values for most requests:

- `pypnm_url` (example: `http://127.0.0.1:8000`)
- `cm_ip_address`
- `cm_mac_address`
- `cm_snmp_community_rw` (or `snmp_v2_community_rw`, depending on request)

Values commonly required for capture/file workflows:

- `tftp_server_ipv4`
- `tftp_server_ipv6`
- `channel_ids`
- `measurement_duration`
- `multi_measurement_duration`
- `op_id` (for status/results/stop requests)
- `transaction_id`
- `filename`
- `operation_id`
- `mac_address`
- `analysis_min_avg_max`

## 6. Import Validation Checklist (Recommended)

After import, verify:

1. The `PyPNM` collection appears in Collections.
2. The `PyPNM Remote Server` environment appears in Environments.
3. Globals include variables such as `pypnm_url`, `cm_ip_address`, and `cm_mac_address`.

## 7. Run a First Request

For a simple connectivity test:

1. Open `PyPNM` collection.
2. Open `Health` -> `Health`.
3. Ensure `pypnm_url` is set.
4. Click `Send`.

Then try a capture request:

1. Open `SingleCapture`.
2. Choose a request such as `Ofdm-RxMER-GetCapture`.
3. Fill required globals (`cm_*`, `tftp_*`, etc.).
4. Click `Send`.

## Repository Notes

- `postman/collections/PyPNM.postman_collection.json` is the primary collection.
- `postman/collections/PyPNM-CMTS.postman_collection.json` currently imports as an empty collection shell (no requests yet).
- `postman/globals/workspace.postman_globals.json` contains shared placeholders used across requests.
- `postman/scripts/update_operation_ids.py` is a helper script for collection edits (not required for normal Postman import/use).
