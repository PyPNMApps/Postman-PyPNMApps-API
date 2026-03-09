# PyPNM-CMTS / ServingGroup / Opertions / Get / topology

## Source Files

- HTML/script: `visual/PyPNM-CMTS/ServingGroup/Opertions/Get/topology.html`
- JSON sample: `visual/PyPNM-CMTS/ServingGroup/Opertions/Get/topology.json`

## Preview

<iframe src="../../../../../../visual-previews/PyPNM-CMTS/ServingGroup/Opertions/Get/topology.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Postman Visualizer: PyPNM-CMTS/ServingGroup/Opertions/Get/topology
// Last Update: 2026-03-08 20:45:00 MST
// Visual Constraints: Follow canonical visual rules in CODING_AGENTS.md.

(function () {
  const response = pm.response.json();

  function safeText(v) {
    if (v === undefined || v === null) return 'N/A';
    const s = String(v).trim();
    return s ? s : 'N/A';
  }

  function n(v) {
    const x = Number(v);
    return Number.isFinite(x) ? x : null;
  }

  function fmtUtc(epochSec) {
    const x = n(epochSec);
    if (x === null) return 'N/A';
    const d = new Date(x * 1000);
    if (!Number.isFinite(d.getTime())) return 'N/A';
    const p = (y) => String(y).padStart(2, '0');
    return d.getUTCFullYear() + '-' + p(d.getUTCMonth() + 1) + '-' + p(d.getUTCDate()) + ' ' + p(d.getUTCHours()) + ':' + p(d.getUTCMinutes()) + ':' + p(d.getUTCSeconds()) + ' UTC';
  }

  function sanitizeMac(value) {
    const raw = safeText(value);
    if (raw === 'N/A') return raw;
    const compact = raw.replace(/[^0-9a-f]/gi, '').toLowerCase();
    if (compact.length !== 12) return raw.toLowerCase();
    return compact.match(/.{1,2}/g).join(':');
  }

  function sortByLowerHz(a, b) {
    const al = n(a && a.lower_frequency_hz);
    const bl = n(b && b.lower_frequency_hz);
    if (al !== null && bl !== null) return al - bl;
    const ai = n(a && a.channel_id);
    const bi = n(b && b.channel_id);
    if (ai !== null && bi !== null) return ai - bi;
    return String(safeText(a && a.channel_id)).localeCompare(String(safeText(b && b.channel_id)), undefined, { numeric: true });
  }

  function bucketChannels(groups) {
    return groups.map((g) => {
      const channels = (g && g.channels && typeof g.channels === 'object') ? g.channels : {};
      const ds = (channels.ds && typeof channels.ds === 'object') ? channels.ds : {};
      const us = (channels.us && typeof channels.us === 'object') ? channels.us : {};

      const dsScQam = Array.isArray(ds.sc_qam) ? ds.sc_qam.slice().sort(sortByLowerHz) : [];
      const dsOfdm = Array.isArray(ds.ofdm) ? ds.ofdm.slice().sort(sortByLowerHz) : [];
      const usScQam = Array.isArray(us.sc_qam) ? us.sc_qam.slice().sort(sortByLowerHz) : [];
      const usOfdma = Array.isArray(us.ofdma) ? us.ofdma.slice().sort(sortByLowerHz) : [];

      const modemMap = (g && g.modems && typeof g.modems === 'object' && !Array.isArray(g.modems)) ? g.modems : {};
      const modemRows = Object.keys(modemMap).map((mac) => {
        const m = modemMap[mac] && typeof modemMap[mac] === 'object' ? modemMap[mac] : {};
        const sys = m && typeof m.sysdescr === 'object' ? m.sysdescr : {};
        return {
          mac: sanitizeMac(mac),
          model: safeText(sys.MODEL),
          vendor: safeText(sys.VENDOR),
          sw: safeText(sys.SW_REV),
          hw: safeText(sys.HW_REV),
          bootr: safeText(sys.BOOTR)
        };
      }).sort((a, b) => String(a.mac).localeCompare(String(b.mac)));

      return {
        sgId: safeText(g && g.sg_id),
        dsChSetId: safeText(g && g.ds_ch_set_id),
        usChSetId: safeText(g && g.us_ch_set_id),
        modemCount: n(g && g.modem_count) !== null ? n(g && g.modem_count) : modemRows.length,
        successCount: n(g && g.success_count) !== null ? n(g && g.success_count) : 0,
        failureCount: n(g && g.failure_count) !== null ? n(g && g.failure_count) : 0,
        dsScQam,
        dsOfdm,
        usScQam,
        usOfdma,
        modemRows
      };
    });
  }

  function channelNode(label, ch) {
    const rawType = ch && ch.channel_type ? String(ch.channel_type).toLowerCase() : '';
    const cf = n(ch && ch.center_frequency_hz);
    const lo = n(ch && ch.lower_frequency_hz);
    const hi = n(ch && ch.upper_frequency_hz);
    const bw = n(ch && ch.channel_width_hz);
    const id = safeText(ch && ch.channel_id);
    let subtitle = 'CF: ' + (cf !== null ? (Math.round(cf / 1e6) + ' MHz') : 'N/A') + (bw !== null ? (' · BW: ' + Math.round(bw / 1e6) + ' MHz') : '');
    if (rawType === 'ofdm' || rawType === 'ofdma') {
      const range = (lo !== null && hi !== null) ? (Math.round(lo / 1e6) + ' - ' + Math.round(hi / 1e6) + ' MHz') : 'N/A';
      subtitle = 'Range: ' + range + (bw !== null ? (' · BW: ' + Math.round(bw / 1e6) + ' MHz') : '');
    }
    return {
      name: label + ' ' + id,
      subtitle,
      kind: label.startsWith('DS') ? 'ds' : 'us'
    };
  }

  function buildTree(mapped) {
    return {
      name: 'CMTS',
      subtitle: 'Serving Group Topology',
      kind: 'root',
      children: mapped.map((g) => {
        const dsChildren = [];
        if (g.dsScQam.length) dsChildren.push({ name: 'DS SCQAM', kind: 'ds', children: g.dsScQam.map((ch) => channelNode('DS', ch)) });
        if (g.dsOfdm.length) dsChildren.push({ name: 'DS OFDM', kind: 'ds', children: g.dsOfdm.map((ch) => channelNode('DS', ch)) });

        const usChildren = [];
        if (g.usScQam.length) usChildren.push({ name: 'US SCQAM', kind: 'us', children: g.usScQam.map((ch) => channelNode('US', ch)) });
        if (g.usOfdma.length) usChildren.push({ name: 'US OFDMA', kind: 'us', children: g.usOfdma.map((ch) => channelNode('US', ch)) });

        const modelBuckets = {};
        g.modemRows.forEach((m) => {
          const model = safeText(m && m.model);
          if (!modelBuckets[model]) modelBuckets[model] = [];
          modelBuckets[model].push(m);
        });

        const modemChildren = Object.keys(modelBuckets)
          .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
          .map((model) => {
            const list = modelBuckets[model]
              .slice()
              .sort((a, b) => String(a.mac).localeCompare(String(b.mac)));
            return {
              name: model,
              subtitle: 'Modem (' + String(list.length) + ')',
              kind: 'modem',
              children: list.slice(0, 120).map((m) => ({
                name: m.mac,
                subtitle: m.sw,
                kind: 'modem'
              }))
            };
          });

        return {
          name: 'SG ' + g.sgId,
          subtitle: 'DS set ' + g.dsChSetId + ' · US set ' + g.usChSetId,
          kind: 'sg',
          children: [
            { name: 'Downstream', kind: 'ds', children: dsChildren.length ? dsChildren : [{ name: 'No DS channels', kind: 'empty' }] },
            { name: 'Upstream', kind: 'us', children: usChildren.length ? usChildren : [{ name: 'No US channels', kind: 'empty' }] },
            { name: 'Cable Modems (' + g.modemCount + ')', kind: 'modem', children: modemChildren.length ? modemChildren : [{ name: 'No modems', kind: 'empty' }] }
          ]
        };
      })
    };
  }

  const groups = Array.isArray(response && response.groups) ? response.groups : [];
  const mapped = bucketChannels(groups);
  const tree = buildTree(mapped);

  const template = `
  <style>
    body { background:#141821; color:#e7edf8; font-family:Arial,sans-serif; margin:0; padding:16px; }
    .wrap { max-width:1600px; margin:0 auto; display:grid; gap:12px; }
    .card { background:#1b2332; border:1px solid rgba(255,255,255,0.09); border-radius:10px; padding:14px; }
    .title { margin:0 0 8px 0; color:#f3f6ff; text-align:center; font-size:20px; font-weight:700; }
    .meta { color:#dbe3ff; font-size:12px; text-align:center; }
    .kpis { display:grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap:10px; margin-top:10px; }
    .kpi { background:#202938; border:1px solid rgba(255,255,255,0.10); border-radius:8px; padding:8px; }
    .kpi .label { font-size:11px; color:#dbe3ff; }
    .kpi .value { font-size:14px; color:#f3f6ff; font-weight:700; margin-top:4px; }

    .tree-wrap { border:1px solid rgba(255,255,255,0.10); border-radius:8px; overflow:auto; background:#202938; }
    .tree-head { color:#9ec0ff; font-size:14px; font-weight:700; margin-bottom:8px; }
    .tree-note { color:#dbe3ff; font-size:12px; margin-bottom:8px; }

    .sg-grid { display:grid; grid-template-columns:1fr; gap:12px; }
    .sg-title { margin:0 0 8px 0; color:#9ec0ff; font-size:17px; font-weight:700; }
    .sg-meta { color:#dbe3ff; font-size:12px; margin-bottom:10px; }

    .tbl-wrap { margin-top:10px; border:1px solid rgba(255,255,255,0.10); border-radius:8px; overflow:auto; }
    table { width:100%; border-collapse:collapse; min-width:860px; }
    th, td { padding:8px 10px; border-bottom:1px solid rgba(255,255,255,0.10); font-size:12px; text-align:left; }
    th { background:#202938; color:#dbe3ff; }
    td { color:#f3f6ff; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }

    .empty { color:#dbe3ff; font-size:12px; padding:8px 0; }

    .tree-svg .link { fill:none; stroke:rgba(255,255,255,0.20); stroke-width:1.2px; }
    .tree-svg .node circle { stroke-width:1.5px; }
    .tree-svg .node text { font-size:12px; fill:#e7edf8; }
    .tree-svg .node .sub { font-size:10px; fill:#dbe3ff; }

    @media (max-width:1100px) {
      .kpis { grid-template-columns: repeat(2, minmax(0,1fr)); }
    }
  </style>

  <div class="wrap">
    <div class="card">
      <h1 class="title">Serving Group Operations Get Topology</h1>
      <div class="meta">POST /cmts/servingGroup/operations/get/topology · Capture Time: {{captureTime}}</div>
      <div class="kpis">
        <div class="kpi"><div class="label">Status</div><div class="value">{{status}}</div></div>
        <div class="kpi"><div class="label">Resolved SG IDs</div><div class="value">{{resolvedCount}}</div></div>
        <div class="kpi"><div class="label">Missing SG IDs</div><div class="value">{{missingCount}}</div></div>
        <div class="kpi"><div class="label">Groups</div><div class="value">{{groupCount}}</div></div>
      </div>
    </div>

    <div class="card">
      <div class="tree-head">Graphical Topology</div>
      <div class="tree-note">Click nodes to collapse/expand branches.</div>
      <div id="topologyTree" class="tree-wrap"></div>
    </div>

    <div class="sg-grid" id="sgRoot"></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <script>
    (function () {
      const groups = {{{groupsJson}}};
      const treeData = {{{treeJson}}};
      const root = document.getElementById('sgRoot');
      if (!root || !Array.isArray(groups)) return;

      function renderTree(data) {
        const host = document.getElementById('topologyTree');
        if (!host || !window.d3 || !data) return;
        host.innerHTML = '';

        const d3 = window.d3;
        const width = Math.max(1200, host.clientWidth || 1200);
        const dx = 22;
        const dy = 220;
        const tree = d3.tree().nodeSize([dx, dy]);
        const diagonal = d3.linkHorizontal().x(function (d) { return d.y; }).y(function (d) { return d.x; });

        const root = d3.hierarchy(data);
        root.x0 = dx;
        root.y0 = 0;
        let i = 0;

        root.descendants().forEach(function (d) {
          d.id = i++;
          d._children = d.children;
          if (d.depth > 1) d.children = null;
        });

        const svg = d3.create('svg')
          .attr('class', 'tree-svg')
          .attr('width', width)
          .attr('height', dx)
          .attr('viewBox', [-40, -20, width, dx])
          .style('font', '12px Arial');

        const gLink = svg.append('g').attr('fill', 'none').attr('stroke', 'rgba(255,255,255,0.2)').attr('stroke-opacity', 1).attr('stroke-width', 1.2);
        const gNode = svg.append('g').attr('cursor', 'pointer').attr('pointer-events', 'all');

        function nodeColor(kind) {
          if (kind === 'ds') return '#5a6fd8';
          if (kind === 'us') return '#39c28e';
          if (kind === 'modem') return '#f1c40f';
          if (kind === 'sg') return '#9ec0ff';
          if (kind === 'root') return '#c62828';
          return '#94a3b8';
        }

        function update(source) {
          const duration = 220;
          const nodes = root.descendants().reverse();
          const links = root.links();
          tree(root);

          let left = root;
          let right = root;
          root.eachBefore(function (node) {
            if (node.x < left.x) left = node;
            if (node.x > right.x) right = node;
          });

          const height = right.x - left.x + dx * 2;

          const transition = svg.transition().duration(duration)
            .attr('height', height)
            .attr('viewBox', [-40, left.x - dx, width, height]);

          const node = gNode.selectAll('g').data(nodes, function (d) { return d.id; });

          const nodeEnter = node.enter().append('g')
            .attr('transform', function () { return 'translate(' + source.y0 + ',' + source.x0 + ')'; })
            .attr('fill-opacity', 0)
            .attr('stroke-opacity', 0)
            .on('click', function (event, d) {
              d.children = d.children ? null : d._children;
              update(d);
            });

          nodeEnter.append('circle')
            .attr('r', 5)
            .attr('fill', function (d) { return d._children ? nodeColor(d.data.kind) : '#1b2332'; })
            .attr('stroke', function (d) { return nodeColor(d.data.kind); });

          nodeEnter.append('text')
            .attr('dy', '0.31em')
            .attr('x', function (d) { return d._children ? -10 : 10; })
            .attr('text-anchor', function (d) { return d._children ? 'end' : 'start'; })
            .text(function (d) {
              const name = d && d.data && d.data.name ? String(d.data.name) : 'N/A';
              const subtitle = d && d.data && d.data.subtitle ? String(d.data.subtitle) : '';
              return subtitle ? (name + ' · ' + subtitle) : name;
            });

          const nodeUpdate = node.merge(nodeEnter).transition(transition)
            .attr('transform', function (d) { return 'translate(' + d.y + ',' + d.x + ')'; })
            .attr('fill-opacity', 1)
            .attr('stroke-opacity', 1);

          node.merge(nodeEnter).select('circle')
            .attr('fill', function (d) { return d._children ? nodeColor(d.data.kind) : '#1b2332'; })
            .attr('stroke', function (d) { return nodeColor(d.data.kind); });

          node.exit().transition(transition).remove()
            .attr('transform', function () { return 'translate(' + source.y + ',' + source.x + ')'; })
            .attr('fill-opacity', 0)
            .attr('stroke-opacity', 0);

          const link = gLink.selectAll('path').data(links, function (d) { return d.target.id; });

          const linkEnter = link.enter().append('path')
            .attr('d', function () {
              const o = { x: source.x0, y: source.y0 };
              return diagonal({ source: o, target: o });
            });

          link.merge(linkEnter).transition(transition).attr('d', diagonal);

          link.exit().transition(transition).remove().attr('d', function () {
            const o = { x: source.x, y: source.y };
            return diagonal({ source: o, target: o });
          });

          root.eachBefore(function (d) {
            d.x0 = d.x;
            d.y0 = d.y;
          });
        }

        update(root);
        host.appendChild(svg.node());
      }

      renderTree(treeData);

      groups.forEach(function (g) {
        const card = document.createElement('section');
        card.className = 'card';
        card.innerHTML = '' +
          '<h2 class="sg-title">Serving Group ' + g.sgId + '</h2>' +
          '<div class="sg-meta">DS Set: ' + g.dsChSetId + ' · US Set: ' + g.usChSetId + ' · Modems: ' + g.modemCount + ' · Success: ' + g.successCount + ' · Failure: ' + g.failureCount + '</div>';

        const tableWrap = document.createElement('div');
        tableWrap.className = 'tbl-wrap';
        tableWrap.innerHTML = '' +
          '<table>' +
            '<thead><tr><th>MacAddress</th><th>Model</th><th>Vendor</th><th>SW Version</th><th>HW Version</th><th>Boot ROM</th></tr></thead>' +
            '<tbody>' +
              (g.modemRows.length
                ? g.modemRows.map(function (m) {
                    return '<tr>' +
                      '<td class="mono">' + m.mac + '</td>' +
                      '<td>' + m.model + '</td>' +
                      '<td>' + m.vendor + '</td>' +
                      '<td class="mono">' + m.sw + '</td>' +
                      '<td class="mono">' + m.hw + '</td>' +
                      '<td class="mono">' + m.bootr + '</td>' +
                    '</tr>';
                  }).join('')
                : '<tr><td colspan="6">No cable modems in response</td></tr>') +
            '</tbody>' +
          '</table>';

        card.appendChild(tableWrap);
        root.appendChild(card);
      });
    })();
  </script>
  `;

  pm.visualizer.set(template, {
    status: response && response.status !== undefined ? String(response.status) : 'N/A',
    captureTime: fmtUtc(response && response.timestamp),
    resolvedCount: Array.isArray(response && response.resolved_sg_ids) ? response.resolved_sg_ids.length : 0,
    missingCount: Array.isArray(response && response.missing_sg_ids) ? response.missing_sg_ids.length : 0,
    groupCount: mapped.length,
    groupsJson: JSON.stringify(mapped),
    treeJson: JSON.stringify(tree)
  });
})();
````
</details>

