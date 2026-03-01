# PyPNM / MultiCapture / ChannelEstimation / Ofdm-ChannelEstimation-Analysis-LTE-Detection-Phase-Slope

## Source Files

- HTML/script: `visual/PyPNM/MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-LTE-Detection-Phase-Slope.html`
- JSON sample: `visual/PyPNM/MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-LTE-Detection-Phase-Slope.json`

## Preview

<iframe src="../../../../visual-previews/MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-LTE-Detection-Phase-Slope.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Postman Visualizer: MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-LTE-Detection-Phase-Slope
// Last Update: 2026-03-01 14:10:00 MST

const template = `
<style>
  body { background:#0b0b0b; color:#e8e8e8; font-family:Arial,sans-serif; margin:0; padding:16px; }
  .container { max-width: 1500px; margin: 0 auto; }
  .header-row { display:grid; grid-template-columns: 1fr auto 1fr; align-items:center; gap:8px; margin-bottom:12px; }
  .page-title { grid-column:2; text-align:center; margin:0; color:#f2f2f2; font-size:22px; font-weight:700; }
  .capture-time { grid-column:3; justify-self:end; font-size:12px; color:#d7deec; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:999px; padding:6px 10px; white-space:nowrap; }

  .device-info { background:#151515; padding:14px; margin-bottom:14px; border-radius:10px; border:1px solid #2a2a2a; }
  .table-wrap { overflow-x:auto; border:1px solid rgba(255,255,255,0.08); border-radius:10px; }
  .table-title { font-size:11px; text-transform:uppercase; letter-spacing:.7px; padding:10px 12px; background:rgba(255,255,255,0.03); border-bottom:1px solid rgba(255,255,255,0.08); color:#dbe3ff; }
  .table { width:100%; min-width:720px; border-collapse:collapse; }
  .table th { text-align:left; white-space:nowrap; padding:9px 12px; font-size:11px; text-transform:uppercase; letter-spacing:.45px; color:#dbe3ff; background:rgba(255,255,255,0.03); }
  .table td { padding:10px 12px; font-size:12px; color:#fff; white-space:nowrap; border-top:1px solid rgba(255,255,255,0.08); }
  .mono { font-family:Consolas,"Liberation Mono",Menlo,monospace; }

  .chart-container { background:#202020; border:1px solid #303030; border-radius:10px; padding:14px; margin-bottom:14px; }
  .chart-title { margin:0 0 10px 0; color:#5a6fd8; text-align:center; font-size:14px; font-weight:700; }
  .chart-wrap { position:relative; height:320px; }
  .chart-canvas { display:block; width:100% !important; height:100% !important; box-sizing:border-box; background:#1a1a1a; border:1px solid #4d4d4d; border-radius:6px; }

  .summary-table { width:100%; border-collapse:collapse; margin-top:10px; }
  .summary-table th, .summary-table td { border:1px solid rgba(255,255,255,0.08); padding:8px 10px; font-size:12px; }
  .summary-table th { background:rgba(255,255,255,0.03); color:#dbe3ff; }
  .chip { display:inline-block; padding:2px 8px; border-radius:999px; font-size:11px; border:1px solid rgba(255,255,255,0.15); }
  .chip-high { color:#ff8f8f; border-color:rgba(255,107,107,0.45); background:rgba(255,107,107,0.08); }
  .chip-low { color:#9be8c7; border-color:rgba(57,194,142,0.45); background:rgba(57,194,142,0.08); }
</style>

<div class="container">
  <div class="header-row">
    <div class="page-title">OFDM Channel Estimation LTE Detection (Phase Slope)</div>
    {{#if captureTime}}<div class="capture-time">Capture Time: {{captureTime}}</div>{{/if}}
  </div>

  {{#if showDeviceInfo}}
  <div class="device-info">
    <div class="table-wrap">
      <div class="table-title">Device Info</div>
      <table class="table">
        <thead><tr><th>MacAddress</th><th>Model</th><th>Vendor</th><th>SW Version</th><th>HW Version</th><th>Boot ROM</th></tr></thead>
        <tbody><tr><td class="mono">{{deviceInfo.macAddress}}</td><td>{{deviceInfo.MODEL}}</td><td>{{deviceInfo.VENDOR}}</td><td class="mono">{{deviceInfo.SW_REV}}</td><td class="mono">{{deviceInfo.HW_REV}}</td><td class="mono">{{deviceInfo.BOOTR}}</td></tr></tbody>
      </table>
    </div>
  </div>
  {{/if}}

  <div class="chart-container">
    <div class="chart-title">Anomaly Count By Channel</div>
    <div class="chart-wrap"><canvas id="anomalyCountChart" class="chart-canvas"></canvas></div>
  </div>

  <div class="chart-container">
    <div class="chart-title">Per-Channel Threshold And Bin-Width Summary</div>
    <table class="summary-table">
      <thead>
        <tr><th>Channel</th><th>Anomaly Count</th><th>Threshold</th><th>Bin Widths (Hz)</th><th>Severity</th></tr>
      </thead>
      <tbody>
      {{#each rows}}
        <tr>
          <td>{{channelId}}</td>
          <td>{{anomalyCount}}</td>
          <td>{{threshold}}</td>
          <td class="mono">{{binWidths}}</td>
          <td>{{{severityHtml}}}</td>
        </tr>
      {{/each}}
      </tbody>
    </table>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js"></script>
<script>
pm.getData(function (err, value) {
  if (err || !value) return;

  const textColor = '#e0e0e0';
  const gridColor = 'rgba(255,255,255,0.1)';
  const labels = (value.rows || []).map(r => String(r.channelId));
  const counts = (value.rows || []).map(r => Number(r.anomalyCount) || 0);

  const ctx = document.getElementById('anomalyCountChart');
  if (!ctx) return;

  new Chart(ctx.getContext('2d'), {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Anomaly Count',
        data: counts,
        backgroundColor: 'rgba(90,111,216,0.45)',
        borderColor: '#5a6fd8',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: textColor } } },
      scales: {
        x: { ticks: { color: textColor }, grid: { color: gridColor }, title: { display: true, text: 'Channel', color: textColor } },
        y: { ticks: { color: textColor, precision: 0 }, grid: { color: gridColor }, title: { display: true, text: 'Anomaly Count', color: textColor } }
      }
    }
  });
});
</script>
`;

