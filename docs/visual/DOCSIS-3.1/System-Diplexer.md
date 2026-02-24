# PyPNM / DOCSIS-3.1 / System-Diplexer

## Source Files

- HTML/script: `visual/PyPNM/DOCSIS-3.1/System-Diplexer.html`
- JSON sample: `visual/PyPNM/DOCSIS-3.1/System-Diplexer.json`

## Preview

<iframe src="../../../visual-previews/DOCSIS-3.1/System-Diplexer.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Visualization Script
// Visualization Script
var template = `
<style>
    .container {
        font-family: Arial, sans-serif;
        padding: 20px;
        background: #1a1a2e;
        color: #eee;
    }
    .title {
        text-align: center;
        font-size: 18px;
        margin-bottom: 5px;
        color: #00d4ff;
    }
    .subtitle {
        text-align: center;
        font-size: 12px;
        color: #888;
        margin-bottom: 20px;
    }
    .chart-container {
        background: #0d0d1a;
        border-radius: 8px;
        padding: 15px;
    }
    .legend {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 15px;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
    }
    .legend-color {
        width: 30px;
        height: 4px;
        border-radius: 2px;
    }
    .legend-us { background: #ff6b6b; }
    .legend-ds { background: #4dabf7; }

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

    .stats {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
        padding: 15px;
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
    }
    .stat-box {
        text-align: center;
    }
    .stat-value {
        font-size: 18px;
        font-weight: bold;
        color: #00d4ff;
    }
    .stat-label {
        font-size: 10px;
        color: #888;
        margin-top: 3px;
    }
</style>

<div class="container">
    

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
    
        
    <div class="title">Diplexer Frequency Response (9th Order Butterworth)</div>
    <div class="subtitle">MAC: {{macAddress}} | Diplexer Capability: {{diplexerCap}}</div>
<div class="chart-container">
        <canvas id="diplexerChart" height="90"></canvas>
    </div>
    
    <div class="legend">
        <div class="legend-item">
            <div class="legend-color legend-us"></div>
            <span>Upstream (Low-Pass) | 5 - {{bandEdge}} MHz</span>
        </div>
        <div class="legend-item">
            <div class="legend-color legend-ds"></div>
            <span>Downstream (High-Pass) | {{dsLower}} - {{dsUpper}} MHz</span>
        </div>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-value">{{bandEdge}} MHz</div>
            <div class="stat-label">US Cutoff (Band Edge)</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{{dsLower}} MHz</div>
            <div class="stat-label">DS Lower Band Edge</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{{dsUpper}} MHz</div>
            <div class="stat-label">DS Upper Band Edge</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{{dsLowerCap}} / {{dsUpperCap}}</div>
            <div class="stat-label">DS Lower/Upper Cap</div>
        </div>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>
<script>
    if (typeof Chart !== 'undefined' && Chart.pluginService && !window.__diplexerCutoffPluginRegistered) {
        Chart.pluginService.register({
            afterDatasetsDraw: function(chart) {
                var markers = chart.config && chart.config.options && chart.config.options.cutoffMarkers;
                if (!Array.isArray(markers) || !markers.length) return;

                var xScale = chart.scales['x-axis-0'];
                var yScale = chart.scales['y-axis-0'];
                if (!xScale || !yScale) return;

                var labels = (chart.data && Array.isArray(chart.data.labels)) ? chart.data.labels : [];
                var ctx = chart.chart.ctx;
                var area = chart.chartArea;
                if (!ctx || !area) return;

                function nearestLabelIndex(target) {
                    var bestIdx = -1;
                    var bestDiff = Infinity;
                    for (var i = 0; i < labels.length; i++) {
                        var n = Number(labels[i]);
                        if (!isFinite(n)) continue;
                        var d = Math.abs(n - target);
                        if (d < bestDiff) {
                            bestDiff = d;
                            bestIdx = i;
                        }
                    }
                    return bestIdx;
                }

                ctx.save();
                ctx.setLineDash([6, 4]);
                ctx.lineWidth = 1.5;

                markers.forEach(function(m) {
                    var freq = Number(m && m.freqMHz);
                    if (!isFinite(freq)) return;
                    var idx = nearestLabelIndex(freq);
                    if (idx < 0) return;
                    var x = xScale.getPixelForTick(idx);
                    if (!isFinite(x)) return;

                    ctx.strokeStyle = (m && m.color) || '#ffffff';
                    ctx.beginPath();
                    ctx.moveTo(x, area.top);
                    ctx.lineTo(x, area.bottom);
                    ctx.stroke();
                });

                ctx.restore();
            }
        });
        window.__diplexerCutoffPluginRegistered = true;
    }

    var ctx = document.getElementById("diplexerChart");
    var diplexerChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Upstream (Low-Pass)',
                    data: [],
                    borderColor: '#ff6b6b',
                    backgroundColor: 'rgba(255, 107, 107, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    pointRadius: 0,
                    tension: 0.4
                },
                {
                    label: 'Downstream (High-Pass)',
                    data: [],
                    borderColor: '#4dabf7',
                    backgroundColor: 'rgba(77, 171, 247, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    pointRadius: 0,
                    tension: 0.4
                }
            ]
        },
        options: {
            cutoffMarkers: [],
            legend: { display: false },
            title: {
                display: false
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Frequency (MHz)',
                        fontColor: '#888'
                    },
                    ticks: {
                        fontColor: '#666',
                        maxTicksLimit: 15
                    },
                    gridLines: {
                        color: 'rgba(255,255,255,0.1)'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Magnitude (dB)',
                        fontColor: '#888'
                    },
                    ticks: {
                        fontColor: '#666',
                        min: -60,
                        max: 5
                    },
                    gridLines: {
                        color: 'rgba(255,255,255,0.1)'
                    }
                }]
            }
        }
    });

    pm.getData(function (err, value) {
        diplexerChart.data.labels = value.freqLabels;
        diplexerChart.data.datasets[0].data = value.upstreamData;
        diplexerChart.data.datasets[1].data = value.downstreamData;
        diplexerChart.options.cutoffMarkers = [
            { freqMHz: value.bandEdge, color: '#ff6b6b' },
            { freqMHz: value.dsLower, color: '#4dabf7' },
            { freqMHz: value.dsUpper, color: '#4dabf7' }
        ];
        diplexerChart.update();
    });
</script>
`;

