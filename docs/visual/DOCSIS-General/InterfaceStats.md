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
// Last Update: 2026-03-11 09:05:00 MST
// Visual Constraints: Follow canonical visual rules in CODING_AGENTS.md.

(function () {
  const response = pm.response.json() || {};

  function safeText(value) {
    if (value === undefined || value === null) return 'N/A';
    const text = String(value).trim();
    return text ? text : 'N/A';
  }

  function n(value) {
    const numeric = Number(value);
    return Number.isFinite(numeric) ? numeric : null;
  }

  function sanitizeMac(value) {
    const raw = safeText(value);
    if (raw === 'N/A') return raw;
    const compact = raw.replace(/[^0-9a-f]/gi, '').toLowerCase();
    if (compact.length !== 12) return raw.toLowerCase();
    return compact.match(/.{1,2}/g).join(':');
  }

  function fmtInt(value) {
    const numeric = n(value);
    if (numeric === null) return 'N/A';
    return Math.trunc(numeric).toLocaleString('en-US');
  }

  function fmtSpeedBps(value) {
    const numeric = n(value);
    if (numeric === null || numeric <= 0) return 'N/A';
    if (numeric >= 1e9) return (numeric / 1e9).toFixed(2) + ' Gbps';
    if (numeric >= 1e6) return (numeric / 1e6).toFixed(2) + ' Mbps';
    if (numeric >= 1e3) return (numeric / 1e3).toFixed(2) + ' Kbps';
    return String(Math.round(numeric)) + ' bps';
  }

  function adminOper(value) {
    const numeric = n(value);
    if (numeric === 1) return 'up';
    if (numeric === 2) return 'down';
    if (numeric === 3) return 'testing';
    return 'unknown';
  }

  function ifTypeLabel(value) {
    const numeric = n(value);
    const labels = {
      6: 'Ethernet',
      127: 'MAC',
      128: 'SCQAM DS',
      129: 'SCQAM US',
      277: 'OFDM DS',
      278: 'OFDMA US'
    };
    if (numeric === null) return 'N/A';
    return labels[numeric] ? labels[numeric] + ' (' + numeric + ')' : String(numeric);
  }

  function groupMeta(key) {
    const map = {
      ethernetCsmacd: { title: 'Ethernet', color: 'eth', branch: 'Ethernet' },
      docsCableMaclayer: { title: 'DOCSIS MAC Layer', color: 'mac', branch: 'RF MAC' },
      docsCableDownstream: { title: 'SCQAM Downstream', color: 'ds', branch: 'Downstream' },
      docsOfdmDownstream: { title: 'OFDM Downstream', color: 'ds', branch: 'Downstream' },
      docsCableUpstream: { title: 'SCQAM Upstream', color: 'us', branch: 'Upstream' },
      docsOfdmaUpstream: { title: 'OFDMA Upstream', color: 'us', branch: 'Upstream' }
    };
    return map[key] || { title: safeText(key), color: 'gen', branch: 'Interfaces' };
  }

  function normalizeItem(item) {
    const ifEntry = item && item.ifEntry && typeof item.ifEntry === 'object' ? item.ifEntry : {};
    const ifXEntry = item && item.ifXEntry && typeof item.ifXEntry === 'object' ? item.ifXEntry : {};
    const inOctets = n(ifXEntry.ifHCInOctets) !== null ? n(ifXEntry.ifHCInOctets) : n(ifEntry.ifInOctets);
    const outOctets = n(ifXEntry.ifHCOutOctets) !== null ? n(ifXEntry.ifHCOutOctets) : n(ifEntry.ifOutOctets);
    const speedBps = n(ifEntry.ifSpeed);
    const highSpeedMbps = n(ifXEntry.ifHighSpeed);

    return {
      ifIndex: safeText(ifEntry.ifIndex),
      ifName: safeText(ifXEntry.ifName),
      ifDescr: safeText(ifEntry.ifDescr),
      ifType: ifTypeLabel(ifEntry.ifType),
      admin: adminOper(ifEntry.ifAdminStatus),
      oper: adminOper(ifEntry.ifOperStatus),
      speedBps: speedBps,
      highSpeedMbps: highSpeedMbps,
      speedLabel: highSpeedMbps !== null && highSpeedMbps > 0 ? String(Math.round(highSpeedMbps)) + ' Mbps' : fmtSpeedBps(speedBps),
      inOctets: inOctets,
      outOctets: outOctets,
      inOctetsLabel: fmtInt(inOctets),
      outOctetsLabel: fmtInt(outOctets)
    };
  }

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

  const results = response && typeof response.results === 'object' ? response.results : {};
  const bridge = results && results.bridge && typeof results.bridge === 'object' ? results.bridge : {};
  const bridgeIfIndexes = bridge && bridge.ifIndexes && typeof bridge.ifIndexes === 'object' ? bridge.ifIndexes : {};

  function bridgeIfName(ifIndex) {
    const key = String(ifIndex);
    const entry = bridgeIfIndexes[key] && typeof bridgeIfIndexes[key] === 'object' ? bridgeIfIndexes[key] : {};
    return safeText(entry.ifName);
  }

  function bridgeIfDescr(ifIndex) {
    const key = String(ifIndex);
    const entry = bridgeIfIndexes[key] && typeof bridgeIfIndexes[key] === 'object' ? bridgeIfIndexes[key] : {};
    return safeText(entry.ifDescription);
  }

  const groups = Object.keys(results)
    .filter(function (key) { return Array.isArray(results[key]) && results[key].length > 0; })
    .map(function (key) {
      const meta = groupMeta(key);
      const rows = results[key].map(function (item) {
        const row = normalizeItem(item);
        const bridgeName = bridgeIfName(row.ifIndex);
        const bridgeDescr = bridgeIfDescr(row.ifIndex);
        if (bridgeName !== 'N/A') {
          row.ifName = bridgeName;
        }
        if (row.ifDescr === 'N/A' && bridgeDescr !== 'N/A') {
          row.ifDescr = bridgeDescr;
        }
        return row;
      }).sort(function (a, b) {
        return Number(a.ifIndex) - Number(b.ifIndex);
      });
      let upCount = 0;
      let downCount = 0;
      let inOctets = 0;
      let outOctets = 0;
      let maxSpeed = 0;
      rows.forEach(function (row) {
        if (row.oper === 'up') upCount += 1;
        if (row.oper === 'down') downCount += 1;
        if (row.inOctets !== null) inOctets += row.inOctets;
        if (row.outOctets !== null) outOctets += row.outOctets;
        if (row.speedBps !== null && row.speedBps > maxSpeed) maxSpeed = row.speedBps;
      });
      return {
        key: key,
        title: meta.title,
        color: meta.color,
        branch: meta.branch,
        rows: rows,
        count: rows.length,
        upCount: upCount,
        downCount: downCount,
        inOctets: inOctets,
        outOctets: outOctets,
        inOctetsLabel: fmtInt(inOctets),
        outOctetsLabel: fmtInt(outOctets),
        maxSpeed: maxSpeed,
        maxSpeedLabel: fmtSpeedBps(maxSpeed)
      };
    })
    .sort(function (a, b) {
      const order = { Ethernet: 1, 'DOCSIS MAC Layer': 2, 'SCQAM Downstream': 3, 'OFDM Downstream': 4, 'SCQAM Upstream': 5, 'OFDMA Upstream': 6 };
      return (order[a.title] || 99) - (order[b.title] || 99);
    });

  const totalInterfaces = groups.reduce(function (sum, group) { return sum + group.count; }, 0);
  const totalUp = groups.reduce(function (sum, group) { return sum + group.upCount; }, 0);
  const totalDown = groups.reduce(function (sum, group) { return sum + group.downCount; }, 0);

  function buildTreeData() {
    const ethernetGroups = groups.filter(function (group) {
      return group.branch === 'Ethernet';
    });
    const macGroups = groups.filter(function (group) {
      return group.branch === 'RF MAC';
    });
    const downstreamGroups = groups.filter(function (group) {
      return group.branch === 'Downstream';
    });
    const upstreamGroups = groups.filter(function (group) {
      return group.branch === 'Upstream';
    });
    const otherGroups = groups.filter(function (group) {
      return ['Ethernet', 'RF MAC', 'Downstream', 'Upstream'].indexOf(group.branch) === -1;
    });

    function groupNode(group) {
      return {
        name: group.title,
        subtitle: 'Interfaces (' + group.count + ') · Up (' + group.upCount + ') · Down (' + group.downCount + ')',
        kind: group.color,
        children: group.rows.map(function (row) {
          return {
            name: 'if' + row.ifIndex + ' ' + row.ifName,
            subtitle: row.ifDescr + ' · ' + row.oper + ' · ' + row.speedLabel,
            kind: row.oper === 'up' ? 'ok' : (row.oper === 'down' ? 'nok' : 'gen')
          };
        })
      };
    }

    const rootChildren = [];

    if (ethernetGroups.length) {
      rootChildren.push({
        name: 'Ethernet',
        subtitle: 'Root-linked via ifStack lowerLayer 0',
        kind: 'eth',
        children: ethernetGroups.map(groupNode)
      });
    }

    const rfMacChildren = [];
    if (macGroups.length) {
      rfMacChildren.push.apply(rfMacChildren, macGroups.map(groupNode));
    }
    if (downstreamGroups.length) {
      rfMacChildren.push({
        name: 'Downstream',
        subtitle: 'Linked to RF MAC ifIndex 2',
        kind: 'ds',
        children: downstreamGroups.map(groupNode)
      });
    }
    if (upstreamGroups.length) {
      rfMacChildren.push({
        name: 'Upstream',
        subtitle: 'Linked to RF MAC ifIndex 2',
        kind: 'us',
        children: upstreamGroups.map(groupNode)
      });
    }
    if (otherGroups.length) {
      rfMacChildren.push({
        name: 'Other Interfaces',
        subtitle: 'Unclassified groups',
        kind: 'gen',
        children: otherGroups.map(groupNode)
      });
    }

    if (rfMacChildren.length) {
      rootChildren.push({
        name: 'RF MAC ifIndex 2 ' + bridgeIfName(2),
        subtitle: 'Only RF MAC is root-linked from bridge index 0',
        kind: 'mac',
        children: rfMacChildren
      });
    }

    return {
      name: 'Device ' + deviceInfo.macAddress,
      subtitle: deviceInfo.model + ' · ' + deviceInfo.swVersion,
      kind: 'root',
      children: rootChildren
    };
  }

  const treeData = buildTreeData();

  const template = `
  <style>
    :root {
      --bg: #141821;
      --panel: #1b2332;
      --panel2: #202938;
      --line: rgba(255,255,255,0.10);
      --text: #e7edf8;
      --muted: #dbe3ff;
      --title: #f3f6ff;
      --accent: #9ec0ff;
      --ds: #5a6fd8;
      --us: #39c28e;
      --mac: #f1c40f;
      --eth: #6ab0ff;
      --voice: #ff8f66;
      --ok: #39c28e;
      --nok: #c62828;
    }

    body {
      margin: 0;
      padding: 16px;
      background: radial-gradient(circle at top left, rgba(90,111,216,0.18), transparent 26%), linear-gradient(180deg, #141821 0%, #101621 100%);
      color: var(--text);
      font-family: Arial, sans-serif;
    }

    .wrap {
      max-width: 1600px;
      margin: 0 auto;
      display: grid;
      gap: 12px;
    }

    .card {
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)), var(--panel);
      border: 1px solid rgba(255,255,255,0.09);
      border-radius: 10px;
      padding: 14px;
      box-shadow: 0 14px 30px rgba(0,0,0,0.18);
    }

    .title {
      margin: 0 0 8px 0;
      color: var(--title);
      text-align: center;
      font-size: 20px;
      font-weight: 700;
    }

    .meta {
      color: var(--muted);
      font-size: 12px;
      text-align: center;
    }

    .kpis {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-top: 10px;
    }

    .kpi {
      background: var(--panel2);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px;
    }

    .kpi .label {
      font-size: 11px;
      color: var(--muted);
    }

    .kpi .value {
      font-size: 14px;
      color: var(--title);
      font-weight: 700;
      margin-top: 4px;
    }

    .section-title {
      margin: 0 0 8px 0;
      font-size: 16px;
      color: var(--accent);
      font-weight: 700;
    }

    .tree-note {
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 8px;
    }

    .tree-wrap {
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: auto;
      background: var(--panel2);
    }

    .tbl-wrap {
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: auto;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 920px;
    }

    th, td {
      padding: 8px 10px;
      border-bottom: 1px solid var(--line);
      font-size: 12px;
      text-align: left;
      vertical-align: top;
    }

    th {
      background: var(--panel2);
      color: var(--muted);
    }

    td {
      color: var(--title);
    }

    .mono {
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }

    .group-title {
      margin: 0 0 8px 0;
      font-size: 16px;
      font-weight: 700;
    }

    .group-title.ds { color: var(--ds); }
    .group-title.us { color: var(--us); }
    .group-title.mac { color: var(--mac); }
    .group-title.eth { color: var(--eth); }
    .group-title.voice { color: var(--voice); }
    .group-title.gen { color: var(--accent); }

    .tree-svg .node text {
      font-size: 12px;
      fill: var(--text);
    }

    @media (max-width: 1100px) {
      .kpis {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
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
      <h2 class="section-title">Device Info</h2>
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
      <h2 class="section-title">Topology</h2>
      <div class="tree-note">Click nodes to collapse/expand. Hover junction circles for details.</div>
      <div id="topologyTree" class="tree-wrap"></div>
    </div>

    <div class="card">
      <h2 class="section-title">Group Summary</h2>
      <div class="tbl-wrap">
        <table>
          <thead>
            <tr><th>Group</th><th>Branch</th><th>Interfaces</th><th>Up</th><th>Down</th><th>In Octets</th><th>Out Octets</th><th>Max Speed</th></tr>
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

      function esc(value) {
        if (value === undefined || value === null) return 'N/A';
        return String(value)
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
        if (kind === 'eth') return '#6ab0ff';
        if (kind === 'voice') return '#ff8f66';
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
        const width = Math.max(1320, host.clientWidth || 1320);
        const dx = 22;
        const dy = 280;
        const tree = d3.tree().nodeSize([dx, dy]);
        const diagonal = d3.linkHorizontal().x(function (d) { return d.y; }).y(function (d) { return d.x; });

        const root = d3.hierarchy(data);
        root.x0 = dx;
        root.y0 = 0;
        let nextId = 0;

        root.descendants().forEach(function (node) {
          node.id = nextId++;
          node._children = node.children;
          if (node.depth > 1) {
            node.children = null;
          }
        });

        const svg = d3.create('svg')
          .attr('class', 'tree-svg')
          .attr('width', width)
          .attr('height', dx)
          .attr('viewBox', [-40, -20, width, dx])
          .style('font', '12px Arial');

        const gLink = svg.append('g')
          .attr('fill', 'none')
          .attr('stroke', 'rgba(255,255,255,0.20)')
          .attr('stroke-width', 1.2);

        const gNode = svg.append('g')
          .attr('cursor', 'pointer')
          .attr('pointer-events', 'all');

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
          const transition = svg.transition()
            .duration(duration)
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
            .attr('r', function (d) { return d && (d.children || d._children) ? 6 : 4; })
            .attr('fill', function (d) { return d._children ? nodeColor(d.data.kind) : '#1b2332'; })
            .attr('stroke', function (d) { return nodeColor(d.data.kind); })
            .attr('stroke-width', 1.5);

          nodeEnter.append('title')
            .text(function (d) {
              const name = d && d.data && d.data.name ? String(d.data.name) : 'N/A';
              const subtitle = d && d.data && d.data.subtitle ? String(d.data.subtitle) : '';
              return subtitle ? (name + ' | ' + subtitle) : name;
            });

          nodeEnter.append('text')
            .attr('dy', '0.31em')
            .attr('x', 10)
            .attr('text-anchor', 'start')
            .text(function (d) {
              const isLeaf = !(d && (d.children || d._children));
              if (!isLeaf) return '';
              return d && d.data && d.data.name ? String(d.data.name) : 'N/A';
            });

          node.merge(nodeEnter).transition(transition)
            .attr('transform', function (d) { return 'translate(' + d.y + ',' + d.x + ')'; })
            .attr('fill-opacity', 1)
            .attr('stroke-opacity', 1);

          node.merge(nodeEnter).select('circle')
            .attr('fill', function (d) { return d._children ? nodeColor(d.data.kind) : '#1b2332'; })
            .attr('stroke', function (d) { return nodeColor(d.data.kind); });

          node.merge(nodeEnter).select('title')
            .text(function (d) {
              const name = d && d.data && d.data.name ? String(d.data.name) : 'N/A';
              const subtitle = d && d.data && d.data.subtitle ? String(d.data.subtitle) : '';
              return subtitle ? (name + ' | ' + subtitle) : name;
            });

          node.exit().transition(transition).remove()
            .attr('transform', function () { return 'translate(' + source.y + ',' + source.x + ')'; })
            .attr('fill-opacity', 0)
            .attr('stroke-opacity', 0);

          const link = gLink.selectAll('path').data(links, function (d) { return d.target.id; });

          const linkEnter = link.enter().append('path')
            .attr('d', function () {
              const origin = { x: source.x0, y: source.y0 };
              return diagonal({ source: origin, target: origin });
            });

          link.merge(linkEnter).transition(transition).attr('d', diagonal);

          link.exit().transition(transition).remove().attr('d', function () {
            const origin = { x: source.x, y: source.y };
            return diagonal({ source: origin, target: origin });
          });

          root.eachBefore(function (node) {
            node.x0 = node.x;
            node.y0 = node.y;
          });
        }

        update(root);
        host.appendChild(svg.node());
      }

      renderTree(treeData);

      const summaryRows = document.getElementById('summaryRows');
      if (summaryRows && Array.isArray(groups)) {
        summaryRows.innerHTML = groups.map(function (group) {
          return '<tr>' +
            '<td>' + esc(group.title) + '</td>' +
            '<td>' + esc(group.branch) + '</td>' +
            '<td>' + esc(group.count) + '</td>' +
            '<td>' + esc(group.upCount) + '</td>' +
            '<td>' + esc(group.downCount) + '</td>' +
            '<td class="mono">' + esc(group.inOctetsLabel) + '</td>' +
            '<td class="mono">' + esc(group.outOctetsLabel) + '</td>' +
            '<td>' + esc(group.maxSpeedLabel) + '</td>' +
          '</tr>';
        }).join('');
      }

      const groupTables = document.getElementById('groupTables');
      if (groupTables && Array.isArray(groups)) {
        groupTables.innerHTML = groups.map(function (group) {
          return '<section class="card">' +
            '<h2 class="group-title ' + esc(group.color) + '">' + esc(group.title) + ' · Interfaces (' + esc(group.count) + ')</h2>' +
            '<div class="tbl-wrap">' +
              '<table>' +
                '<thead><tr><th>ifIndex</th><th>ifName</th><th>ifDescr</th><th>ifType</th><th>Admin</th><th>Oper</th><th>Speed</th><th>In Octets</th><th>Out Octets</th></tr></thead>' +
                '<tbody>' +
                  group.rows.map(function (row) {
                    return '<tr>' +
                      '<td class="mono">' + esc(row.ifIndex) + '</td>' +
                      '<td class="mono">' + esc(row.ifName) + '</td>' +
                      '<td>' + esc(row.ifDescr) + '</td>' +
                      '<td>' + esc(row.ifType) + '</td>' +
                      '<td>' + esc(row.admin) + '</td>' +
                      '<td>' + esc(row.oper) + '</td>' +
                      '<td>' + esc(row.speedLabel) + '</td>' +
                      '<td class="mono">' + esc(row.inOctetsLabel) + '</td>' +
                      '<td class="mono">' + esc(row.outOctetsLabel) + '</td>' +
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

  pm.visualizer.set(template, {
    status: response && response.status !== undefined ? String(response.status) : 'N/A',
    message: safeText(response && response.message),
    groupCount: groups.length,
    totalInterfaces: totalInterfaces,
    totalUp: totalUp,
    totalDown: totalDown,
    deviceInfo: deviceInfo,
    groupsJson: JSON.stringify(groups),
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
        "mac_address": "b0:f5:30:b7:76:30",
        "system_description": {
            "HW_REV": "1A",
            "VENDOR": "Hitron Technologies",
            "BOOTR": "2022.01-MXL-v-4.0.369",
            "SW_REV": "8.5.0.0.1b4",
            "MODEL": "CODA60",
            "is_empty": false
        }
    },
    "results": {
        "ethernetCsmacd": [
            {
                "ifEntry": {
                    "ifIndex": 1,
                    "ifDescr": "eRouter Embedded Interface",
                    "ifType": 6,
                    "ifMtu": 0,
                    "ifSpeed": 10000000,
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
                    "ifOutOctets": 0,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "esafe0",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 4294967295,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 0,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 18446744073709551615,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 10,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 5,
                    "ifDescr": "Ethernet CPE Interface",
                    "ifType": 6,
                    "ifMtu": 1500,
                    "ifSpeed": 4294967295,
                    "ifPhysAddress": "0x3ebb56fca6f2",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 2,
                    "ifLastChange": 2916018,
                    "ifInOctets": 0,
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
                    "ifName": "eth0_1",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 0,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 10000,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 6,
                    "ifDescr": "Ethernet CPE Interface",
                    "ifType": 6,
                    "ifMtu": 1500,
                    "ifSpeed": 2500000000,
                    "ifPhysAddress": "0x2e48a6452f48",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 2,
                    "ifLastChange": 2916018,
                    "ifInOctets": 0,
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
                    "ifName": "eth0_6",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 0,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 2500,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 7,
                    "ifDescr": "Ethernet CPE Interface",
                    "ifType": 6,
                    "ifMtu": 1500,
                    "ifSpeed": 2500000000,
                    "ifPhysAddress": "0x36bbc3ede1c2",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 2,
                    "ifLastChange": 2916018,
                    "ifInOctets": 0,
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
                    "ifName": "eth0_7",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 0,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 0,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 2500,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 8,
                    "ifDescr": "Ethernet CPE Interface",
                    "ifType": 6,
                    "ifMtu": 1500,
                    "ifSpeed": 1000000000,
                    "ifPhysAddress": "0xbad5c63b0d45",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 2918454,
                    "ifInOctets": 2633696,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 2368,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 694660,
                    "ifOutUcastPkts": 42,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "eth0_8",
                    "ifInMulticastPkts": 39144,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 7239,
                    "ifOutBroadcastPkts": 509,
                    "ifHCInOctets": 2633760,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 39144,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 694660,
                    "ifHCOutUcastPkts": 42,
                    "ifHCOutMulticastPkts": 7239,
                    "ifHCOutBroadcastPkts": 509,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 1000,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 9,
                    "ifDescr": "Ethernet CPE Interface",
                    "ifType": 6,
                    "ifMtu": 1500,
                    "ifSpeed": 10000000,
                    "ifPhysAddress": "0xb0f530b7763c",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 2916018,
                    "ifInOctets": 3707765762,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 103483910,
                    "ifOutUcastPkts": 1073,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "wlan0.0",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 72771730547934210,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 144398866474273286,
                    "ifHCOutUcastPkts": 1073,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 10,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 10,
                    "ifDescr": "Ethernet CPE Interface",
                    "ifType": 6,
                    "ifMtu": 1500,
                    "ifSpeed": 10000000,
                    "ifPhysAddress": "0xb0f530b77631",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 2916018,
                    "ifInOctets": 3707765762,
                    "ifInUcastPkts": 6800,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 103483910,
                    "ifOutUcastPkts": 4486,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "wlan2.0",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 24904819,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 60,
                    "ifHCInOctets": 72771730547934210,
                    "ifHCInUcastPkts": 6800,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 24904819,
                    "ifHCOutOctets": 144398866474273286,
                    "ifHCOutUcastPkts": 4486,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 60,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 10,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 11,
                    "ifDescr": "Ethernet CPE Interface",
                    "ifType": 6,
                    "ifMtu": 1500,
                    "ifSpeed": 10000000,
                    "ifPhysAddress": "0xb0f530b77647",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 2916018,
                    "ifInOctets": 3707765762,
                    "ifInUcastPkts": 0,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 103483910,
                    "ifOutUcastPkts": 0,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "wlan4.0",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 72771730547934210,
                    "ifHCInUcastPkts": 0,
                    "ifHCInMulticastPkts": 0,
                    "ifHCInBroadcastPkts": 0,
                    "ifHCOutOctets": 144398866474273286,
                    "ifHCOutUcastPkts": 0,
                    "ifHCOutMulticastPkts": 0,
                    "ifHCOutBroadcastPkts": 0,
                    "ifLinkUpDownTrapEnable": 2,
                    "ifHighSpeed": 10,
                    "ifPromiscuousMode": true,
                    "ifConnectorPresent": true,
                    "ifAlias": "",
                    "ifCounterDiscontinuityTime": 0
                }
            }
        ],
        "docsCableMaclayer": [
            {
                "ifEntry": {
                    "ifIndex": 2,
                    "ifDescr": "RF MAC Interface",
                    "ifType": 127,
                    "ifMtu": 1522,
                    "ifSpeed": 0,
                    "ifPhysAddress": "0xb0f530b77630",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 512521493,
                    "ifInUcastPkts": 367889,
                    "ifInNUcastPkts": null,
                    "ifInDiscards": 0,
                    "ifInErrors": 0,
                    "ifInUnknownProtos": 0,
                    "ifOutOctets": 12679833,
                    "ifOutUcastPkts": 71399,
                    "ifOutNUcastPkts": null,
                    "ifOutDiscards": 0,
                    "ifOutErrors": 0,
                    "ifOutQLen": null,
                    "ifSpecific": null
                },
                "ifXEntry": {
                    "ifName": "cni0",
                    "ifInMulticastPkts": 114,
                    "ifInBroadcastPkts": 247768,
                    "ifOutMulticastPkts": 358,
                    "ifOutBroadcastPkts": 18,
                    "ifHCInOctets": 512521493,
                    "ifHCInUcastPkts": 367889,
                    "ifHCInMulticastPkts": 114,
                    "ifHCInBroadcastPkts": 247768,
                    "ifHCOutOctets": 12679833,
                    "ifHCOutUcastPkts": 71399,
                    "ifHCOutMulticastPkts": 358,
                    "ifHCOutBroadcastPkts": 18,
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
                    "ifIndex": 50,
                    "ifDescr": "RF Downstream Interface 3",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 769,
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
                    "ifHCInOctets": 769,
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
                    "ifCounterDiscontinuityTime": 2916019
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 79,
                    "ifDescr": "RF Downstream Interface",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 1187,
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
                    "ifHCInOctets": 1187,
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
                    "ifIndex": 112,
                    "ifDescr": "RF Downstream Interface 33",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 1187,
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
                    "ifName": "dsch34",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 1187,
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
                    "ifIndex": 113,
                    "ifDescr": "RF Downstream Interface 34",
                    "ifType": 128,
                    "ifMtu": 1764,
                    "ifSpeed": 42884296,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 1187,
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
                    "ifName": "dsch35",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 1187,
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
                    "ifOutOctets": 2539019,
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
                    "ifOutOctets": 2640648,
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
                    "ifOutOctets": 2553925,
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
                    "ifOutOctets": 2557396,
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
                    "ifDescr": "RF Downstream Interface 32",
                    "ifType": 277,
                    "ifMtu": 1764,
                    "ifSpeed": 1779270016,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 2916019,
                    "ifInOctets": 246603236,
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
                    "ifName": "dsch33",
                    "ifInMulticastPkts": 0,
                    "ifInBroadcastPkts": 0,
                    "ifOutMulticastPkts": 0,
                    "ifOutBroadcastPkts": 0,
                    "ifHCInOctets": 246603236,
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
                    "ifCounterDiscontinuityTime": 2916019
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
                    "ifLastChange": 2916019,
                    "ifInOctets": 189237077,
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
                    "ifHCInOctets": 189237077,
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
                    "ifCounterDiscontinuityTime": 2916019
                }
            },
            {
                "ifEntry": {
                    "ifIndex": 49,
                    "ifDescr": "RF Downstream Interface 2",
                    "ifType": 277,
                    "ifMtu": 1764,
                    "ifSpeed": 1779270016,
                    "ifPhysAddress": "",
                    "ifAdminStatus": 1,
                    "ifOperStatus": 1,
                    "ifLastChange": 0,
                    "ifInOctets": 174378563,
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
                    "ifHCInOctets": 174389318,
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
                    "ifOutOctets": 2199472,
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
                    "ifOutOctets": 2501645,
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
        "bridge": {
            "ifIndexes": {
                "0": {
                    "ifType": null,
                    "ifDescription": "",
                    "ifName": "",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 0,
                            "ifStackLowerLayer": 2,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 3,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 4,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 48,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 49,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 50,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 51,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 52,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 53,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 54,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 55,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 56,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 57,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 58,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 59,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 60,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 61,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 62,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 63,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 64,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 65,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 66,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 67,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 68,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 69,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 70,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 71,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 72,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 73,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 74,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 75,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 76,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 77,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 78,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 79,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 80,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 81,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 82,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 83,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 84,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 112,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 113,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "1": {
                    "ifType": 6,
                    "ifDescription": "eRouter Embedded Interface",
                    "ifName": "esafe0",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [
                        {
                            "dot1dBasePort": 1,
                            "dot1dBasePortIfIndex": 1,
                            "dot1dBasePortCircuit": "0.0",
                            "dot1dBasePortDelayExceededDiscards": 0,
                            "dot1dBasePortMtuExceededDiscards": 0
                        }
                    ],
                    "dot1dTpPortEntry": [
                        {
                            "dot1dTpPort": 1,
                            "dot1dTpPortMaxInfo": 0,
                            "dot1dTpPortInFrames": 0,
                            "dot1dTpPortOutFrames": 4294967295,
                            "dot1dTpPortInDiscards": 0
                        }
                    ],
                    "dot1dTpFdbEntry": [
                        {
                            "dot1dTpFdbAddress": "00:00:00:00:00:00",
                            "dot1dTpFdbPort": 1,
                            "dot1dTpFdbStatus": 4
                        },
                        {
                            "dot1dTpFdbAddress": "b0:f5:30:b7:76:33",
                            "dot1dTpFdbPort": 1,
                            "dot1dTpFdbStatus": 5
                        }
                    ],
                    "ifStackEntry": []
                },
                "2": {
                    "ifType": 127,
                    "ifDescription": "RF MAC Interface",
                    "ifName": "cni0",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [
                        {
                            "dot1dBasePort": 2,
                            "dot1dBasePortIfIndex": 2,
                            "dot1dBasePortCircuit": "0.0",
                            "dot1dBasePortDelayExceededDiscards": 0,
                            "dot1dBasePortMtuExceededDiscards": 0
                        }
                    ],
                    "dot1dTpPortEntry": [
                        {
                            "dot1dTpPort": 2,
                            "dot1dTpPortMaxInfo": 1522,
                            "dot1dTpPortInFrames": 620036,
                            "dot1dTpPortOutFrames": 75695,
                            "dot1dTpPortInDiscards": 0
                        }
                    ],
                    "dot1dTpFdbEntry": [
                        {
                            "dot1dTpFdbAddress": "b0:f5:30:b7:76:30",
                            "dot1dTpFdbPort": 2,
                            "dot1dTpFdbStatus": 4
                        }
                    ],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 0,
                            "ifStackLowerLayer": 2,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 3,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 4,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 48,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 49,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 50,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 51,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 52,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 53,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 54,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 55,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 56,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 57,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 58,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 59,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 60,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 61,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 62,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 63,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 64,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 65,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 66,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 67,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 68,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 69,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 70,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 71,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 72,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 73,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 74,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 75,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 76,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 77,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 78,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 79,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 80,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 81,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 82,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 83,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 84,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 112,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 113,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "3": {
                    "ifType": 277,
                    "ifDescription": "RF Downstream Interface 32",
                    "ifName": "dsch33",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 3,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 3,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "4": {
                    "ifType": 278,
                    "ifDescription": "RF Upstream Interface",
                    "ifName": "usch1",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 4,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 4,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "5": {
                    "ifType": 6,
                    "ifDescription": "Ethernet CPE Interface",
                    "ifName": "eth0_1",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [
                        {
                            "dot1dBasePort": 5,
                            "dot1dBasePortIfIndex": 5,
                            "dot1dBasePortCircuit": "0.0",
                            "dot1dBasePortDelayExceededDiscards": 0,
                            "dot1dBasePortMtuExceededDiscards": 0
                        }
                    ],
                    "dot1dTpPortEntry": [
                        {
                            "dot1dTpPort": 5,
                            "dot1dTpPortMaxInfo": 1500,
                            "dot1dTpPortInFrames": 0,
                            "dot1dTpPortOutFrames": 0,
                            "dot1dTpPortInDiscards": 0
                        }
                    ],
                    "dot1dTpFdbEntry": [
                        {
                            "dot1dTpFdbAddress": "3e:bb:56:fc:a6:f2",
                            "dot1dTpFdbPort": 5,
                            "dot1dTpFdbStatus": 4
                        }
                    ],
                    "ifStackEntry": []
                },
                "6": {
                    "ifType": 6,
                    "ifDescription": "Ethernet CPE Interface",
                    "ifName": "eth0_6",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [
                        {
                            "dot1dBasePort": 6,
                            "dot1dBasePortIfIndex": 6,
                            "dot1dBasePortCircuit": "0.0",
                            "dot1dBasePortDelayExceededDiscards": 0,
                            "dot1dBasePortMtuExceededDiscards": 0
                        }
                    ],
                    "dot1dTpPortEntry": [
                        {
                            "dot1dTpPort": 6,
                            "dot1dTpPortMaxInfo": 1500,
                            "dot1dTpPortInFrames": 0,
                            "dot1dTpPortOutFrames": 0,
                            "dot1dTpPortInDiscards": 0
                        }
                    ],
                    "dot1dTpFdbEntry": [
                        {
                            "dot1dTpFdbAddress": "2e:48:a6:45:2f:48",
                            "dot1dTpFdbPort": 6,
                            "dot1dTpFdbStatus": 4
                        }
                    ],
                    "ifStackEntry": []
                },
                "7": {
                    "ifType": 6,
                    "ifDescription": "Ethernet CPE Interface",
                    "ifName": "eth0_7",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [
                        {
                            "dot1dBasePort": 7,
                            "dot1dBasePortIfIndex": 7,
                            "dot1dBasePortCircuit": "0.0",
                            "dot1dBasePortDelayExceededDiscards": 0,
                            "dot1dBasePortMtuExceededDiscards": 0
                        }
                    ],
                    "dot1dTpPortEntry": [
                        {
                            "dot1dTpPort": 7,
                            "dot1dTpPortMaxInfo": 1500,
                            "dot1dTpPortInFrames": 0,
                            "dot1dTpPortOutFrames": 0,
                            "dot1dTpPortInDiscards": 0
                        }
                    ],
                    "dot1dTpFdbEntry": [
                        {
                            "dot1dTpFdbAddress": "36:bb:c3:ed:e1:c2",
                            "dot1dTpFdbPort": 7,
                            "dot1dTpFdbStatus": 4
                        }
                    ],
                    "ifStackEntry": []
                },
                "8": {
                    "ifType": 6,
                    "ifDescription": "Ethernet CPE Interface",
                    "ifName": "eth0_8",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [
                        {
                            "dot1dBasePort": 8,
                            "dot1dBasePortIfIndex": 8,
                            "dot1dBasePortCircuit": "0.0",
                            "dot1dBasePortDelayExceededDiscards": 0,
                            "dot1dBasePortMtuExceededDiscards": 0
                        }
                    ],
                    "dot1dTpPortEntry": [
                        {
                            "dot1dTpPort": 8,
                            "dot1dTpPortMaxInfo": 1500,
                            "dot1dTpPortInFrames": 39179,
                            "dot1dTpPortOutFrames": 7798,
                            "dot1dTpPortInDiscards": 0
                        }
                    ],
                    "dot1dTpFdbEntry": [
                        {
                            "dot1dTpFdbAddress": "ba:d5:c6:3b:0d:45",
                            "dot1dTpFdbPort": 8,
                            "dot1dTpFdbStatus": 4
                        }
                    ],
                    "ifStackEntry": []
                },
                "9": {
                    "ifType": 6,
                    "ifDescription": "Ethernet CPE Interface",
                    "ifName": "wlan0.0",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [
                        {
                            "dot1dBasePort": 9,
                            "dot1dBasePortIfIndex": 9,
                            "dot1dBasePortCircuit": "0.0",
                            "dot1dBasePortDelayExceededDiscards": 0,
                            "dot1dBasePortMtuExceededDiscards": 0
                        }
                    ],
                    "dot1dTpPortEntry": [
                        {
                            "dot1dTpPort": 9,
                            "dot1dTpPortMaxInfo": 1500,
                            "dot1dTpPortInFrames": 0,
                            "dot1dTpPortOutFrames": 1073,
                            "dot1dTpPortInDiscards": 0
                        }
                    ],
                    "dot1dTpFdbEntry": [
                        {
                            "dot1dTpFdbAddress": "b0:f5:30:b7:76:3c",
                            "dot1dTpFdbPort": 9,
                            "dot1dTpFdbStatus": 4
                        }
                    ],
                    "ifStackEntry": []
                },
                "10": {
                    "ifType": 6,
                    "ifDescription": "Ethernet CPE Interface",
                    "ifName": "wlan2.0",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [
                        {
                            "dot1dBasePort": 10,
                            "dot1dBasePortIfIndex": 10,
                            "dot1dBasePortCircuit": "0.0",
                            "dot1dBasePortDelayExceededDiscards": 0,
                            "dot1dBasePortMtuExceededDiscards": 0
                        }
                    ],
                    "dot1dTpPortEntry": [
                        {
                            "dot1dTpPort": 10,
                            "dot1dTpPortMaxInfo": 1500,
                            "dot1dTpPortInFrames": 24924499,
                            "dot1dTpPortOutFrames": 4552,
                            "dot1dTpPortInDiscards": 0
                        }
                    ],
                    "dot1dTpFdbEntry": [
                        {
                            "dot1dTpFdbAddress": "b0:f5:30:b7:76:31",
                            "dot1dTpFdbPort": 10,
                            "dot1dTpFdbStatus": 4
                        }
                    ],
                    "ifStackEntry": []
                },
                "11": {
                    "ifType": 6,
                    "ifDescription": "Ethernet CPE Interface",
                    "ifName": "wlan4.0",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [
                        {
                            "dot1dBasePort": 11,
                            "dot1dBasePortIfIndex": 11,
                            "dot1dBasePortCircuit": "0.0",
                            "dot1dBasePortDelayExceededDiscards": 0,
                            "dot1dBasePortMtuExceededDiscards": 0
                        }
                    ],
                    "dot1dTpPortEntry": [
                        {
                            "dot1dTpPort": 11,
                            "dot1dTpPortMaxInfo": 1500,
                            "dot1dTpPortInFrames": 0,
                            "dot1dTpPortOutFrames": 0,
                            "dot1dTpPortInDiscards": 0
                        }
                    ],
                    "dot1dTpFdbEntry": [
                        {
                            "dot1dTpFdbAddress": "b0:f5:30:b7:76:47",
                            "dot1dTpFdbPort": 11,
                            "dot1dTpFdbStatus": 4
                        }
                    ],
                    "ifStackEntry": []
                },
                "48": {
                    "ifType": 277,
                    "ifDescription": "RF Downstream Interface 1",
                    "ifName": "dsch2",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 48,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 48,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "49": {
                    "ifType": 277,
                    "ifDescription": "RF Downstream Interface 2",
                    "ifName": "dsch3",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 49,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 49,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "50": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 3",
                    "ifName": "dsch4",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 50,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 50,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "51": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 4",
                    "ifName": "dsch5",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 51,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 51,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "52": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 5",
                    "ifName": "dsch6",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 52,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 52,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "53": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 6",
                    "ifName": "dsch7",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 53,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 53,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "54": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 7",
                    "ifName": "dsch8",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 54,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 54,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "55": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 8",
                    "ifName": "dsch9",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 55,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 55,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "56": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 9",
                    "ifName": "dsch10",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 56,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 56,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "57": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 10",
                    "ifName": "dsch11",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 57,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 57,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "58": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 11",
                    "ifName": "dsch12",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 58,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 58,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "59": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 12",
                    "ifName": "dsch13",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 59,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 59,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "60": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 13",
                    "ifName": "dsch14",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 60,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 60,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "61": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 14",
                    "ifName": "dsch15",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 61,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 61,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "62": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 15",
                    "ifName": "dsch16",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 62,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 62,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "63": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 16",
                    "ifName": "dsch17",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 63,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 63,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "64": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 17",
                    "ifName": "dsch18",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 64,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 64,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "65": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 18",
                    "ifName": "dsch19",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 65,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 65,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "66": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 19",
                    "ifName": "dsch20",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 66,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 66,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "67": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 20",
                    "ifName": "dsch21",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 67,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 67,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "68": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 21",
                    "ifName": "dsch22",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 68,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 68,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "69": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 22",
                    "ifName": "dsch23",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 69,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 69,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "70": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 23",
                    "ifName": "dsch24",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 70,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 70,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "71": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 24",
                    "ifName": "dsch25",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 71,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 71,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "72": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 25",
                    "ifName": "dsch26",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 72,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 72,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "73": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 26",
                    "ifName": "dsch27",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 73,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 73,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "74": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 27",
                    "ifName": "dsch28",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 74,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 74,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "75": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 28",
                    "ifName": "dsch29",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 75,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 75,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "76": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 29",
                    "ifName": "dsch30",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 76,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 76,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "77": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 30",
                    "ifName": "dsch31",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 77,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 77,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "78": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 31",
                    "ifName": "dsch32",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 78,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 78,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "79": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface",
                    "ifName": "dsch1",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 79,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 79,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "80": {
                    "ifType": 129,
                    "ifDescription": "RF Upstream Interface 1",
                    "ifName": "usch2",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 80,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 80,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "81": {
                    "ifType": 129,
                    "ifDescription": "RF Upstream Interface 2",
                    "ifName": "usch3",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 81,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 81,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "82": {
                    "ifType": 129,
                    "ifDescription": "RF Upstream Interface 3",
                    "ifName": "usch4",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 82,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 82,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "83": {
                    "ifType": 129,
                    "ifDescription": "RF Upstream Interface 4",
                    "ifName": "usch5",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 83,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 83,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "84": {
                    "ifType": 278,
                    "ifDescription": "RF Upstream Interface 5",
                    "ifName": "usch6",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 84,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 84,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "112": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 33",
                    "ifName": "dsch34",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 112,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 112,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                },
                "113": {
                    "ifType": 128,
                    "ifDescription": "RF Downstream Interface 34",
                    "ifName": "dsch35",
                    "dot1dBase": [
                        {
                            "dot1dBaseBridgeAddress": "0x2e48a6452f48",
                            "dot1dBaseNumPorts": 9,
                            "dot1dBaseType": 2
                        }
                    ],
                    "dot1dBasePortEntry": [],
                    "dot1dTpPortEntry": [],
                    "dot1dTpFdbEntry": [],
                    "ifStackEntry": [
                        {
                            "ifStackHigherLayer": 2,
                            "ifStackLowerLayer": 113,
                            "ifStackStatus": 1
                        },
                        {
                            "ifStackHigherLayer": 113,
                            "ifStackLowerLayer": 0,
                            "ifStackStatus": 1
                        }
                    ]
                }
            }
        }
    }
}
````
</details>
