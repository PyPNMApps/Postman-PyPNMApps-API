# PyPNM-CMTS / ServingGroup / Opertions / Get / cableModems

## Source Files

- HTML/script: `visual/PyPNM-CMTS/ServingGroup/Opertions/Get/cableModems.html`
- JSON sample: `visual/PyPNM-CMTS/ServingGroup/Opertions/Get/cableModems.json`

## Preview

<iframe src="../../../../../../visual-previews/PyPNM-CMTS/ServingGroup/Opertions/Get/cableModems.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Postman Visualizer: PyPNM-CMTS/ServingGroup/Opertions/Get/cableModems
// Last Update: 2026-03-08 20:05:00 MST
// Visual Constraints: Follow canonical visual rules in CODING_AGENTS.md.

(function () {
  const response = pm.response.json();

  const template = `
  <style>
    body { background:#141821; color:#e7edf8; font-family:Arial,sans-serif; margin:0; padding:16px; }
    .wrap { max-width:1600px; margin:0 auto; }
    .card { background:#1b2332; border:1px solid rgba(255,255,255,0.09); border-radius:10px; padding:14px; }
    .title { margin:0 0 8px 0; color:#f3f6ff; text-align:center; font-size:20px; font-weight:700; }
    .meta { color:#dbe3ff; font-size:12px; margin-bottom:10px; text-align:center; }
    pre { margin:0; padding:10px; border-radius:6px; background:#1a1a1a; border:1px solid #4d4d4d; overflow:auto; font-size:12px; }
  </style>
  <div class="wrap">
    <div class="card">
      <h1 class="title">Serving Group Operations Get Cable Modems</h1>
      <div class="meta">POST /cmts/servingGroup/operations/get/cableModems</div>
      <pre>{{raw}}</pre>
    </div>
  </div>
  `;

  pm.visualizer.set(template, { raw: JSON.stringify(response, null, 2) });
})();
````
</details>

<details>
<summary>Sample JSON payload</summary>

````json
{
    "status": 0,
    "message": "Stub sample for /cmts/servingGroup/operations/get/cableModems",
    "cmts": {
        "serving_group": {
            "id": []
        }
    },
    "refresh": {
        "mode": "none",
        "wait_for_cache": false,
        "timeout_seconds": 8
    },
    "data": []
}
````
</details>
