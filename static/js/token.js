const token = localStorage.getItem('student_token');
if (!token) window.location.href = '/';

(async () => {
  const r = await fetch('/api/student/token', { headers: { 'Authorization': 'Bearer ' + token } });
  if (!r.ok) { window.location.href = '/food'; return; }
  const d = await r.json();
  document.getElementById('tName').textContent = d.name;
  document.getElementById('tRoll').textContent = d.roll_no;
  document.getElementById('tFood').textContent = d.food_type;
  document.getElementById('tToken').textContent = d.token_id;
  const img = document.getElementById('tQR');
  img.src = d.qr_code;
  const dlPng = document.getElementById('dlPng');
  dlPng.href = d.qr_code;
  dlPng.download = d.token_id + '.png';
})();

// PDF link needs auth header → fetch & blob
document.getElementById('dlPdf').addEventListener('click', async (e) => {
  e.preventDefault();
  const r = await fetch('/api/student/token.pdf', { headers: { 'Authorization': 'Bearer ' + token } });
  const blob = await r.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'token.pdf'; a.click();
  URL.revokeObjectURL(url);
});

document.getElementById('logout').addEventListener('click', () => {
  localStorage.clear(); window.location.href = '/';
});