<details>
<summary>Sample JSON payload</summary>

````json
{
  "status": 0,
  "message": "",
  "timestamp": 1773023407,
  "requested_sg_ids": [],
  "resolved_sg_ids": [
    1
  ],
  "missing_sg_ids": [],
  "groups": [
    {
      "sg_id": 1,
      "ds_ch_set_id": 256,
      "us_ch_set_id": 256,
      "channels": {
        "ds": {
          "sc_qam": [
            {
              "channel_id": 1,
              "channel_type": "sc_qam",
              "center_frequency_hz": 519000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 516000000,
              "upper_frequency_hz": 522000000
            },
            {
              "channel_id": 2,
              "channel_type": "sc_qam",
              "center_frequency_hz": 525000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 522000000,
              "upper_frequency_hz": 528000000
            },
            {
              "channel_id": 3,
              "channel_type": "sc_qam",
              "center_frequency_hz": 531000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 528000000,
              "upper_frequency_hz": 534000000
            },
            {
              "channel_id": 4,
              "channel_type": "sc_qam",
              "center_frequency_hz": 537000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 534000000,
              "upper_frequency_hz": 540000000
            },
            {
              "channel_id": 5,
              "channel_type": "sc_qam",
              "center_frequency_hz": 543000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 540000000,
              "upper_frequency_hz": 546000000
            },
            {
              "channel_id": 6,
              "channel_type": "sc_qam",
              "center_frequency_hz": 549000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 546000000,
              "upper_frequency_hz": 552000000
            },
            {
              "channel_id": 7,
              "channel_type": "sc_qam",
              "center_frequency_hz": 555000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 552000000,
              "upper_frequency_hz": 558000000
            },
            {
              "channel_id": 8,
              "channel_type": "sc_qam",
              "center_frequency_hz": 561000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 558000000,
              "upper_frequency_hz": 564000000
            },
            {
              "channel_id": 9,
              "channel_type": "sc_qam",
              "center_frequency_hz": 567000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 564000000,
              "upper_frequency_hz": 570000000
            },
            {
              "channel_id": 10,
              "channel_type": "sc_qam",
              "center_frequency_hz": 573000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 570000000,
              "upper_frequency_hz": 576000000
            },
            {
              "channel_id": 11,
              "channel_type": "sc_qam",
              "center_frequency_hz": 579000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 576000000,
              "upper_frequency_hz": 582000000
            },
            {
              "channel_id": 12,
              "channel_type": "sc_qam",
              "center_frequency_hz": 585000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 582000000,
              "upper_frequency_hz": 588000000
            },
            {
              "channel_id": 13,
              "channel_type": "sc_qam",
              "center_frequency_hz": 591000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 588000000,
              "upper_frequency_hz": 594000000
            },
            {
              "channel_id": 14,
              "channel_type": "sc_qam",
              "center_frequency_hz": 597000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 594000000,
              "upper_frequency_hz": 600000000
            },
            {
              "channel_id": 15,
              "channel_type": "sc_qam",
              "center_frequency_hz": 603000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 600000000,
              "upper_frequency_hz": 606000000
            },
            {
              "channel_id": 16,
              "channel_type": "sc_qam",
              "center_frequency_hz": 609000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 606000000,
              "upper_frequency_hz": 612000000
            },
            {
              "channel_id": 17,
              "channel_type": "sc_qam",
              "center_frequency_hz": 615000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 612000000,
              "upper_frequency_hz": 618000000
            },
            {
              "channel_id": 18,
              "channel_type": "sc_qam",
              "center_frequency_hz": 621000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 618000000,
              "upper_frequency_hz": 624000000
            },
            {
              "channel_id": 19,
              "channel_type": "sc_qam",
              "center_frequency_hz": 627000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 624000000,
              "upper_frequency_hz": 630000000
            },
            {
              "channel_id": 20,
              "channel_type": "sc_qam",
              "center_frequency_hz": 633000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 630000000,
              "upper_frequency_hz": 636000000
            },
            {
              "channel_id": 21,
              "channel_type": "sc_qam",
              "center_frequency_hz": 639000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 636000000,
              "upper_frequency_hz": 642000000
            },
            {
              "channel_id": 22,
              "channel_type": "sc_qam",
              "center_frequency_hz": 645000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 642000000,
              "upper_frequency_hz": 648000000
            },
            {
              "channel_id": 23,
              "channel_type": "sc_qam",
              "center_frequency_hz": 651000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 648000000,
              "upper_frequency_hz": 654000000
            },
            {
              "channel_id": 24,
              "channel_type": "sc_qam",
              "center_frequency_hz": 657000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 654000000,
              "upper_frequency_hz": 660000000
            },
            {
              "channel_id": 25,
              "channel_type": "sc_qam",
              "center_frequency_hz": 663000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 660000000,
              "upper_frequency_hz": 666000000
            },
            {
              "channel_id": 26,
              "channel_type": "sc_qam",
              "center_frequency_hz": 669000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 666000000,
              "upper_frequency_hz": 672000000
            },
            {
              "channel_id": 27,
              "channel_type": "sc_qam",
              "center_frequency_hz": 675000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 672000000,
              "upper_frequency_hz": 678000000
            },
            {
              "channel_id": 28,
              "channel_type": "sc_qam",
              "center_frequency_hz": 681000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 678000000,
              "upper_frequency_hz": 684000000
            },
            {
              "channel_id": 29,
              "channel_type": "sc_qam",
              "center_frequency_hz": 687000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 684000000,
              "upper_frequency_hz": 690000000
            },
            {
              "channel_id": 30,
              "channel_type": "sc_qam",
              "center_frequency_hz": 693000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 690000000,
              "upper_frequency_hz": 696000000
            },
            {
              "channel_id": 31,
              "channel_type": "sc_qam",
              "center_frequency_hz": 699000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 696000000,
              "upper_frequency_hz": 702000000
            },
            {
              "channel_id": 32,
              "channel_type": "sc_qam",
              "center_frequency_hz": 705000000,
              "channel_width_hz": 6000000,
              "lower_frequency_hz": 702000000,
              "upper_frequency_hz": 708000000
            }
          ],
          "ofdm": [
            {
              "channel_id": 33,
              "channel_type": "ofdm",
              "plc_frequency_hz": 725800000,
              "channel_width_hz": 206700000,
              "lower_frequency_hz": 693250000,
              "upper_frequency_hz": 899950000
            },
            {
              "channel_id": 34,
              "channel_type": "ofdm",
              "plc_frequency_hz": 497800000,
              "channel_width_hz": 206700000,
              "lower_frequency_hz": 297250000,
              "upper_frequency_hz": 503950000
            }
          ],
          "counts": [
            {
              "channel_id": 1,
              "modem_count": 0
            },
            {
              "channel_id": 2,
              "modem_count": 0
            },
            {
              "channel_id": 3,
              "modem_count": 0
            },
            {
              "channel_id": 4,
              "modem_count": 0
            },
            {
              "channel_id": 5,
              "modem_count": 0
            },
            {
              "channel_id": 6,
              "modem_count": 0
            },
            {
              "channel_id": 7,
              "modem_count": 0
            },
            {
              "channel_id": 8,
              "modem_count": 0
            },
            {
              "channel_id": 9,
              "modem_count": 0
            },
            {
              "channel_id": 10,
              "modem_count": 0
            },
            {
              "channel_id": 11,
              "modem_count": 0
            },
            {
              "channel_id": 12,
              "modem_count": 0
            },
            {
              "channel_id": 13,
              "modem_count": 0
            },
            {
              "channel_id": 14,
              "modem_count": 0
            },
            {
              "channel_id": 15,
              "modem_count": 0
            },
            {
              "channel_id": 16,
              "modem_count": 0
            },
            {
              "channel_id": 17,
              "modem_count": 0
            },
            {
              "channel_id": 18,
              "modem_count": 0
            },
            {
              "channel_id": 19,
              "modem_count": 0
            },
            {
              "channel_id": 20,
              "modem_count": 0
            },
            {
              "channel_id": 21,
              "modem_count": 0
            },
            {
              "channel_id": 22,
              "modem_count": 0
            },
            {
              "channel_id": 23,
              "modem_count": 0
            },
            {
              "channel_id": 24,
              "modem_count": 0
            },
            {
              "channel_id": 25,
              "modem_count": 0
            },
            {
              "channel_id": 26,
              "modem_count": 0
            },
            {
              "channel_id": 27,
              "modem_count": 0
            },
            {
              "channel_id": 28,
              "modem_count": 0
            },
            {
              "channel_id": 29,
              "modem_count": 0
            },
            {
              "channel_id": 30,
              "modem_count": 0
            },
            {
              "channel_id": 31,
              "modem_count": 0
            },
            {
              "channel_id": 32,
              "modem_count": 0
            },
            {
              "channel_id": 33,
              "modem_count": 0
            },
            {
              "channel_id": 34,
              "modem_count": 0
            }
          ],
          "set_counts": [
            {
              "ch_set_id": 16777217,
              "modem_count": 21
            },
            {
              "ch_set_id": 16777220,
              "modem_count": 1
            },
            {
              "ch_set_id": 16777222,
              "modem_count": 1
            }
          ]
        },
        "us": {
          "sc_qam": [
            {
              "channel_id": 1,
              "channel_type": "sc_qam",
              "center_frequency_hz": 17200000,
              "channel_width_hz": 6400000,
              "lower_frequency_hz": 14000000,
              "upper_frequency_hz": 20400000
            },
            {
              "channel_id": 2,
              "channel_type": "sc_qam",
              "center_frequency_hz": 23600000,
              "channel_width_hz": 6400000,
              "lower_frequency_hz": 20400000,
              "upper_frequency_hz": 26800000
            },
            {
              "channel_id": 3,
              "channel_type": "sc_qam",
              "center_frequency_hz": 30000000,
              "channel_width_hz": 6400000,
              "lower_frequency_hz": 26800000,
              "upper_frequency_hz": 33200000
            },
            {
              "channel_id": 4,
              "channel_type": "sc_qam",
              "center_frequency_hz": 36400000,
              "channel_width_hz": 6400000,
              "lower_frequency_hz": 33200000,
              "upper_frequency_hz": 39600000
            }
          ],
          "ofdma": [
            {
              "channel_id": 25,
              "channel_type": "ofdma",
              "channel_width_hz": 43000000,
              "lower_frequency_hz": 42000000,
              "upper_frequency_hz": 85000000
            },
            {
              "channel_id": 26,
              "channel_type": "ofdma",
              "channel_width_hz": 95000000,
              "lower_frequency_hz": 108000000,
              "upper_frequency_hz": 203000000
            }
          ],
          "counts": [
            {
              "channel_id": 1,
              "modem_count": 0
            },
            {
              "channel_id": 2,
              "modem_count": 0
            },
            {
              "channel_id": 3,
              "modem_count": 0
            },
            {
              "channel_id": 4,
              "modem_count": 0
            },
            {
              "channel_id": 25,
              "modem_count": 0
            },
            {
              "channel_id": 26,
              "modem_count": 0
            }
          ],
          "set_counts": [
            {
              "ch_set_id": 16777217,
              "modem_count": 10
            },
            {
              "ch_set_id": 16777218,
              "modem_count": 12
            },
            {
              "ch_set_id": 16777219,
              "modem_count": 1
            }
          ]
        }
      },
      "modem_count": 23,
      "success_count": 23,
      "failure_count": 0,
      "modems": {
        "1c:ab:c0:9d:d6:00": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "mango-1.6.5-ge4b629a1",
            "SW_REV": "4.5.11.26b1",
            "MODEL": "CGNM-SHW",
            "is_empty": false
          }
        },
        "20:6a:94:34:63:f4": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.727888.R.2304181116",
            "SW_REV": "7.3.5.3.3b2",
            "MODEL": "EN2251-RES",
            "is_empty": false
          }
        },
        "20:6a:94:d7:d3:60": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGR2.86C.610248.R.2210181404",
            "SW_REV": "7.3.5.3.1b5",
            "MODEL": "CODA5814Q",
            "is_empty": false
          }
        },
        "38:ad:2b:3e:86:54": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "2022.01-MXL-v-4.0.357",
            "SW_REV": "8.4.0.0.1b2",
            "MODEL": "CODA60",
            "is_empty": false
          }
        },
        "38:ad:2b:3e:87:7c": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "2022.01-MXL-v-4.0.369.F",
            "SW_REV": "8.5.0.0.5b4",
            "MODEL": "CODA60V",
            "is_empty": false
          }
        },
        "60:6c:63:f4:64:f8": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.727888.R.2305250917.F",
            "SW_REV": "7.3.5.3.2b1",
            "MODEL": "CODA56",
            "is_empty": false
          }
        },
        "74:9b:e8:72:7a:54": {
          "sysdescr": {
            "HW_REV": "0.65",
            "VENDOR": "Hitron Technologies Inc.",
            "BOOTR": "NONE",
            "SW_REV": "7.2.4.0.3.b5",
            "MODEL": "ODIN-1112",
            "is_empty": false
          }
        },
        "84:0b:7c:0b:e5:48": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.727889.R.2402291559.F",
            "SW_REV": "7.3.5.3U8-UNI-CTR",
            "MODEL": "EN2251",
            "is_empty": false
          }
        },
        "90:aa:c3:4b:75:60": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.668728.R.2407251438",
            "SW_REV": "7.3.5.3.1b5",
            "MODEL": "CODA-4589-RES",
            "is_empty": false
          }
        },
        "90:aa:c3:8a:bd:18": {
          "sysdescr": {
            "HW_REV": "2A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.727888.R.2305251031.F",
            "SW_REV": "7.3.5.3.2b2",
            "MODEL": "CODA",
            "is_empty": false
          }
        },
        "90:aa:c3:c9:d0:d0": {
          "sysdescr": {
            "HW_REV": "0A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.635901.R.2008260951",
            "SW_REV": "7.2.4.5.1b6",
            "MODEL": "CGNDP3M",
            "is_empty": false
          }
        },
        "b0:f5:30:b7:76:30": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "2022.01-MXL-v-4.0.369",
            "SW_REV": "8.5.0.0.1b5",
            "MODEL": "CODA6021U",
            "is_empty": false
          }
        },
        "dc:36:0c:79:e0:36": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.727888.R.2305250917.F",
            "SW_REV": "7.3.5.3.2b1",
            "MODEL": "CODA56",
            "is_empty": false
          }
        },
        "dc:36:0c:79:f1:8c": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.727888.R.2304140934.F",
            "SW_REV": "7.3.5.3.2b1",
            "MODEL": "CODA56",
            "is_empty": false
          }
        },
        "dc:36:0c:ee:ce:e0": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGR2.86C.703059.R.2405091611",
            "SW_REV": "7.3.5.3.1b5",
            "MODEL": "CODA5834",
            "is_empty": false
          }
        },
        "f8:1d:0f:cd:a0:f0": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.597968.R.1811011626",
            "SW_REV": "7.1.1.2.5b3",
            "MODEL": "CODA-4589-RES",
            "is_empty": false
          }
        },
        "f8:34:5a:53:27:48": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.727888.R.2304181538.F",
            "SW_REV": "7.3.5.3.2b3",
            "MODEL": "CODA-57-RES",
            "is_empty": false
          }
        },
        "f8:34:5a:7f:d6:80": {
          "sysdescr": {
            "HW_REV": "1C",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGR2.86C.668728.R.2206081646",
            "SW_REV": "7.3.5.3.1b5",
            "MODEL": "CODA-5810",
            "is_empty": false
          }
        },
        "f8:34:5a:80:84:12": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.727888.R.2304181538",
            "SW_REV": "7.3.5.3.2b3",
            "MODEL": "CODA-56-RES",
            "is_empty": false
          }
        },
        "f8:34:5a:83:35:34": {
          "sysdescr": {
            "HW_REV": "2A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.727888.R.2304181116",
            "SW_REV": "7.3.5.3.3b2",
            "MODEL": "EN2251-HSP",
            "is_empty": false
          }
        },
        "fc:77:7b:11:8f:da": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.727888.R.2304181538",
            "SW_REV": "7.3.5.3.3b2",
            "MODEL": "CODA-57-RES",
            "is_empty": false
          }
        },
        "fc:77:7b:ca:7b:10": {
          "sysdescr": {
            "HW_REV": "2A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGM2.86C.635901.R.2008260951",
            "SW_REV": "7.2.4.5.1b8",
            "MODEL": "CGNDP3M",
            "is_empty": false
          }
        },
        "fc:77:7b:cc:04:b0": {
          "sysdescr": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "CGR2.86C.610248.R.2210181404",
            "SW_REV": "7.3.5.3.1b3",
            "MODEL": "CODA5610Q",
            "is_empty": false
          }
        }
      },
      "metadata": {
        "snapshot_time_epoch": 1773023367.02929,
        "age_seconds": 40.27694034576416,
        "last_heavy_refresh_epoch": 1773023367.02929,
        "last_light_refresh_epoch": 1773023367.02929,
        "refresh_state": "OK",
        "last_error": null
      }
    }
  ]
}
````
</details>
