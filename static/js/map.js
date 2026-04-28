// Initialize Tactical Map
const map = L.map('map', { zoomControl: false }).setView([12.2958, 76.6394], 14);

// Tactical Dark Tiles
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png').addTo(map);

let selectedCoords = null;
let targetMarker = null;

// Map click listener for targeting
map.on('click', (e) => {
    selectedCoords = e.latlng;
    document.getElementById('coords-label').innerText = `${selectedCoords.lat.toFixed(4)}, ${selectedCoords.lng.toFixed(4)}`;
    
    if (targetMarker) map.removeLayer(targetMarker);
    targetMarker = L.circleMarker(selectedCoords, { color: '#ff3131', radius: 10 }).addTo(map);
});

async function uploadEvidence() {
    const fileInput = document.getElementById('imageInput');
    if (!selectedCoords || !fileInput.files[0]) return alert("LOCK TARGET & SELECT IMAGE");

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    formData.append('lat', selectedCoords.lat);
    formData.append('lng', selectedCoords.lng);

    const res = await fetch('/report-heat', { method: 'POST', body: formData });
    const result = await res.json();
    
    // Simulate "Useful" Data Update
    document.getElementById('uv-saved').innerText = (Math.random() * 40 + 30).toFixed(0) + "%";
    document.getElementById('dist-cool').innerText = "1.4 km";
    document.getElementById('dist-std').innerText = "1.2 km";
    document.querySelector('.hidden')?.classList.remove('hidden');

    alert(`ANALYSIS COMPLETE: ${result.risk} RISK`);
    location.reload(); // Refresh to see the new heatmap point
}