# PyPNM / DOCSIS-3.0 / US-ATDMA-Stats

## Source Files

- HTML/script: `visual/PyPNM/DOCSIS-3.0/US-ATDMA-Stats.html`
- JSON sample: `visual/PyPNM/DOCSIS-3.0/US-ATDMA-Stats.json`

## Preview

<iframe src="../../../visual-previews/DOCSIS-3.0/US-ATDMA-Stats.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Postman Visualizer: Upstream ATDMA Channel Stats (Per-Channel Cards)
// FIX: Bar graph now uses an absolute padded Y-axis (not min/max normalization), so the min channel
//      does not collapse to a thin line.
// X = channel_id, Y = dBmV, sorted by Frequency (low → high).
// EQ data excluded from visuals.
// Paste into Tests tab.

(function () {
  const resp = pm.response.json();

  const safe = (v, d = "") => (v === undefined || v === null ? d : v);
  const esc = (s) =>
    String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");

  const fmt = (v, digits = 2) => (typeof v === "number" && isFinite(v) ? v.toFixed(digits) : "—");

  const results = safe(resp.results, {});
  const entriesRaw = Array.isArray(results.entries) ? results.entries.slice() : [];
  const dwr = results.dwr_window_check || {};

  const warnDb = Number(dwr.dwr_warning_db);
  const violDb = Number(dwr.dwr_violation_db);

  const entries = entriesRaw.slice().sort((a, b) => {
    const fa = Number(a?.entry?.docsIfUpChannelFrequency);
    const fb = Number(b?.entry?.docsIfUpChannelFrequency);
    if (isFinite(fa) && isFinite(fb) && fa !== fb) return fa - fb;
    if (isFinite(fa) && !isFinite(fb)) return -1;
    if (!isFinite(fa) && isFinite(fb)) return 1;

    const ca = Number(a?.channel_id);
    const cb = Number(b?.channel_id);
    if (isFinite(ca) && isFinite(cb) && ca !== cb) return ca - cb;

    return Number(a?.index) - Number(b?.index);
  });

  const ch = entries.map((rec) => {
    const chId = rec?.channel_id;
    const freqHz = Number(rec?.entry?.docsIfUpChannelFrequency);
    const txp = Number(rec?.entry?.docsIf3CmStatusUsTxPower);
    return { rec, chId, freqHz, txp };
  });

  const pVals = ch.map((x) => x.txp).filter((v) => isFinite(v));
  const pMin = pVals.length ? Math.min(...pVals) : 0;
  const pMax = pVals.length ? Math.max(...pVals) : 1;

  const spreadDb = Number(dwr.spread_db);
  const setState =
    isFinite(violDb) && isFinite(spreadDb) && spreadDb >= violDb
      ? "bad"
      : isFinite(warnDb) && isFinite(spreadDb) && spreadDb >= warnDb
      ? "warn"
      : "good";

  function hzToMHz(v) {
    const n = Number(v);
    if (!isFinite(n)) return "—";
    return fmt(n / 1e6, 3);
  }

  function statusBadge(label, kind) {
    return `<span class="badge ${esc(kind)}">${esc(label)}</span>`;
  }

  function rangingStatusBadge(code) {
    const n = Number(code);
    if (!Number.isInteger(n)) return statusBadge("Ranging: —", "neutral");
    if (n === 4) return statusBadge("Ranging: 4", "good");
    if (n === 0) return statusBadge("Ranging: 0", "warn");
    return statusBadge(`Ranging: ${n}`, "neutral");
  }

  function chTypeBadge(code) {
    const n = Number(code);
    if (!Number.isInteger(n)) return statusBadge("Type: —", "neutral");
    return statusBadge(`Type: ${n}`, "neutral");
  }

  function boolPill(v) {
    const b = Boolean(v);
    return b ? `<span class="pill yes">true</span>` : `<span class="pill no">false</span>`;
  }

  // Absolute Y-axis with padding (prevents min channel looking like "zero")
  const PAD_DB = 1.0;
  const ROUND_STEP_DB = 0.5;

  function floorToStep(v, step) {
    return Math.floor(v / step) * step;
  }

  function ceilToStep(v, step) {
    return Math.ceil(v / step) * step;
  }

  const yMinRaw = pMin - PAD_DB;
  const yMaxRaw = pMax + PAD_DB;
  const yMin = floorToStep(yMinRaw, ROUND_STEP_DB);
  const yMax = ceilToStep(yMaxRaw, ROUND_STEP_DB);
  const ySpan = Math.max(1e-9, yMax - yMin);

  function barHeightPctAbsolute(p) {
    if (!(typeof p === "number" && isFinite(p))) return 0;
    const pct = ((p - yMin) / ySpan) * 100;
    const clamped = Math.min(100, Math.max(0, pct));

    const MIN_VISIBLE = 6; // percent (only for finite values)
    if (clamped <= 0) return MIN_VISIBLE;
    return Math.max(MIN_VISIBLE, clamped);
  }

  function buildVerticalPowerBars() {
    const state = setState;
    const hasP = pVals.length > 0;

    const tooltipLines = (x) => {
      const f = Number(x?.rec?.entry?.docsIfUpChannelFrequency);
      const w = Number(x?.rec?.entry?.docsIfUpChannelWidth);
      return [
        `ChId: ${safe(x.chId, "—")}`,
        `TxP: ${fmt(x.txp, 1)} dBmV`,
        `Freq: ${hzToMHz(f)} MHz`,
        `Width: ${hzToMHz(w)} MHz`,
      ].join("\n");
    };

    const yMid = (yMin + yMax) / 2;

    return `
      <div class="bars-wrap">
        <div class="bars-head">
          <div class="bars-title">Tx Power (Y = dBmV, X = Channel ID, Sorted By Frequency Low → High)</div>
          <div class="bars-meta mono">
            axis=${esc(fmt(yMin, 1))}..${esc(fmt(yMax, 1))} dBmV · min=${esc(fmt(pMin, 1))} · max=${esc(fmt(pMax, 1))} · spread=${esc(fmt(spreadDb, 2))} dB
          </div>
        </div>

        <div class="bars-plot" role="img" aria-label="Per-channel Tx power vertical bars sorted by frequency">
          ${
            hasP
              ? ch
                  .map((x) => {
                    const missing = !(typeof x.txp === "number" && isFinite(x.txp));
                    const h = missing ? 0 : barHeightPctAbsolute(x.txp);
                    const label = safe(x.chId, "—");
                    return `
                      <div class="bar-col" title="${esc(tooltipLines(x))}">
                        <div class="bar-slot">
                          <div class="vbar ${esc(state)} ${missing ? "missing" : ""}" style="height:${h.toFixed(2)}%"></div>
                        </div>
                        <div class="bar-x mono">Ch ${esc(String(label))}</div>
                        <div class="bar-x2 mono">${esc(hzToMHz(x.freqHz))} MHz</div>
                      </div>
                    `;
                  })
                  .join("")
              : `<div class="bars-empty">No docsIf3CmStatusUsTxPower values found.</div>`
          }
        </div>

        <div class="bars-axis">
          <div class="mono">${esc(fmt(yMin, 1))} dBmV</div>
          <div class="mono">${esc(fmt(yMid, 1))} dBmV</div>
          <div class="mono">${esc(fmt(yMax, 1))} dBmV</div>
        </div>

        <div class="legend">
          <div class="leg"><span class="sw good"></span><span>Good</span></div>
          <div class="leg"><span class="sw warn"></span><span>Warning</span></div>
          <div class="leg"><span class="sw bad"></span><span>Violation</span></div>
        </div>
      </div>
    `;
  }

  function buildDwrPanel() {
    const warn = Number(dwr.dwr_warning_db);
    const viol = Number(dwr.dwr_violation_db);
    const spread = Number(dwr.spread_db);
    const chCount = safe(dwr.channel_count, entries.length);

    const minP = safe(dwr.min_power_dbmv, isFinite(pMin) ? pMin : "—");
    const maxP = safe(dwr.max_power_dbmv, isFinite(pMax) ? pMax : "—");

    const isWarn = Boolean(dwr.is_warning);
    const isViol = Boolean(dwr.is_violation);

    const extreme = Array.isArray(dwr.extreme_channel_ids) ? dwr.extreme_channel_ids : [];
    const extremeStr = extreme.length ? extreme.join(", ") : "—";

    let state = statusBadge("OK", "good");
    if (isViol) state = statusBadge("VIOLATION", "bad");
    else if (isWarn) state = statusBadge("WARNING", "warn");

    return `
      <div class="dwr">
        <div class="dwr-head">
          <div class="h1">DWR Window Check</div>
          <div class="badges">
            ${state}
            ${statusBadge(`Channels ${esc(String(chCount))}`, "neutral")}
            ${isFinite(warn) ? statusBadge(`Warn ${esc(fmt(warn, 2))} dB`, "neutral") : ""}
            ${isFinite(viol) ? statusBadge(`Viol ${esc(fmt(viol, 2))} dB`, "neutral") : ""}
            ${isFinite(spread) ? statusBadge(`Spread ${esc(fmt(spread, 2))} dB`, "accent") : ""}
          </div>
        </div>

        <div class="dwr-grid">
          <div class="kv">
            <div class="k">Min Power</div>
            <div class="v mono">${esc(fmt(Number(minP), 1))} dBmV</div>
          </div>
          <div class="kv">
            <div class="k">Max Power</div>
            <div class="v mono">${esc(fmt(Number(maxP), 1))} dBmV</div>
          </div>
          <div class="kv">
            <div class="k">Spread</div>
            <div class="v mono">${esc(fmt(spread, 2))} dB</div>
          </div>
          <div class="kv">
            <div class="k">Extreme Channel IDs</div>
            <div class="v mono">${esc(extremeStr)}</div>
          </div>
        </div>
      </div>
    `;
  }

  function buildChannelCard(rec) {
    const idx = safe(rec.index, "—");
    const chId = safe(rec.channel_id, "—");
    const e = rec.entry || {};

    const upId = safe(e.docsIfUpChannelId, "—");
    const freqHz = Number(e.docsIfUpChannelFrequency);
    const widthHz = Number(e.docsIfUpChannelWidth);
    const txp = Number(e.docsIf3CmStatusUsTxPower);

    const isMuted = Boolean(e.docsIf3CmStatusUsIsMuted);
    const preEqEnabled = Boolean(e.docsIfUpChannelPreEqEnable);
    const status = safe(e.docsIfUpChannelStatus, "—");

    const t3 = safe(e.docsIf3CmStatusUsT3Timeouts, "—");
    const t4 = safe(e.docsIf3CmStatusUsT4Timeouts, "—");
    const t3x = safe(e.docsIf3CmStatusUsT3Exceededs, "—");
    const abort = safe(e.docsIf3CmStatusUsRangingAborteds, "—");

    const modType = safe(e.docsIf3CmStatusUsModulationType, "—");
    const slot = safe(e.docsIfUpChannelSlotSize, "—");
    const timing = safe(e.docsIfUpChannelTxTimingOffset, "—");

    const ranging = rangingStatusBadge(e.docsIf3CmStatusUsRangingStatus);
    const ctype = chTypeBadge(e.docsIfUpChannelType);

    const badges = [
      statusBadge(`Index ${idx}`, "neutral"),
      statusBadge(`ChId ${chId}`, "accent"),
      statusBadge(`UpId ${upId}`, "neutral"),
      statusBadge(`Freq ${hzToMHz(freqHz)} MHz`, "neutral"),
      ranging,
      ctype,
      isMuted ? statusBadge("Muted", "bad") : statusBadge("Not Muted", "good"),
    ].join("");

    return `
      <div class="card">
        <div class="card-head">
          <div class="card-title">
            <div class="h1">US Channel ${esc(String(chId))}</div>
            <div class="badges">${badges}</div>
          </div>

          <div class="power">
            <div class="power-top">
              <div class="k">Tx Power</div>
              <div class="v mono">${esc(fmt(txp, 1))} dBmV</div>
            </div>
            <div class="power-foot mono">
              axis=${esc(fmt(yMin, 1))}..${esc(fmt(yMax, 1))} · min=${esc(fmt(pMin, 1))} · max=${esc(fmt(pMax, 1))}
            </div>
          </div>
        </div>

        <div class="kv-grid">
          <div class="kv">
            <div class="k">Frequency</div>
            <div class="v mono">${esc(hzToMHz(freqHz))} MHz</div>
          </div>
          <div class="kv">
            <div class="k">Width</div>
            <div class="v mono">${esc(hzToMHz(widthHz))} MHz</div>
          </div>
          <div class="kv">
            <div class="k">Status</div>
            <div class="v mono">${esc(String(status))}</div>
          </div>
          <div class="kv">
            <div class="k">Pre-EQ Enable</div>
            <div class="v">${boolPill(preEqEnabled)}</div>
          </div>

          <div class="kv">
            <div class="k">Mod Type</div>
            <div class="v mono">${esc(String(modType))}</div>
          </div>
          <div class="kv">
            <div class="k">Slot Size</div>
            <div class="v mono">${esc(String(slot))}</div>
          </div>
          <div class="kv">
            <div class="k">Tx Timing Offset</div>
            <div class="v mono">${esc(String(timing))}</div>
          </div>
          <div class="kv">
            <div class="k">Muted</div>
            <div class="v">${boolPill(isMuted)}</div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="counters">
          <div class="ct">
            <div class="k">T3 Timeouts</div>
            <div class="v mono">${esc(String(t3))}</div>
          </div>
          <div class="ct">
            <div class="k">T4 Timeouts</div>
            <div class="v mono">${esc(String(t4))}</div>
          </div>
          <div class="ct">
            <div class="k">T3 Exceededs</div>
            <div class="v mono">${esc(String(t3x))}</div>
          </div>
          <div class="ct">
            <div class="k">Ranging Aborteds</div>
            <div class="v mono">${esc(String(abort))}</div>
          </div>
        </div>
      </div>
    `;
  }

  const template = `
  <style>
    :root {
      --bg: #0b1220;
      --panel: #0f1a2b;
      --panel2: #0c1727;
      --text: #e6edf3;
      --muted: #94a3b8;

      --accent: #60a5fa;

      --good: #34d399;
      --warn: #fbbf24;
      --bad:  #fb7185;

      --border: rgba(148,163,184,0.22);
      --shadow: rgba(0,0,0,0.40);

      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      --sans: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
    }

    body { margin: 0; padding: 18px 18px 28px 18px; background: var(--bg); color: var(--text); font-family: var(--sans); }

    .top { display: flex; flex-wrap: wrap; gap: 10px 18px; align-items: baseline; margin-bottom: 14px; }
    .title { font-size: 18px; font-weight: 800; letter-spacing: 0.2px; }
    .sub { color: var(--muted); font-size: 12px; }
    .mono { font-family: var(--mono); }

    .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }
    .chip { background: rgba(96,165,250,0.12); border: 1px solid var(--border); border-radius: 999px; padding: 6px 10px; font-size: 12px; color: var(--text); }
    .chip .k { color: var(--muted); margin-right: 6px; }

    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 14px; }

    .h1 { font-size: 14px; font-weight: 800; letter-spacing: 0.2px; }

    .badges { display: flex; flex-wrap: wrap; gap: 8px; }
    .badge { border-radius: 999px; padding: 4px 8px; font-size: 11px; border: 1px solid var(--border); background: rgba(148,163,184,0.10); color: var(--text); font-weight: 700; }
    .badge.accent { background: rgba(96,165,250,0.18); border-color: rgba(96,165,250,0.38); }
    .badge.good { background: rgba(52,211,153,0.14); border-color: rgba(52,211,153,0.38); }
    .badge.warn { background: rgba(251,191,36,0.14); border-color: rgba(251,191,36,0.42); }
    .badge.bad  { background: rgba(251,113,133,0.14); border-color: rgba(251,113,133,0.42); }
    .badge.neutral { background: rgba(148,163,184,0.10); border-color: var(--border); }

    .pill { display: inline-block; border-radius: 999px; padding: 4px 8px; font-size: 11px; font-weight: 800; border: 1px solid var(--border); }
    .pill.yes { background: rgba(52,211,153,0.14); border-color: rgba(52,211,153,0.38); color: var(--text); }
    .pill.no  { background: rgba(148,163,184,0.10); border-color: var(--border); color: var(--text); }

    .dwr {
      background: linear-gradient(180deg, var(--panel), var(--panel2));
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: 0 12px 26px var(--shadow);
      padding: 12px 14px;
      margin-bottom: 14px;
    }
    .dwr-head { display: flex; flex-wrap: wrap; gap: 10px 14px; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    .dwr-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; }

    .kv .k { color: var(--muted); font-size: 11px; font-weight: 700; }
    .kv .v { font-size: 12px; font-weight: 700; margin-top: 2px; }

    .bars-wrap {
      background: linear-gradient(180deg, var(--panel), var(--panel2));
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: 0 12px 26px var(--shadow);
      padding: 12px 14px 14px 14px;
      margin-bottom: 14px;
      display: grid;
      gap: 10px;
    }

    .bars-head { display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-between; align-items: baseline; }
    .bars-title { font-size: 12px; font-weight: 800; }
    .bars-meta { font-size: 11px; color: var(--muted); }

    .bars-plot {
      height: 210px;
      border-radius: 12px;
      border: 1px solid rgba(148,163,184,0.20);
      background: rgba(148,163,184,0.08);
      padding: 10px 10px 6px 10px;
      display: grid;
      grid-auto-flow: column;
      grid-auto-columns: minmax(56px, 1fr);
      gap: 8px;
      align-items: end;
      overflow: hidden;
    }

    .bar-col { display: grid; gap: 6px; align-items: end; }
    .bar-slot {
      height: 130px;
      border-radius: 10px;
      border: 1px solid rgba(148,163,184,0.16);
      background: rgba(0,0,0,0.14);
      display: flex;
      align-items: end;
      padding: 6px;
    }

    .vbar {
      width: 100%;
      height: 0%;
      border-radius: 8px 8px 4px 4px;
      box-shadow: 0 10px 20px rgba(0,0,0,0.25);
      transition: height 120ms ease;
    }

    .vbar.good { background: linear-gradient(180deg, rgba(52,211,153,0.95), rgba(96,165,250,0.65)); }
    .vbar.warn { background: linear-gradient(180deg, rgba(251,191,36,0.95), rgba(96,165,250,0.55)); }
    .vbar.bad  { background: linear-gradient(180deg, rgba(251,113,133,0.95), rgba(96,165,250,0.50)); }

    .vbar.missing {
      height: 6px !important;
      background: rgba(148,163,184,0.28);
      box-shadow: none;
      border-radius: 8px;
    }

    .bar-x { text-align: center; color: rgba(148,163,184,0.95); font-size: 11px; }
    .bar-x2 { text-align: center; color: rgba(148,163,184,0.70); font-size: 10px; margin-top: -2px; }

    .bars-axis {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      color: var(--muted);
      font-size: 11px;
    }
    .bars-axis > div:nth-child(1) { text-align: left; }
    .bars-axis > div:nth-child(2) { text-align: center; }
    .bars-axis > div:nth-child(3) { text-align: right; }

    .legend { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
    .leg { display: inline-flex; gap: 8px; align-items: center; color: var(--muted); font-size: 11px; font-weight: 800; }
    .sw { width: 14px; height: 10px; border-radius: 4px; border: 1px solid rgba(148,163,184,0.25); display: inline-block; }
    .sw.good { background: rgba(52,211,153,0.85); }
    .sw.warn { background: rgba(251,191,36,0.90); }
    .sw.bad  { background: rgba(251,113,133,0.85); }

    .bars-empty { color: var(--muted); font-size: 12px; padding: 10px; }

    .card {
      background: linear-gradient(180deg, var(--panel), var(--panel2));
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: 0 12px 26px var(--shadow);
      overflow: hidden;
    }

    .card-head {
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      display: grid;
      grid-template-columns: 1fr minmax(220px, 260px);
      gap: 12px;
      align-items: start;
    }

    .card-title { display: grid; gap: 8px; }

    .kv-grid {
      padding: 12px 14px 10px 14px;
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px 12px;
    }

    .divider { height: 1px; background: var(--border); margin: 0 14px; }

    .counters {
      padding: 10px 14px 14px 14px;
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }
    .ct {
      border: 1px solid rgba(148,163,184,0.18);
      background: rgba(148,163,184,0.06);
      border-radius: 12px;
      padding: 8px 10px;
      display: grid;
      gap: 2px;
    }
    .ct .k { color: var(--muted); font-size: 11px; font-weight: 700; }
    .ct .v { font-size: 13px; font-weight: 900; }

    @media (max-width: 980px) {
      .card-head { grid-template-columns: 1fr; }
      .counters { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
  </style>

  <div class="top">
    <div class="title">Upstream ATDMA Channel Statistics</div>
    <div class="sub">Per-channel cards (EQ excluded) + Tx power bar graph (absolute y-axis) sorted by frequency</div>
  </div>

  <div class="chips">
    <div class="chip"><span class="k">MAC</span> <span class="mono">${esc(safe(resp.mac_address, ""))}</span></div>
    <div class="chip"><span class="k">Status</span> <span class="mono">${esc(String(safe(resp.status, "")))}</span></div>
    <div class="chip"><span class="k">Message</span> <span>${esc(safe(resp.message, ""))}</span></div>
    <div class="chip"><span class="k">Channels</span> <span class="mono">${esc(String(entries.length))}</span></div>
    <div class="chip"><span class="k">DWR State</span> <span class="mono">${esc(setState.toUpperCase())}</span></div>
    <div class="chip"><span class="k">Warn/Viol</span> <span class="mono">${esc(fmt(warnDb, 2))}/${esc(fmt(violDb, 2))} dB</span></div>
  </div>

  ${buildDwrPanel()}

  ${buildVerticalPowerBars()}

  <div class="grid">
    ${entries.map(buildChannelCard).join("")}
  </div>
  `;

  pm.visualizer.set(template, {});
})();
````
</details>

