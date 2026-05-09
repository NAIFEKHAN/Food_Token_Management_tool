const token = localStorage.getItem('admin_token');
if (!token) window.location.href = '/admin/login';

const result = document.getElementById('result');
let scanner = null;
let busy = false;

function show(html) { result.innerHTML = html; }

async function verify(tokenId) {
  busy = true;
  try {
    const r = await fetch('/api/admin/verify-token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
      body: JSON.stringify({ token_id: tokenId }),
    });
    const d = await r.json();
    const cls = d.status === 'valid' ? 'success' : (d.status === 'already_used' ? 'warning' : 'danger');
    show(`<div class="alert alert-${cls}">
      <h5 class="mb-1">${d.message}</h5>
      ${d.name ? `<div><strong>${d.name}</strong> (${d.roll_no}) — ${d.food_type}</div>` : ''}
      <div class="small mt-1">Token: ${tokenId}</div></div>`);
  } catch (e) {
    show('<div class="alert alert-danger">Network error</div>');
  }
}

function start() {
  scanner = new Html5Qrcode('reader');
  scanner.start(
    { facingMode: 'environment' },
    { fps: 10, qrbox: 250 },
    async (decoded) => {
      if (busy) return;
      await scanner.stop();
      verify(decoded.trim());
    },
    () => {} // ignore per-frame errors
  ).catch((err) => show(`<div class="alert alert-danger">Camera error: ${err}</div>`));
}

document.getElementById('reset').addEventListener('click', async () => {
  busy = false; result.innerHTML = '';
  if (scanner) { try { await scanner.stop(); } catch(e) {} }
  start();
});

start();
