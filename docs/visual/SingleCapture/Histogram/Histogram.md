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
// Visualization Script
const template = `
<style>
    body {
        font-family: Arial, sans-serif;
        padding: 20px;
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    .container {
        max-width: 1200px;
        margin: 0 auto;
    }
    .header {
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
        color: #e0e0e0;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .header h1 {
        margin: 0 0 10px 0;
        font-size: 24px;
        color: #e0e0e0;
    }
    .header p {
        margin: 5px 0;
        opacity: 0.9;
        color: #b0b0b0;
    }
    .device-info {
        background: #2d2d2d;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .device-info h2 {
        margin-top: 0;
        color: #e0e0e0;
        border-bottom: 2px solid #4a5568;
        padding-bottom: 10px;
    }
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-top: 15px;
    }
    .info-item {
        padding: 10px;
        background: #3d3d3d;
        border-radius: 4px;
    }
    .info-label {
        font-weight: bold;
        color: #7c9cbf;
        font-size: 12px;
        text-transform: uppercase;
    }
    .info-value {
        color: #e0e0e0;
        font-size: 16px;
        margin-top: 5px;
    }
    .chart-container {
        background: #2d2d2d;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .chart-container h2 {
        margin-top: 0;
        color: #e0e0e0;
        border-bottom: 2px solid #4a5568;
        padding-bottom: 10px;
    }
    .stats-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }
    .stats-table th {
        background: #3d3d3d;
        color: #e0e0e0;
        padding: 10px;
        text-align: left;
        border-bottom: 2px solid #4a5568;
    }
    .stats-table td {
        padding: 8px 10px;
        border-bottom: 1px solid #3d3d3d;
        color: #b0b0b0;
    }
    .stats-table tr:hover {
        background: #3d3d3d;
    }
    canvas {
        max-width: 100%;
        height: auto !important;
    }
</style>

<div class="container">
    <div class="header">
        <h1>📊 Histogram Capture Analysis</h1>
        <p><strong>MAC Address:</strong> {{mac_address}}</p>
        <p><strong>Status:</strong> {{status_message}}</p>
    </div>

    {{#if device_details}}
    <div class="device-info">
        <h2>🖥️ Device Information</h2>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Vendor</div>
                <div class="info-value">{{device_details.VENDOR}}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Model</div>
                <div class="info-value">{{device_details.MODEL}}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Hardware Rev</div>
                <div class="info-value">{{device_details.HW_REV}}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Software Rev</div>
                <div class="info-value">{{device_details.SW_REV}}</div>
            </div>
        </div>
    </div>
    {{/if}}

    {{#if measurement_stats}}
    <div class="device-info">
        <h2>📈 Measurement Statistics</h2>
        <table class="stats-table">
            <thead>
                <tr>
                    <th>Parameter</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                {{#each measurement_stats}}
                <tr>
                    <td>{{this.label}}</td>
                    <td>{{this.value}}</td>
                </tr>
                {{/each}}
            </tbody>
        </table>
    </div>
    {{/if}}

    <div class="chart-container">
        <h2>📊 Histogram Distribution</h2>
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
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
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
                            color: '#3d3d3d'
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
                            color: '#3d3d3d'
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
    
    // Extract basic info
    const macAddress = response.mac_address || 'N/A';
    const status = response.status;
    const statusMessage = status === 0 ? '✅ Success' : '❌ Failed';
    
    // Extract device details
    let deviceDetails = null;
    if (response.data && response.data.analysis && response.data.analysis.length > 0) {
        const analysis = response.data.analysis[0];
        if (analysis.device_details && analysis.device_details.system_description) {
            deviceDetails = analysis.device_details.system_description;
        }
    }
    
    // Extract measurement stats
    let measurementStats = [];
    if (response.data && response.data.measurement_stats && response.data.measurement_stats.length > 0) {
        const stats = response.data.measurement_stats[0].entry;
        measurementStats = [
            { label: 'Histogram Enabled', value: stats.docsPnmCmDsHistEnable ? 'Yes' : 'No' },
            { label: 'Timeout (seconds)', value: stats.docsPnmCmDsHistTimeOut },
            { label: 'Measurement Status', value: stats.docsPnmCmDsHistMeasStatus },
            { label: 'File Name', value: stats.docsPnmCmDsHistFileName }
        ];
    }
    
    // Extract histogram data for chart - MODIFIED TO REMOVE "Bin_" PREFIX
    let chartLabels = [];
    let chartData = [];
    
    if (response.data && response.data.analysis && response.data.analysis.length > 0) {
        const analysis = response.data.analysis[0];
        if (analysis.hit_counts && Array.isArray(analysis.hit_counts)) {
            chartData = analysis.hit_counts;
            // Generate labels as just the numeric index (0, 1, 2, 3, ...)
            chartLabels = analysis.hit_counts.map((_, index) => String(index));
        }
    }
    
    return {
        mac_address: macAddress,
        status_message: statusMessage,
        device_details: deviceDetails,
        measurement_stats: measurementStats,
        chart_labels: chartLabels,
        chart_data: chartData
    };
}

pm.visualizer.set(template, constructVisualizerPayload());
````
</details>

<details>
<summary>Sample JSON payload</summary>

````json
{
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
