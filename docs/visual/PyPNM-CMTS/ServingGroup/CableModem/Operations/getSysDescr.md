# PyPNM-CMTS / ServingGroup / CableModem / Operations / getSysDescr

## Source Files

- HTML/script: `visual/PyPNM-CMTS/ServingGroup/CableModem/Operations/getSysDescr.html`
- JSON sample: `visual/PyPNM-CMTS/ServingGroup/CableModem/Operations/getSysDescr.json`

## Preview

<iframe src="../../../../../../visual-previews/PyPNM-CMTS/ServingGroup/CableModem/Operations/getSysDescr.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Postman Visualizer: PyPNM-CMTS/ServingGroup/CableModem/Operations/getSysDescr
// Last Update: 2026-03-03 23:48:00 MST
// Visual Constraints: Follow canonical visual rules in CODING_AGENTS.md.

const response = pm.response.json() || {};

function safeText(value, fallback) {
  const fb = fallback == null ? 'N/A' : fallback;
  if (value == null) return fb;
  const s = String(value).trim();
  return s ? s : fb;
}

function sanitizeMac(value) {
  const raw = safeText(value, 'N/A');
  if (raw === 'N/A') return raw;
  const compact = raw.replace(/[^0-9a-f]/gi, '').toLowerCase();
  if (compact.length !== 12) return raw.toLowerCase();
  return compact.match(/.{1,2}/g).join(':');
}

function fmtUtc(epochSec) {
  const n = Number(epochSec);
  if (!Number.isFinite(n)) return 'N/A';
  const d = new Date(n * 1000);
  if (!Number.isFinite(d.getTime())) return 'N/A';
  const p = (x) => String(x).padStart(2, '0');
  return d.getUTCFullYear() + '-' + p(d.getUTCMonth() + 1) + '-' + p(d.getUTCDate()) + ' ' + p(d.getUTCHours()) + ':' + p(d.getUTCMinutes()) + ':' + p(d.getUTCSeconds()) + ' UTC';
}

function toSortedEntries(obj) {
  if (!obj || typeof obj !== 'object' || Array.isArray(obj)) return [];
  return Object.keys(obj).sort((a, b) => String(a).localeCompare(String(b))).map((k) => [k, obj[k]]);
}

function buildPayload(resp) {
  const groups = Array.isArray(resp && resp.groups) ? resp.groups : [];
  const rows = [];
  let modemCount = 0;
  let successCount = 0;
  let failureCount = 0;

  const vendorCounts = Object.create(null);
  const modelCounts = Object.create(null);

  for (let i = 0; i < groups.length; i += 1) {
    const g = groups[i] || {};
    const sgId = g.service_group_id != null ? String(g.service_group_id) : 'N/A';
    modemCount += Number.isFinite(Number(g.modem_count)) ? Number(g.modem_count) : 0;
    successCount += Number.isFinite(Number(g.success_count)) ? Number(g.success_count) : 0;
    failureCount += Number.isFinite(Number(g.failure_count)) ? Number(g.failure_count) : 0;

    const modems = g.modems && typeof g.modems === 'object' ? g.modems : {};
    const entries = toSortedEntries(modems);
    for (let j = 0; j < entries.length; j += 1) {
      const mac = entries[j][0];
      const modemObj = entries[j][1] || {};
      const sys = modemObj && modemObj.sysdescr && typeof modemObj.sysdescr === 'object' ? modemObj.sysdescr : {};

      const vendor = safeText(sys.VENDOR);
      const model = safeText(sys.MODEL);

      if (vendor !== 'N/A') vendorCounts[vendor] = (vendorCounts[vendor] || 0) + 1;
      if (model !== 'N/A') modelCounts[model] = (modelCounts[model] || 0) + 1;

      rows.push({
        serviceGroupId: sgId,
        macAddress: sanitizeMac(mac),
        model: model,
        vendor: vendor,
        swVersion: safeText(sys.SW_REV),
        hwVersion: safeText(sys.HW_REV),
        bootRom: safeText(sys.BOOTR),
        sysDescrStatus: sys && sys.is_empty === false ? 'Available' : 'Empty'
      });
    }
  }

  rows.sort((a, b) => {
    const sgCmp = String(a.serviceGroupId).localeCompare(String(b.serviceGroupId), undefined, { numeric: true });
    if (sgCmp !== 0) return sgCmp;
    return String(a.macAddress).localeCompare(String(b.macAddress));
  });

  const serviceGroupBuckets = Object.create(null);
  for (let i = 0; i < rows.length; i += 1) {
    const row = rows[i];
    const sgId = row.serviceGroupId || 'N/A';
    if (!serviceGroupBuckets[sgId]) {
      serviceGroupBuckets[sgId] = { serviceGroupId: sgId, rows: [] };
    }
    serviceGroupBuckets[sgId].rows.push(row);
  }
  const serviceGroups = Object.keys(serviceGroupBuckets)
    .sort((a, b) => String(a).localeCompare(String(b), undefined, { numeric: true }))
    .map((key) => serviceGroupBuckets[key]);

  function toTopList(countMap) {
    return Object.keys(countMap)
      .sort((a, b) => countMap[b] - countMap[a] || a.localeCompare(b))
      .slice(0, 8)
      .map((name) => ({ name, count: countMap[name] }));
  }

  return {
    title: 'Serving Group Cable Modem getSysDescr',
    message: safeText(resp && resp.message),
    status: Number(resp && resp.status),
    statusText: Number(resp && resp.status) === 0 ? 'Success' : 'Error',
    pollType: safeText((resp && (resp.poll_type || resp.pollType || (resp.poll && resp.poll.type) || resp.request_type)), 'N/A'),
    captureTime: fmtUtc(resp && resp.timestamp),
    groupCount: groups.length,
    modemCount: modemCount,
    successCount: successCount,
    failureCount: failureCount,
    topVendors: toTopList(vendorCounts),
    topModels: toTopList(modelCounts),
    hasRows: rows.length > 0,
    serviceGroups: serviceGroups,
    rows: rows
  };
}

