# PyPNM / DOCSIS-3.0 / DS-SCQAM-Stats

## Source Files

- HTML/script: `visual/PyPNM/DOCSIS-3.0/DS-SCQAM-Stats.html`
- JSON sample: `visual/PyPNM/DOCSIS-3.0/DS-SCQAM-Stats.json`

## Preview

<iframe src="../../../visual-previews/DOCSIS-3.0/DS-SCQAM-Stats.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Postman Visualizer - Downstream SC-QAM Channel Stats (Dark Mode)
// Useful visuals:
// 1) RxMER (dB) vs Frequency (MHz)  [line]
// 2) Downstream Power (dBmV) vs Frequency (MHz) [line]
// 3) Correcteds / Uncorrectables / Microreflections by Channel [bar]
// 4) Key metadata + highlights (min/max)

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
    padding: 16px 16px 10px 16px;
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
    margin: 0 0 6px 0;
    font-size: 12px;
    color: rgba(234,234,234,0.85);
  }
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
  .divider {
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 14px 0;
  }
  .kpi {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    margin-top: 10px;
  }
  .kpiItem {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px;
  }
  .kpiItem .k {
    font-size: 11px;
    color: rgba(234,234,234,0.8);
    margin-bottom: 4px;
  }
  .kpiItem .v {
    font-size: 16px;
    font-weight: 700;
    color: #eaeaea;
  }
  .kpiItem .h {
    margin-top: 4px;
    font-size: 11px;
    color: rgba(159,180,255,0.95);
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
  <div class="title">Downstream SC-QAM Channel Stats</div>
  <div class="meta">
    <div class="pill"><b>MAC</b> {{mac}}</div>
    <div class="pill"><b>Status</b> {{statusText}}</div>
    <div class="pill"><b>Channels</b> {{channelCount}}</div>
    <div class="pill"><b>Freq Span</b> {{freqSpanMHz}} MHz</div>
  </div>
  <div class="sub">{{message}}</div>

  <div class="kpi">
    <div class="kpiItem">
      <div class="k">Min RxMER (dB)</div>
      <div class="v">{{kpi.minRxMerDb}}</div>
      <div class="h">Ch {{kpi.minRxMerCh}} @ {{kpi.minRxMerFreq}} MHz</div>
    </div>
    <div class="kpiItem">
      <div class="k">Avg RxMER (dB)</div>
      <div class="v">{{kpi.avgRxMerDb}}</div>
      <div class="h">Across all channels</div>
    </div>
    <div class="kpiItem">
      <div class="k">Power Range (dBmV)</div>
      <div class="v">{{kpi.pwrRange}}</div>
      <div class="h">Min {{kpi.minPwr}} / Max {{kpi.maxPwr}}</div>
    </div>
  </div>
</div>

<div class="grid">
  <div class="card">
    <h3>RxMER (dB) vs Frequency (MHz)</h3>
    <div class="sub">Quick health view. Lower RxMER typically indicates impairment.</div>
    <canvas id="chart_rxmer" height="90"></canvas>
  </div>

  <div class="card">
    <h3>Downstream Power (dBmV) vs Frequency (MHz)</h3>
    <div class="sub">Helps identify tilt and level issues across the band.</div>
    <canvas id="chart_power" height="90"></canvas>
  </div>

  <div class="card">
    <h3>Impairment Counters By Channel</h3>
    <div class="sub">Grouped by channel (X-axis sorted by frequency low → high).</div>
    <canvas id="chart_counters" height="110"></canvas>
  </div>

  <div class="card">
    <h3>Channel Table (Top Fields)</h3>
    <div class="sub">Sorted by frequency (ascending).</div>
    <table>
      <thead>
        <tr>
          <th>Ch</th>
          <th>Freq (MHz)</th>
          <th>Width (MHz)</th>
          <th>Power (dBmV)</th>
          <th>RxMER (dB)</th>
          <th>Correcteds</th>
          <th>Uncorrectables</th>
          <th>Microref</th>
        </tr>
      </thead>
      <tbody>
        {{#each rows}}
        <tr>
          <td>{{ch}}</td>
          <td>{{freqMHz}}</td>
          <td>{{widthMHz}}</td>
          <td>{{pwr}}</td>
          <td class="{{rxmerClass}}">{{rxmerDb}}</td>
          <td>{{corr}}</td>
          <td class="{{uncClass}}">{{unc}}</td>
          <td>{{micro}}</td>
        </tr>
        {{/each}}
      </tbody>
    </table>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js"></script>
<script>
pm.getData(function (err, value) {
  if (err) {
    console.error(err);
    return;
  }

  var gridColor  = 'rgba(255,255,255,0.12)';
  var tickColor  = 'rgba(234,234,234,0.85)';
  var labelColor = '#eaeaea';

  var rgbaFill = function(rgb, a) {
    return rgb.replace('rgb', 'rgba').replace(')', ', ' + a + ')');
  };

  // --- RxMER chart ---
  (function renderRxMer() {
    var canvas = document.getElementById('chart_rxmer');
    if (!canvas) return;

    var c = 'rgb(54, 162, 235)';

    new Chart(canvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: value.freqMHz,
        datasets: [{
          label: 'RxMER (dB)',
          data: value.rxMerDb,
          borderColor: c,
          backgroundColor: rgbaFill(c, 0.08),
          borderWidth: 1.6,
          fill: false,
          pointRadius: 0,
          pointHoverRadius: 0,
          lineTension: 0.12
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        legend: { display: true, labels: { fontColor: labelColor } },
        tooltips: { mode: 'index', intersect: false },
        hover: { mode: 'nearest', intersect: false },
        scales: {
          xAxes: [{
            ticks: { fontColor: tickColor, maxTicksLimit: 12 },
            gridLines: { color: gridColor },
            scaleLabel: { display: true, labelString: 'Frequency (MHz)', fontColor: labelColor }
          }],
          yAxes: [{
            ticks: { fontColor: tickColor },
            gridLines: { color: gridColor },
            scaleLabel: { display: true, labelString: 'RxMER (dB)', fontColor: labelColor }
          }]
        }
      }
    });
  })();

  // --- Power chart ---
  (function renderPower() {
    var canvas = document.getElementById('chart_power');
    if (!canvas) return;

    var c = 'rgb(75, 192, 192)';

    new Chart(canvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: value.freqMHz,
        datasets: [{
          label: 'Power (dBmV)',
          data: value.powerDbmv,
          borderColor: c,
          backgroundColor: rgbaFill(c, 0.08),
          borderWidth: 1.6,
          fill: false,
          pointRadius: 0,
          pointHoverRadius: 0,
          lineTension: 0.12
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        legend: { display: true, labels: { fontColor: labelColor } },
        tooltips: { mode: 'index', intersect: false },
        hover: { mode: 'nearest', intersect: false },
        scales: {
          xAxes: [{
            ticks: { fontColor: tickColor, maxTicksLimit: 12 },
            gridLines: { color: gridColor },
            scaleLabel: { display: true, labelString: 'Frequency (MHz)', fontColor: labelColor }
          }],
          yAxes: [{
            ticks: { fontColor: tickColor },
            gridLines: { color: gridColor },
            scaleLabel: { display: true, labelString: 'Power (dBmV)', fontColor: labelColor }
          }]
        }
      }
    });
  })();

  // --- Counters chart (bar) ---
  (function renderCounters() {
    var canvas = document.getElementById('chart_counters');
    if (!canvas) return;

    // Bars are grouped per label by default in Chart.js 2.x (side-by-side per channel).
    // Labels must already be in frequency-sorted order.
    var c1 = 'rgb(255, 206, 86)';   // correcteds
    var c2 = 'rgb(255, 99, 132)';   // uncorrectables
    var c3 = 'rgb(153, 102, 255)';  // microreflections

    new Chart(canvas.getContext('2d'), {
      type: 'bar',
      data: {
        // Use frequency-sorted labels so counters line up by channel in low->high frequency order.
        labels: value.chFreqLabels,
        datasets: [
          {
            label: 'Correcteds',
            data: value.correcteds,
            backgroundColor: rgbaFill(c1, 0.55),
            borderColor: c1,
            borderWidth: 1
          },
          {
            label: 'Uncorrectables',
            data: value.uncorrectables,
            backgroundColor: rgbaFill(c2, 0.55),
            borderColor: c2,
            borderWidth: 1
          },
          {
            label: 'Microreflections',
            data: value.microreflections,
            backgroundColor: rgbaFill(c3, 0.55),
            borderColor: c3,
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
            ticks: {
              fontColor: tickColor,
              maxTicksLimit: 18
            },
            gridLines: { color: gridColor },
            scaleLabel: { display: true, labelString: 'Channel (Sorted By Frequency Low → High)', fontColor: labelColor }
          }],
          yAxes: [{
            ticks: { fontColor: tickColor, beginAtZero: true },
            gridLines: { color: gridColor },
            scaleLabel: { display: true, labelString: 'Count', fontColor: labelColor }
          }]
        }
      }
    });
  })();
});
</script>
`;

function constructVisualizerPayload() {
  const r = pm.response.json();

  const mac = r.mac_address || 'N/A';
  const status = (r.status !== undefined && r.status !== null) ? r.status : 'N/A';
  const statusText = status === 0 ? 'Success' : String(status);
  const message = r.message || '';

  const results = Array.isArray(r.results) ? r.results : [];

  // normalize rows and sort by frequency ascending
  const rowsNorm = results.map((item, idx) => {
    const entry = item && item.entry ? item.entry : {};
    const ch = (item && item.channel_id !== undefined && item.channel_id !== null)
      ? item.channel_id
      : (entry.docsIfDownChannelId !== undefined ? entry.docsIfDownChannelId : idx + 1);

    const freqHz = entry.docsIfDownChannelFrequency;
    const widthHz = entry.docsIfDownChannelWidth;

    const freqMHz = (typeof freqHz === 'number') ? (freqHz / 1e6) : null;
    const widthMHz = (typeof widthHz === 'number') ? (widthHz / 1e6) : null;

    const pwr = (entry.docsIfDownChannelPower !== undefined && entry.docsIfDownChannelPower !== null) ? entry.docsIfDownChannelPower : null;

    // RxMER may arrive either as dB (e.g. 43.3) or tenths of dB (e.g. 433).
    const rxMerRaw = entry.docsIf3SignalQualityExtRxMER;
    let rxmerDb = null;
    if (typeof rxMerRaw === 'number' && isFinite(rxMerRaw)) {
      rxmerDb = rxMerRaw > 100 ? (rxMerRaw / 10.0) : rxMerRaw;
    }

    const corr = (entry.docsIfSigQExtCorrecteds !== undefined && entry.docsIfSigQExtCorrecteds !== null)
      ? entry.docsIfSigQExtCorrecteds
      : (entry.docsIfSigQCorrecteds !== undefined ? entry.docsIfSigQCorrecteds : 0);

    const unc = (entry.docsIfSigQExtUncorrectables !== undefined && entry.docsIfSigQExtUncorrectables !== null)
      ? entry.docsIfSigQExtUncorrectables
      : (entry.docsIfSigQUncorrectables !== undefined ? entry.docsIfSigQUncorrectables : 0);

    const micro = (entry.docsIfSigQMicroreflections !== undefined && entry.docsIfSigQMicroreflections !== null)
      ? entry.docsIfSigQMicroreflections
      : 0;

    return {
      ch,
      freqMHz,
      widthMHz,
      pwr,
      rxmerDb,
      corr,
      unc,
      micro
    };
  }).filter(rw => rw.freqMHz !== null);

  // This sort drives ALL visuals (table + RxMER line + power line + counters bar)
  rowsNorm.sort((a, b) => a.freqMHz - b.freqMHz);

  const freqs = rowsNorm.map(rw => Number(rw.freqMHz.toFixed(3)));
  const rxmer = rowsNorm.map(rw => rw.rxmerDb);
  const pwr = rowsNorm.map(rw => rw.pwr);

  // Labels aligned with sorted order:
  // - chLabels: just channel id
  // - chFreqLabels: channel id + freq so the counters chart ordering is unambiguous
  const chLabels = rowsNorm.map(rw => String(rw.ch));
  const chFreqLabels = rowsNorm.map(rw => `Ch ${rw.ch} @ ${rw.freqMHz.toFixed(3)} MHz`);

  const correcteds = rowsNorm.map(rw => rw.corr);
  const uncorrectables = rowsNorm.map(rw => rw.unc);
  const microreflections = rowsNorm.map(rw => rw.micro);

  // KPIs
  const finiteRx = rowsNorm.filter(rw => typeof rw.rxmerDb === 'number' && isFinite(rw.rxmerDb));
  const finitePwr = rowsNorm.filter(rw => typeof rw.pwr === 'number' && isFinite(rw.pwr));

  let minRx = null;
  let maxRx = null;
  let avgRx = null;

  if (finiteRx.length) {
    minRx = finiteRx.reduce((m, rr) => (m === null || rr.rxmerDb < m.rxmerDb) ? rr : m, null);
    maxRx = finiteRx.reduce((m, rr) => (m === null || rr.rxmerDb > m.rxmerDb) ? rr : m, null);
    avgRx = finiteRx.reduce((s, rr) => s + rr.rxmerDb, 0) / finiteRx.length;
  }

  let minP = null;
  let maxP = null;
  if (finitePwr.length) {
    minP = finitePwr.reduce((m, rr) => (m === null || rr.pwr < m.pwr) ? rr : m, null);
    maxP = finitePwr.reduce((m, rr) => (m === null || rr.pwr > m.pwr) ? rr : m, null);
  }

  const freqSpan = freqs.length ? (Math.max(...freqs) - Math.min(...freqs)) : 0;

  // table rows with simple highlighting heuristics
  const rows = rowsNorm.map(rw => {
    const rxmerClass = (typeof rw.rxmerDb === 'number')
      ? (rw.rxmerDb < 35 ? 'bad' : (rw.rxmerDb < 38 ? 'warn' : ''))
      : '';
    const uncClass = (rw.unc && rw.unc > 0) ? 'bad' : '';
    return {
      ch: rw.ch,
      freqMHz: rw.freqMHz.toFixed(3),
      widthMHz: (rw.widthMHz !== null && rw.widthMHz !== undefined) ? rw.widthMHz.toFixed(3) : 'N/A',
      pwr: (rw.pwr !== null && rw.pwr !== undefined) ? rw.pwr.toFixed(2) : 'N/A',
      rxmerDb: (rw.rxmerDb !== null && rw.rxmerDb !== undefined) ? rw.rxmerDb.toFixed(1) : 'N/A',
      rxmerClass,
      corr: rw.corr,
      unc: rw.unc,
      uncClass,
      micro: rw.micro
    };
  });

  const kpi = {
    minRxMerDb: minRx ? minRx.rxmerDb.toFixed(1) : 'N/A',
    minRxMerCh: minRx ? String(minRx.ch) : 'N/A',
    minRxMerFreq: minRx ? minRx.freqMHz.toFixed(3) : 'N/A',
    avgRxMerDb: (avgRx !== null && avgRx !== undefined) ? avgRx.toFixed(1) : 'N/A',
    pwrRange: (minP && maxP) ? (maxP.pwr - minP.pwr).toFixed(2) : 'N/A',
    minPwr: minP ? minP.pwr.toFixed(2) : 'N/A',
    maxPwr: maxP ? maxP.pwr.toFixed(2) : 'N/A'
  };

  return {
    mac,
    statusText,
    channelCount: rowsNorm.length,
    freqSpanMHz: freqSpan.toFixed(3),
    message,
    // chart series
    freqMHz: freqs,
    rxMerDb: rxmer,
    powerDbmv: pwr,
    // counters chart labels/series (aligned to frequency-sorted order)
    chLabels,
    chFreqLabels,
    correcteds,
    uncorrectables,
    microreflections,
    // KPI + table
    kpi,
    rows
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
    "message": "Successfully retrieved downstream SC-QAM channel stats",
    "results": [
        {
            "index": 3,
            "channel_id": 3,
            "entry": {
                "docsIfDownChannelId": 3,
                "docsIfDownChannelFrequency": 621000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": 0.2,
                "docsIfSigQUnerroreds": 361176685,
                "docsIfSigQCorrecteds": 5,
                "docsIfSigQUncorrectables": 33,
                "docsIfSigQMicroreflections": 37,
                "docsIfSigQExtUnerroreds": 361180048,
                "docsIfSigQExtCorrecteds": 5,
                "docsIfSigQExtUncorrectables": 33,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 50,
            "channel_id": 32,
            "entry": {
                "docsIfDownChannelId": 32,
                "docsIfDownChannelFrequency": 795000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -3.0,
                "docsIfSigQUnerroreds": 360435561,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 36,
                "docsIfSigQExtUnerroreds": 360438743,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 40.9
            }
        },
        {
            "index": 51,
            "channel_id": 31,
            "entry": {
                "docsIfDownChannelId": 31,
                "docsIfDownChannelFrequency": 789000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -3.2,
                "docsIfSigQUnerroreds": 360442221,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 36,
                "docsIfSigQExtUnerroreds": 360446821,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 40.9
            }
        },
        {
            "index": 52,
            "channel_id": 30,
            "entry": {
                "docsIfDownChannelId": 30,
                "docsIfDownChannelFrequency": 783000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -2.5,
                "docsIfSigQUnerroreds": 360461573,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 32,
                "docsIfSigQExtUnerroreds": 360465165,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 40.9
            }
        },
        {
            "index": 53,
            "channel_id": 29,
            "entry": {
                "docsIfDownChannelId": 29,
                "docsIfDownChannelFrequency": 777000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -2.0,
                "docsIfSigQUnerroreds": 360463850,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 37,
                "docsIfSigQExtUnerroreds": 360466347,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 54,
            "channel_id": 28,
            "entry": {
                "docsIfDownChannelId": 28,
                "docsIfDownChannelFrequency": 771000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -2.4,
                "docsIfSigQUnerroreds": 360469374,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 34,
                "docsIfSigQExtUnerroreds": 360472617,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 40.9
            }
        },
        {
            "index": 55,
            "channel_id": 27,
            "entry": {
                "docsIfDownChannelId": 27,
                "docsIfDownChannelFrequency": 765000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -2.7,
                "docsIfSigQUnerroreds": 360476442,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 37,
                "docsIfSigQExtUnerroreds": 360480395,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 40.9
            }
        },
        {
            "index": 56,
            "channel_id": 26,
            "entry": {
                "docsIfDownChannelId": 26,
                "docsIfDownChannelFrequency": 759000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -2.7,
                "docsIfSigQUnerroreds": 360534231,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 38,
                "docsIfSigQExtUnerroreds": 360550838,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 57,
            "channel_id": 25,
            "entry": {
                "docsIfDownChannelId": 25,
                "docsIfDownChannelFrequency": 753000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -2.2,
                "docsIfSigQUnerroreds": 360627000,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 38,
                "docsIfSigQExtUnerroreds": 360630589,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 58,
            "channel_id": 24,
            "entry": {
                "docsIfDownChannelId": 24,
                "docsIfDownChannelFrequency": 747000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -2.2,
                "docsIfSigQUnerroreds": 360634609,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 38,
                "docsIfSigQExtUnerroreds": 360638287,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 59,
            "channel_id": 23,
            "entry": {
                "docsIfDownChannelId": 23,
                "docsIfDownChannelFrequency": 741000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -1.7,
                "docsIfSigQUnerroreds": 360650853,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 36,
                "docsIfSigQExtUnerroreds": 360654944,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 40.9
            }
        },
        {
            "index": 60,
            "channel_id": 22,
            "entry": {
                "docsIfDownChannelId": 22,
                "docsIfDownChannelFrequency": 735000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -1.2,
                "docsIfSigQUnerroreds": 360641541,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 35,
                "docsIfSigQExtUnerroreds": 360646799,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 61,
            "channel_id": 21,
            "entry": {
                "docsIfDownChannelId": 21,
                "docsIfDownChannelFrequency": 729000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -1.2,
                "docsIfSigQUnerroreds": 360668519,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 37,
                "docsIfSigQExtUnerroreds": 360670926,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 62,
            "channel_id": 20,
            "entry": {
                "docsIfDownChannelId": 20,
                "docsIfDownChannelFrequency": 723000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -1.7,
                "docsIfSigQUnerroreds": 360606404,
                "docsIfSigQCorrecteds": 7,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 34,
                "docsIfSigQExtUnerroreds": 360609819,
                "docsIfSigQExtCorrecteds": 7,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 40.9
            }
        },
        {
            "index": 63,
            "channel_id": 19,
            "entry": {
                "docsIfDownChannelId": 19,
                "docsIfDownChannelFrequency": 717000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -1.9,
                "docsIfSigQUnerroreds": 360682861,
                "docsIfSigQCorrecteds": 3,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 35,
                "docsIfSigQExtUnerroreds": 360686823,
                "docsIfSigQExtCorrecteds": 3,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 40.9
            }
        },
        {
            "index": 64,
            "channel_id": 18,
            "entry": {
                "docsIfDownChannelId": 18,
                "docsIfDownChannelFrequency": 711000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -0.7,
                "docsIfSigQUnerroreds": 360704058,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 30,
                "docsIfSigQExtUnerroreds": 360707420,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 40.9
            }
        },
        {
            "index": 65,
            "channel_id": 17,
            "entry": {
                "docsIfDownChannelId": 17,
                "docsIfDownChannelFrequency": 705000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": 0.0,
                "docsIfSigQUnerroreds": 360711653,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 36,
                "docsIfSigQExtUnerroreds": 360715222,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 66,
            "channel_id": 16,
            "entry": {
                "docsIfDownChannelId": 16,
                "docsIfDownChannelFrequency": 699000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -0.5,
                "docsIfSigQUnerroreds": 360712871,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 36,
                "docsIfSigQExtUnerroreds": 360717002,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 67,
            "channel_id": 15,
            "entry": {
                "docsIfDownChannelId": 15,
                "docsIfDownChannelFrequency": 693000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -0.7,
                "docsIfSigQUnerroreds": 360712842,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 38,
                "docsIfSigQExtUnerroreds": 360716752,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 68,
            "channel_id": 14,
            "entry": {
                "docsIfDownChannelId": 14,
                "docsIfDownChannelFrequency": 687000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -0.5,
                "docsIfSigQUnerroreds": 360739764,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 38,
                "docsIfSigQExtUnerroreds": 360745837,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 69,
            "channel_id": 13,
            "entry": {
                "docsIfDownChannelId": 13,
                "docsIfDownChannelFrequency": 681000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -0.5,
                "docsIfSigQUnerroreds": 360690924,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 37,
                "docsIfSigQExtUnerroreds": 360694202,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 70,
            "channel_id": 12,
            "entry": {
                "docsIfDownChannelId": 12,
                "docsIfDownChannelFrequency": 675000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -0.5,
                "docsIfSigQUnerroreds": 360763497,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 37,
                "docsIfSigQExtUnerroreds": 360767563,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 71,
            "channel_id": 11,
            "entry": {
                "docsIfDownChannelId": 11,
                "docsIfDownChannelFrequency": 669000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": 0.0,
                "docsIfSigQUnerroreds": 360767616,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 35,
                "docsIfSigQExtUnerroreds": 360771134,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 72,
            "channel_id": 10,
            "entry": {
                "docsIfDownChannelId": 10,
                "docsIfDownChannelFrequency": 663000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": 0.4,
                "docsIfSigQUnerroreds": 360755707,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 37,
                "docsIfSigQExtUnerroreds": 360759548,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 73,
            "channel_id": 9,
            "entry": {
                "docsIfDownChannelId": 9,
                "docsIfDownChannelFrequency": 657000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": 0.5,
                "docsIfSigQUnerroreds": 360786800,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 36,
                "docsIfSigQExtUnerroreds": 360790844,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 74,
            "channel_id": 8,
            "entry": {
                "docsIfDownChannelId": 8,
                "docsIfDownChannelFrequency": 651000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": 0.0,
                "docsIfSigQUnerroreds": 360795015,
                "docsIfSigQCorrecteds": 9,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 37,
                "docsIfSigQExtUnerroreds": 360798559,
                "docsIfSigQExtCorrecteds": 9,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 75,
            "channel_id": 7,
            "entry": {
                "docsIfDownChannelId": 7,
                "docsIfDownChannelFrequency": 645000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": 0.0,
                "docsIfSigQUnerroreds": 360802345,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 33,
                "docsIfSigQExtUnerroreds": 360806078,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 76,
            "channel_id": 6,
            "entry": {
                "docsIfDownChannelId": 6,
                "docsIfDownChannelFrequency": 639000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": 0.7,
                "docsIfSigQUnerroreds": 360783250,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 33,
                "docsIfSigQExtUnerroreds": 360787028,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 77,
            "channel_id": 5,
            "entry": {
                "docsIfDownChannelId": 5,
                "docsIfDownChannelFrequency": 633000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": 0.7,
                "docsIfSigQUnerroreds": 360828995,
                "docsIfSigQCorrecteds": 8,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 37,
                "docsIfSigQExtUnerroreds": 360833051,
                "docsIfSigQExtCorrecteds": 8,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 44.6
            }
        },
        {
            "index": 78,
            "channel_id": 4,
            "entry": {
                "docsIfDownChannelId": 4,
                "docsIfDownChannelFrequency": 627000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": 0.2,
                "docsIfSigQUnerroreds": 360833055,
                "docsIfSigQCorrecteds": 11,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 38,
                "docsIfSigQExtUnerroreds": 360836487,
                "docsIfSigQExtCorrecteds": 11,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 79,
            "channel_id": 2,
            "entry": {
                "docsIfDownChannelId": 2,
                "docsIfDownChannelFrequency": 615000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": 0.2,
                "docsIfSigQUnerroreds": 360835947,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 33,
                "docsIfSigQExtUnerroreds": 360839264,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        },
        {
            "index": 112,
            "channel_id": 1,
            "entry": {
                "docsIfDownChannelId": 1,
                "docsIfDownChannelFrequency": 609000000,
                "docsIfDownChannelWidth": 6000000,
                "docsIfDownChannelModulation": "qam256",
                "docsIfDownChannelInterleave": "taps32Increment4",
                "docsIfDownChannelPower": -0.7,
                "docsIfSigQUnerroreds": 360852291,
                "docsIfSigQCorrecteds": 0,
                "docsIfSigQUncorrectables": 0,
                "docsIfSigQMicroreflections": 35,
                "docsIfSigQExtUnerroreds": 360895145,
                "docsIfSigQExtCorrecteds": 0,
                "docsIfSigQExtUncorrectables": 0,
                "docsIf3SignalQualityExtRxMER": 43.3
            }
        }
    ]
}
````
</details>
