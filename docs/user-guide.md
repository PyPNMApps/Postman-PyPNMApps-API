# User Guide

## Overview

This repository provides Postman collections, environment, globals, and visualizer examples for PyPNM API workflows.

Main artifacts:

- `postman/collections/PyPNM.postman_collection.json`
- `postman/collections/PyPNM-CMTS.postman_collection.json` (placeholder shell)
- `postman/environments/PyPNM Remote Server.postman_environment.json`
- `postman/globals/workspace.postman_globals.json`

## Install Postman

1. Follow `docs/postman-install.md` for Ubuntu/Windows download and install steps
2. Install and open Postman

## Clone Repository

```bash
git clone https://github.com/PyPNMApps/Postman-PyPNMApps-API.git
cd Postman-PyPNMApps-API
```

## Import Into Postman

Follow `docs/postman-import-and-navigation.md` for:

- importing collections/environment/globals
- configuring `pypnm_url`
- navigating the `PyPNM` collection and first request

## Configure URL and Variables

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
