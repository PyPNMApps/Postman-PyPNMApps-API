# PyPNM / SingleCapture / SpectrumAnalysis / GetCapture-SCQAM

## Source Files

- HTML/script: `visual/PyPNM/SingleCapture/SpectrumAnalysis/GetCapture-SCQAM.html`
- JSON sample: missing

## Preview

Preview unavailable because no matching sample JSON fixture exists for this visual.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Spectrum Analysis Visualizer - Grouped By Channel
// Changes requested:
// - Remove redundant capture-parameter columns from each row
// - Show Device Details as a table in a separate container
// - Show Capture Parameters once per channel in a separate container

var template = `
<style>
    body { margin: 0; padding: 0; background: #0f1220; }
    .container {
        background-color: #1a1a2e;
        padding: 20px;
        border-radius: 10px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #ffffff;
        max-width: 1600px;
        margin: 0 auto;
    }
    .channel-block {
        margin-bottom: 28px;
        padding: 18px;
        border-radius: 10px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
    }
    .channel-title {
        margin: 0 0 12px 0;
        font-size: 18px;
        color: #00d9ff;
        letter-spacing: 0.3px;
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        gap: 12px;
        flex-wrap: wrap;
    }
    .channel-subtitle {
        font-size: 12px;
        color: rgba(255,255,255,0.75);
        margin-top: 4px;
    }
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 11px;
        background: rgba(0,217,255,0.12);
        border: 1px solid rgba(0,217,255,0.25);
        color: #c9f7ff;
    }

    .split-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
        gap: 14px;
        margin: 10px 0 18px 0;
    }
    .panel {
        padding: 14px;
        border-radius: 10px;
        background: rgba(0,0,0,0.18);
        border: 1px solid rgba(255,255,255,0.06);
    }
    .panel-title {
        margin: 0 0 10px 0;
        color: #00d9ff;
        font-size: 14px;
        border-bottom: 1px solid rgba(15, 52, 96, 0.9);
        padding-bottom: 6px;
        letter-spacing: 0.2px;
    }

    .kv-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
    }
    .kv-table th {
        background-color: #16213e;
        color: #00d9ff;
        padding: 9px 8px;
        text-align: left;
        border-bottom: 2px solid #0f3460;
        white-space: nowrap;
    }
    .kv-table td {
        padding: 9px 8px;
        border-bottom: 1px solid #0f3460;
        color: #e0e0e0;
        white-space: nowrap;
    }
    .kv-table tr:nth-child(even) { background-color: rgba(15, 52, 96, 0.25); }

    .chart-container {
        position: relative;
        margin: 12px 0 18px 0;
        padding: 14px;
        border-radius: 10px;
        background: rgba(0,0,0,0.18);
        border: 1px solid rgba(255,255,255,0.06);
    }

    .table-container {
        margin-top: 14px;
        overflow-x: auto;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .data-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
        min-width: 860px;
    }
    .data-table th {
        background-color: #16213e;
        color: #00d9ff;
        padding: 10px 8px;
        text-align: left;
        border-bottom: 2px solid #0f3460;
        white-space: nowrap;
    }
    .data-table td {
        padding: 9px 8px;
        border-bottom: 1px solid #0f3460;
        color: #e0e0e0;
        white-space: nowrap;
    }
    .data-table tr:hover { background-color: #0f3460; }
    .data-table tr:nth-child(even) { background-color: rgba(15, 52, 96, 0.25); }
</style>

<div class="container">
  {{#unless channels.length}}
    <div style="padding: 22px; color: rgba(255,255,255,0.75);">No analyses found in response.</div>
  {{/unless}}

  {{#each channels}}
    <div class="channel-block">
      <div class="channel-title">
        <div>
          Channel {{channelId}}
          <span class="badge">captures: {{captureCount}}</span>
          <div class="channel-subtitle">MAC: {{macAddress}}</div>
        </div>
      </div>

      <div class="split-grid">
        <div class="panel">
          <div class="panel-title">Device Details</div>
          <table class="kv-table">
            <thead>
              <tr><th>Field</th><th>Value</th></tr>
            </thead>
            <tbody>
              {{#each deviceDetailsRows}}
                <tr><td>{{k}}</td><td>{{v}}</td></tr>
              {{/each}}
            </tbody>
          </table>
        </div>

        <div class="panel">
          <div class="panel-title">Capture Parameters</div>
          <table class="kv-table">
            <thead>
              <tr><th>Field</th><th>Value</th></tr>
            </thead>
            <tbody>
              {{#each captureParamsRows}}
                <tr><td>{{k}}</td><td>{{v}}</td></tr>
              {{/each}}
            </tbody>
          </table>
        </div>
      </div>

      <div class="chart-container">
        <canvas id="spectrumChart-ch{{channelId}}" height="380"></canvas>
      </div>

      <div class="panel" style="margin-top: 12px;">
        <div class="panel-title">Channel Analysis Details</div>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Capture</th>
                <th>Freq Range (MHz)</th>
                <th>Center (MHz)</th>
                <th>Avg Power (dB)</th>
                <th>Min / Max (dB)</th>
              </tr>
            </thead>
            <tbody>
              {{#each tableRows}}
                <tr>
                  <td>{{captureLabel}}</td>
                  <td>{{freqRangeMHz}}</td>
                  <td>{{centerMHz}}</td>
                  <td>{{avgPower}}</td>
                  <td>{{minMaxPower}}</td>
                </tr>
              {{/each}}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  {{/each}}
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>
<script>
(function () {
  function palette(i) {
    var colors = [
      {border: 'rgba(255, 99, 132, 1)'},
      {border: 'rgba(54, 162, 235, 1)'},
      {border: 'rgba(255, 206, 86, 1)'},
      {border: 'rgba(75, 192, 192, 1)'},
      {border: 'rgba(153, 102, 255, 1)'},
      {border: 'rgba(255, 159, 64, 1)'},
      {border: 'rgba(199, 199, 199, 1)'},
      {border: 'rgba(83, 102, 255, 1)'},
      {border: 'rgba(255, 99, 255, 1)'},
      {border: 'rgba(99, 255, 132, 1)'}
    ];
    return colors[i % colors.length];
  }

  pm.getData(function (err, value) {
    if (err || !value || !Array.isArray(value.channels)) return;

    value.channels.forEach(function (ch) {
      var el = document.getElementById('spectrumChart-ch' + ch.channelId);
      if (!el) return;

      var ctx = el.getContext('2d');
      var datasets = [];

      (ch.captures || []).forEach(function (cap, idx) {
        var sig = cap.signal_analysis || {};
        var freqs = Array.isArray(sig.frequencies) ? sig.frequencies : [];
        var mags  = Array.isArray(sig.magnitudes)  ? sig.magnitudes  : [];
        if (!freqs.length || !mags.length) return;

        var pts = [];
        var n = Math.min(freqs.length, mags.length);
        for (var i = 0; i < n; i++) {
          pts.push({ x: freqs[i], y: mags[i] });
        }

        var c = palette(idx);
        datasets.push({
          label: cap.captureLabel,
          data: pts,
          borderColor: c.border,
          backgroundColor: 'transparent',
          fill: false,
          borderWidth: 1.6,
          pointRadius: 0,
          lineTension: 0
        });
      });

      new Chart(ctx, {
        type: "line",
        data: { datasets: datasets },
        options: {
          responsive: true,
          legend: {
            display: true,
            position: 'top',
            labels: { fontColor: '#ffffff', fontSize: 11 }
          },
          title: {
            display: true,
            text: 'Spectrum Analysis - Ch ' + ch.channelId + ' (Frequency vs Magnitude)',
            fontColor: '#ffffff',
            fontSize: 14
          },
          elements: {
            point: { radius: 0 },
            line: { borderWidth: 1.6 }
          },
          scales: {
            xAxes: [{
              type: 'linear',
              position: 'bottom',
              scaleLabel: { display: true, labelString: 'Frequency (MHz)', fontColor: '#ffffff' },
              ticks: {
                fontColor: '#ffffff',
                callback: function (value) { return (value / 1000000).toFixed(0); }
              },
              gridLines: { color: 'rgba(255, 255, 255, 0.08)' }
            }],
            yAxes: [{
              scaleLabel: { display: true, labelString: 'Magnitude (dB)', fontColor: '#ffffff' },
              ticks: { fontColor: '#ffffff' },
              gridLines: { color: 'rgba(255, 255, 255, 0.08)' }
            }]
          },
          tooltips: {
            mode: 'nearest',
            intersect: false,
            callbacks: {
              label: function (tooltipItem, data) {
                var dsLabel = (data.datasets[tooltipItem.datasetIndex] && data.datasets[tooltipItem.datasetIndex].label) || '';
                var freqMHz = (tooltipItem.xLabel / 1000000).toFixed(2);
                var magDb = Number(tooltipItem.yLabel).toFixed(2);
                return dsLabel + ': ' + freqMHz + ' MHz, ' + magDb + ' dB';
              }
            }
          }
        }
      });
    });
  });
})();
</script>
`;

