# Postman Visualizer Section Template

Use this as the starting pattern for new visuals. Build the page in sections and keep `Device Info` standardized.

## Section Order (Standard)

1. Page header (title + optional `Capture Time` at top right)
2. `Device Info` block (separate from channel/capture block)
3. Channel/capture metadata block (frequencies shown in `MHz`, optional `Hz` in parentheses)
4. Summary/stat cards
5. Charts
6. Detail tables / debug tables

## Device Info Display Standard

Preferred display labels (exact casing):

- `MacAddress`
- `Model`
- `Vendor`
- `SW Version`
- `HW Version`
- `Boot ROM`

Rules:

- Render `Device Info` before channel graphs/content.
- Do not repeat `MacAddress` again in the channel header if already shown in `Device Info`.
- Use `N/A` for missing fields.
- Do not use vendor-specific fallback values in UI defaults.
- If available, place `Capture Time` next to the page title/header (layout-only, not inside chart sections).
- Format `Capture Time` as a human-readable date/time string (not raw epoch seconds).

## HTML / Visualizer Scaffold (Copy + adapt)

```javascript
const template = `
<style>
  body { font-family: Arial, sans-serif; padding: 20px; background: #1e1e1e; color: #e0e0e0; }
  .container { max-width: 1400px; margin: 0 auto; }
  .header { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 8px; margin-bottom: 24px; }
  h1 { color: #e0e0e0; text-align: center; margin: 0; grid-column: 2; }
  .capture-time { grid-column: 3; justify-self: end; font-size: 12px; color: #cfd6e5; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 999px; padding: 6px 10px; white-space: nowrap; }

  .section { background: #2d2d2d; padding: 20px; margin: 18px 0; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.25); }
  .device-info-block { background: #343447; border: 1px solid rgba(255,255,255,0.08); }
  .channel-block { background: linear-gradient(135deg, #5a6fd8 0%, #6f4aa6 100%); color: white; }

  .subtle { opacity: 0.9; font-size: 14px; }
  .mono { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; }

  .table-wrap { overflow-x: auto; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; }
  .table-title { font-size: 11px; text-transform: uppercase; letter-spacing: 0.6px; padding: 10px 12px; background: rgba(0,0,0,0.18); border-bottom: 1px solid rgba(255,255,255,0.08); }
  .table { width: 100%; min-width: 680px; border-collapse: collapse; }
  .table th { text-align: left; white-space: nowrap; padding: 9px 12px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.45px; color: #dbe3ff; background: rgba(255,255,255,0.03); }
  .table td { padding: 10px 12px; font-size: 12px; color: #ffffff; white-space: nowrap; border-top: 1px solid rgba(255,255,255,0.08); }

  .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
  .card { background: #3a3a3a; border-radius: 8px; padding: 12px; }
  .card-label { font-size: 11px; text-transform: uppercase; color: #b0b0b0; }
  .card-value { font-size: 18px; font-weight: 700; color: #8b9dff; margin-top: 4px; }

  .chart { background: #2d2d2d; border-radius: 8px; padding: 16px; margin-top: 16px; }
  .chart-title { text-align: center; margin: 0 0 10px 0; font-weight: 700; }
  canvas { max-height: 360px; }
</style>

<div class="container">
  <div class="header">
    <h1>{{pageTitle}}</h1>
    {{#if captureTime}}
      <div class="capture-time">Capture Time: {{captureTime}}</div>
    {{/if}}
  </div>

  {{#each channels}}
    <div class="section device-info-block">
      <div class="table-wrap">
        <div class="table-title">Device Info</div>
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
              <td class="mono">{{macAddress}}</td>
              <td>{{deviceInfo.MODEL}}</td>
              <td>{{deviceInfo.VENDOR}}</td>
              <td class="mono">{{deviceInfo.SW_REV}}</td>
              <td class="mono">{{deviceInfo.HW_REV}}</td>
              <td class="mono">{{deviceInfo.BOOTR}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="section channel-block">
      <div style="font-size: 26px; font-weight: 700;">Channel {{channelId}}</div>
      <div class="subtle">
        Frequency: {{frequencyMHz}} MHz{{#if frequencyHz}} <span class="mono">({{frequencyHz}} Hz)</span>{{/if}}
      </div>
    </div>

    <div class="section">
      <div class="cards">
        {{#each statsCards}}
          <div class="card">
            <div class="card-label">{{label}}</div>
            <div class="card-value">{{value}}</div>
          </div>
        {{/each}}
      </div>
    </div>

    <div class="section chart">
      <div class="chart-title">Primary Chart</div>
      <canvas id="chart-{{channelId}}"></canvas>
    </div>
  {{/each}}
</div>
`;

function constructVisualizerPayload() {
  const resp = pm.response.json();

  function isPresent(v) {
    return v !== undefined && v !== null && String(v).trim() !== '';
  }

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

  function toDeviceInfoRecord(sys) {
    const out = { MODEL: 'N/A', VENDOR: 'N/A', SW_REV: 'N/A', HW_REV: 'N/A', BOOTR: 'N/A' };
    if (!sys || typeof sys !== 'object') return out;
    Object.keys(out).forEach(k => {
      if (isPresent(sys[k])) out[k] = String(sys[k]).trim();
    });
    return out;
  }

  function toMHzFixedOrNA(v, digits) {
    if (typeof v !== 'number' || !isFinite(v)) return 'N/A';
    return (v / 1e6).toFixed(digits);
  }

  function formatCaptureTime(raw) {
    if (raw === undefined || raw === null || raw === '') return 'N/A';
    if (typeof raw === 'number' && isFinite(raw)) {
      var ms = raw > 1e12 ? raw : raw * 1000;
      var d = new Date(ms);
      if (isNaN(d.getTime())) return 'N/A';
      return d.toISOString().slice(0, 19).replace('T', ' ') + ' UTC';
    }
    var n = Number(raw);
    if (!isNaN(n) && isFinite(n)) return formatCaptureTime(n);
    var d2 = new Date(raw);
    if (isNaN(d2.getTime())) return String(raw);
    return d2.toISOString().slice(0, 19).replace('T', ' ') + ' UTC';
  }

  return {
    pageTitle: 'Replace Me',
    captureTime: null, // e.g. formatCaptureTime(((resp.data||{}).analysis||[])[0]?.pnm_header?.capture_time)
    channels: []
  };
}

pm.visualizer.set(template, constructVisualizerPayload());
```

## Workflow (Recommended)

1. Copy scaffold into new `visual/.../*.html`
2. Build payload first (`constructVisualizerPayload`)
3. Render `Device Info` + channel blocks
4. Add summary cards
5. Add charts and chart JS
6. Add detail tables
7. Regenerate docs: `python3 tools/docs/build_visual_docs.py`
8. Verify: `python3 tools/docs/build_visual_docs.py --check`
