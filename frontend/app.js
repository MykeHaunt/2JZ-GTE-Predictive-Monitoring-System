// DOM references
const statusEl = document.getElementById('status');
const lastUpdateEl = document.getElementById('lastUpdate');
const readoutsEl = document.getElementById('readouts');

// Fetch and render loop
async function refresh() {
  try {
    const [sRes, aRes] = await Promise.all([
      fetch('/api/sensors'),
      fetch('/api/anomalies')
    ]);
    if (!sRes.ok || !aRes.ok) throw new Error('Network error');

    const sensors   = await sRes.json();
    const anomalies = await aRes.json();

    renderTiles(sensors, anomalies);

    const now = new Date();
    statusEl.textContent = 'Connected';
    lastUpdateEl.textContent = now.toLocaleTimeString();
  } catch (err) {
    statusEl.textContent = 'Error';
    console.error(err);
  }
}

// Build sensor tiles
function renderTiles(sensors, anomalies) {
  readoutsEl.innerHTML = '';
  sensors.forEach(({ id, name, value, unit }) => {
    const tile = document.createElement('div');
    tile.className = 'tile';

    const val    = document.createElement('h2');
    val.textContent = `${value.toFixed(0)}`;  // zero‑decimal for speed of reading

    const label  = document.createElement('p');
    label.textContent = name;

    tile.append(val, label);

    // only show anomaly if above 0.5
    const score = anomalies[id] ?? 0;
    if (score > 0.5) {
      const warn = document.createElement('div');
      warn.className = 'alert';
      warn.textContent = `⚠ ${score.toFixed(2)}`;
      tile.append(warn);
    }

    readoutsEl.append(tile);
  });
}

// Start polling every 1.5 s
setInterval(refresh, 1500);
refresh();