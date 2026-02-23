# PyPNM / SingleCapture / Histogram / Histogram

## Source Files

- HTML/script: `visual/PyPNM/SingleCapture/Histogram/Histogram.html`
- JSON sample: `visual/PyPNM/SingleCapture/Histogram/Histogram.json`

## Preview

<iframe src="../../../../visual-previews/SingleCapture/Histogram/Histogram.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Remarks (CODING_AGENTS visual standard)
// - Device Info uses a separate top block with standardized labels
// - Histogram chart remains the primary visualization
// - Missing sysDescr fields render as N/A
const template = `
<style>
    body {
        font-family: Arial, sans-serif;
        padding: 16px;
        background-color: #0b0b0b;
        color: #e8e8e8;
    }
    .container {
        max-width: 1280px;
        margin: 0 auto;
    }
    .header {
        margin-bottom: 12px;
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        gap: 8px;
    }
    .header h1 {
        margin: 0;
        font-size: 22px;
        color: #f2f2f2;
        grid-column: 2;
        text-align: center;
    }
    .capture-time {
        grid-column: 3;
        justify-self: end;
        font-size: 12px;
        color: #d7deec;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 999px;
        padding: 6px 10px;
        white-space: nowrap;
    }
    .panel {
        background: #151515;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .panel-title {
        margin: 0 0 10px 0;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        color: #dbe3ff;
    }
    .table-wrap {
        overflow-x: auto;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
    }
    .table {
        width: 100%;
        min-width: 720px;
        border-collapse: collapse;
    }
    .table th {
        text-align: left;
        white-space: nowrap;
        padding: 9px 12px;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.45px;
        color: #dbe3ff;
        background: rgba(255,255,255,0.03);
    }
    .table td {
        padding: 10px 12px;
        font-size: 12px;
        color: #ffffff;
        white-space: nowrap;
        border-top: 1px solid rgba(255,255,255,0.08);
    }
    .mono {
        font-family: Consolas, "Liberation Mono", Menlo, monospace;
    }
    .meta-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 8px;
        color: #cfd6e5;
        font-size: 12px;
    }
    .meta-pill {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 999px;
        padding: 6px 10px;
    }
    canvas {
        max-width: 100%;
        height: auto !important;
    }
</style>

<div class="container">
    <div class="header">
        <h1>Histogram Capture Analysis</h1>
        <div class="capture-time">Capture Time: {{capture_time}}</div>
    </div>

    <div class="panel">
        <div class="panel-title">Device Info</div>
        <div class="table-wrap">
            <table class="table">
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
                    <tr>
                        <td class="mono">{{device_info.macAddress}}</td>
                        <td>{{device_info.MODEL}}</td>
                        <td>{{device_info.VENDOR}}</td>
                        <td class="mono">{{device_info.SW_REV}}</td>
                        <td class="mono">{{device_info.HW_REV}}</td>
                        <td class="mono">{{device_info.BOOTR}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="meta-row">
            <div class="meta-pill">Bins: {{bin_count}}</div>
        </div>
    </div>

    <div class="panel">
        <div class="panel-title">Histogram Distribution</div>
        <canvas id="histogramChart"></canvas>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js"></script>
<script>
    pm.getData(function (err, data) {
        if (err) {
            console.error('Error getting data:', err);
            return;
        }

        const ctx = document.getElementById('histogramChart').getContext('2d');
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.chart_labels,
                datasets: [{
                    label: 'Hit Count',
                    data: data.chart_data,
                    backgroundColor: 'rgba(0, 194, 255, 0.45)',
                    borderColor: 'rgba(0, 194, 255, 0.95)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            fontColor: '#e0e0e0'
                        },
                        gridLines: {
                            color: 'rgba(255,255,255,0.08)'
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Hit Count',
                            fontColor: '#e0e0e0'
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            fontColor: '#e0e0e0'
                        },
                        gridLines: {
                            color: 'rgba(255,255,255,0.06)'
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Bin Index',
                            fontColor: '#e0e0e0'
                        }
                    }]
                },
                legend: {
                    labels: {
                        fontColor: '#e0e0e0'
                    }
                }
            }
        });
    });
</script>
`;

