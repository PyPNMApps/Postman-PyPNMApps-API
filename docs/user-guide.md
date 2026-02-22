# User Guide

## Overview

This repository provides Postman collections, environment, globals, and visualizer examples for PyPNM API workflows.

Main artifacts:

- `postman/collections/PyPNM.postman_collection.json`
- `postman/collections/PyPNM-CMTS.postman_collection.json` (placeholder shell)
- `postman/environments/PyPNM Remote Server.postman_environment.json`
- `postman/globals/workspace.postman_globals.json`

## Install Postman

1. Download Postman Desktop from `https://www.postman.com/downloads/`
2. Install and open Postman

## Clone Repository

```bash
git clone https://github.com/PyPNMApps/Postman-PyPNMApps-API.git
cd Postman-PyPNMApps-API
```

## Import Into Postman

Import these files in Postman:

- `postman/collections/PyPNM.postman_collection.json`
- `postman/collections/PyPNM-CMTS.postman_collection.json`
- `postman/environments/PyPNM Remote Server.postman_environment.json`
- `postman/globals/workspace.postman_globals.json`

## Configure URL and Variables

Important:

- Collection requests use `{{pypnm_url}}` (global variable)
- The provided environment file contains `base_url`
- Set `pypnm_url` in Globals, or update requests to use `base_url`

Minimum globals commonly needed:

- `pypnm_url`
- `cm_ip_address`
- `cm_mac_address`
- `cm_snmp_community_rw` or `snmp_v2_community_rw`

Additional workflow variables often needed:

- `tftp_server_ipv4`
- `tftp_server_ipv6`
- `channel_ids`
- `measurement_duration`
- `multi_measurement_duration`
- `op_id`
- `transaction_id`
- `filename`
- `operation_id`
- `mac_address`
- `analysis_min_avg_max`

## First Request

Health check:

1. Open `PyPNM -> Health -> Health`
2. Set `pypnm_url`
3. Click `Send`

Then try a single capture request such as `Ofdm-RxMER-GetCapture`.

## Visualizer Notes

The visual HTML templates in `visual/` are example visualizers for Postman Visualizer usage.

- Example MAC and `system_description` values are sanitized to generic placeholders.
- See `docs/tools.md` for the sanitize tool that enforces this.
