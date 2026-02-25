# PyPNM / DOCSIS-3.1 / US-OFDMA-ChannelStats

## Source Files

- HTML/script: `visual/PyPNM/DOCSIS-3.1/US-OFDMA-ChannelStats.html`
- JSON sample: `visual/PyPNM/DOCSIS-3.1/US-OFDMA-ChannelStats.json`

## Preview

<iframe src="../../../visual-previews/DOCSIS-3.1/US-OFDMA-ChannelStats.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Postman Visualizer: DOCSIS-3.1/US-OFDMA-ChannelStats
// Last Update: 2026-02-25 06:01:33 MST

// Postman Visualizer - US OFDMA Channel Statistics (Dark Mode)
// Separate, useful visuals per channel (no overlap):
// 1) Global View: Active spectrum windows (start/end) for all channels, with per-channel Tx power marker (secondary chart)
// 2) Per-channel: Active spectrum window (range bar) with derived start/end from subcarrier params
// 3) Per-channel: Timeouts/Events (T3/T4/Abort/Exceed) as vertical bars
// 4) Per-channel: Status + config (Tx power, pre-eq enabled, muted, ranging status) as a compact KPI strip

const template = `
<style>
  body {
    font-family: Arial, sans-serif;
    padding: 20px;
    background-color: #0f1220;
    color: #eaeaea;
  }
  .header {
    background-color: #151a2e;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 16px 16px 12px 16px;
    border-radius: 10px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.35);
  }
  .title {
    font-size: 18px;
    font-weight: bold;
    margin: 0 0 10px 0;
    color: #ff4d6d;
  }
  .meta {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 10px;
  }
  .pill {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 12px;
    color: #eaeaea;
  }
  .pill b { color: #9fb4ff; font-weight: 700; }

  .kpi {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
    margin-top: 12px;
  }
  .kpiItem {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px;
  }
  .kpiItem .k { font-size: 11px; color: rgba(234,234,234,0.8); margin-bottom: 4px; }
  .kpiItem .v { font-size: 16px; font-weight: 700; color: #eaeaea; }
  .kpiItem .h { margin-top: 4px; font-size: 11px; color: rgba(159,180,255,0.95); }

  .sub {
    margin: 0;
    font-size: 12px;
    color: rgba(234,234,234,0.85);
  }
  .divider {
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 14px 0;
  }


  .deviceInfoCard {
    background-color: #151a2e;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.35);
  }
  .deviceInfoCard h3 { margin: 0 0 8px 0; font-size: 14px; color: #9fb4ff; }
  .deviceInfoTable { width: 100%; border-collapse: collapse; font-size: 12px; }
  .deviceInfoTable th, .deviceInfoTable td { border-bottom: 1px solid rgba(255,255,255,0.08); padding: 8px 6px; text-align: left; white-space: nowrap; }
  .deviceInfoTable th { color: #9fb4ff; font-weight: 700; }
  .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }

  .grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
    align-items: start;
  }
  .card {
    background-color: #151a2e;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.35);
  }
  .card h3 {
    margin: 0 0 6px 0;
    font-size: 14px;
    color: #9fb4ff;
  }

  .strip {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 10px;
    margin: 10px 0 12px 0;
  }
  .stripItem {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px;
  }
  .stripItem .k { font-size: 11px; color: rgba(234,234,234,0.8); margin-bottom: 4px; }
  .stripItem .v { font-size: 14px; font-weight: 700; color: #eaeaea; }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    font-size: 12px;
  }
  .tableWrap {
    width: 100%;
    overflow-x: auto;
  }
  th, td {
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding: 8px 6px;
    text-align: left;
    white-space: nowrap;
  }
  th { color: #9fb4ff; font-weight: 700; }

  @media (max-width: 1200px) {
    .strip {
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }
  }

  @media (max-width: 980px) {
    .grid {
      grid-template-columns: 1fr;
    }
    .kpi {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .strip {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }

  @media (max-width: 640px) {
    body {
      padding: 12px;
    }
    .header, .card {
      padding: 12px;
    }
    .kpi {
      grid-template-columns: 1fr;
    }
    .strip {
      grid-template-columns: 1fr;
    }
  }
</style>


<div class="deviceInfoCard">
  <h3>Device Info</h3>
  <table class="deviceInfoTable">
    <thead>
      <tr>
        <th>MacAddress</th><th>Model</th><th>Vendor</th><th>SW Version</th><th>HW Version</th><th>Boot ROM</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="mono">{{deviceInfo.macAddress}}</td>
        <td>{{deviceInfo.MODEL}}</td>
        <td>{{deviceInfo.VENDOR}}</td>
        <td class="mono">{{deviceInfo.SW_REV}}</td>
        <td class="mono">{{deviceInfo.HW_REV}}</td>
        <td class="mono">{{deviceInfo.BOOTR}}</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="header">
  <div class="title">US OFDMA Channel Statistics</div>
  <div class="meta">
    <div class="pill"><b>MAC</b> {{mac}}</div>
    <div class="pill"><b>Status</b> {{statusText}}</div>
    <div class="pill"><b>Channels</b> {{channelCount}}</div>
    <div class="pill"><b>Pre-check</b> {{precheck}}</div>
  </div>
  <p class="sub">{{message}}</p>

  <div class="kpi">
    <div class="kpiItem">
      <div class="k">Total Active Subcarriers</div>
      <div class="v">{{kpi.totalActive}}</div>
      <div class="h">Sum across channels</div>
    </div>
    <div class="kpiItem">
      <div class="k">Global Active Spectrum Span</div>
      <div class="v">{{kpi.globalSpanMHz}}</div>
      <div class="h">{{kpi.globalSpanRange}}</div>
    </div>
    <div class="kpiItem">
      <div class="k">Worst T3 Timeouts</div>
      <div class="v">{{kpi.worstT3}}</div>
      <div class="h">Ch {{kpi.worstT3Ch}}</div>
    </div>
    <div class="kpiItem">
      <div class="k">Any Muted</div>
      <div class="v">{{kpi.anyMuted}}</div>
      <div class="h">Muted flag across channels</div>
    </div>
  </div>

  <div class="divider"></div>

  <div class="sub"><b>Global View · Active Spectrum Windows (All Channels)</b></div>
  <div class="sub">Each row is one channel. Bar shows active start/end.</div>
  <canvas id="globalRangeChart" height="110"></canvas>

  <div class="divider"></div>

  <div class="sub"><b>Global View · Tx Power (dBmV)</b></div>
  <div class="sub">One bar per channel.</div>
  <canvas id="globalTxChart" height="90"></canvas>

  <div class="divider"></div>

  <div class="sub"><b>Quick Table</b></div>
  <div class="tableWrap">
    <table>
      <thead>
        <tr>
          <th>Channel</th>
          <th>Zero (MHz)</th>
          <th>Start (MHz)</th>
          <th>End (MHz)</th>
          <th>BW (MHz)</th>
          <th>Tx (dBmV)</th>
          <th>Pre-EQ</th>
          <th>Muted</th>
          <th>Ranging</th>
        </tr>
      </thead>
      <tbody>
        {{#each tableRows}}
        <tr>
          <td>{{channel}}</td>
          <td>{{zero}}</td>
          <td>{{start}}</td>
          <td>{{end}}</td>
          <td>{{bw}}</td>
          <td>{{tx}}</td>
          <td>{{preeq}}</td>
          <td>{{muted}}</td>
          <td>{{ranging}}</td>
        </tr>
        {{/each}}
      </tbody>
    </table>
  </div>
</div>


<div class="grid">
  {{#each channels}}
  <div class="card">
    <h3>{{label}} · Active Spectrum Window</h3>
    <p class="sub">Range bar derived from subcarrier params. Uses MHz.</p>

    <div class="strip">
      <div class="stripItem">
        <div class="k">Tx Power (dBmV)</div>
        <div class="v">{{txPower}}</div>
      </div>
      <div class="stripItem">
        <div class="k">Pre-EQ Enabled</div>
        <div class="v">{{preEq}}</div>
      </div>
      <div class="stripItem">
        <div class="k">Muted</div>
        <div class="v">{{muted}}</div>
      </div>
      <div class="stripItem">
        <div class="k">Ranging Status</div>
        <div class="v">{{rangingStatus}}</div>
      </div>
      <div class="stripItem">
        <div class="k">Config Change Ct</div>
        <div class="v">{{cfgChange}}</div>
      </div>
    </div>

    <canvas id="range_{{canvas_id}}" height="90"></canvas>

    <div class="divider"></div>

    <h3>{{label}} · Timeout / Event Counters</h3>
    <p class="sub">T3/T4/Abort/Exceed as bars.</p>
    <canvas id="events_{{canvas_id}}" height="110"></canvas>
  </div>
  {{/each}}
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js"></script>
<script>

    pm.getData(function (err, value) {
  if (err) {
    console.error(err);
    return;
  }

  var gridColor = 'rgba(255,255,255,0.12)';
  var tickColor = 'rgba(234,234,234,0.85)';
  var labelColor = '#eaeaea';

  var cRange = 'rgb(54, 162, 235)';
  var cTx    = 'rgb(75, 192, 192)';
  var cErr   = 'rgb(255, 99, 132)';

  var rgbaFill = function(rgb, a) {
    return rgb.replace('rgb', 'rgba').replace(')', ', ' + a + ')');
  };

  // Global range chart
  (function renderGlobalRanges() {
    var canvas = document.getElementById('globalRangeChart');
    if (!canvas) return;

    var labels = (value.global || {}).labels || [];
    var ranges = (value.global || {}).ranges || []; // {x:[start,end], y:i}

    new Chart(canvas.getContext('2d'), {
      type: 'horizontalBar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Active Window (MHz)',
          data: ranges,
          backgroundColor: rgbaFill(cRange, 0.45),
          borderColor: cRange,
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        legend: { display: true, labels: { fontColor: labelColor } },
        tooltips: {
          mode: 'nearest',
          intersect: false,
          callbacks: {
            label: function(tooltipItem, data) {
              var v = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
              if (v && v.x && Array.isArray(v.x)) {
                return 'Active: ' + v.x[0].toFixed(3) + ' - ' + v.x[1].toFixed(3) + ' MHz';
              }
              return tooltipItem.xLabel;
            }
          }
        },
        scales: {
          xAxes: [{
            ticks: { fontColor: tickColor },
            gridLines: { color: gridColor },
            scaleLabel: { display: true, labelString: 'Frequency (MHz)', fontColor: labelColor }
          }],
          yAxes: [{
            ticks: { fontColor: tickColor },
            gridLines: { color: gridColor }
          }]
        }
      }
    });
  })();

  // Global Tx chart
  (function renderGlobalTx() {
    var canvas = document.getElementById('globalTxChart');
    if (!canvas) return;

    var labels = (value.tx || {}).labels || [];
    var txData = (value.tx || {}).tx || [];

    new Chart(canvas.getContext('2d'), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Tx Power (dBmV)',
          data: txData,
          backgroundColor: rgbaFill(cTx, 0.45),
          borderColor: cTx,
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        legend: { display: true, labels: { fontColor: labelColor } },
        scales: {
          xAxes: [{
            ticks: { fontColor: tickColor },
            gridLines: { color: gridColor }
          }],
          yAxes: [{
            ticks: { fontColor: tickColor, beginAtZero: true },
            gridLines: { color: gridColor },
            scaleLabel: { display: true, labelString: 'dBmV', fontColor: labelColor }
          }]
        }
      }
    });
  })();

  // Per-channel charts (no overlap)
  (value.channels || []).forEach(function(ch) {
    // Range chart
    (function renderRange() {
      var canvas = document.getElementById('range_' + ch.canvas_id);
      if (!canvas) return;

      var ranges = [{ x: [ch.activeStartMHz, ch.activeEndMHz], y: 0 }];

      new Chart(canvas.getContext('2d'), {
        type: 'horizontalBar',
        data: {
          labels: ['Active'],
          datasets: [{
            label: 'Active Window (MHz)',
            data: ranges,
            backgroundColor: rgbaFill(cRange, 0.45),
            borderColor: cRange,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          legend: { display: true, labels: { fontColor: labelColor } },
          tooltips: {
            callbacks: {
              label: function(tooltipItem, data) {
                var v = data.datasets[0].data[0];
                return 'Active: ' + v.x[0].toFixed(3) + ' - ' + v.x[1].toFixed(3) + ' MHz';
              }
            }
          },
          scales: {
            xAxes: [{
              ticks: { fontColor: tickColor },
              gridLines: { color: gridColor },
              scaleLabel: { display: true, labelString: 'Frequency (MHz)', fontColor: labelColor }
            }],
            yAxes: [{
              ticks: { fontColor: tickColor },
              gridLines: { color: gridColor }
            }]
          }
        }
      });
    })();

    // Events chart
    (function renderEvents() {
      var canvas = document.getElementById('events_' + ch.canvas_id);
      if (!canvas) return;

      new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
          labels: ['T3', 'T4', 'Abort', 'Exceed'],
          datasets: [{
            label: 'Count',
            data: [ch.t3, ch.t4, ch.abort, ch.exceed],
            backgroundColor: rgbaFill(cErr, 0.55),
            borderColor: cErr,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          legend: { display: true, labels: { fontColor: labelColor } },
          scales: {
            xAxes: [{
              ticks: { fontColor: tickColor },
              gridLines: { color: gridColor }
            }],
            yAxes: [{
              ticks: { fontColor: tickColor, beginAtZero: true },
              gridLines: { color: gridColor }
            }]
          }
        }
      });
    })();
  });
});
</script>
`;