function constructVisualizerPayload() {
    const response = pm.response.json();
    const data = response.data || {};
    const firstAnalysis = (data.analysis && data.analysis[0]) || {};
    const pnmHeader = firstAnalysis.pnm_header || {};

    function formatCaptureTime(raw) {
        if (raw === undefined || raw === null || raw === '') return 'N/A';
        if (typeof raw === 'number' && isFinite(raw)) {
            const ms = raw > 1e12 ? raw : raw * 1000;
            const d = new Date(ms);
            if (isNaN(d.getTime())) return 'N/A';
            return d.toISOString().slice(0, 19).replace('T', ' ') + ' UTC';
        }
        const n = Number(raw);
        if (!isNaN(n) && isFinite(n)) {
            return formatCaptureTime(n);
        }
        const d = new Date(raw);
        if (isNaN(d.getTime())) return String(raw);
        return d.toISOString().slice(0, 19).replace('T', ' ') + ' UTC';
    }
    
    // Extract basic info
    const macAddress = firstAnalysis.mac_address || response.mac_address || 'N/A';
    const status = response.status;
    const statusMessage = status === 0 ? 'Success' : 'Failed';
    const captureTime = formatCaptureTime(pnmHeader.capture_time);
    
    // Extract device details
    const sys = ((firstAnalysis.device_details || {}).system_description) || {};
    const deviceInfo = {
        macAddress: macAddress,
        MODEL: (sys.MODEL && String(sys.MODEL).trim()) || 'N/A',
        VENDOR: (sys.VENDOR && String(sys.VENDOR).trim()) || 'N/A',
        SW_REV: (sys.SW_REV && String(sys.SW_REV).trim()) || 'N/A',
        HW_REV: (sys.HW_REV && String(sys.HW_REV).trim()) || 'N/A',
        BOOTR: (sys.BOOTR && String(sys.BOOTR).trim()) || 'N/A'
    };
    
    // Extract histogram data for chart - MODIFIED TO REMOVE "Bin_" PREFIX
    let chartLabels = [];
    let chartData = [];
    
    if (data.analysis && data.analysis.length > 0) {
        const analysis = data.analysis[0];
        if (analysis.hit_counts && Array.isArray(analysis.hit_counts)) {
            chartData = analysis.hit_counts;
            // Generate labels as just the numeric index (0, 1, 2, 3, ...)
            chartLabels = analysis.hit_counts.map((_, index) => String(index));
        }
    }
    
    return {
        mac_address: macAddress,
        status_message: statusMessage,
        capture_time: captureTime,
        device_info: deviceInfo,
        chart_labels: chartLabels,
        chart_data: chartData,
        bin_count: chartData.length
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
    "mac_address": "aabbccddeeff",
    "status": 0,
    "message": null,
    "data": {
        "analysis": [
            {
                "device_details": {
                    "system_description": {
                        "HW_REV": "1.0",
                        "VENDOR": "LANCity",
                        "BOOTR": "NONE",
                        "SW_REV": "1.0.0",
                        "MODEL": "LCPET-3"
                    }
                },
                "pnm_header": {
                    "file_type": "PNN",
                    "file_type_version": 5,
                    "major_version": 1,
                    "minor_version": 0,
                    "capture_time": 1740236465
                },
                "mac_address": "aa:bb:cc:dd:ee:ff",
                "symmetry": 2,
                "dwell_counts": [
                    1406249999
                ],
                "hit_counts": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                    0,
                    7,
                    20,
                    111,
                    215,
                    552,
                    1311,
                    3073,
                    6881,
                    15401,
                    31408,
                    63828,
                    123760,
                    234654,
                    432294,
                    764677,
                    1297511,
                    2191743,
                    3491751,
                    5508147,
                    8208783,
                    12140702,
                    17338270,
                    23528753,
                    31530249,
                    40950495,
                    51020014,
                    61428442,
                    72321749,
                    82467167,
                    91065068,
                    96064371,
                    100079085,
                    99864515,
                    97105477,
                    90225910,
                    82343616,
                    73238688,
                    61788155,
                    50576999,
                    41370050,
                    31516931,
                    23989402,
                    17051591,
                    12222733,
                    8385387,
                    5532446,
                    3506651,
                    2202638,
                    1329581,
                    767116,
                    434536,
                    239625,
                    126263,
                    62850,
                    31553,
                    14659,
                    6724,
                    3068,
                    1329,
                    604,
                    262,
                    85,
                    33,
                    20,
                    6,
                    2,
                    1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ]
            }
        ],
        "measurement_stats": [
            {
                "index": 2,
                "entry": {
                    "docsPnmCmDsHistEnable": true,
                    "docsPnmCmDsHistTimeOut": 10,
                    "docsPnmCmDsHistMeasStatus": "sample_ready",
                    "docsPnmCmDsHistFileName": "ds_histogram_aabbccddeeff_0_1771803166.bin"
                }
            }
        ]
    }
}
````
</details>
