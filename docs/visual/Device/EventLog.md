# PyPNM / Device / EventLog

## Source Files

- HTML/script: `visual/PyPNM/Device/EventLog.html`
- JSON sample: `visual/PyPNM/Device/EventLog.json`

## Preview

<iframe src="../../../visual-previews/Device/EventLog.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Postman Visualizer: Device/EventLog
// Last Update: 2026-02-25 06:01:33 MST

// Postman Visualizer - DOCSIS Event Log (Dark Mode)
// Layout: Table first, then useful stats below.
// Input JSON shape:
// {
//   "mac_address": "aabbccddeeff",
//   "status": 0,
//   "message": null,
//   "logs": [ { docsDevEvFirstTime, docsDevEvLastTime, docsDevEvCounts, docsDevEvLevel, docsDevEvId, docsDevEvText }, ... ]
// }

const template = `
<style>
  body {
    font-family: Arial, sans-serif;
    padding: 18px;
    background-color: #0f1220;
    color: #eaeaea;
  }

  .header {
    background-color: #151a2e;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 14px 14px 10px 14px;
    border-radius: 10px;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.35);
  }

  .title {
    font-size: 16px;
    font-weight: 700;
    margin: 0 0 8px 0;
    color: #9fb4ff;
  }

  .meta {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 8px;
  }

  .pill {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 12px;
    color: #eaeaea;
  }

  .pill b { color: rgba(234,234,234,0.85); font-weight: 700; }

  .sub {
    margin: 0;
    font-size: 12px;
    color: rgba(234,234,234,0.85);
  }
  .deviceInfoTable { width: 100%; border-collapse: collapse; font-size: 12px; }
  .deviceInfoTable th, .deviceInfoTable td { border-top: 1px solid rgba(255,255,255,0.08); padding: 8px 6px; text-align: left; white-space: nowrap; }
  .deviceInfoTable th { color: #9fb4ff; font-weight: 700; border-top: none; }

  .card {
    background-color: #151a2e;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 12px;
    margin-top: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.35);
  }

  .card h3 {
    margin: 0 0 8px 0;
    font-size: 13px;
    color: #9fb4ff;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
  }

  th, td {
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding: 8px 6px;
    text-align: left;
    vertical-align: top;
  }

  th { color: #9fb4ff; font-weight: 700; }

  .lvl {
    font-weight: 700;
    border-radius: 999px;
    padding: 2px 8px;
    display: inline-block;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.06);
  }

  .lvl6 { color: #ff6b6b; border-color: rgba(255,107,107,0.35); background: rgba(255,107,107,0.12); }
  .lvl5 { color: #ffcc66; border-color: rgba(255,204,102,0.35); background: rgba(255,204,102,0.12); }
  .lvl4 { color: #8fd3ff; border-color: rgba(143,211,255,0.35); background: rgba(143,211,255,0.12); }
  .lvl3 { color: #b8ffb0; border-color: rgba(184,255,176,0.35); background: rgba(184,255,176,0.10); }
  .lvlX { color: rgba(234,234,234,0.85); }

  .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }

  .muted { color: rgba(234,234,234,0.75); }

  .kpi {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
  }

  .kpiItem {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px;
  }

  .kpiItem .k {
    font-size: 11px;
    color: rgba(234,234,234,0.80);
    margin-bottom: 4px;
  }

  .kpiItem .v {
    font-size: 16px;
    font-weight: 800;
    color: #eaeaea;
  }

  .kpiItem .h {
    margin-top: 4px;
    font-size: 11px;
    color: rgba(159,180,255,0.95);
  }

  .split {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .list {
    margin: 0;
    padding-left: 18px;
    font-size: 12px;
    color: rgba(234,234,234,0.90);
  }

  .note {
    font-size: 11px;
    color: rgba(234,234,234,0.78);
    margin-top: 8px;
  }

  .textCell {
    max-width: 860px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .textCell span {
    cursor: help;
  }

  .nowrap { white-space: nowrap; }
</style>


<div class="card">
  <h3>Device Info</h3>
  <table class="deviceInfoTable">
    <thead><tr><th>MacAddress</th><th>Model</th><th>Vendor</th><th>SW Version</th><th>HW Version</th><th>Boot ROM</th></tr></thead>
    <tbody><tr><td class="mono">{{deviceInfo.macAddress}}</td><td>{{deviceInfo.MODEL}}</td><td>{{deviceInfo.VENDOR}}</td><td class="mono">{{deviceInfo.SW_REV}}</td><td class="mono">{{deviceInfo.HW_REV}}</td><td class="mono">{{deviceInfo.BOOTR}}</td></tr></tbody>
  </table>
</div>

<div class="header">
  <div class="title">DOCSIS Event Log</div>
  <div class="meta">
    <div class="pill"><b>MAC</b> <span class="mono">{{mac}}</span></div>
    <div class="pill"><b>Status</b> {{statusText}}</div>
    <div class="pill"><b>Raw Entries</b> {{rawCount}}</div>
    <div class="pill"><b>Unique Entries</b> {{uniqCount}}</div>
    <div class="pill"><b>Time Span</b> {{timeSpan}}</div>
  </div>
  {{#if message}}
  <p class="sub">{{message}}</p>
  {{/if}}
</div>

<div class="card">
  <h3>Event Table (Deduped, Sorted By Time Asc)</h3>
  <div class="sub">Columns include extracted fields (when present) from the event text.</div>

  <table>
    <thead>
      <tr>
        <th class="nowrap">First Time</th>
        <th class="nowrap">Last Time</th>
        <th class="nowrap">Level</th>
        <th class="nowrap">Event ID</th>
        <th class="nowrap">Counts</th>
        <th class="nowrap">Event Type</th>
        <th class="nowrap">Chan ID</th>
        <th class="nowrap">Profile</th>
        <th class="nowrap">DSID</th>
        <th class="nowrap">CMTS-MAC</th>
        <th>Text</th>
      </tr>
    </thead>
    <tbody>
      {{#each rows}}
      <tr>
        <td class="nowrap muted">{{firstTime}}</td>
        <td class="nowrap muted">{{lastTime}}</td>
        <td class="nowrap"><span class="lvl {{lvlClass}}">L{{level}}</span></td>
        <td class="nowrap mono">{{eventId}}</td>
        <td class="nowrap">{{counts}}</td>
        <td class="nowrap">{{eventType}}</td>
        <td class="nowrap">{{chanId}}</td>
        <td class="nowrap">{{profile}}</td>
        <td class="nowrap">{{dsid}}</td>
        <td class="nowrap mono">{{cmtsMac}}</td>
        <td class="textCell">
          <span title="{{fullText}}">{{textPreview}}</span>
        </td>
      </tr>
      {{/each}}
    </tbody>
  </table>

  <div class="note">
    Note: duplicates are removed using a stable key built from (Event ID, Level, First/Last Time, Counts, Text).
  </div>
</div>

<div class="card">
  <h3>Useful Stats</h3>

  <div class="kpi">
    <div class="kpiItem">
      <div class="k">Critical (L6)</div>
      <div class="v">{{stats.level6}}</div>
      <div class="h">Unique events at level 6</div>
    </div>
    <div class="kpiItem">
      <div class="k">Warning (L5)</div>
      <div class="v">{{stats.level5}}</div>
      <div class="h">Unique events at level 5</div>
    </div>
    <div class="kpiItem">
      <div class="k">Earliest</div>
      <div class="v">{{stats.earliest}}</div>
      <div class="h">First observable timestamp</div>
    </div>
    <div class="kpiItem">
      <div class="k">Latest</div>
      <div class="v">{{stats.latest}}</div>
      <div class="h">Last observable timestamp</div>
    </div>
  </div>

  <div style="height: 12px;"></div>

  <div class="split">
    <div class="kpiItem">
      <div class="k">Top Event IDs By Total Counts</div>
      <ol class="list">
        {{#each stats.topEventIds}}
          <li><span class="mono">{{id}}</span> — {{sumCounts}} counts ({{occurrences}} unique)</li>
        {{/each}}
      </ol>
    </div>

    <div class="kpiItem">
      <div class="k">Level Distribution (Unique)</div>
      <ul class="list">
        <li><span class="lvl lvl6">L6</span> {{stats.level6}}</li>
        <li><span class="lvl lvl5">L5</span> {{stats.level5}}</li>
        <li><span class="lvl lvl4">L4</span> {{stats.level4}}</li>
        <li><span class="lvl lvl3">L3</span> {{stats.level3}}</li>
        <li><span class="lvl lvlX">Other</span> {{stats.levelOther}}</li>
      </ul>
      <div class="note">
        “Unique” means after dedupe, one row per unique event key.
      </div>
    </div>
  </div>
</div>
`;