function constructVisualizerPayload() {
  const r = pm.response.json();
  const device = (r.device && typeof r.device === "object") ? r.device : {};
  const sys = (device.system_description && typeof device.system_description === "object") ? device.system_description : {};

  const mac = ((r.device || {}).mac_address) || 'N/A';
  const status = (r.status !== undefined && r.status !== null) ? r.status : 'N/A';
  const statusText = status === 0 ? 'Success' : String(status);
  const message = r.message ? r.message : '';
  const precheck = message && message.toLowerCase().indexOf('pre-check') >= 0 ? 'OK' : 'N/A';

  const results = Array.isArray(r.results) ? r.results : [];

  let totalActive = 0;
  let anyMuted = false;

  let worstT3 = -1;
  let worstT3Ch = 'N/A';

  let globalMinMHz = null;
  let globalMaxMHz = null;

  const tableRows = [];

  const channels = results.map((item, idx) => {
    const channelId = (item && item.channel_id !== undefined && item.channel_id !== null) ? item.channel_id : ('idx-' + (idx + 1));
    const e = item && item.entry ? item.entry : {};

    // NOTE: spacing appears to be "50" in sample payload (likely kHz). We defensively interpret:
    // - if spacing >= 1000: assume Hz
    // - else: assume kHz and convert to Hz (common: 50 kHz for OFDMA)
    const zeroHz = Number(e.docsIf31CmUsOfdmaChanSubcarrierZeroFreq || 0);
    const first = Number(e.docsIf31CmUsOfdmaChanFirstActiveSubcarrierNum || 0);
    const last = Number(e.docsIf31CmUsOfdmaChanLastActiveSubcarrierNum || 0);
    const numActive = Number(e.docsIf31CmUsOfdmaChanNumActiveSubcarriers || 0);

    const spacingRaw = Number(e.docsIf31CmUsOfdmaChanSubcarrierSpacing || 0);
    const spacingHz = (spacingRaw >= 1000) ? spacingRaw : (spacingRaw * 1000);

    const activeStartHz = zeroHz + (first * spacingHz);
    const activeEndHz = zeroHz + (last * spacingHz);
    const bwHz = (last >= first) ? ((last - first + 1) * spacingHz) : 0;

    const zeroMHz = zeroHz / 1e6;
    const activeStartMHz = activeStartHz / 1e6;
    const activeEndMHz = activeEndHz / 1e6;
    const bwMHz = bwHz / 1e6;

    const txPower = (e.docsIf31CmUsOfdmaChanTxPower !== undefined && e.docsIf31CmUsOfdmaChanTxPower !== null)
      ? Number(e.docsIf31CmUsOfdmaChanTxPower)
      : 0;

    const preEqEnabled = !!e.docsIf31CmUsOfdmaChanPreEqEnabled;
    const isMuted = !!e.docsIf31CmStatusOfdmaUsIsMuted;
    const rangingStatus = (e.docsIf31CmStatusOfdmaUsRangingStatus !== undefined && e.docsIf31CmStatusOfdmaUsRangingStatus !== null)
      ? String(e.docsIf31CmStatusOfdmaUsRangingStatus)
      : 'N/A';

    const cfgChange = Number(e.docsIf31CmUsOfdmaChanConfigChangeCt || 0);

    const t3 = Number(e.docsIf31CmStatusOfdmaUsT3Timeouts || 0);
    const t4 = Number(e.docsIf31CmStatusOfdmaUsT4Timeouts || 0);
    const abort = Number(e.docsIf31CmStatusOfdmaUsRangingAborteds || 0);
    const exceed = Number(e.docsIf31CmStatusOfdmaUsT3Exceededs || 0);

    totalActive += numActive;

    if (isMuted) anyMuted = true;
    if (t3 > worstT3) {
      worstT3 = t3;
      worstT3Ch = String(channelId);
    }

    if (Number.isFinite(activeStartMHz) && Number.isFinite(activeEndMHz)) {
      if (globalMinMHz === null || activeStartMHz < globalMinMHz) globalMinMHz = activeStartMHz;
      if (globalMaxMHz === null || activeEndMHz > globalMaxMHz) globalMaxMHz = activeEndMHz;
    }

    tableRows.push({
      channel: String(channelId),
      zero: zeroMHz.toFixed(3),
      start: activeStartMHz.toFixed(3),
      end: activeEndMHz.toFixed(3),
      bw: bwMHz.toFixed(3),
      tx: txPower.toFixed(1),
      preeq: preEqEnabled ? 'true' : 'false',
      muted: isMuted ? 'true' : 'false',
      ranging: rangingStatus
    });

    return {
      label: 'OFDMA Channel ' + String(channelId),
      canvas_id: 'c' + String(idx + 1),

      activeStartMHz,
      activeEndMHz,
      bwMHz,

      txPower: txPower.toFixed(1),
      preEq: preEqEnabled ? 'true' : 'false',
      muted: isMuted ? 'true' : 'false',
      rangingStatus: rangingStatus,
      cfgChange: String(cfgChange),

      t3, t4, abort, exceed
    };
  });

  const labels = channels.map(ch => ch.label.replace('OFDMA ', 'Ch '));
  const ranges = channels.map((ch, i) => ({ x: [ch.activeStartMHz, ch.activeEndMHz], y: i }));

  const txLabels = channels.map(ch => ch.label.replace('OFDMA Channel ', 'Ch '));
  const tx = channels.map(ch => Number(ch.txPower));

  const globalSpanMHz = (globalMinMHz !== null && globalMaxMHz !== null) ? (globalMaxMHz - globalMinMHz) : 0;
  const globalSpanRange = (globalMinMHz !== null && globalMaxMHz !== null)
    ? (globalMinMHz.toFixed(3) + ' - ' + globalMaxMHz.toFixed(3) + ' MHz')
    : 'N/A';

  const kpi = {
    totalActive: String(totalActive),
    globalSpanMHz: globalSpanMHz.toFixed(3) + ' MHz',
    globalSpanRange: globalSpanRange,
    worstT3: String(Math.max(0, worstT3)),
    worstT3Ch: worstT3Ch,
    anyMuted: anyMuted ? 'true' : 'false'
  };

  return {
    deviceInfo: {
      macAddress: device.mac_address || "N/A",
      MODEL: sys.MODEL || "N/A",
      VENDOR: sys.VENDOR || "N/A",
      SW_REV: sys.SW_REV || "N/A",
      HW_REV: sys.HW_REV || "N/A",
      BOOTR: sys.BOOTR || "N/A"
    },
    mac,
    statusText,
    message,
    precheck,
    channelCount: channels.length,
    kpi,
    tableRows,
    global: { labels, ranges },
    tx: { labels: txLabels, tx },
    channels
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
    "message": "Pre-check successful: CableModem reachable via ping and SNMP",
    "device": {
        "mac_address": "aa:bb:cc:dd:ee:ff",
        "system_description": {
            "HW_REV": "1.0",
            "VENDOR": "LANCity",
            "BOOTR": "NONE",
            "SW_REV": "1.0.0",
            "MODEL": "LCPET-3"
        }
    },
    "results": [
        {
            "index": 81,
            "channel_id": 42,
            "entry": {
                "docsIf31CmUsOfdmaChanChannelId": 42,
                "docsIf31CmUsOfdmaChanConfigChangeCt": 0,
                "docsIf31CmUsOfdmaChanSubcarrierZeroFreq": 104800000,
                "docsIf31CmUsOfdmaChanFirstActiveSubcarrierNum": 74,
                "docsIf31CmUsOfdmaChanLastActiveSubcarrierNum": 1969,
                "docsIf31CmUsOfdmaChanNumActiveSubcarriers": 1896,
                "docsIf31CmUsOfdmaChanSubcarrierSpacing": 50,
                "docsIf31CmUsOfdmaChanCyclicPrefix": 192,
                "docsIf31CmUsOfdmaChanRollOffPeriod": 128,
                "docsIf31CmUsOfdmaChanNumSymbolsPerFrame": 10,
                "docsIf31CmUsOfdmaChanTxPower": 16.6,
                "docsIf31CmUsOfdmaChanPreEqEnabled": true,
                "docsIf31CmStatusOfdmaUsT3Timeouts": 0,
                "docsIf31CmStatusOfdmaUsT4Timeouts": 0,
                "docsIf31CmStatusOfdmaUsRangingAborteds": 0,
                "docsIf31CmStatusOfdmaUsT3Exceededs": 0,
                "docsIf31CmStatusOfdmaUsIsMuted": false,
                "docsIf31CmStatusOfdmaUsRangingStatus": "success"
            }
        },
        {
            "index": 82,
            "channel_id": 41,
            "entry": {
                "docsIf31CmUsOfdmaChanChannelId": 41,
                "docsIf31CmUsOfdmaChanConfigChangeCt": 0,
                "docsIf31CmUsOfdmaChanSubcarrierZeroFreq": 22000000,
                "docsIf31CmUsOfdmaChanFirstActiveSubcarrierNum": 74,
                "docsIf31CmUsOfdmaChanLastActiveSubcarrierNum": 1249,
                "docsIf31CmUsOfdmaChanNumActiveSubcarriers": 1176,
                "docsIf31CmUsOfdmaChanSubcarrierSpacing": 50,
                "docsIf31CmUsOfdmaChanCyclicPrefix": 192,
                "docsIf31CmUsOfdmaChanRollOffPeriod": 128,
                "docsIf31CmUsOfdmaChanNumSymbolsPerFrame": 10,
                "docsIf31CmUsOfdmaChanTxPower": 16.6,
                "docsIf31CmUsOfdmaChanPreEqEnabled": true,
                "docsIf31CmStatusOfdmaUsT3Timeouts": 0,
                "docsIf31CmStatusOfdmaUsT4Timeouts": 0,
                "docsIf31CmStatusOfdmaUsRangingAborteds": 0,
                "docsIf31CmStatusOfdmaUsT3Exceededs": 0,
                "docsIf31CmStatusOfdmaUsIsMuted": false,
                "docsIf31CmStatusOfdmaUsRangingStatus": "success"
            }
        }
    ]
}
````
</details>
