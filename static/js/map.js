const map = L.map('map', { zoomControl: false }).setView([12.3051, 76.6551], 14);
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(map);

let heatLayer, startPt, endPt, startMarker, endMarker, coolRoute, stdRoute, clickMode = 'target';

async function init() {
    const resH = await fetch('/get-map-data');
    const dataH = await resH.json();
    heatLayer = L.heatLayer(dataH.map(p => [p.lat, p.lng, (100-p.shade)/100]), {
        radius: 35, blur: 15, gradient: {0.4: '#1a73e8', 0.6: '#fbbc04', 1.0: '#ea4335'}
    }).addTo(map);

    const resL = await fetch('/get-leaderboard');
    const wards = await resL.json();
    const list = document.getElementById('leaderboard-list');
    wards.forEach((w, i) => {
        list.innerHTML += `
            <div class="ward-card">
                <div style="display:flex; justify-content:space-between;"><strong>${i+1}. ${w.name}</strong> <span>${w.risk_score}</span></div>
                <div class="bar-bg"><div class="bar-fill" style="width:${w.risk_score}%"></div></div>
            </div>`;
    });
}

function setMode(m) { clickMode = m; }

map.on('click', (e) => {
    if (clickMode === 'start') {
        startPt = e.latlng;
        if (startMarker) map.removeLayer(startMarker);
        startMarker = L.marker(startPt).addTo(map);
        document.getElementById('start-input').value = startPt.lat.toFixed(3);
        setMode('target');
    } else if (clickMode === 'end') {
        endPt = e.latlng;
        if (endMarker) map.removeLayer(endMarker);
        endMarker = L.marker(endPt).addTo(map);
        document.getElementById('end-input').value = endPt.lat.toFixed(3);
        setMode('target');
    }
});

async function getRoute() {
    if(!startPt || !endPt) return alert("Select start and end points.");
    const sens = document.getElementById('sens-slider').value / 100;
    const res = await fetch(`/get-cool-route?s_lat=${startPt.lat}&e_lat=${endPt.lat}&sens=${sens}`);
    const data = await res.json();
    
    if (coolRoute) map.removeLayer(coolRoute);
    if (stdRoute) map.removeLayer(stdRoute);

    stdRoute = L.polyline(data.std_path, {color: '#70757a', weight: 2, dashArray: '5, 10'}).addTo(map);
    coolRoute = L.polyline(data.cool_path, {color: '#1a73e8', weight: 6}).addTo(map);
    
    document.getElementById('uv-score').innerText = data.uv_reduction + " Coolers";
    document.getElementById('steps-ul').innerHTML = data.directions.map(s => `<li>${s}</li>`).join("");
    document.getElementById('route-data').style.display = 'block';
    map.fitBounds(coolRoute.getBounds());
}

async function runSimulation() {
    const ward = document.getElementById('sim-ward').value;
    const count = document.getElementById('sim-count').value;
    const res = await fetch('/simulate', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ward, count})
    });
    const data = await res.json();
    document.getElementById('sim-impact').style.display = 'block';
    document.getElementById('res-temp').innerText = data.temp_reduction;
    document.getElementById('res-roi').innerText = data.energy_roi;
    L.circle(map.getCenter(), {color: 'green', radius: count*1.5}).addTo(map).bindPopup(`${count} Simulated Trees`).openPopup();
}

async function runAudit() {
    const res = await fetch('/audit-albedo', { method: 'POST' });
    const data = await res.json();
    alert(`AUDIT RESULT: ${data.status}\n${data.roi}`);
}

init();