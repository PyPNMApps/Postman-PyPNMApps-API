# PyPNM / SingleCapture / SpectrumAnalysis / GetCapture-FBC

## Source Files

- HTML/script: `visual/PyPNM/SingleCapture/SpectrumAnalysis/GetCapture-FBC.html`
- JSON sample: missing

## Preview

Preview unavailable because no matching sample JSON fixture exists for this visual.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Postman Visualizer: Spectrum Capture Viewer
// Direction-aware version with dynamic titles and labels

(function () {
  var resp = pm.response.json();

  // Helper function to safely get nested properties
  function get(obj, path, fallback) {
    try {
      var keys = path.split('.');
      var result = obj;
      for (var i = 0; i < keys.length; i++) {
        if (result && keys[i] in result) {
          result = result[keys[i]];
        } else {
          return fallback;
        }
      }
      return result !== undefined ? result : fallback;
    } catch (e) {
      return fallback;
    }
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

  // Extract direction from response or fall back to request body
  function getDirection() {
    // Try response: data.analysis[0].capture_parameters.direction
    var direction = get(resp, 'data.analysis.0.capture_parameters.direction', null);
    
    // Try response: data.primative[0].spectrum_analysis_snmp_capture_parameters.direction
    if (!direction) {
      direction = get(resp, 'data.primative.0.spectrum_analysis_snmp_capture_parameters.direction', null);
    }
    
    // Try response: data.primative[0].spectrum_config.direction
    if (!direction) {
      direction = get(resp, 'data.primative.0.spectrum_config.direction', null);
    }
    
    // Try response: data.primative[0].direction
    if (!direction) {
      direction = get(resp, 'data.primative.0.direction', null);
    }
    
    // Fall back to request body
    if (!direction) {
      try {
        var requestBody = JSON.parse(pm.request.body.raw);
        direction = get(requestBody, 'capture_parameters.direction', null);
      } catch (e) {
        // Ignore parse errors
      }
    }
    
    // Default fallback
    return direction || 'upstream';
  }

  // Capitalize first letter of direction for display
  function capitalizeDirection(dir) {
    if (!dir || typeof dir !== 'string') return 'Spectrum';
    return dir.charAt(0).toUpperCase() + dir.slice(1).toLowerCase();
  }

  // Get direction values
  var direction = getDirection();
  var directionDisplay = capitalizeDirection(direction);

  // Check if value is a finite number
  function isNum(v) {
    return typeof v === "number" && Number.isFinite(v);
  }

  // Convert x/y arrays to pairs with downsampling
  function toPairs(xs, ys, maxPoints) {
    var n = Math.min(xs.length, ys.length);
    if (n === 0) return [];
    var stride = Math.max(1, Math.floor(n / maxPoints));
    var out = [];
    for (var i = 0; i < n; i += stride) {
      out.push({ x: xs[i], y: ys[i] });
    }
    // Always include last point
    if (out.length && out[out.length - 1].x !== xs[n - 1]) {
      out.push({ x: xs[n - 1], y: ys[n - 1] });
    }
    return out;
  }

  // Extract signal analysis data
  var signalAnalysis = get(resp, 'data.analysis.0.signal_analysis', null);
  var captureParams = get(resp, 'data.analysis.0.capture_parameters', {});
  var deviceDetails = get(resp, 'data.analysis.0.device_details', {});

  // Get frequencies and magnitudes
  var frequencies = [];
  var magnitudes = [];
  var windowAvgMagnitudes = [];

  if (signalAnalysis) {
    frequencies = Array.isArray(signalAnalysis.frequencies) ? signalAnalysis.frequencies : [];
    magnitudes = Array.isArray(signalAnalysis.magnitudes) ? signalAnalysis.magnitudes : [];
    windowAvgMagnitudes = get(signalAnalysis, 'window_average.magnitudes', []);
  }

  // Convert frequencies to MHz for display
  var freqsMHz = frequencies.map(function(f) { return f / 1000000; });

  // Prepare chart data with downsampling for performance
  var maxPoints = 500;
  var spectrumData = toPairs(freqsMHz, magnitudes, maxPoints);
  var windowAvgData = toPairs(freqsMHz, windowAvgMagnitudes, maxPoints);

  // Calculate statistics
  var minMag = magnitudes.length > 0 ? Math.min.apply(null, magnitudes) : 0;
  var maxMag = magnitudes.length > 0 ? Math.max.apply(null, magnitudes) : 0;
  var avgMag = magnitudes.length > 0 ? magnitudes.reduce(function(a, b) { return a + b; }, 0) / magnitudes.length : 0;

  // Get device info
  var deviceInfo = sanitizeSystemDescription(get(deviceDetails, 'system_description', {}));
  var vendor = deviceInfo.VENDOR || 'Unknown';
  var model = deviceInfo.MODEL || 'Unknown';
  var swRev = deviceInfo.SW_REV || 'Unknown';

  // Get channel power
  var channelPower = get(signalAnalysis, 'channel_power_dbmv', null);

  // Build the template
  var template = '\
<!DOCTYPE html>\
<html>\
<head>\
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js"></script>\
  <style>\
    * { box-sizing: border-box; margin: 0; padding: 0; }\
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }\
    .container { max-width: 1200px; margin: 0 auto; }\
    .header { text-align: center; margin-bottom: 20px; }\
    .header h1 { font-size: 24px; color: #00d4ff; margin-bottom: 5px; }\
    .header h2 { font-size: 16px; color: #888; font-weight: normal; }\
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px; }\
    .stat-card { background: #16213e; border-radius: 8px; padding: 15px; text-align: center; }\
    .stat-card .label { font-size: 11px; color: #888; text-transform: uppercase; margin-bottom: 5px; }\
    .stat-card .value { font-size: 20px; font-weight: bold; color: #00d4ff; }\
    .stat-card .unit { font-size: 12px; color: #666; }\
    .chart-container { background: #16213e; border-radius: 8px; padding: 20px; margin-bottom: 20px; }\
    .chart-wrapper { position: relative; height: 400px; }\
    .device-info { background: #16213e; border-radius: 8px; padding: 15px; }\
    .device-info h3 { font-size: 14px; color: #00d4ff; margin-bottom: 10px; }\
    .device-info .info-row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #2a2a4a; }\
    .device-info .info-row:last-child { border-bottom: none; }\
    .device-info .info-label { color: #888; }\
    .device-info .info-value { color: #eee; }\
    .direction-badge { display: inline-block; background: #00d4ff; color: #1a1a2e; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; margin-left: 10px; }\
  </style>\
</head>\
<body>\
  <div class="container">\
    <div class="header">\
      <h1>{{directionDisplay}} Full Band Capture - Spectrum Analysis <span class="direction-badge">{{directionDisplay}}</span></h1>\
      <h2>{{directionDisplay}} Spectrum Visualization | {{vendor}} {{model}}</h2>\
    </div>\
    <div class="stats-grid">\
      <div class="stat-card">\
        <div class="label">Direction</div>\
        <div class="value">{{directionDisplay}}</div>\
      </div>\
      <div class="stat-card">\
        <div class="label">Min Power</div>\
        <div class="value">{{minMag}}<span class="unit"> dBmV</span></div>\
      </div>\
      <div class="stat-card">\
        <div class="label">Max Power</div>\
        <div class="value">{{maxMag}}<span class="unit"> dBmV</span></div>\
      </div>\
      <div class="stat-card">\
        <div class="label">Avg Power</div>\
        <div class="value">{{avgMag}}<span class="unit"> dBmV</span></div>\
      </div>\
      <div class="stat-card">\
        <div class="label">Channel Power</div>\
        <div class="value">{{channelPower}}<span class="unit"> dBmV</span></div>\
      </div>\
      <div class="stat-card">\
        <div class="label">Data Points</div>\
        <div class="value">{{dataPoints}}</div>\
      </div>\
    </div>\
    <div class="chart-container">\
      <div class="chart-wrapper">\
        <canvas id="spectrumChart"></canvas>\
      </div>\
    </div>\
    <div class="device-info">\
      <h3>Device Information</h3>\
      <div class="info-row"><span class="info-label">Vendor</span><span class="info-value">{{vendor}}</span></div>\
      <div class="info-row"><span class="info-label">Model</span><span class="info-value">{{model}}</span></div>\
      <div class="info-row"><span class="info-label">Software Version</span><span class="info-value">{{swRev}}</span></div>\
      <div class="info-row"><span class="info-label">MAC Address</span><span class="info-value">{{macAddress}}</span></div>\
      <div class="info-row"><span class="info-label">Capture Direction</span><span class="info-value">{{directionDisplay}}</span></div>\
      <div class="info-row"><span class="info-label">Noise BW</span><span class="info-value">{{noiseBw}} Hz</span></div>\
      <div class="info-row"><span class="info-label">Num Averages</span><span class="info-value">{{numAverages}}</span></div>\
    </div>\
  </div>\
  <script>\
    pm.getData(function(err, value) {\
      if (err) { console.error(err); return; }\
      var ctx = document.getElementById("spectrumChart").getContext("2d");\
      var dirDisplay = value.directionDisplay || "Spectrum";\
      new Chart(ctx, {\
        type: "line",\
        data: {\
          datasets: [{\
            label: dirDisplay + " Magnitude (dBmV)",\
            data: value.spectrumData,\
            borderColor: "#00d4ff",\
            backgroundColor: "rgba(0, 212, 255, 0.1)",\
            borderWidth: 1.5,\
            pointRadius: 0,\
            fill: true\
          }, {\
            label: dirDisplay + " Window Average (dBmV)",\
            data: value.windowAvgData,\
            borderColor: "#ff6b6b",\
            backgroundColor: "transparent",\
            borderWidth: 2,\
            pointRadius: 0,\
            fill: false\
          }]\
        },\
        options: {\
          responsive: true,\
          maintainAspectRatio: false,\
          title: {\
            display: true,\
            text: dirDisplay + " Spectrum - Full Band Capture",\
            fontColor: "#00d4ff",\
            fontSize: 16\
          },\
          legend: {\
            labels: { fontColor: "#ccc" }\
          },\
          scales: {\
            xAxes: [{\
              type: "linear",\
              position: "bottom",\
              scaleLabel: {\
                display: true,\
                labelString: dirDisplay + " Frequency (MHz)",\
                fontColor: "#888"\
              },\
              ticks: { fontColor: "#888" },\
              gridLines: { color: "rgba(255,255,255,0.1)" }\
            }],\
            yAxes: [{\
              scaleLabel: {\
                display: true,\
                labelString: dirDisplay + " Power Level (dBmV)",\
                fontColor: "#888"\
              },\
              ticks: { fontColor: "#888" },\
              gridLines: { color: "rgba(255,255,255,0.1)" }\
            }]\
          },\
          tooltips: {\
            mode: "index",\
            intersect: false,\
            callbacks: {\
              title: function(items) { return dirDisplay + " Freq: " + items[0].xLabel.toFixed(2) + " MHz"; },\
              label: function(item, data) { return data.datasets[item.datasetIndex].label + ": " + item.yLabel.toFixed(2) + " dBmV"; }\
            }\
          }\
        }\
      });\
    });\
  </script>\
</body>\
</html>';

  // Prepare data for template
  var templateData = {
    directionDisplay: directionDisplay,
    direction: direction,
    spectrumData: spectrumData,
    windowAvgData: windowAvgData,
    minMag: isNum(minMag) ? minMag.toFixed(2) : 'N/A',
    maxMag: isNum(maxMag) ? maxMag.toFixed(2) : 'N/A',
    avgMag: isNum(avgMag) ? avgMag.toFixed(2) : 'N/A',
    channelPower: isNum(channelPower) ? channelPower.toFixed(2) : 'N/A',
    dataPoints: frequencies.length,
    vendor: vendor,
    model: model,
    swRev: swRev,
    macAddress: sanitizeMac(resp.mac_address, 'N/A'),
    noiseBw: captureParams.noise_bw || 'N/A',
    numAverages: captureParams.num_averages || 'N/A'
  };

  pm.visualizer.set(template, templateData);
})();
````
</details>
