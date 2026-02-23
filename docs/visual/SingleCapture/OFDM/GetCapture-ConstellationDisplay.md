# PyPNM / SingleCapture / OFDM / GetCapture-ConstellationDisplay

## Source Files

- HTML/script: `visual/PyPNM/SingleCapture/OFDM/GetCapture-ConstellationDisplay.html`
- JSON sample: `visual/PyPNM/SingleCapture/OFDM/GetCapture-ConstellationDisplay.json`

## Preview

<iframe src="../../../../visual-previews/SingleCapture/OFDM/GetCapture-ConstellationDisplay.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Postman Visualizer: Constellation Grid (pm.getData-safe; avoids inline huge JSON)
// Env knobs:
// - CONST_MAX_POINTS_PER_CH (default 5000)
// - CONST_COLS (default 2)
// - CONST_SERIES_MODE = both|soft|hard (default both)

(function () {
  const res = pm.response.json();

  const MAX_POINTS_PER_CH = parseInt(pm.environment.get("CONST_MAX_POINTS_PER_CH") || "5000", 10);
  const COLS = parseInt(pm.environment.get("CONST_COLS") || "2", 10);
  const SERIES_MODE = (pm.environment.get("CONST_SERIES_MODE") || "both").toLowerCase();

  function isFiniteNum(v) { return typeof v === "number" && isFinite(v); }
  function isPair(p) { return Array.isArray(p) && p.length >= 2 && isFiniteNum(p[0]) && isFiniteNum(p[1]); }

  function asPoints(any) {
    if (Array.isArray(any)) return any.filter(isPair);
    if (any && Array.isArray(any.complex)) return any.complex.filter(isPair);
    return [];
  }

  function reservoirSample(arr, k) {
    const n = arr.length;
    if (k >= n) return arr;
    const out = arr.slice(0, k);
    for (let i = k; i < n; i++) {
      const j = Math.floor(Math.random() * (i + 1));
      if (j < k) out[j] = arr[i];
    }
    return out;
  }

  function pickList(payload) {
    const candidates = [payload?.data?.analysis, payload?.analysis, payload?.data];
    for (const c of candidates) {
      if (Array.isArray(c) && c.length) return c;
    }
    return [];
  }

  function safeStr(v) {
    if (v === undefined || v === null) return "N/A";
    if (typeof v === "string" && v.trim() === "") return "N/A";
    return String(v);
  }

  function sanitizeMac(value, fallback) {
    const fb = (fallback === undefined || fallback === null) ? "N/A" : fallback;
    if (value === undefined || value === null) return fb;
    const text = String(value).trim();
    if (!text) return fb;
    const compact = text.replace(/[^0-9a-f]/gi, "").toLowerCase();
    if (compact.length !== 12) return text;
    if (text.indexOf(":") !== -1) return compact.match(/.{1,2}/g).join(":");
    if (text.indexOf("-") !== -1) return compact.match(/.{1,2}/g).join("-");
    if (text.indexOf("_") !== -1) return compact.match(/.{1,2}/g).join("_");
    return compact;
  }

  function sanitizeSystemDescription(_sys) {
    return {
      HW_REV: "1.0",
      VENDOR: "LANCity",
      BOOTR: "NONE",
      SW_REV: "1.0.0",
      MODEL: "LCPET-3"
    };
  }

  const list = pickList(res);

  // Build metadata (best-effort)
  const mac = sanitizeMac(res?.mac_address || res?.data?.mac_address, "N/A");
  const device = res?.data?.device_details || res?.device_details || {};
  const sys = sanitizeSystemDescription(
    res?.data?.device_details?.system_description || device?.system_description || device?.sysDescr || {}
  );

  const devLine = [
    `MAC: ${mac}`,
    `VENDOR: ${safeStr(sys?.VENDOR || device?.vendor)}`,
    `MODEL: ${safeStr(sys?.MODEL || device?.model)}`,
    `SW: ${safeStr(sys?.SW_REV || device?.sw_rev)}`,
    `HW: ${safeStr(sys?.HW_REV || device?.hw_rev)}`
  ].join(" · ");

  if (!Array.isArray(list) || list.length === 0) {
    pm.visualizer.set(
      "<div style='font-family:Arial,sans-serif;padding:12px;'>No analysis list found (expected data.analysis[] or analysis[]).</div>",
      {}
    );
    return;
  }

  // Prepare channels without putting them into the HTML string
  const channels = list
    .map((e) => {
      const softRaw = asPoints(e?.soft);
      const hardRaw = asPoints(e?.hard);

      const soft = reservoirSample(softRaw, MAX_POINTS_PER_CH);
      const hard = reservoirSample(hardRaw, MAX_POINTS_PER_CH);

      const pointsForBounds = []
        .concat(SERIES_MODE === "hard" ? [] : soft)
        .concat(SERIES_MODE === "soft" ? [] : hard);

      if (pointsForBounds.length === 0) {
        return {
          channel_id: e?.channel_id ?? null,
          modulation_order: e?.modulation_order ?? null,
          num_sample_symbols: e?.num_sample_symbols ?? null,
          soft: [],
          hard: [],
          bounds: null
        };
      }

      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      for (const p of pointsForBounds) {
        const x = p[0], y = p[1];
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
      }

      const spanX = (maxX - minX) || 1;
      const spanY = (maxY - minY) || 1;
      const span = Math.max(spanX, spanY);
      const cx = (minX + maxX) / 2;
      const cy = (minY + maxY) / 2;
      const pad = 0.07 * span;
      const half = (span / 2) + pad;

      return {
        channel_id: e?.channel_id ?? null,
        modulation_order: e?.modulation_order ?? null,
        num_sample_symbols: e?.num_sample_symbols ?? null,
        soft: soft,
        hard: hard,
        bounds: { xmin: cx - half, xmax: cx + half, ymin: cy - half, ymax: cy + half }
      };
    })
    .sort((a, b) => Number(a.channel_id) - Number(b.channel_id));

  // Layout sizing (cap canvas growth if many channels)
  const cols = Math.max(1, Math.min(4, COLS));
  const rows = Math.ceil(channels.length / cols);

  const TILE_W = 540;
  const TILE_H = 420;
  const PAD = 10;

  const canvasW = cols * TILE_W + PAD * 2;
  const canvasH = rows * TILE_H + PAD * 2;

  const template = `
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    body { margin:0; padding:14px; background:#0b0b0b; color:#eaeaea; font-family: Arial, sans-serif; }
    .hdr { font-size:14px; font-weight:700; margin-bottom:6px; }
    .sub { font-size:12px; color:#cfcfcf; margin-top:4px; }
    .box { border:1px solid #2a2a2a; border-radius:10px; background:#050505; padding:10px; margin-top:10px; }
    .err { margin-top:10px; padding:10px; border:1px solid rgba(255,120,120,0.5); border-radius:10px; background:rgba(255,0,0,0.06); color:#ffd1d1; white-space:pre-wrap; font-size:12px; }
    canvas { display:block; }
  </style>
</head>
<body>
  <div class="hdr">CONSTELLATION GRID · Channels: {{chCount}} · Series: {{seriesMode}}</div>
  <div class="sub">{{devLine}}</div>
  <div class="sub">Per-channel cap: {{cap}} points · Columns: {{cols}}</div>

  <div class="box">
    <canvas id="cv" width="{{cw}}" height="{{ch}}"></canvas>
  </div>

  <div id="err" class="err" style="display:none;"></div>

  <script>
    function showErr(msg) {
      var el = document.getElementById("err");
      el.style.display = "block";
      el.textContent = msg;
    }

    try {
      pm.getData(function (e, data) {
        if (e) {
          showErr("pm.getData error:\\n" + String(e));
          return;
        }

        var channels = (data && data.channels) ? data.channels : [];
        var seriesMode = (data && data.seriesMode) ? data.seriesMode : "both";

        if (!Array.isArray(channels) || channels.length === 0) {
          showErr("No channel data provided to visualizer.");
          return;
        }

        var cv = document.getElementById("cv");
        var ctx = cv.getContext("2d");

        // Theme
        var BG = "#000";
        var GRID = "rgba(255,255,255,0.14)";
        var FRAME = "rgba(255,255,255,0.80)";
        var TXT = "rgba(255,255,255,0.88)";
        var SUBTXT = "rgba(255,255,255,0.72)";
        var SOFT = "rgba(47,98,255,0.75)";
        var HARD = "rgba(60,255,130,0.60)";

        // Tile geometry
        var cols = data.cols;
        var tileW = data.tileW;
        var tileH = data.tileH;
        var pad = data.pad;

        // Plot margins inside tile
        var mL = 58, mR = 14, mT = 28, mB = 48;

        // Background
        ctx.fillStyle = BG;
        ctx.fillRect(0,0,cv.width,cv.height);

        function drawTile(tileX, tileY, tileW, tileH, ch) {
          // Tile frame
          ctx.strokeStyle = "rgba(255,255,255,0.20)";
          ctx.lineWidth = 1;
          ctx.strokeRect(tileX + 0.5, tileY + 0.5, tileW - 1, tileH - 1);

          // Title
          ctx.fillStyle = TXT;
          ctx.font = "bold 13px Arial";
          ctx.textAlign = "left";
          ctx.textBaseline = "top";

          var title = "Channel: " + (ch.channel_id ?? "N/A") +
                      " · QAM: " + (ch.modulation_order ?? "N/A") +
                      " · Samples: " + (ch.num_sample_symbols ?? "N/A");
          ctx.fillText(title, tileX + 10, tileY + 8);

          // Legend
          ctx.fillStyle = SUBTXT;
          ctx.font = "12px Arial";
          var legend = "";
          if (seriesMode === "soft") legend = "Soft only";
          else if (seriesMode === "hard") legend = "Hard only";
          else legend = "Soft (blue) + Hard (green)";
          ctx.fillText(legend, tileX + 10, tileY + 26);

          // Plot area
          var px = tileX + mL;
          var py = tileY + mT;
          var pw = tileW - mL - mR;
          var ph = tileH - mT - mB;

          // Frame
          ctx.strokeStyle = FRAME;
          ctx.lineWidth = 1.2;
          ctx.strokeRect(px, py, pw, ph);

          // Grid
          ctx.strokeStyle = GRID;
          ctx.lineWidth = 1;
          ctx.setLineDash([6,4]);
          var ticks = 6;

          for (var i=1;i<ticks;i++){
            var gx = px + (i*pw/ticks);
            ctx.beginPath(); ctx.moveTo(gx, py); ctx.lineTo(gx, py+ph); ctx.stroke();
          }
          for (var j=1;j<ticks;j++){
            var gy = py + (j*ph/ticks);
            ctx.beginPath(); ctx.moveTo(px, gy); ctx.lineTo(px+pw, gy); ctx.stroke();
          }
          ctx.setLineDash([]);

          // Labels
          ctx.fillStyle = SUBTXT;
          ctx.font = "12px Arial";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText("I", px + pw/2, tileY + tileH - 20);

          ctx.save();
          ctx.translate(tileX + 18, py + ph/2);
          ctx.rotate(-Math.PI/2);
          ctx.fillText("Q", 0, 0);
          ctx.restore();

          if (!ch.bounds) {
            ctx.fillStyle = SUBTXT;
            ctx.font = "12px Arial";
            ctx.textAlign = "left";
            ctx.textBaseline = "top";
            ctx.fillText("No points for this channel.", px + 10, py + 10);
            return;
          }

          var xmin = ch.bounds.xmin, xmax = ch.bounds.xmax;
          var ymin = ch.bounds.ymin, ymax = ch.bounds.ymax;

          function xToPx(x){ return px + ((x - xmin) / (xmax - xmin)) * pw; }
          function yToPx(y){ return py + ph - ((y - ymin) / (ymax - ymin)) * ph; }

          function drawPoints(arr, color) {
            ctx.fillStyle = color;
            for (var k=0; k<arr.length; k++){
              var p = arr[k];
              var x = xToPx(p[0]);
              var y = yToPx(p[1]);
              if (x < px || x > (px+pw) || y < py || y > (py+ph)) continue;
              ctx.fillRect(x, y, 1, 1);
            }
          }

          if (seriesMode === "soft") {
            drawPoints(ch.soft || [], SOFT);
          } else if (seriesMode === "hard") {
            drawPoints(ch.hard || [], HARD);
          } else {
            drawPoints(ch.soft || [], SOFT);
            drawPoints(ch.hard || [], HARD);
          }
        }

        for (var idx=0; idx<channels.length; idx++){
          var r = Math.floor(idx / cols);
          var c = idx % cols;
          var x = pad + c * tileW;
          var y = pad + r * tileH;
          drawTile(x, y, tileW - pad, tileH - pad, channels[idx]);
        }
      });
    } catch (ex) {
      showErr("Visualizer exception:\\n" + (ex && ex.stack ? ex.stack : String(ex)));
    }
  </script>
</body>
</html>
  `;

  pm.visualizer.set(template, {
    devLine: devLine,
    chCount: channels.length,
    seriesMode: SERIES_MODE,
    cap: MAX_POINTS_PER_CH,
    cols: cols,
    cw: canvasW,
    ch: canvasH,

    // pass runtime params to pm.getData
    channels: channels,
    pad: PAD,
    tileW: TILE_W,
    tileH: TILE_H,
    colsRuntime: cols
  });

  // pm.getData receives the object passed to visualizer.set as "data".
  // To keep names consistent for the HTML script:
  // Postman puts all variables into data; we alias expected names:
  // (Some Postman versions don't preserve renamed keys reliably if you shadow them.)
  // So we provide duplicates:
  pm.visualizer.set(template, {
    devLine: devLine,
    chCount: channels.length,
    seriesMode: SERIES_MODE,
    cap: MAX_POINTS_PER_CH,
    cols: cols,
    cw: canvasW,
    ch: canvasH,

    channels: channels,
    pad: PAD,
    tileW: TILE_W,
    tileH: TILE_H,
    cols: cols
  });
})();
````
</details>

<details>
<summary>Sample JSON payload</summary>

````json

````
</details>