function createPayload() {
    var response = pm.response.json();
    var diplexer = response.results.diplexer;
    var device = (response.device && typeof response.device === "object") ? response.device : {};
    var sys = (device.system_description && typeof device.system_description === "object") ? device.system_description : {};
    
    var bandEdge = diplexer.cfg_band_edge / 1000000;
    var dsLower = diplexer.cfg_ds_lower_band_edge / 1000000;
    var dsUpper = diplexer.cfg_ds_upper_band_edge / 1000000;
    
    var order = 9;
    var freqLabels = [];
    var upstreamData = [];
    var downstreamData = [];
    
    var maxFreq = 1400;
    var numPoints = 200;
    
    for (var i = 0; i <= numPoints; i++) {
        var freq = (i / numPoints) * maxFreq;
        freqLabels.push(Math.round(freq));
        
        // 9th order Butterworth low-pass response for upstream
        // H(f) = 1 / sqrt(1 + (f/fc)^(2n))
        // In dB: -10 * log10(1 + (f/fc)^(2n))
        var usRatio = freq / bandEdge;
        var usMag = -10 * Math.log10(1 + Math.pow(usRatio, 2 * order));
        usMag = Math.max(usMag, -60);
        upstreamData.push(usMag.toFixed(2));
        
        // 9th order Butterworth high-pass response for downstream
        // H(f) = 1 / sqrt(1 + (fc/f)^(2n))
        // In dB: -10 * log10(1 + (fc/f)^(2n))
        var dsRatio = dsLower / freq;
        var dsMag;
        if (freq < 1) {
            dsMag = -60;
        } else {
            dsMag = -10 * Math.log10(1 + Math.pow(dsRatio, 2 * order));
            // Apply upper cutoff as well (bandpass effect)
            var dsUpperRatio = freq / dsUpper;
            var dsUpperMag = -10 * Math.log10(1 + Math.pow(dsUpperRatio, 2 * order));
            dsMag = dsMag + dsUpperMag;
        }
        dsMag = Math.max(dsMag, -60);
        downstreamData.push(dsMag.toFixed(2));
    }
    
    return {
        macAddress: ((response.device || {}).mac_address) || "N/A",
        deviceInfo: { macAddress: device.mac_address || "N/A", MODEL: sys.MODEL || "N/A", VENDOR: sys.VENDOR || "N/A", SW_REV: sys.SW_REV || "N/A", HW_REV: sys.HW_REV || "N/A", BOOTR: sys.BOOTR || "N/A" },
        bandEdge: bandEdge,
        dsLower: dsLower,
        dsUpper: dsUpper,
        diplexerCap: diplexer.diplexer_capability,
        dsLowerCap: diplexer.ds_lower_capability,
        dsUpperCap: diplexer.ds_upper_capability,
        freqLabels: freqLabels,
        upstreamData: upstreamData,
        downstreamData: downstreamData
    };
}

pm.visualizer.set(template, createPayload());
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
        "mac_address": "aa:bb:cc:dd:ee:ff",
        "system_description": {
            "HW_REV": "1.0",
            "VENDOR": "LANCity",
            "BOOTR": "NONE",
            "SW_REV": "1.0.0",
            "MODEL": "LCPET-3"
        }
    },
    "results": {
        "diplexer": {
            "diplexer_capability": 20,
            "cfg_band_edge": 204000000,
            "ds_lower_capability": 3,
            "cfg_ds_lower_band_edge": 258000000,
            "ds_upper_capability": 2,
            "cfg_ds_upper_band_edge": 1794000000
        }
    }
}
````
</details>