<details>
<summary>Sample JSON payload</summary>

````json
{
    "mac_address": "aa:bb:cc:dd:ee:ff",
    "status": 0,
    "message": "Successfully retrieved upstream ATDMA channel statistics",
    "results": {
        "entries": [
            {
                "index": 4,
                "channel_id": 4,
                "entry": {
                    "docsIfUpChannelId": 4,
                    "docsIfUpChannelFrequency": 35200000,
                    "docsIfUpChannelWidth": 6400000,
                    "docsIfUpChannelModulationProfile": 0,
                    "docsIfUpChannelSlotSize": 1,
                    "docsIfUpChannelTxTimingOffset": 8588,
                    "docsIfUpChannelRangingBackoffStart": 3,
                    "docsIfUpChannelRangingBackoffEnd": 8,
                    "docsIfUpChannelTxBackoffStart": 2,
                    "docsIfUpChannelTxBackoffEnd": 6,
                    "docsIfUpChannelType": 2,
                    "docsIfUpChannelCloneFrom": 0,
                    "docsIfUpChannelUpdate": false,
                    "docsIfUpChannelStatus": 1,
                    "docsIfUpChannelPreEqEnable": true,
                    "docsIf3CmStatusUsTxPower": 50.8,
                    "docsIf3CmStatusUsT3Timeouts": 0,
                    "docsIf3CmStatusUsT4Timeouts": 0,
                    "docsIf3CmStatusUsRangingAborteds": 0,
                    "docsIf3CmStatusUsModulationType": 2,
                    "docsIf3CmStatusUsEqData": "0x08011800fffefffe0004fffc00000004fffcfffa0002000afffeffeefffa002407fd0000ffd4ffc400080018fffafff400000006fffefffa00020002fffcfffe00020000fffcfffe000000000000fffe0002000000000000fffe00000000000200000000",
                    "docsIf3CmStatusUsT3Exceededs": 0,
                    "docsIf3CmStatusUsIsMuted": false,
                    "docsIf3CmStatusUsRangingStatus": "success"
                }
            },
            {
                "index": 80,
                "channel_id": 1,
                "entry": {
                    "docsIfUpChannelId": 1,
                    "docsIfUpChannelFrequency": 16000000,
                    "docsIfUpChannelWidth": 6400000,
                    "docsIfUpChannelModulationProfile": 0,
                    "docsIfUpChannelSlotSize": 1,
                    "docsIfUpChannelTxTimingOffset": 8588,
                    "docsIfUpChannelRangingBackoffStart": 3,
                    "docsIfUpChannelRangingBackoffEnd": 8,
                    "docsIfUpChannelTxBackoffStart": 2,
                    "docsIfUpChannelTxBackoffEnd": 6,
                    "docsIfUpChannelType": 2,
                    "docsIfUpChannelCloneFrom": 0,
                    "docsIfUpChannelUpdate": false,
                    "docsIfUpChannelStatus": 1,
                    "docsIfUpChannelPreEqEnable": true,
                    "docsIf3CmStatusUsTxPower": 50.8,
                    "docsIf3CmStatusUsT3Timeouts": 0,
                    "docsIf3CmStatusUsT4Timeouts": 0,
                    "docsIf3CmStatusUsRangingAborteds": 0,
                    "docsIf3CmStatusUsModulationType": 2,
                    "docsIf3CmStatusUsEqData": "0x08011800000100040000fff70003000efffcffe900060020fffbffc4fff9009807f6ffec0006ffb2fffd00290004ffe6fffe00110003fff5000000070001fffc000300010000ffff0000ffff0000fffffffe0001fffffffefffeffff0000ffff00000001",
                    "docsIf3CmStatusUsT3Exceededs": 0,
                    "docsIf3CmStatusUsIsMuted": false,
                    "docsIf3CmStatusUsRangingStatus": "success"
                }
            },
            {
                "index": 81,
                "channel_id": 3,
                "entry": {
                    "docsIfUpChannelId": 3,
                    "docsIfUpChannelFrequency": 28800000,
                    "docsIfUpChannelWidth": 6400000,
                    "docsIfUpChannelModulationProfile": 0,
                    "docsIfUpChannelSlotSize": 1,
                    "docsIfUpChannelTxTimingOffset": 8588,
                    "docsIfUpChannelRangingBackoffStart": 3,
                    "docsIfUpChannelRangingBackoffEnd": 8,
                    "docsIfUpChannelTxBackoffStart": 2,
                    "docsIfUpChannelTxBackoffEnd": 6,
                    "docsIfUpChannelType": 2,
                    "docsIfUpChannelCloneFrom": 0,
                    "docsIfUpChannelUpdate": false,
                    "docsIfUpChannelStatus": 1,
                    "docsIfUpChannelPreEqEnable": true,
                    "docsIf3CmStatusUsTxPower": 50.8,
                    "docsIf3CmStatusUsT3Timeouts": 0,
                    "docsIf3CmStatusUsT4Timeouts": 0,
                    "docsIf3CmStatusUsRangingAborteds": 0,
                    "docsIf3CmStatusUsModulationType": 2,
                    "docsIf3CmStatusUsEqData": "0x0801180000020002000200020002fffe0000000000060002fff60000001a000a07ff00000018000efff8fffc00020002fffcfffefffe000000020002fffe00020004000000000002fffe000000000004fffe00020000fffefffe0002fffe0000fffe0002",
                    "docsIf3CmStatusUsT3Exceededs": 0,
                    "docsIf3CmStatusUsIsMuted": false,
                    "docsIf3CmStatusUsRangingStatus": "success"
                }
            },
            {
                "index": 82,
                "channel_id": 2,
                "entry": {
                    "docsIfUpChannelId": 2,
                    "docsIfUpChannelFrequency": 22400000,
                    "docsIfUpChannelWidth": 6400000,
                    "docsIfUpChannelModulationProfile": 0,
                    "docsIfUpChannelSlotSize": 1,
                    "docsIfUpChannelTxTimingOffset": 8589,
                    "docsIfUpChannelRangingBackoffStart": 3,
                    "docsIfUpChannelRangingBackoffEnd": 8,
                    "docsIfUpChannelTxBackoffStart": 2,
                    "docsIfUpChannelTxBackoffEnd": 6,
                    "docsIfUpChannelType": 2,
                    "docsIfUpChannelCloneFrom": 0,
                    "docsIfUpChannelUpdate": false,
                    "docsIfUpChannelStatus": 1,
                    "docsIfUpChannelPreEqEnable": true,
                    "docsIf3CmStatusUsTxPower": 50.8,
                    "docsIf3CmStatusUsT3Timeouts": 1,
                    "docsIf3CmStatusUsT4Timeouts": 0,
                    "docsIf3CmStatusUsRangingAborteds": 0,
                    "docsIf3CmStatusUsModulationType": 2,
                    "docsIf3CmStatusUsEqData": "0x08011800fffafffc00040004fffefffb0001000afffafff400080016ffe1ffe307f9fffcfff5008cfff9ffd10000001bfffeffef0001000c0003fffafffe00040004fffc000000020000fffe0004000100000002ffff000100000000fffd0000fffdfffd",
                    "docsIf3CmStatusUsT3Exceededs": 0,
                    "docsIf3CmStatusUsIsMuted": false,
                    "docsIf3CmStatusUsRangingStatus": "success"
                }
            }
        ],
        "dwr_window_check": {
            "dwr_warning_db": 6.0,
            "dwr_violation_db": 12.0,
            "channel_count": 4,
            "min_power_dbmv": 50.8,
            "max_power_dbmv": 50.8,
            "spread_db": 0.0,
            "is_warning": false,
            "is_violation": false,
            "extreme_channel_ids": [
                4,
                1,
                3,
                2
            ]
        }
    }
}
````
</details>
