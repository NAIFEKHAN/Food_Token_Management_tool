const token = localStorage.getItem('admin_token');
if (!token) window.location.href = '/admin/login';
const auth = { 'Authorization': 'Bearer ' + token };

let chartFood, chartStatus;

async function loadStats() {
  const r = await fetch('/api/admin/stats', { headers: auth });
  if (r.status === 401) { localStorage.clear(); window.location.href = '/admin/login'; return; }
  const s = await r.json();
  sTotal.textContent = s.total; sVeg.textContent = s.veg; sNon.textContent = s.non_veg;
  sNot.textContent = s.not_selected; sUsed.textContent = s.used; sUnused.textContent = s.unused;

  const fdata = { labels: ['Veg', 'Non-Veg', 'Not Selected'], datasets: [{
    data: [s.veg, s.non_veg, s.not_selected],
    backgroundColor: ['#1f7a3a', '#a23030', '#666']
  }]};
  const sdata = { labels: ['Used', 'Unused'], datasets: [{
    data: [s.used, s.unused], backgroundColor: ['#555', '#d4af37']
  }]};
  if (chartFood) chartFood.destroy();
  if (chartStatus) chartStatus.destroy();
  chartFood = new Chart(document.getElementById('chartFood'),
    { type: 'doughnut', data: fdata, options: { plugins: { legend: { labels: { color: '#eee' }}}}});
  chartStatus = new Chart(document.getElementById('chartStatus'),
    { type: 'doughnut', data: sdata, options: { plugins: { legend: { labels: { color: '#eee' }}}}});
}

async function loadStudents() {
  const q = document.getElementById('search').value;
  const food = document.getElementById('filterFood').value;
  const params = new URLSearchParams();
  if (q) params.set('q', q);
  if (food) params.set('food', food);
  const r = await fetch('/api/admin/students?' + params, { headers: auth });
  const rows = await r.json();
  const tbody = document.getElementById('tbody');
  tbody.innerHTML = rows.map((s, i) => `
    <tr>
      <td>${i + 1}</td>
      <td>${s.name}</td>
      <td>${s.roll_no}</td>
      <td>${s.food_type ? `<span class="badge ${s.food_type === 'Veg' ? 'badge-veg' : 'badge-nonveg'}">${s.food_type}</span>` : '<span class="text-secondary">—</span>'}</td>
      <td>${s.token_id || '—'}</td>
      <td>${s.token_id ? `<span class="badge ${s.token_status === 'Used' ? 'badge-used' : 'badge-unused'}">${s.token_status}</span>` : '—'}</td>
    </tr>`).join('');
}

document.getElementById('search').addEventListener('input', loadStudents);
document.getElementById('filterFood').addEventListener('change', loadStudents);
document.getElementById('reload').addEventListener('click', () => { loadStats(); loadStudents(); });

document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const r = await fetch('/api/admin/upload-excel', { method: 'POST', headers: auth, body: fd });
  const data = await r.json();
  document.getElementById('uploadMsg').textContent = r.ok
    ? `Inserted ${data.inserted}, skipped ${data.skipped_duplicates} duplicates.`
    : (data.detail || 'Upload failed');
  loadStats(); loadStudents();
});

document.getElementById('exportBtn').addEventListener('click', async (e) => {
  e.preventDefault();
  const r = await fetch('/api/admin/export-excel', { headers: auth });
  const blob = await r.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'students_tokens.xlsx'; a.click();
  URL.revokeObjectURL(url);
});

document.getElementById('logout').addEventListener('click', () => {
  localStorage.removeItem('admin_token'); window.location.href = '/admin/login';
});

loadStats(); loadStudents();