function sanitizeMac(value, fallback) {
  var fb = (fallback === undefined || fallback === null) ? 'N/A' : fallback;
  if (value === undefined || value === null) return fb;
  var text = String(value).trim();
  if (!text) return fb;
  var compact = text.replace(/[^0-9a-f]/gi, '').toLowerCase();
  if (compact.length !== 12) return text;
  return compact.match(/.{1,2}/g).join(':');
}

function sanitizeSystemDescription(_sys) {
  var sys = (_sys && typeof _sys === 'object') ? _sys : {};
  function present(v) { return v !== undefined && v !== null && String(v).trim() !== ''; }
  return {
    MODEL: present(sys.MODEL) ? String(sys.MODEL).trim() : 'LCPET-3',
    VENDOR: present(sys.VENDOR) ? String(sys.VENDOR).trim() : 'LANCity',
    SW_REV: present(sys.SW_REV) ? String(sys.SW_REV).trim() : '1.0.0',
    HW_REV: present(sys.HW_REV) ? String(sys.HW_REV).trim() : '1.0',
    BOOTR: present(sys.BOOTR) ? String(sys.BOOTR).trim() : 'NONE'
  };
}

function formatCaptureTime(raw) {
  if (raw === undefined || raw === null || raw === '') return null;
  if (typeof raw === 'number' && isFinite(raw)) {
    var ms = raw > 1e12 ? raw : raw * 1000;
    var d = new Date(ms);
    if (isNaN(d.getTime())) return null;
    return d.toISOString().slice(0, 19).replace('T', ' ') + ' UTC';
  }
  return String(raw);
}

function constructVisualizerPayload() {
  const response = pm.response.json();
  const rawData = (response && response.data && typeof response.data === 'object') ? response.data : {};
  const results = Array.isArray(rawData.results) ? rawData.results : [];

  const rows = results.map((r, idx) => {
    const anomalies = Array.isArray(r.anomalies) ? r.anomalies : [];
    const threshold = (typeof r.threshold === 'number' && isFinite(r.threshold)) ? r.threshold : null;
    const binWidths = Array.isArray(r.bin_widths) ? r.bin_widths : [];
    const anomalyCount = anomalies.filter(v => typeof v === 'number' && isFinite(v)).length;
    const severityHigh = anomalyCount > 5;
    return {
      channelId: (r.channel_id !== undefined && r.channel_id !== null) ? r.channel_id : (idx + 1),
      anomalyCount: anomalyCount,
      threshold: threshold === null ? 'N/A' : threshold.toExponential(3),
      binWidths: binWidths.length ? binWidths.join(', ') : 'N/A',
      severityHtml: severityHigh
        ? '<span class="chip chip-high">High</span>'
        : '<span class="chip chip-low">Low</span>'
    };
  }).sort((a, b) => Number(a.channelId) - Number(b.channelId));

  const deviceInfo = sanitizeSystemDescription(response.system_description || {});
  return {
    rows,
    captureTime: formatCaptureTime(((rawData.pnm_header || {}).capture_time) || response.capture_time),
    showDeviceInfo: true,
    deviceInfo: {
      macAddress: sanitizeMac(response.mac_address, 'N/A'),
      MODEL: deviceInfo.MODEL,
      VENDOR: deviceInfo.VENDOR,
      SW_REV: deviceInfo.SW_REV,
      HW_REV: deviceInfo.HW_REV,
      BOOTR: deviceInfo.BOOTR
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
    "mac_address": "aa:bb:cc:dd:ee:ff",
    "message": "Analysis LTE_DETECTION_PHASE_SLOPE completed",
    "data": {
        "analysis_type": "LTE_DETECTION_PHASE_SLOPE",
        "results": [
            {
                "channel_id": 193,
                "anomalies": [
                    1.2e-09,
                    1.8e-09,
                    1.1e-09
                ],
                "threshold": 1e-09,
                "bin_widths": [
                    1000000,
                    500000,
                    100000
                ]
            },
            {
                "channel_id": 194,
                "anomalies": [
                    9.8e-10
                ],
                "threshold": 1e-09,
                "bin_widths": [
                    1000000,
                    500000,
                    100000
                ]
            }
        ]
    }
}
````
</details>
