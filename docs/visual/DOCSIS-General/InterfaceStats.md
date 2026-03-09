# PyPNM / DOCSIS-General / InterfaceStats

## Source Files

- HTML/script: `visual/PyPNM/DOCSIS-General/InterfaceStats.html`
- JSON sample: `visual/PyPNM/DOCSIS-General/InterfaceStats.json`

## Preview

<iframe src="../../../visual-previews/DOCSIS-General/InterfaceStats.html" style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>

Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed.

<details>
<summary>Visualizer HTML/script source</summary>

````html
// Postman Visualizer: DOCSIS-General/InterfaceStats
// Last Update: 2026-03-09 10:20:00 MST
// Visual Constraints: Follow canonical visual rules in CODING_AGENTS.md.

(function () {
  const response = pm.response.json() || {};

  function safeText(v) {
    if (v === undefined || v === null) return 'N/A';
    const s = String(v).trim();
    return s ? s : 'N/A';
  }

  function n(v) {
    const x = Number(v);
    return Number.isFinite(x) ? x : null;
  }

  function sanitizeMac(value) {
    const raw = safeText(value);
    if (raw === 'N/A') return raw;
    const compact = raw.replace(/[^0-9a-f]/gi, '').toLowerCase();
    if (compact.length !== 12) return raw.toLowerCase();
    return compact.match(/.{1,2}/g).join(':');
  }

  function adminOper(v) {
    const x = n(v);
    if (x === 1) return 'up';
    if (x === 2) return 'down';
    if (x === 3) return 'testing';
    return 'unknown';
  }

  function fmtInt(v) {
    const x = n(v);
    if (x === null) return 'N/A';
    return Math.trunc(x).toLocaleString('en-US');
  }

  function fmtBps(v) {
    const x = n(v);
    if (x === null || x <= 0) return 'N/A';
    if (x >= 1e9) return (x / 1e9).toFixed(2) + ' Gbps';
    if (x >= 1e6) return (x / 1e6).toFixed(2) + ' Mbps';
    if (x >= 1e3) return (x / 1e3).toFixed(2) + ' Kbps';
    return String(Math.round(x)) + ' bps';
  }

  function normalizeItem(item) {
    const ife = item && item.ifEntry && typeof item.ifEntry === 'object' ? item.ifEntry : {};
    const ifx = item && item.ifXEntry && typeof item.ifXEntry === 'object' ? item.ifXEntry : {};
    return {
      ifIndex: safeText(ife.ifIndex),
      ifName: safeText(ifx.ifName),
      ifDescr: safeText(ife.ifDescr),
      ifType: safeText(ife.ifType),
      admin: adminOper(ife.ifAdminStatus),
      oper: adminOper(ife.ifOperStatus),
      speedBps: n(ife.ifSpeed),
      highSpeedMbps: n(ifx.ifHighSpeed),
      inOctets: n(ifx.ifHCInOctets) !== null ? n(ifx.ifHCInOctets) : n(ife.ifInOctets),
      outOctets: n(ifx.ifHCOutOctets) !== null ? n(ifx.ifHCOutOctets) : n(ife.ifOutOctets)
    };
  }

  function classifyGroup(key) {
    const k = String(key || '').toLowerCase();
    if (k.includes('downstream')) return { direction: 'DS', color: 'ds' };
    if (k.includes('upstream')) return { direction: 'US', color: 'us' };
    if (k.includes('maclayer')) return { direction: 'MAC', color: 'mac' };
    return { direction: 'GEN', color: 'gen' };
  }

  function titleForKey(key) {
    const map = {
      docsCableMaclayer: 'DOCSIS MAC Layer',
      docsOfdmDownstream: 'OFDM Downstream',
      docsCableDownstream: 'SCQAM Downstream',
      docsOfdmaUpstream: 'OFDMA Upstream',
      docsCableUpstream: 'SCQAM Upstream'
    };
    return map[key] || key;
  }

  const results = response && typeof response.results === 'object' ? response.results : {};
  const groups = Object.keys(results)
    .filter((k) => Array.isArray(results[k]))
    .map((key) => {
      const rows = results[key].map(normalizeItem);
      const upCount = rows.filter((r) => r.oper === 'up').length;
      const downCount = rows.filter((r) => r.oper === 'down').length;
      let inOctets = 0;
      let outOctets = 0;
      let maxSpeed = 0;
      rows.forEach((r) => {
        if (r.inOctets !== null) inOctets += r.inOctets;
        if (r.outOctets !== null) outOctets += r.outOctets;
        if (r.speedBps !== null && r.speedBps > maxSpeed) maxSpeed = r.speedBps;
      });
      const cls = classifyGroup(key);
      return {
        key,
        title: titleForKey(key),
        direction: cls.direction,
        color: cls.color,
        rows,
        count: rows.length,
        upCount,
        downCount,
        inOctets,
        outOctets,
        maxSpeed
      };
    })
    .filter((g) => g.count > 0)
    .sort((a, b) => a.title.localeCompare(b.title));

  const totalInterfaces = groups.reduce((s, g) => s + g.count, 0);
  const totalUp = groups.reduce((s, g) => s + g.upCount, 0);
  const totalDown = groups.reduce((s, g) => s + g.downCount, 0);

  const device = response && typeof response.device === 'object' ? response.device : {};
  const sys = device && typeof device.system_description === 'object' ? device.system_description : {};
  const deviceInfo = {
    macAddress: sanitizeMac(device.mac_address),
    model: safeText(sys.MODEL),
    vendor: safeText(sys.VENDOR),
    swVersion: safeText(sys.SW_REV),
    hwVersion: safeText(sys.HW_REV),
    bootRom: safeText(sys.BOOTR)
  };

  function buildTreeData() {
    return {
      name: 'Device ' + deviceInfo.macAddress,
      subtitle: 'DOCSIS Interface Stats',
      kind: 'root',
      children: groups.map((g) => ({
        name: g.direction + ' ' + g.title,
        subtitle: 'Interfaces (' + g.count + ') · Up (' + g.upCount + ') · Down (' + g.downCount + ')',
        kind: g.color,
        children: g.rows.slice(0, 150).map((r) => ({
          name: 'if' + r.ifIndex + ' ' + r.ifName,
          subtitle: r.ifDescr + ' · ' + safeText(r.oper) + ' · ' + fmtBps(r.speedBps),
          kind: r.oper === 'up' ? 'ok' : (r.oper === 'down' ? 'nok' : 'gen')
        }))
      }))
    };
  }

  const treeData = buildTreeData();

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

    .device-title { margin:0 0 8px 0; font-size:16px; color:#9ec0ff; font-weight:700; }
    .tbl-wrap { border:1px solid rgba(255,255,255,0.10); border-radius:8px; overflow:auto; }
    table { width:100%; border-collapse:collapse; min-width:860px; }
    th, td { padding:8px 10px; border-bottom:1px solid rgba(255,255,255,0.10); font-size:12px; text-align:left; }
    th { background:#202938; color:#dbe3ff; }
    td { color:#f3f6ff; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }

    .tree-head { color:#9ec0ff; font-size:14px; font-weight:700; margin-bottom:8px; }
    .tree-note { color:#dbe3ff; font-size:12px; margin-bottom:8px; }
    .tree-wrap { border:1px solid rgba(255,255,255,0.10); border-radius:8px; overflow:auto; background:#202938; }

    .group-title { margin:0 0 8px 0; color:#9ec0ff; font-size:16px; font-weight:700; }
    .group-title.ds { color:#5a6fd8; }
    .group-title.us { color:#39c28e; }
    .group-title.mac { color:#f1c40f; }

    .tree-svg .node text { font-size:12px; fill:#e7edf8; }

    @media (max-width:1100px) {
      .kpis { grid-template-columns: repeat(2, minmax(0,1fr)); }
    }
  </style>

  <div class="wrap">
    <div class="card">
      <h1 class="title">DOCSIS Interface Stats</h1>
      <div class="meta">Status: {{status}} · {{message}}</div>
      <div class="kpis">
        <div class="kpi"><div class="label">Interface Groups</div><div class="value">{{groupCount}}</div></div>
        <div class="kpi"><div class="label">Interfaces</div><div class="value">{{totalInterfaces}}</div></div>
        <div class="kpi"><div class="label">Oper Up</div><div class="value">{{totalUp}}</div></div>
        <div class="kpi"><div class="label">Oper Down</div><div class="value">{{totalDown}}</div></div>
      </div>
    </div>

    <div class="card">
      <h2 class="device-title">Device Info</h2>
      <div class="tbl-wrap">
        <table>
          <thead>
            <tr><th>MacAddress</th><th>Model</th><th>Vendor</th><th>SW Version</th><th>HW Version</th><th>Boot ROM</th></tr>
          </thead>
          <tbody>
            <tr>
              <td class="mono">{{deviceInfo.macAddress}}</td>
              <td>{{deviceInfo.model}}</td>
              <td>{{deviceInfo.vendor}}</td>
              <td class="mono">{{deviceInfo.swVersion}}</td>
              <td class="mono">{{deviceInfo.hwVersion}}</td>
              <td class="mono">{{deviceInfo.bootRom}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card">
      <div class="tree-head">Graphical Topology</div>
      <div class="tree-note">Click nodes to collapse or expand branches.</div>
      <div id="topologyTree" class="tree-wrap"></div>
    </div>

    <div class="card">
      <h2 class="device-title">Group Summary</h2>
      <div class="tbl-wrap">
        <table>
          <thead>
            <tr><th>Group</th><th>Direction</th><th>Interfaces</th><th>Up</th><th>Down</th><th>In Octets</th><th>Out Octets</th><th>Max Speed</th></tr>
          </thead>
          <tbody id="summaryRows"></tbody>
        </table>
      </div>
    </div>

    <div id="groupTables"></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <script>
    (function () {
      const treeData = {{{treeJson}}};
      const groups = {{{groupsJson}}};

      const summaryRoot = document.getElementById('summaryRows');
      const groupRoot = document.getElementById('groupTables');

      function esc(v) {
        if (v === undefined || v === null) return 'N/A';
        return String(v)
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;')
          .replace(/'/g, '&#039;');
      }

      function nodeColor(kind) {
        if (kind === 'ds') return '#5a6fd8';
        if (kind === 'us') return '#39c28e';
        if (kind === 'mac') return '#f1c40f';
        if (kind === 'ok') return '#39c28e';
        if (kind === 'nok') return '#c62828';
        if (kind === 'root') return '#9ec0ff';
        return '#94a3b8';
      }

      function renderTree(data) {
        const host = document.getElementById('topologyTree');
        if (!host || !window.d3 || !data) return;
        host.innerHTML = '';

        const d3 = window.d3;
        const width = Math.max(1300, host.clientWidth || 1300);
        const dx = 22;
        const dy = 260;
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

        const gLink = svg.append('g').attr('fill', 'none').attr('stroke', 'rgba(255,255,255,0.20)').attr('stroke-width', 1.2);
        const gNode = svg.append('g').attr('cursor', 'pointer').attr('pointer-events', 'all');

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
            .attr('stroke', function (d) { return nodeColor(d.data.kind); })
            .attr('stroke-width', 1.5);

          nodeEnter.append('text')
            .attr('dy', '0.31em')
            .attr('x', function (d) { return d._children ? -10 : 10; })
            .attr('text-anchor', function (d) { return d._children ? 'end' : 'start'; })
            .text(function (d) {
              const name = d && d.data && d.data.name ? String(d.data.name) : 'N/A';
              const subtitle = d && d.data && d.data.subtitle ? String(d.data.subtitle) : '';
              return subtitle ? (name + ' · ' + subtitle) : name;
            });

          node.merge(nodeEnter).transition(transition)
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

      if (summaryRoot && Array.isArray(groups)) {
        summaryRoot.innerHTML = groups.map(function (g) {
          return '<tr>' +
            '<td>' + esc(g.title) + '</td>' +
            '<td>' + esc(g.direction) + '</td>' +
            '<td>' + esc(g.count) + '</td>' +
            '<td>' + esc(g.upCount) + '</td>' +
            '<td>' + esc(g.downCount) + '</td>' +
            '<td class="mono">' + esc(g.inOctetsFmt) + '</td>' +
            '<td class="mono">' + esc(g.outOctetsFmt) + '</td>' +
            '<td>' + esc(g.maxSpeedFmt) + '</td>' +
          '</tr>';
        }).join('');
      }

      if (groupRoot && Array.isArray(groups)) {
        groupRoot.innerHTML = groups.map(function (g) {
          return '<section class="card">' +
            '<h2 class="group-title ' + esc(g.color) + '">' + esc(g.title) + ' · Interfaces (' + esc(g.count) + ')</h2>' +
            '<div class="tbl-wrap">' +
              '<table>' +
                '<thead><tr><th>ifIndex</th><th>ifName</th><th>ifDescr</th><th>ifType</th><th>Admin</th><th>Oper</th><th>Speed</th><th>In Octets</th><th>Out Octets</th></tr></thead>' +
                '<tbody>' +
                  g.rows.map(function (r) {
                    return '<tr>' +
                      '<td class="mono">' + esc(r.ifIndex) + '</td>' +
                      '<td class="mono">' + esc(r.ifName) + '</td>' +
                      '<td>' + esc(r.ifDescr) + '</td>' +
                      '<td class="mono">' + esc(r.ifType) + '</td>' +
                      '<td>' + esc(r.admin) + '</td>' +
                      '<td>' + esc(r.oper) + '</td>' +
                      '<td>' + esc(r.speedFmt) + '</td>' +
                      '<td class="mono">' + esc(r.inOctetsFmt) + '</td>' +
                      '<td class="mono">' + esc(r.outOctetsFmt) + '</td>' +
                    '</tr>';
                  }).join('') +
                '</tbody>' +
              '</table>' +
            '</div>' +
          '</section>';
        }).join('');
      }
    })();
  </script>
  `;

  const groupsView = groups.map((g) => ({
    title: g.title,
    direction: g.direction,
    color: g.color,
    count: g.count,
    upCount: g.upCount,
    downCount: g.downCount,
    inOctetsFmt: fmtInt(g.inOctets),
    outOctetsFmt: fmtInt(g.outOctets),
    maxSpeedFmt: fmtBps(g.maxSpeed),
    rows: g.rows.map((r) => ({
      ifIndex: r.ifIndex,
      ifName: r.ifName,
      ifDescr: r.ifDescr,
      ifType: r.ifType,
      admin: r.admin,
      oper: r.oper,
      speedFmt: fmtBps(r.speedBps),
      inOctetsFmt: fmtInt(r.inOctets),
      outOctetsFmt: fmtInt(r.outOctets)
    }))
  }));

  pm.visualizer.set(template, {
    status: response && response.status !== undefined ? String(response.status) : 'N/A',
    message: safeText(response && response.message),
    groupCount: groupsView.length,
    totalInterfaces: totalInterfaces,
    totalUp: totalUp,
    totalDown: totalDown,
    deviceInfo: deviceInfo,
    groupsJson: JSON.stringify(groupsView),
    treeJson: JSON.stringify(treeData)
  });
})();
````
</details>

<details>
<summary>Sample JSON payload</summary>

````json
{
    "status": 0,
    "message": "Interface statistics retrieved successfully",
    "device": {
        "mac_address": "38:ad:2b:3e:86:54",
        "system_description": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "2022.01-MXL-v-4.0.357",
            "SW_REV": "8.4.0.0.1b2",
            "MODEL": "CODA60",
            "is_empty": false
        }
    },
    "results": {
        "docsCableMaclayer": [
            {
                "ifEntry": {
                    "ifIndex": 2,
                    "ifDescr": "RF MAC Interface",
                    "ifType": 127,
                    "ifMtu": 1522,
                    "ifSpeed": 0,
                    "ifPhysAddress": "0x38ad2b3e8654",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 306683388,
                    "ifInUcastPkts": 112383,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 7062572,
                    "ifOutUcastPkts": 36560,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "cni0",
                    "ifInMulticastPkts": 2065,
                    "ifInBroadcastPkts": 3287808,
                    "ifOutMulticastPkts": 4,
                    "ifOutBroadcastPkts": 229,
                    "ifHCInOctets": 306683388,
                    "ifHCInUcastPkts": 112383,
                    "ifHCInMulticastPkts": 2065,
                    "ifHCInBroadcastPkts": 3287808,
                    "ifHCOutOctets": 7062572,
                    "ifHCOutUcastPkts": 36560,
                    "ifHCOutMulticastPkts": 4,
                    "ifHCOutBroadcastPkts": 229,
                    "ifLinkUpDownTrapEnable": 1,
                    "ifHighSpeed": 0,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            }
        ],
        "docsCableDownstream": [
            {
                "ifEntry": {
                    "ifIndex": 49,
                    "ifDescr": "RF Downstream Interface 2",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch3",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 50,
                    "ifDescr": "RF Downstream Interface 3",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 59919479,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch4",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 51,
                    "ifDescr": "RF Downstream Interface 4",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 60492105,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch5",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 52,
                    "ifDescr": "RF Downstream Interface 5",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 59155597,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch6",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 53,
                    "ifDescr": "RF Downstream Interface 6",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 59918364,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch7",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 54,
                    "ifDescr": "RF Downstream Interface 7",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch8",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 55,
                    "ifDescr": "RF Downstream Interface 8",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch9",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 56,
                    "ifDescr": "RF Downstream Interface 9",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch10",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 57,
                    "ifDescr": "RF Downstream Interface 10",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch11",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 58,
                    "ifDescr": "RF Downstream Interface 11",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch12",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 59,
                    "ifDescr": "RF Downstream Interface 12",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch13",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 60,
                    "ifDescr": "RF Downstream Interface 13",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch14",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 61,
                    "ifDescr": "RF Downstream Interface 14",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch15",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 62,
                    "ifDescr": "RF Downstream Interface 15",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch16",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 63,
                    "ifDescr": "RF Downstream Interface 16",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch17",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 64,
                    "ifDescr": "RF Downstream Interface 17",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch18",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 65,
                    "ifDescr": "RF Downstream Interface 18",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch19",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 66,
                    "ifDescr": "RF Downstream Interface 19",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch20",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 67,
                    "ifDescr": "RF Downstream Interface 20",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch21",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 68,
                    "ifDescr": "RF Downstream Interface 21",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch22",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 69,
                    "ifDescr": "RF Downstream Interface 22",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch23",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 70,
                    "ifDescr": "RF Downstream Interface 23",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch24",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 71,
                    "ifDescr": "RF Downstream Interface 24",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch25",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 72,
                    "ifDescr": "RF Downstream Interface 25",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch26",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 73,
                    "ifDescr": "RF Downstream Interface 26",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch27",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 74,
                    "ifDescr": "RF Downstream Interface 27",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch28",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 75,
                    "ifDescr": "RF Downstream Interface 28",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 748,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch29",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 748,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 76,
                    "ifDescr": "RF Downstream Interface 29",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 1165,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch30",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 1165,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 77,
                    "ifDescr": "RF Downstream Interface 30",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 1165,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch31",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 1165,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 78,
                    "ifDescr": "RF Downstream Interface 31",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 1165,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch32",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 1165,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 43,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            }
        ],
        "docsCableUpstream": [
            {
                "ifEntry": {
                    "ifIndex": 80,
                    "ifDescr": "RF Upstream Interface 1",
                    "ifType": 129,
                    "ifMtu": 1764,
                    "ifSpeed": 30720000,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 0,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 1542043,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": null
            },
            {
                "ifEntry": {
                    "ifIndex": 81,
                    "ifDescr": "RF Upstream Interface 2",
                    "ifType": 129,
                    "ifMtu": 1764,
                    "ifSpeed": 30720000,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 0,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 1586244,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": null
            },
            {
                "ifEntry": {
                    "ifIndex": 82,
                    "ifDescr": "RF Upstream Interface 3",
                    "ifType": 129,
                    "ifMtu": 1764,
                    "ifSpeed": 30720000,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 0,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 1594504,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": null
            },
            {
                "ifEntry": {
                    "ifIndex": 83,
                    "ifDescr": "RF Upstream Interface 4",
                    "ifType": 129,
                    "ifMtu": 1764,
                    "ifSpeed": 30720000,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 0,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 1640532,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": null
            }
        ],
        "docsOfdmDownstream": [
            {
                "ifEntry": {
                    "ifIndex": 3,
                    "ifDescr": "RF Downstream Interface",
                    "ifType": 277,
                    "ifMtu": 1764,
                    "ifSpeed": 1779270016,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 1289946665,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch1",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 1289946665,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 1779,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 48,
                    "ifDescr": "RF Downstream Interface 1",
                    "ifType": 277,
                    "ifMtu": 1764,
                    "ifSpeed": 1779270016,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 320780935,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "dsch2",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 320780935,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 1779,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            }
        ],
        "docsOfdmaUpstream": [
            {
                "ifEntry": {
                    "ifIndex": 4,
                    "ifDescr": "RF Upstream Interface",
                    "ifType": 278,
                    "ifMtu": 1764,
                    "ifSpeed": 846746232,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 0,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 1545656,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": null
            },
            {
                "ifEntry": {
                    "ifIndex": 84,
                    "ifDescr": "RF Upstream Interface 5",
                    "ifType": 278,
                    "ifMtu": 1764,
                    "ifSpeed": 381580920,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 0,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 1427173,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": null
            }
        ]
    }
}
````
</details>
