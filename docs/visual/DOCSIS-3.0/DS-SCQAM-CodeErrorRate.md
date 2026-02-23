# PyPNM / DOCSIS-3.0 / DS-SCQAM-CodeErrorRate

## Source Files

- HTML/script: `visual/PyPNM/DOCSIS-3.0/DS-SCQAM-CodeErrorRate.html`
- JSON sample: `visual/PyPNM/DOCSIS-3.0/DS-SCQAM-CodeErrorRate.json`

## Preview

<iframe src="../../../visual-previews/DOCSIS-3.0/DS-SCQAM-CodeErrorRate.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Visualization Script
// Visualization Script
var template = `
<canvas id="myChart" height="100"></canvas>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script> 
<script>
    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Total Codewords',
                    data: [],
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Total Errors',
                    data: [],
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            legend: { display: true },
            title: {
                display: true,
                text: 'Codeword Error Rate by Channel ID'
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Channel ID'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Count'
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    pm.getData(function (err, value) {
        myChart.data.labels = value.channelIds;
        myChart.data.datasets[0].data = value.totalCodewords;
        myChart.data.datasets[1].data = value.totalErrors;
        myChart.update();
    });

</script>`;

function createPayload() {
    var responseData = pm.response.json();
    var results = responseData.results || [];
    
    var channelIds = [];
    var totalCodewords = [];
    var totalErrors = [];
    
    for (var i = 0; i < results.length; i++) {
        channelIds.push(results[i].channel_id.toString());
        totalCodewords.push(results[i].codeword_totals.total_codewords);
        totalErrors.push(results[i].codeword_totals.total_errors);
    }
    
    return {
        channelIds: channelIds,
        totalCodewords: totalCodewords,
        totalErrors: totalErrors
    };
}

pm.visualizer.set(template, createPayload());
````
</details>

<details>
<summary>Sample JSON payload</summary>

````json
{
    "mac_address": "aa:bb:cc:dd:ee:ff",
    "status": 0,
    "message": "Successfully retrieved codeword error rate",
    "results": [
        {
            "index": 3,
            "channel_id": 3,
            "codeword_totals": {
                "total_codewords": 801466,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 160293.2,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 50,
            "channel_id": 32,
            "codeword_totals": {
                "total_codewords": 801254,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 160250.8,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 51,
            "channel_id": 31,
            "codeword_totals": {
                "total_codewords": 803484,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 160696.8,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 52,
            "channel_id": 30,
            "codeword_totals": {
                "total_codewords": 805598,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 161119.6,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 53,
            "channel_id": 29,
            "codeword_totals": {
                "total_codewords": 799451,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 159890.2,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 54,
            "channel_id": 28,
            "codeword_totals": {
                "total_codewords": 799208,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 159841.6,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 55,
            "channel_id": 27,
            "codeword_totals": {
                "total_codewords": 798799,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 159759.8,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 56,
            "channel_id": 26,
            "codeword_totals": {
                "total_codewords": 798983,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 159796.6,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 57,
            "channel_id": 25,
            "codeword_totals": {
                "total_codewords": 798555,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 159711.0,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 58,
            "channel_id": 24,
            "codeword_totals": {
                "total_codewords": 765770,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 153154.0,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 59,
            "channel_id": 23,
            "codeword_totals": {
                "total_codewords": 674493,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 134898.6,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 60,
            "channel_id": 22,
            "codeword_totals": {
                "total_codewords": 664659,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 132931.8,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 61,
            "channel_id": 21,
            "codeword_totals": {
                "total_codewords": 658032,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 131606.4,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 62,
            "channel_id": 20,
            "codeword_totals": {
                "total_codewords": 663866,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 132773.2,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 63,
            "channel_id": 19,
            "codeword_totals": {
                "total_codewords": 666260,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 133252.0,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 64,
            "channel_id": 18,
            "codeword_totals": {
                "total_codewords": 667387,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 133477.4,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 65,
            "channel_id": 17,
            "codeword_totals": {
                "total_codewords": 659818,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 131963.6,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 66,
            "channel_id": 16,
            "codeword_totals": {
                "total_codewords": 663416,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 132683.2,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 67,
            "channel_id": 15,
            "codeword_totals": {
                "total_codewords": 775145,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 155029.0,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 68,
            "channel_id": 14,
            "codeword_totals": {
                "total_codewords": 793486,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 158697.2,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 69,
            "channel_id": 13,
            "codeword_totals": {
                "total_codewords": 794895,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 158979.0,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 70,
            "channel_id": 12,
            "codeword_totals": {
                "total_codewords": 792756,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 158551.2,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 71,
            "channel_id": 11,
            "codeword_totals": {
                "total_codewords": 796557,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 159311.4,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 72,
            "channel_id": 10,
            "codeword_totals": {
                "total_codewords": 793542,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 158708.4,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 73,
            "channel_id": 9,
            "codeword_totals": {
                "total_codewords": 799482,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 159896.4,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 74,
            "channel_id": 8,
            "codeword_totals": {
                "total_codewords": 799303,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 159860.6,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 75,
            "channel_id": 7,
            "codeword_totals": {
                "total_codewords": 801459,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 160291.8,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 76,
            "channel_id": 6,
            "codeword_totals": {
                "total_codewords": 801542,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 160308.4,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 77,
            "channel_id": 5,
            "codeword_totals": {
                "total_codewords": 796760,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 159352.0,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 78,
            "channel_id": 4,
            "codeword_totals": {
                "total_codewords": 795338,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 159067.6,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 79,
            "channel_id": 2,
            "codeword_totals": {
                "total_codewords": 795617,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 159123.4,
                "errors_per_second": 0.0
            }
        },
        {
            "index": 112,
            "channel_id": 1,
            "codeword_totals": {
                "total_codewords": 799526,
                "total_errors": 0,
                "time_elapsed": 5.0,
                "error_rate": 0.0,
                "codewords_per_second": 159905.2,
                "errors_per_second": 0.0
            }
        }
    ]
}
````
</details>
