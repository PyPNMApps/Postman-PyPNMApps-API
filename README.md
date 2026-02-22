# Postman PyPNMApps API Collections

This repository contains Postman collections, environment, and globals for PyPNM API workflows.

Repository version source of truth:

- `VERSION` (must stay in sync with `pyproject.toml`)

The main collection (`PyPNM`) includes requests for:

- Single-capture PNM workflows
- Multi-capture start/status/results/stop/analysis flows
- File manager endpoints
- Interface and DOCSIS endpoints
- System and health endpoints

Current collection snapshot:

- `PyPNM`: 60 requests across 21 folders (`POST`, `GET`, `DELETE` workflows)
- `PyPNM-CMTS`: placeholder collection shell (currently no requests)

## Documentation

User and tooling documentation is available in `docs/`:

- `docs/README.md`
- `docs/user-guide.md`
- `docs/tools.md`
- `docs/release.md`

## Local Tools (Sanitize / Version / Release)

This repository keeps local tooling under `tools/` to keep the project root lean.

Create a local virtual environment and install tool dependencies:

```bash
./install.sh
```

Common commands:

```bash
.venv/bin/python tools/sanitize.py --check
.venv/bin/python tools/sanitize.py --fix
.venv/bin/python tools/support/bump_version.py --version 0.1.1 --check
.venv/bin/python tools/release/release.py --version-info
./tools/git/git-save.sh --help
./tools/git/git-push.sh --help
```

## 1. Download and Install Postman

1. Go to https://www.postman.com/downloads/
2. Download the Postman Desktop App for your OS.
3. Install and open Postman.

## 2. Install Git (Windows and Linux)

### Windows (Git Bash / Git for Windows)

1. Go to https://git-scm.com/download/win
2. Download and install **Git for Windows**
3. Open **Git Bash** after installation
4. Verify installation:

```bash
git --version
```

### Windows (GitHub Desktop, optional)

If you prefer a desktop Git client:

1. Go to https://desktop.github.com/
2. Download and install **GitHub Desktop**
3. Sign in to GitHub (optional, but recommended)
4. You can clone this repository using the desktop app (steps below)

### Linux

Install Git using your distro package manager, then verify:

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install -y git
git --version
```

Fedora:

```bash
sudo dnf install -y git
git --version
```

RHEL / CentOS (older systems may use `yum`):

```bash
sudo yum install -y git
git --version
```

## 3. Clone This Repository

### Option A: Git Bash / Linux terminal (recommended)

```bash
git clone https://github.com/PyPNMApps/Postman-PyPNMApps-API.git
cd Postman-PyPNMApps-API
```

### Option B: GitHub Desktop

1. Open GitHub Desktop
2. Select `File` -> `Clone repository...`
3. Choose the repository URL:

```text
https://github.com/PyPNMApps/Postman-PyPNMApps-API.git
```

4. Choose a local folder
5. Click `Clone`

## 4. Import Files into Postman

In Postman:

1. Click `Import`.
2. Choose `Files` (or drag and drop).
3. Import the following files:

- `postman/collections/PyPNM.postman_collection.json`
- `postman/collections/PyPNM-CMTS.postman_collection.json`
- `postman/environments/PyPNM Remote Server.postman_environment.json`
- `postman/globals/workspace.postman_globals.json`

## 5. Select Environment and Set Base URL

1. Select `PyPNM Remote Server` in the environment dropdown.
2. Update `base_url` in that environment to your PyPNM server (if needed).

Example:

```text
http://127.0.0.1:8000
```

Important:

- The collection requests currently use `{{pypnm_url}}` (a global variable), not `{{base_url}}`.
- You must set `pypnm_url` in Globals (recommended) or update the collection to use `base_url`.

## 6. Configure Required Global Variables

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

## 7. Import Validation Checklist (Recommended)

After import, verify:

1. The `PyPNM` collection appears in Collections.
2. The `PyPNM Remote Server` environment appears in Environments.
3. Globals include variables such as `pypnm_url`, `cm_ip_address`, and `cm_mac_address`.

## 8. Run a First Request

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

## 9. FullBandCapture Visualizer (Postman)

The `SingleCapture -> SpectrumAnalyzer -> File-Upload -> GetCapture-FullBandCapture` request includes a Postman
Visualizer script that renders:

- Device details (vendor/model/revisions)
- Spectrum chart (raw magnitudes and moving average)

If the response schema differs or the request fails, the visualizer may not render. Validate the response body first
before troubleshooting the chart.

## Repository Notes

- `postman/collections/PyPNM.postman_collection.json` is the primary collection.
- `postman/collections/PyPNM-CMTS.postman_collection.json` currently imports as an empty collection shell (no requests yet).
- `postman/globals/workspace.postman_globals.json` contains shared placeholders used across requests.
- `postman/scripts/update_operation_ids.py` is a helper script for collection edits (not required for normal Postman import/use).
- Visual example sanitization is handled by `tools/sanitize.py` for both `visual/**/*.json` and `visual/**/*.html`.
- Version synchronization is handled by `tools/support/bump_version.py` (`VERSION` + `pyproject.toml`).