function constructVisualizerPayload() {
  var response = pm.response.json();
  var analyses = (response && response.data && Array.isArray(response.data.analyses)) ? response.data.analyses : [];

  function safeStr(v, fallback) {
    return (typeof v === 'string' && v.length) ? v : fallback;
  }

  function safeNum(v, fallback) {
    return (typeof v === 'number' && isFinite(v)) ? v : fallback;
  }

  var SANITIZE_GENERIC_SYSTEM_DESCRIPTION = {
    HW_REV: '1.0',
    VENDOR: 'LANCity',
    BOOTR: 'NONE',
    SW_REV: '1.0.0',
    MODEL: 'LCPET-3'
  };

  function sanitizeMac(value, fallback) {
    var fb = (fallback === undefined || fallback === null) ? 'N/A' : fallback;
    if (value === undefined || value === null) return fb;
    var text = String(value).trim();
    if (!text) return fb;
    var compact = text.replace(/[^0-9a-f]/gi, '').toLowerCase();
    if (compact.length !== 12) return text;
    if (text.indexOf(':') !== -1) return compact.match(/.{1,2}/g).join(':');
    if (text.indexOf('-') !== -1) return compact.match(/.{1,2}/g).join('-');
    if (text.indexOf('_') !== -1) return compact.match(/.{1,2}/g).join('_');
    return compact;
  }

  function sanitizeSystemDescription(_sys) {
    return {
      HW_REV: SANITIZE_GENERIC_SYSTEM_DESCRIPTION.HW_REV,
      VENDOR: SANITIZE_GENERIC_SYSTEM_DESCRIPTION.VENDOR,
      BOOTR: SANITIZE_GENERIC_SYSTEM_DESCRIPTION.BOOTR,
      SW_REV: SANITIZE_GENERIC_SYSTEM_DESCRIPTION.SW_REV,
      MODEL: SANITIZE_GENERIC_SYSTEM_DESCRIPTION.MODEL
    };
  }

  function toMHz(vHz) {
    if (typeof vHz !== 'number' || !isFinite(vHz)) return 'N/A';
    return (vHz / 1e6).toFixed(2);
  }

  function computeStats(mags) {
    if (!Array.isArray(mags) || mags.length === 0) return { avg: 'N/A', min: 'N/A', max: 'N/A' };
    var sum = 0;
    var min = Infinity;
    var max = -Infinity;
    var n = 0;
    for (var i = 0; i < mags.length; i++) {
      var x = mags[i];
      if (typeof x !== 'number' || !isFinite(x)) continue;
      sum += x;
      n += 1;
      if (x < min) min = x;
      if (x > max) max = x;
    }
    var avg = (n > 0) ? (sum / n) : NaN;
    return {
      avg: isFinite(avg) ? avg.toFixed(2) : 'N/A',
      min: isFinite(min) ? min.toFixed(2) : 'N/A',
      max: isFinite(max) ? max.toFixed(2) : 'N/A'
    };
  }

  function kvRows(obj, keys) {
    var rows = [];
    keys.forEach(function (k) {
      rows.push({ k: k, v: (obj && obj[k] !== undefined && obj[k] !== null && String(obj[k]).length) ? String(obj[k]) : 'N/A' });
    });
    return rows;
  }

  var byChannel = {};

  analyses.forEach(function (a) {
    if (!a) return;

    var chId = (typeof a.channel_id === 'number') ? a.channel_id : 0;
    if (!byChannel[chId]) {
      var dd = a.device_details || {};
      var sys = sanitizeSystemDescription(dd.system_description || {});

      byChannel[chId] = {
        channelId: chId,
        macAddress: sanitizeMac(a.mac_address, 'N/A'),
        captures: [],
        tableRows: [],
        deviceDetailsRows: kvRows(sys, ['MODEL', 'SW_REV', 'HW_REV', 'VENDOR', 'BOOTR']),
        captureParamsRows: []
      };
    }

    var cap = a.capture_parameters || {};
    var sig = a.signal_analysis || {};

    var firstHz = safeNum(cap.first_segment_center_freq, NaN);
    var lastHz  = safeNum(cap.last_segment_center_freq, NaN);
    var centerHz = (isFinite(firstHz) && isFinite(lastHz)) ? (firstHz + lastHz) / 2 : NaN;

    var stats = computeStats(sig.magnitudes || []);

    var captureLabel =
      'Capture ' + (byChannel[chId].captures.length + 1) +
      (isFinite(centerHz) ? (' @ ' + toMHz(centerHz) + ' MHz') : '');

    byChannel[chId].captures.push({
      captureLabel: captureLabel,
      capture_parameters: cap,
      signal_analysis: sig
    });

    byChannel[chId].tableRows.push({
      captureLabel: captureLabel,
      freqRangeMHz: (isFinite(firstHz) ? toMHz(firstHz) : 'N/A') + ' - ' + (isFinite(lastHz) ? toMHz(lastHz) : 'N/A'),
      centerMHz: isFinite(centerHz) ? toMHz(centerHz) : 'N/A',
      avgPower: stats.avg,
      minMaxPower: stats.min + ' / ' + stats.max
    });

    // Capture parameters are redundant per your comment; capture them once per channel (first non-empty)
    if (byChannel[chId].captureParamsRows.length === 0) {
      byChannel[chId].captureParamsRows = [
        { k: 'Bin BW (Hz)',       v: (sig.bin_bandwidth !== undefined && sig.bin_bandwidth !== null) ? String(sig.bin_bandwidth) : 'N/A' },
        { k: 'Bins/Segment',      v: (cap.num_bins_per_segment !== undefined && cap.num_bins_per_segment !== null) ? String(cap.num_bins_per_segment) : 'N/A' },
        { k: 'Seg Span (Hz)',     v: (cap.segment_freq_span !== undefined && cap.segment_freq_span !== null) ? String(cap.segment_freq_span) : 'N/A' },
        { k: 'Noise BW',          v: (cap.noise_bw !== undefined && cap.noise_bw !== null) ? String(cap.noise_bw) : 'N/A' },
        { k: 'Window Fn',         v: (cap.window_function !== undefined && cap.window_function !== null) ? String(cap.window_function) : 'N/A' },
        { k: 'Num Averages',      v: (cap.num_averages !== undefined && cap.num_averages !== null) ? String(cap.num_averages) : 'N/A' },
        { k: 'Retrieval Type',    v: (cap.spectrum_retrieval_type !== undefined && cap.spectrum_retrieval_type !== null) ? String(cap.spectrum_retrieval_type) : 'N/A' }
      ];
    }
  });

  var channels = Object.keys(byChannel)
    .map(function (k) { return byChannel[k]; })
    .sort(function (a, b) { return a.channelId - b.channelId; })
    .map(function (ch) {
      ch.captureCount = (ch.captures || []).length;
      return ch;
    });

  return { channels: channels };
}

pm.visualizer.set(template, constructVisualizerPayload());
````
</details>
