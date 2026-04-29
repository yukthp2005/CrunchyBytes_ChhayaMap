const map = L.map('map', { zoomControl: false }).setView([12.302, 76.643], 15);
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(map);

let startPt, endPt, startMarker, endMarker, coolRoute, stdRoute, auditCoords, targetMarker, heatLayer;
let clickMode = 'target';

function setMode(m) { clickMode = m; }

map.on('click', (e) => {
    if (clickMode === 'start') {
        startPt = e.latlng;
        if (startMarker) map.removeLayer(startMarker);
        startMarker = L.marker(startPt, {icon: L.divIcon({className: 'marker-a', html: 'A'})}).addTo(map);
        document.getElementById('start-input').value = `A: ${startPt.lat.toFixed(3)}`;
        setMode('target');
    } else if (clickMode === 'end') {
        endPt = e.latlng;
        if (endMarker) map.removeLayer(endMarker);
        endMarker = L.marker(endPt, {icon: L.divIcon({className: 'marker-b', html: 'B'})}).addTo(map);
        document.getElementById('end-input').value = `B: ${endPt.lat.toFixed(3)}`;
        setMode('target');
    } else {
        auditCoords = e.latlng;
        if (targetMarker) map.removeLayer(targetMarker);
        targetMarker = L.circleMarker(auditCoords, {color: 'red', radius: 8}).addTo(map);
        document.getElementById('audit-target').innerText = `TARGET: ${auditCoords.lat.toFixed(4)}`;
    }
});

async function getBalancedRoute() {
    if (!startPt || !endPt) return alert("Mark A & B.");
    const sens = document.getElementById('sens-slider').value / 100;
    const res = await fetch(`/get-cool-route?s_lat=${startPt.lat}&s_lng=${startPt.lng}&e_lat=${endPt.lat}&e_lng=${endPt.lng}&sens=${sens}`);
    const data = await res.json();
    if (coolRoute) map.removeLayer(coolRoute);
    if (stdRoute) map.removeLayer(stdRoute);
    stdRoute = L.polyline(data.std_path, {color: '#70757a', weight: 2, dashArray: '5,10'}).addTo(map);
    coolRoute = L.polyline(data.cool_path, {color: '#1a73e8', weight: 6}).addTo(map);
    document.getElementById('uv-val').innerText = data.metrics.uv;
    document.getElementById('route-res').style.display = 'block';
    map.fitBounds(coolRoute.getBounds());
}

async function loadLeaderboard() {
    const res = await fetch('/get-leaderboard');
    const data = await res.json();
    const list = document.getElementById('leaderboard-list');
    list.innerHTML = data.map((w, i) => `
        <div style="font-size:0.75rem; margin-bottom:5px;">
            <strong>${i+1}. ${w.name}</strong> <span style="float:right; color:red;">${w.risk_score}</span>
            <div style="height:4px; background:#eee; margin-top:2px;"><div style="width:${w.risk_score}%; background:red; height:100%;"></div></div>
        </div>`).join("");
}

async function runSimulation() {
    const ward = document.getElementById('sim-ward').value;
    const count = document.getElementById('sim-count').value;
    const res = await fetch('/simulate', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ward, count})
    });
    const data = await res.json();
    document.getElementById('sim-res').style.display = 'block';
    document.getElementById('res-temp').innerText = data.temp;
    document.getElementById('res-roi').innerText = data.roi;
    // Visual Tree Planting
    L.circle(map.getCenter(), {color:'green', radius: count*0.8}).addTo(map).bindPopup(`${count} Trees Planted`).openPopup();
}

async function uploadEvidence() {
    const file = document.getElementById('evidence-file').files[0];
    const formData = new FormData();
    formData.append('image', file); formData.append('lat', auditCoords.lat); formData.append('lng', auditCoords.lng);
    await fetch('/report-heat', { method: 'POST', body: formData });
    refreshHeatmap();
}

async function refreshHeatmap() {
    const res = await fetch('/get-map-data');
    const data = await res.json();
    if (heatLayer) map.removeLayer(heatLayer);
    heatLayer = L.heatLayer(data.map(p => [p.lat, p.lng, (100-p.shade)/100]), {radius:30, blur:15}).addTo(map);
}

loadLeaderboard();
refreshHeatmap()