const payload = buildPayload(response);

const template = `
<style>
  :root {
    color-scheme: light dark;
    --bg: #141821;
    --panel: #1b2332;
    --panel2: #182234;
    --line: rgba(255,255,255,0.10);
    --text: #e7edf8;
    --muted: #b8c8e8;
    --accent: #9ec0ff;
    --ok: #39c28e;
    --warn: #f4c84b;
    --nok: #ff7a7a;
  }
  @media (prefers-color-scheme: light) {
    :root {
      --bg: #f4f7fc;
      --panel: #ffffff;
      --panel2: #f7f9fd;
      --line: #d9e1ef;
      --text: #0f172a;
      --muted: #475569;
      --accent: #2563eb;
      --ok: #15803d;
      --warn: #b45309;
      --nok: #dc2626;
    }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 16px;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }
  .wrap { max-width: 1700px; margin: 0 auto; display: grid; gap: 12px; }
  .header-row {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 8px;
  }
  .title {
    grid-column: 2;
    margin: 0;
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    color: var(--text);
  }
  .capture-time {
    justify-self: end;
    font-size: 12px;
    color: var(--text);
    background: var(--panel2);
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: 6px 10px;
    white-space: nowrap;
  }
  .panel {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 12px;
  }
  .panel-title {
    margin: 0 0 8px;
    text-align: center;
    color: var(--accent);
    font-size: 16px;
    font-weight: 700;
  }
  .meta {
    margin: 0;
    text-align: center;
    color: var(--muted);
    font-size: 12px;
  }
  .kpis {
    display: grid;
    gap: 10px;
    grid-template-columns: repeat(7, minmax(0, 1fr));
  }
  @media (max-width: 1200px) {
    .kpis { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  }
  @media (max-width: 760px) {
    .kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
  .kpi {
    background: var(--panel2);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 10px;
  }
  .kpi .label { font-size: 12px; color: var(--muted); }
  .kpi .value { margin-top: 4px; font-weight: 700; font-size: 16px; color: var(--text); }
  .value.ok { color: var(--ok); }
  .value.warn { color: var(--warn); }
  .value.nok { color: var(--nok); }
  .split {
    display: grid;
    gap: 12px;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  @media (max-width: 1000px) {
    .split { grid-template-columns: 1fr; }
  }
  .mini-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
  }
  .mini-table th,
  .mini-table td {
    border: 1px solid var(--line);
    padding: 6px 8px;
    text-align: left;
  }
  .mini-table th { background: var(--panel2); color: var(--text); }
  .mini-table td { background: var(--panel); color: var(--text); }
  .table-wrap { overflow-x: auto; }
  .sg-title {
    margin: 10px 0 6px;
    color: var(--accent);
    font-size: 14px;
    font-weight: 700;
    text-align: left;
  }
  .device-table {
    width: 100%;
    border-collapse: collapse;
    min-width: 1150px;
    font-size: 12px;
  }
  .device-table th,
  .device-table td {
    border: 1px solid var(--line);
    padding: 7px 8px;
    text-align: left;
    vertical-align: top;
    white-space: nowrap;
  }
  .device-table th { background: var(--panel2); color: var(--text); }
  .device-table td { background: var(--panel); color: var(--text); }
  .mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
  .empty {
    text-align: center;
    color: var(--muted);
    font-size: 14px;
    padding: 14px;
    border: 1px dashed var(--line);
    border-radius: 8px;
    background: var(--panel2);
  }
</style>

<div class="wrap">
  <div class="header-row">
    <div></div>
    <h1 class="title">{{title}}</h1>
    <div class="capture-time">Capture Time: {{captureTime}}</div>
  </div>

  <div class="panel">
    <div class="panel-title">Summary</div>
    <p class="meta">Status: <strong>{{statusText}}</strong> · Message: {{message}}</p>
    <div class="kpis">
      <div class="kpi"><div class="label">Serving Groups</div><div class="value">{{groupCount}}</div></div>
      <div class="kpi"><div class="label">Modems</div><div class="value">{{modemCount}}</div></div>
      <div class="kpi"><div class="label">Success Count</div><div class="value ok">{{successCount}}</div></div>
      <div class="kpi"><div class="label">Failure Count</div><div class="value nok">{{failureCount}}</div></div>
      <div class="kpi"><div class="label">PollType</div><div class="value">{{pollType}}</div></div>
    </div>
  </div>

  <div class="split">
    <div class="panel">
      <div class="panel-title">Top Vendors</div>
      <table class="mini-table">
        <thead><tr><th>Vendor</th><th>Count</th></tr></thead>
        <tbody>
          {{#if topVendors.length}}
            {{#each topVendors}}<tr><td>{{name}}</td><td>{{count}}</td></tr>{{/each}}
          {{else}}
            <tr><td colspan="2">N/A</td></tr>
          {{/if}}
        </tbody>
      </table>
    </div>

    <div class="panel">
      <div class="panel-title">Top Models</div>
      <table class="mini-table">
        <thead><tr><th>Model</th><th>Count</th></tr></thead>
        <tbody>
          {{#if topModels.length}}
            {{#each topModels}}<tr><td>{{name}}</td><td>{{count}}</td></tr>{{/each}}
          {{else}}
            <tr><td colspan="2">N/A</td></tr>
          {{/if}}
        </tbody>
      </table>
    </div>
  </div>

  <div class="panel">
    <div class="panel-title">Device Info</div>
    {{#if hasRows}}
      {{#each serviceGroups}}
        <h3 class="sg-title">Service Group {{serviceGroupId}}</h3>
        <div class="table-wrap">
          <table class="device-table">
            <thead>
              <tr>
                <th>MacAddress</th>
                <th>Model</th>
                <th>Vendor</th>
                <th>SW Version</th>
                <th>HW Version</th>
                <th>Boot ROM</th>
              </tr>
            </thead>
            <tbody>
              {{#each rows}}
                <tr>
                  <td class="mono">{{macAddress}}</td>
                  <td>{{model}}</td>
                  <td>{{vendor}}</td>
                  <td class="mono">{{swVersion}}</td>
                  <td class="mono">{{hwVersion}}</td>
                  <td class="mono">{{bootRom}}</td>
                </tr>
              {{/each}}
            </tbody>
          </table>
        </div>
      {{/each}}
    {{else}}
      <div class="empty">No modem sysDescr data found.</div>
    {{/if}}
  </div>
</div>
`;