function normalizeMac(mac) {
  if (!mac || typeof mac !== 'string') return 'N/A';
  const s = mac.trim();
  if (s.includes(':')) return s.toLowerCase();
  if (s.length !== 12) return s;
  return s.toLowerCase().match(/.{1,2}/g).join(':');
}

function parseIsoTime(s) {
  if (!s || typeof s !== 'string') return { ms: null, text: 'N/A' };
  const ms = Date.parse(s);
  if (!isFinite(ms)) return { ms: null, text: s };
  return { ms, text: s };
}

function safeStr(v, fallback) {
  if (v === undefined || v === null) return fallback;
  return String(v);
}

function clipText(s, maxLen) {
  if (!s || typeof s !== 'string') return '';
  if (s.length <= maxLen) return s;
  return s.slice(0, maxLen - 1) + '…';
}

function extractField(re, text) {
  if (!text) return null;
  const m = text.match(re);
  if (!m) return null;
  return m[1] !== undefined ? m[1] : null;
}

function levelClass(level) {
  if (level === 6) return 'lvl6';
  if (level === 5) return 'lvl5';
  if (level === 4) return 'lvl4';
  if (level === 3) return 'lvl3';
  return 'lvlX';
}

function constructVisualizerPayload() {
  const r = pm.response.json();

  const device = (r.device && typeof r.device === "object") ? r.device : {};
  const sys = (device.system_description && typeof device.system_description === "object") ? device.system_description : {};
  const mac = normalizeMac(device.mac_address);
  const status = (r.status !== undefined && r.status !== null) ? r.status : 'N/A';
  const statusText = status === 0 ? 'Success' : String(status);
  const message = r.message ? String(r.message) : '';

  const logsRaw = Array.isArray(r.logs) ? r.logs : [];
  const rawCount = logsRaw.length;

  // Dedup: stable key from core fields
  const seen = new Set();
  const uniq = [];

  for (let i = 0; i < logsRaw.length; i++) {
    const e = logsRaw[i] || {};
    const k = [
      safeStr(e.docsDevEvId, ''),
      safeStr(e.docsDevEvLevel, ''),
      safeStr(e.docsDevEvFirstTime, ''),
      safeStr(e.docsDevEvLastTime, ''),
      safeStr(e.docsDevEvCounts, ''),
      safeStr(e.docsDevEvText, '')
    ].join('|');

    if (seen.has(k)) continue;
    seen.add(k);
    uniq.push(e);
  }

  // Normalize rows, parse times, and sort (FirstTime asc, then LastTime asc, then EventID)
  const rowsNorm = uniq.map((e) => {
    const ft = parseIsoTime(e.docsDevEvFirstTime);
    const lt = parseIsoTime(e.docsDevEvLastTime);

    const level = (typeof e.docsDevEvLevel === 'number') ? e.docsDevEvLevel : parseInt(e.docsDevEvLevel, 10);
    const eventId = safeStr(e.docsDevEvId, 'N/A');
    const counts = (typeof e.docsDevEvCounts === 'number') ? e.docsDevEvCounts : parseInt(e.docsDevEvCounts, 10);

    const text = safeStr(e.docsDevEvText, '');

    // Extract common fields from docsDevEvText (best-effort)
    const eventType = extractField(/Event Type Code:\s*([0-9]+)\s*;/i, text) || 'N/A';
    const chanId = extractField(/Chan ID:\s*([0-9]+)\s*;/i, text) || extractField(/US Chan ID:\s*([0-9]+)\s*;/i, text) || 'N/A';
    const profile = extractField(/Profile ID:\s*([0-9]+)\s*;/i, text) || extractField(/New Profile:\s*([0-9]+)\s*;/i, text) || 'N/A';
    const dsid = extractField(/DSID:\s*([0-9A-Za-z\/]+)\s*;/i, text) || 'N/A';
    const cmtsMac = extractField(/CMTS-MAC=([0-9a-fA-F:]{17}|[0-9a-fA-F]{12})\s*;/, text) || 'N/A';

    const cmtsMacNorm = (cmtsMac !== 'N/A') ? normalizeMac(cmtsMac) : 'N/A';

    return {
      firstMs: ft.ms,
      lastMs: lt.ms,
      firstTime: ft.text,
      lastTime: lt.text,
      level: isFinite(level) ? level : 'N/A',
      lvlClass: levelClass(level),
      eventId,
      counts: isFinite(counts) ? counts : safeStr(e.docsDevEvCounts, 'N/A'),
      eventType,
      chanId,
      profile,
      dsid,
      cmtsMac: cmtsMacNorm,
      fullText: text,
      textPreview: clipText(text, 120)
    };
  });

  const timeSortKey = (ms) => (typeof ms === 'number' && isFinite(ms)) ? ms : Number.POSITIVE_INFINITY;

  rowsNorm.sort((a, b) => {
    const af = timeSortKey(a.firstMs);
    const bf = timeSortKey(b.firstMs);
    if (af !== bf) return af - bf;

    const al = timeSortKey(a.lastMs);
    const bl = timeSortKey(b.lastMs);
    if (al !== bl) return al - bl;

    if (a.eventId !== b.eventId) return String(a.eventId).localeCompare(String(b.eventId));
    return 0;
  });

  // Stats: levels (unique rows)
  const lvlCounts = { 3: 0, 4: 0, 5: 0, 6: 0, other: 0 };
  let earliestMs = null;
  let latestMs = null;

  for (let i = 0; i < rowsNorm.length; i++) {
    const r0 = rowsNorm[i];
    const lvl = r0.level;

    if (lvl === 6) lvlCounts[6] += 1;
    else if (lvl === 5) lvlCounts[5] += 1;
    else if (lvl === 4) lvlCounts[4] += 1;
    else if (lvl === 3) lvlCounts[3] += 1;
    else lvlCounts.other += 1;

    const msCandidates = [r0.firstMs, r0.lastMs].filter((x) => typeof x === 'number' && isFinite(x));
    for (let j = 0; j < msCandidates.length; j++) {
      const ms = msCandidates[j];
      if (earliestMs === null || ms < earliestMs) earliestMs = ms;
      if (latestMs === null || ms > latestMs) latestMs = ms;
    }
  }

  const fmtIso = (ms) => {
    if (ms === null || !isFinite(ms)) return 'N/A';
    try { return new Date(ms).toISOString(); } catch (_) { return 'N/A'; }
  };

  const timeSpan = (() => {
    if (earliestMs === null || latestMs === null) return 'N/A';
    const sec = Math.max(0, Math.floor((latestMs - earliestMs) / 1000));
    const days = Math.floor(sec / 86400);
    const hrs = Math.floor((sec % 86400) / 3600);
    const mins = Math.floor((sec % 3600) / 60);
    const s = sec % 60;
    const parts = [];
    if (days) parts.push(days + 'd');
    if (days || hrs) parts.push(hrs + 'h');
    if (days || hrs || mins) parts.push(mins + 'm');
    parts.push(s + 's');
    return parts.join(' ');
  })();

  // Top Event IDs by total counts (sum docsDevEvCounts)
  const byId = {};
  for (let i = 0; i < rowsNorm.length; i++) {
    const ev = rowsNorm[i];
    const id = String(ev.eventId);
    const c = (typeof ev.counts === 'number' && isFinite(ev.counts)) ? ev.counts : parseInt(ev.counts, 10);
    const add = isFinite(c) ? c : 0;

    if (!byId[id]) byId[id] = { id, sumCounts: 0, occurrences: 0 };
    byId[id].sumCounts += add;
    byId[id].occurrences += 1;
  }

  const topEventIds = Object.keys(byId)
    .map((k) => byId[k])
    .sort((a, b) => (b.sumCounts - a.sumCounts) || (b.occurrences - a.occurrences) || a.id.localeCompare(b.id))
    .slice(0, 8);

  return {
    mac,
    statusText,
    message,
    rawCount,
    uniqCount: rowsNorm.length,
    timeSpan,
    deviceInfo: {
      macAddress: mac || 'N/A',
      MODEL: sys.MODEL || 'N/A',
      VENDOR: sys.VENDOR || 'N/A',
      SW_REV: sys.SW_REV || 'N/A',
      HW_REV: sys.HW_REV || 'N/A',
      BOOTR: sys.BOOTR || 'N/A'
    },
    rows: rowsNorm.map((rw) => ({
      firstTime: rw.firstTime,
      lastTime: rw.lastTime,
      level: rw.level,
      lvlClass: rw.lvlClass,
      eventId: rw.eventId,
      counts: rw.counts,
      eventType: rw.eventType,
      chanId: rw.chanId,
      profile: rw.profile,
      dsid: rw.dsid,
      cmtsMac: rw.cmtsMac,
      fullText: rw.fullText,
      textPreview: rw.textPreview
    })),
    stats: {
      level6: lvlCounts[6],
      level5: lvlCounts[5],
      level4: lvlCounts[4],
      level3: lvlCounts[3],
      levelOther: lvlCounts.other,
      earliest: fmtIso(earliestMs),
      latest: fmtIso(latestMs),
      topEventIds
    }
  };
}

