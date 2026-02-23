# PyPNM / DOCSIS-3.1 / DS-OFDM-ChannelStats

## Source Files

- HTML/script: `visual/PyPNM/DOCSIS-3.1/DS-OFDM-ChannelStats.html`
- JSON sample: `visual/PyPNM/DOCSIS-3.1/DS-OFDM-ChannelStats.json`

## Preview

<iframe src="/visual-previews/DOCSIS-3.1/DS-OFDM-ChannelStats.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Postman Visualizer - DS OFDM Channel Statistics (Dark Mode)
// Useful visuals (separate graphs per channel; no overlap):
// 1) Per-channel: Active spectrum window (start/end freq) as a horizontal "range bar" on a shared MHz axis
// 2) Per-channel: PLC vs Zero frequency (two vertical bars)
// 3) Per-channel: Reliability counters (PLC Total CW vs PLC Unreliable CW; NCP Total Fields vs NCP CRC Failures) (two small bar charts)
// 4) Summary KPIs: channel count, total active subcarriers, estimated occupied bandwidth, worst CRC failures (PLC/NCP)

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
  .sub {
    margin: 0;
    font-size: 12px;
    color: rgba(234,234,234,0.85);
  }
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

  .grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
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
  .mini {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 10px;
  }
  .divider {
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 14px 0;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    font-size: 12px;
  }
  th, td {
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding: 8px 6px;
    text-align: left;
    white-space: nowrap;
  }
  th { color: #9fb4ff; font-weight: 700; }
  .warn { color: #ffcc66; }
  .bad  { color: #ff6b6b; }
</style>

<div class="header">
  <div class="title">DS OFDM Channel Statistics</div>
  <div class="meta">
    <div class="pill"><b>MAC</b> {{mac}}</div>
    <div class="pill"><b>Status</b> {{statusText}}</div>
    <div class="pill"><b>Channels</b> {{channelCount}}</div>
    <div class="pill"><b>Total Active Subcarriers</b> {{kpi.totalActiveSubcarriers}}</div>
  </div>
  <p class="sub">{{message}}</p>

  <div class="kpi">
    <div class="kpiItem">
      <div class="k">Est. Occupied Bandwidth (per channel)</div>
      <div class="v">{{kpi.bandwidthPerChannelMHz}}</div>
      <div class="h">(last - first + 1) · spacing</div>
    </div>
    <div class="kpiItem">
      <div class="k">Worst NCP CRC Failures</div>
      <div class="v">{{kpi.worstNcpCrc}}</div>
      <div class="h">Ch {{kpi.worstNcpCrcCh}}</div>
    </div>
    <div class="kpiItem">
      <div class="k">Worst PLC Unreliable CW</div>
      <div class="v">{{kpi.worstPlcUnrel}}</div>
      <div class="h">Ch {{kpi.worstPlcUnrelCh}}</div>
    </div>
    <div class="kpiItem">
      <div class="k">Global Active Spectrum Span</div>
      <div class="v">{{kpi.globalSpanMHz}}</div>
      <div class="h">{{kpi.globalSpanRange}}</div>
    </div>
  </div>

  <div class="divider"></div>

  <div class="sub"><b>Global View · Active Spectrum Windows (All Channels)</b></div>
  <div class="sub">Each row is one channel. Bar shows active start/end; marker shows PLC frequency.</div>
  <canvas id="globalRangeChart" height="120"></canvas>

  <div class="divider"></div>

  <div class="sub"><b>Quick Table</b></div>
  <table>
    <thead>
      <tr>
        <th>Channel</th>
        <th>Indicator</th>
        <th>Zero Freq (MHz)</th>
        <th>Active Start (MHz)</th>
        <th>Active End (MHz)</th>
        <th>PLC (MHz)</th>
        <th>BW (MHz)</th>
      </tr>
    </thead>
    <tbody>
      {{#each tableRows}}
      <tr>
        <td>{{channel}}</td>
        <td>{{indicator}}</td>
        <td>{{zero}}</td>
        <td>{{start}}</td>
        <td>{{end}}</td>
        <td>{{plc}}</td>
        <td>{{bw}}</td>
      </tr>
      {{/each}}
    </tbody>
  </table>
</div>

<div class="grid">
  {{#each channels}}
  <div class="card">
    <h3>{{label}} · Active Spectrum Window</h3>
    <p class="sub">Horizontal range bar (start/end) with PLC marker. Uses shared MHz axis for this channel.</p>
    <canvas id="range_{{canvas_id}}" height="90"></canvas>

    <div class="divider"></div>

    <div class="mini">
      <div>
        <h3>{{label}} · PLC vs Subcarrier Zero Freq</h3>
        <p class="sub">Two bars in MHz.</p>
        <canvas id="freqs_{{canvas_id}}" height="120"></canvas>
      </div>
      <div>
        <h3>{{label}} · Reliability Counters</h3>
        <p class="sub">PLC / NCP errors vs totals.</p>
        <canvas id="errs_{{canvas_id}}" height="120"></canvas>
      </div>
    </div>
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
  var cPlc   = 'rgb(255, 206, 86)';
  var cZero  = 'rgb(75, 192, 192)';
  var cErr   = 'rgb(255, 99, 132)';

  var rgbaFill = function(rgb, a) {
    return rgb.replace('rgb', 'rgba').replace(')', ', ' + a + ')');
  };

  // Global range chart (one dataset for ranges, one dataset for PLC markers)
  (function renderGlobalRanges() {
    var canvas = document.getElementById('globalRangeChart');
    if (!canvas) return;

    var labels = (value.global || {}).labels || [];
    var ranges = (value.global || {}).ranges || []; // {x:[start,end], y: index}
    var plcPts = (value.global || {}).plcPts || []; // {x: plc, y: index}

    new Chart(canvas.getContext('2d'), {
      type: 'horizontalBar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Active Window (MHz)',
            data: ranges,
            backgroundColor: rgbaFill(cRange, 0.45),
            borderColor: cRange,
            borderWidth: 1
          },
          {
            label: 'PLC (MHz)',
            data: plcPts,
            backgroundColor: rgbaFill(cPlc, 0.9),
            borderColor: cPlc,
            borderWidth: 1,
            barThickness: 2
          }
        ]
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
              var ds = data.datasets[tooltipItem.datasetIndex];
              var v = ds.data[tooltipItem.index];
              if (v && v.x && Array.isArray(v.x)) {
                return ds.label + ': ' + v.x[0].toFixed(2) + ' - ' + v.x[1].toFixed(2) + ' MHz';
              }
              if (v && typeof v.x === 'number') {
                return ds.label + ': ' + v.x.toFixed(2) + ' MHz';
              }
              return ds.label + ': ' + tooltipItem.xLabel;
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

  // Per-channel charts
  (value.channels || []).forEach(function(ch) {
    // Range chart
    (function renderRange() {
      var canvas = document.getElementById('range_' + ch.canvas_id);
      if (!canvas) return;

      // Single-row horizontal range bar with PLC marker overlay
      var labels = ['Active'];
      var ranges = [{ x: [ch.activeStartMHz, ch.activeEndMHz], y: 0 }];
      var plcPts = [{ x: ch.plcMHz, y: 0 }];

      new Chart(canvas.getContext('2d'), {
        type: 'horizontalBar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Active Window (MHz)',
              data: ranges,
              backgroundColor: rgbaFill(cRange, 0.45),
              borderColor: cRange,
              borderWidth: 1
            },
            {
              label: 'PLC (MHz)',
              data: plcPts,
              backgroundColor: rgbaFill(cPlc, 0.9),
              borderColor: cPlc,
              borderWidth: 1,
              barThickness: 2
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          legend: { display: true, labels: { fontColor: labelColor } },
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
          },
          tooltips: {
            mode: 'nearest',
            intersect: false,
            callbacks: {
              label: function(tooltipItem, data) {
                var ds = data.datasets[tooltipItem.datasetIndex];
                var v = ds.data[tooltipItem.index];
                if (v && v.x && Array.isArray(v.x)) {
                  return ds.label + ': ' + v.x[0].toFixed(2) + ' - ' + v.x[1].toFixed(2) + ' MHz';
                }
                if (v && typeof v.x === 'number') {
                  return ds.label + ': ' + v.x.toFixed(2) + ' MHz';
                }
                return ds.label + ': ' + tooltipItem.xLabel;
              }
            }
          }
        }
      });
    })();

    // PLC vs Zero frequency (vertical bar)
    (function renderFreqs() {
      var canvas = document.getElementById('freqs_' + ch.canvas_id);
      if (!canvas) return;

      new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
          labels: ['Zero Freq', 'PLC Freq'],
          datasets: [{
            label: 'MHz',
            data: [ch.zeroMHz, ch.plcMHz],
            backgroundColor: [rgbaFill(cZero, 0.55), rgbaFill(cPlc, 0.55)],
            borderColor: [cZero, cPlc],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          legend: { display: false },
          scales: {
            xAxes: [{
              ticks: { fontColor: tickColor },
              gridLines: { color: gridColor }
            }],
            yAxes: [{
              ticks: { fontColor: tickColor, beginAtZero: true },
              gridLines: { color: gridColor },
              scaleLabel: { display: true, labelString: 'Frequency (MHz)', fontColor: labelColor }
            }]
          }
        }
      });
    })();

    // Reliability counters (two grouped bars)
    (function renderErrs() {
      var canvas = document.getElementById('errs_' + ch.canvas_id);
      if (!canvas) return;

      new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
          labels: ['PLC Codewords', 'NCP Fields'],
          datasets: [
            {
              label: 'Total',
              data: [ch.plcTotalCw, ch.ncpTotalFields],
              backgroundColor: rgbaFill(cRange, 0.35),
              borderColor: cRange,
              borderWidth: 1
            },
            {
              label: 'Errors',
              data: [ch.plcUnreliableCw, ch.ncpCrcFailures],
              backgroundColor: rgbaFill(cErr, 0.65),
              borderColor: cErr,
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          legend: { display: true, labels: { fontColor: labelColor } },
          tooltips: { mode: 'index', intersect: false },
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

  const mac = r.mac_address || 'N/A';
  const status = (r.status !== undefined && r.status !== null) ? r.status : 'N/A';
  const statusText = status === 0 ? 'Success' : String(status);
  const message = r.message ? r.message : '';

  const results = Array.isArray(r.results) ? r.results : [];

  // Build channels with derived frequency window:
  // activeStart = zeroFreq + firstActive * spacing
  // activeEnd   = zeroFreq + lastActive  * spacing
  // bandwidth   = (last-first+1) * spacing
  // All converted to MHz for visuals.
  let totalActiveSubcarriers = 0;

  let worstNcpCrc = -1;
  let worstNcpCrcCh = 'N/A';

  let worstPlcUnrel = -1;
  let worstPlcUnrelCh = 'N/A';

  let globalMinMHz = null;
  let globalMaxMHz = null;

  const tableRows = [];
  const channels = results.map((item, idx) => {
    const channelId = (item && item.channel_id !== undefined && item.channel_id !== null) ? item.channel_id : ('idx-' + (idx + 1));
    const e = item && item.entry ? item.entry : {};

    const zeroHz = Number(e.docsIf31CmDsOfdmChanSubcarrierZeroFreq || 0);
    const spacingHz = Number(e.docsIf31CmDsOfdmChanSubcarrierSpacing || 0);
    const first = Number(e.docsIf31CmDsOfdmChanFirstActiveSubcarrierNum || 0);
    const last = Number(e.docsIf31CmDsOfdmChanLastActiveSubcarrierNum || 0);
    const numActive = Number(e.docsIf31CmDsOfdmChanNumActiveSubcarriers || 0);
    const plcHz = Number(e.docsIf31CmDsOfdmChanPlcFreq || 0);

    const indicator = (e.docsIf31CmDsOfdmChanChanIndicator !== undefined && e.docsIf31CmDsOfdmChanChanIndicator !== null)
      ? e.docsIf31CmDsOfdmChanChanIndicator
      : 'N/A';

    const activeStartHz = zeroHz + (first * spacingHz);
    const activeEndHz = zeroHz + (last * spacingHz);
    const bwHz = (last >= first) ? ((last - first + 1) * spacingHz) : 0;

    const zeroMHz = zeroHz / 1e6;
    const plcMHz = plcHz / 1e6;
    const activeStartMHz = activeStartHz / 1e6;
    const activeEndMHz = activeEndHz / 1e6;
    const bwMHz = bwHz / 1e6;

    const plcTotalCw = Number(e.docsIf31CmDsOfdmChanPlcTotalCodewords || 0);
    const plcUnreliableCw = Number(e.docsIf31CmDsOfdmChanPlcUnreliableCodewords || 0);
    const ncpTotalFields = Number(e.docsIf31CmDsOfdmChanNcpTotalFields || 0);
    const ncpCrcFailures = Number(e.docsIf31CmDsOfdmChanNcpFieldCrcFailures || 0);

    totalActiveSubcarriers += numActive;

    if (ncpCrcFailures > worstNcpCrc) {
      worstNcpCrc = ncpCrcFailures;
      worstNcpCrcCh = String(channelId);
    }
    if (plcUnreliableCw > worstPlcUnrel) {
      worstPlcUnrel = plcUnreliableCw;
      worstPlcUnrelCh = String(channelId);
    }

    if (Number.isFinite(activeStartMHz) && Number.isFinite(activeEndMHz)) {
      if (globalMinMHz === null || activeStartMHz < globalMinMHz) globalMinMHz = activeStartMHz;
      if (globalMaxMHz === null || activeEndMHz > globalMaxMHz) globalMaxMHz = activeEndMHz;
    }

    tableRows.push({
      channel: String(channelId),
      indicator: String(indicator),
      zero: zeroMHz.toFixed(2),
      start: activeStartMHz.toFixed(2),
      end: activeEndMHz.toFixed(2),
      plc: plcMHz.toFixed(2),
      bw: bwMHz.toFixed(2)
    });

    return {
      label: 'OFDM Channel ' + String(channelId),
      canvas_id: 'c' + String(idx + 1),
      channel_id: String(channelId),
      indicator: String(indicator),

      zeroMHz,
      plcMHz,
      activeStartMHz,
      activeEndMHz,
      bwMHz,

      plcTotalCw,
      plcUnreliableCw,
      ncpTotalFields,
      ncpCrcFailures
    };
  });

  // Global chart payload (horizontal range bars)
  // Chart.js 2 horizontalBar can accept "floating bars" if values are [start,end] in data,
  // but we pass as {x:[start,end], y:index} and labels on y-axis for clarity.
  // We keep y labels aligned with array order.
  const labels = channels.map(ch => 'Ch ' + ch.channel_id);
  const ranges = channels.map((ch, i) => ({ x: [ch.activeStartMHz, ch.activeEndMHz], y: i }));
  const plcPts = channels.map((ch, i) => ({ x: ch.plcMHz, y: i }));

  const globalSpanMHz = (globalMinMHz !== null && globalMaxMHz !== null) ? (globalMaxMHz - globalMinMHz) : 0;
  const globalSpanRange = (globalMinMHz !== null && globalMaxMHz !== null)
    ? (globalMinMHz.toFixed(2) + ' - ' + globalMaxMHz.toFixed(2) + ' MHz')
    : 'N/A';

  const kpi = {
    totalActiveSubcarriers: String(totalActiveSubcarriers),
    bandwidthPerChannelMHz: (channels.length > 0 ? channels[0].bwMHz.toFixed(2) : '0.00') + ' MHz',
    worstNcpCrc: String(Math.max(0, worstNcpCrc)),
    worstNcpCrcCh: worstNcpCrcCh,
    worstPlcUnrel: String(Math.max(0, worstPlcUnrel)),
    worstPlcUnrelCh: worstPlcUnrelCh,
    globalSpanMHz: globalSpanMHz.toFixed(2) + ' MHz',
    globalSpanRange: globalSpanRange
  };

  return {
    mac,
    statusText,
    message,
    channelCount: channels.length,
    kpi,
    tableRows,
    global: { labels, ranges, plcPts },
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
    "mac_address": "aa:bb:cc:dd:ee:ff",
    "status": 0,
    "message": "Successfully retrieved downstream OFDM channel statistics",
    "results": [
        {
            "index": 48,
            "channel_id": 194,
            "entry": {
                "docsIf31CmDsOfdmChanChannelId": 194,
                "docsIf31CmDsOfdmChanChanIndicator": "backupPrimary",
                "docsIf31CmDsOfdmChanSubcarrierZeroFreq": 1019600000,
                "docsIf31CmDsOfdmChanFirstActiveSubcarrierNum": 296,
                "docsIf31CmDsOfdmChanLastActiveSubcarrierNum": 7895,
                "docsIf31CmDsOfdmChanNumActiveSubcarriers": 7528,
                "docsIf31CmDsOfdmChanSubcarrierSpacing": 25000,
                "docsIf31CmDsOfdmChanCyclicPrefix": 256,
                "docsIf31CmDsOfdmChanRollOffPeriod": 128,
                "docsIf31CmDsOfdmChanPlcFreq": 1150000000,
                "docsIf31CmDsOfdmChanNumPilots": 56,
                "docsIf31CmDsOfdmChanTimeInterleaverDepth": 16,
                "docsIf31CmDsOfdmChanPlcTotalCodewords": 32837417,
                "docsIf31CmDsOfdmChanPlcUnreliableCodewords": 0,
                "docsIf31CmDsOfdmChanNcpTotalFields": 210146720,
                "docsIf31CmDsOfdmChanNcpFieldCrcFailures": 0
            }
        },
        {
            "index": 49,
            "channel_id": 193,
            "entry": {
                "docsIf31CmDsOfdmChanChannelId": 193,
                "docsIf31CmDsOfdmChanChanIndicator": "backupPrimary",
                "docsIf31CmDsOfdmChanSubcarrierZeroFreq": 827600000,
                "docsIf31CmDsOfdmChanFirstActiveSubcarrierNum": 296,
                "docsIf31CmDsOfdmChanLastActiveSubcarrierNum": 7895,
                "docsIf31CmDsOfdmChanNumActiveSubcarriers": 7528,
                "docsIf31CmDsOfdmChanSubcarrierSpacing": 25000,
                "docsIf31CmDsOfdmChanCyclicPrefix": 256,
                "docsIf31CmDsOfdmChanRollOffPeriod": 128,
                "docsIf31CmDsOfdmChanPlcFreq": 930000000,
                "docsIf31CmDsOfdmChanNumPilots": 56,
                "docsIf31CmDsOfdmChanTimeInterleaverDepth": 16,
                "docsIf31CmDsOfdmChanPlcTotalCodewords": 32838607,
                "docsIf31CmDsOfdmChanPlcUnreliableCodewords": 0,
                "docsIf31CmDsOfdmChanNcpTotalFields": 210153952,
                "docsIf31CmDsOfdmChanNcpFieldCrcFailures": 0
            }
        }
    ]
}
````
</details>