payload.isOk = Number(payload.status) === 0;
pm.visualizer.set(template, payload);
````
</details>

<details>
<summary>Sample JSON payload</summary>

````json
{
    "status": 0,
    "message": "heavy refresh rate limited",
    "timestamp": 1772605145,
    "poll": {
        "type": "heavy"
    },
    "groups": [
        {
            "service_group_id": 1,
            "status": 0,
            "message": "",
            "modem_count": 25,
            "success_count": 22,
            "failure_count": 3,
            "modems": {
                "20:6a:94:d7:d3:70": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "74:9b:e8:11:ed:70": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "a8:4e:3f:37:3e:30": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "1c:ab:c0:9d:d6:00": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "20:6a:94:34:63:f4": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "20:6a:94:d7:d3:60": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "38:ad:2b:3e:86:54": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "38:ad:2b:3e:87:7c": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "60:6c:63:f4:64:f8": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "74:9b:e8:72:7a:54": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "84:0b:7c:0b:e5:48": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "90:aa:c3:4b:75:60": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "90:aa:c3:8a:bd:18": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "90:aa:c3:c9:d0:d0": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "b0:f5:30:b7:76:30": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "dc:36:0c:79:f1:8c": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "dc:36:0c:ee:ce:e0": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "f8:1d:0f:cd:a0:f0": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "f8:34:5a:53:27:48": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "f8:34:5a:7f:d6:80": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "f8:34:5a:80:84:12": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "f8:34:5a:83:35:34": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "fc:77:7b:11:8f:da": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "fc:77:7b:ca:7b:10": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "fc:77:7b:cc:04:b0": {
                    "sysdescr": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                }
            }
        }
    ]
}
````
</details>