pm.visualizer.set(template, constructVisualizerPayload());
````
</details>

<details>
<summary>Sample JSON payload</summary>

````json
{
    "system_description": {
        "HW_REV": "1.0",
        "VENDOR": "LANCity",
        "BOOTR": "NONE",
        "SW_REV": "1.0.0",
        "MODEL": "LCPET-3"
    },
    "status": 0,
    "message": null,
    "device": {
        "mac_address": "aabbccddeeff",
        "system_description": {
            "HW_REV": "1.0",
            "VENDOR": "LANCity",
            "BOOTR": "NONE",
            "SW_REV": "1.0.0",
            "MODEL": "LCPET-3"
        }
    },
    "logs": [
        {
            "docsDevEvFirstTime": "2026-02-18T09:31:57",
            "docsDevEvLastTime": "2026-02-18T09:31:57",
            "docsDevEvCounts": 4,
            "docsDevEvLevel": 3,
            "docsDevEvId": 82000700,
            "docsDevEvText": "Unicast Ranging Received Abort Response - initializing MAC;CM-MAC=aa:bb:cc:dd:ee:ff;CMTS-MAC=aa:bb:cc:dd:ee:ff;CM-QOS=1.1;CM-VER=4.0;"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:01:14",
            "docsDevEvLastTime": "2025-02-18T01:01:14",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 5,
            "docsDevEvId": 90000000,
            "docsDevEvText": "MIMO Event MIMO: Stored MIMO=-1 post cfg file MIMO=-1;CM-MAC=aa:bb:cc:dd:ee:ff;CMTS-MAC=aa:bb:cc:dd:ee:ff;CM-QOS=1.1;CM-VER=4.0;"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:01:15",
            "docsDevEvLastTime": "2025-02-18T01:01:15",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 5,
            "docsDevEvId": 73050400,
            "docsDevEvText": "REG-RSP-MP Mismatch Between Calculated Value for P1.6hi Compared to CCAP Provided Value;CM-MAC=aa:bb:cc:dd:ee:ff;CMTS-MAC=aa:bb:cc:dd:ee:ff;CM-QOS=1.1;CM-VER=4.0;"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:01:15",
            "docsDevEvLastTime": "2025-02-18T01:01:15",
            "docsDevEvCounts": 3,
            "docsDevEvLevel": 5,
            "docsDevEvId": 82001200,
            "docsDevEvText": "RNG-RSP CCAP Commanded Power in Excess of 6 dB Below the Value Corresponding to the Top of the DRW;CM-MAC=aa:bb:cc:dd:ee:ff;CMTS-MAC=aa:bb:cc:dd:ee:ff;CM-QOS=1.1;CM-VER=4.0;"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:01:44",
            "docsDevEvLastTime": "2025-02-18T01:01:49",
            "docsDevEvCounts": 2,
            "docsDevEvLevel": 6,
            "docsDevEvId": 67061601,
            "docsDevEvText": "US profile assignment change.  US Chan ID: 42; Previous Profile: 12; New Profile: 6.;CM-MAC=aa:bb:cc:dd:ee:ff;CMTS-MAC=aa:bb:cc:dd:ee:ff;CM-QOS=1.1;CM-VER=4.0;"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:02:01",
            "docsDevEvLastTime": "2025-02-18T01:02:01",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 6,
            "docsDevEvId": 69010100,
            "docsDevEvText": "SW Download INIT - Via NMS"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:02:01",
            "docsDevEvLastTime": "2025-02-18T01:02:01",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 4,
            "docsDevEvId": 69020100,
            "docsDevEvText": "Improper Code File Controls"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:02:28",
            "docsDevEvLastTime": "2025-02-18T01:02:28",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 6,
            "docsDevEvId": 69010100,
            "docsDevEvText": "SW Download INIT - Via NMS"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:02:28",
            "docsDevEvLastTime": "2025-02-18T01:02:28",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 4,
            "docsDevEvId": 69020100,
            "docsDevEvText": "Improper Code File Controls"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:02:50",
            "docsDevEvLastTime": "2025-02-18T01:02:50",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 6,
            "docsDevEvId": 69010100,
            "docsDevEvText": "SW Download INIT - Via NMS"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:02:50",
            "docsDevEvLastTime": "2025-02-18T01:02:50",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 4,
            "docsDevEvId": 69020100,
            "docsDevEvText": "Improper Code File Controls"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:03:05",
            "docsDevEvLastTime": "2025-02-18T01:03:05",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 6,
            "docsDevEvId": 69010100,
            "docsDevEvText": "SW Download INIT - Via NMS"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:03:05",
            "docsDevEvLastTime": "2025-02-18T01:03:05",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 4,
            "docsDevEvId": 69020100,
            "docsDevEvText": "Improper Code File Controls"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:03:20",
            "docsDevEvLastTime": "2025-02-18T01:03:20",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 6,
            "docsDevEvId": 69010100,
            "docsDevEvText": "SW Download INIT - Via NMS"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:03:20",
            "docsDevEvLastTime": "2025-02-18T01:03:20",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 4,
            "docsDevEvId": 69020100,
            "docsDevEvText": "Improper Code File Controls"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:03:37",
            "docsDevEvLastTime": "2025-02-18T01:03:37",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 6,
            "docsDevEvId": 69010100,
            "docsDevEvText": "SW Download INIT - Via NMS"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:03:37",
            "docsDevEvLastTime": "2025-02-18T01:03:37",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 4,
            "docsDevEvId": 69020100,
            "docsDevEvText": "Improper Code File Controls"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:03:53",
            "docsDevEvLastTime": "2025-02-18T01:03:53",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 6,
            "docsDevEvId": 69010100,
            "docsDevEvText": "SW Download INIT - Via NMS"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:03:53",
            "docsDevEvLastTime": "2025-02-18T01:03:53",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 4,
            "docsDevEvId": 69020100,
            "docsDevEvText": "Improper Code File Controls"
        },
        {
            "docsDevEvFirstTime": "2025-02-18T01:06:59",
            "docsDevEvLastTime": "2025-02-18T01:06:59",
            "docsDevEvCounts": 1,
            "docsDevEvLevel": 6,
            "docsDevEvId": 67061601,
            "docsDevEvText": "US profile assignment change.  US Chan ID: 42; Previous Profile: 6; New Profile: 5.;CM-MAC=aa:bb:cc:dd:ee:ff;CMTS-MAC=aa:bb:cc:dd:ee:ff;CM-QOS=1.1;CM-VER=4.0;"
        }
    ]
}
````
</details>
