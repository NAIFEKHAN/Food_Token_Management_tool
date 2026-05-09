const token = localStorage.getItem('student_token');
if (!token) window.location.href = '/';
document.getElementById('sName').textContent = localStorage.getItem('student_name') || '';
document.getElementById('sRoll').textContent = localStorage.getItem('student_roll') || '';

document.querySelectorAll('button[data-food]').forEach(btn => {
  btn.addEventListener('click', async () => {
    const msg = document.getElementById('msg');
    msg.textContent = '';
    if (!confirm(`Confirm ${btn.dataset.food}? You cannot change this later.`)) return;
    try {
      const r = await fetch('/api/student/select-food', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
        body: JSON.stringify({ food_type: btn.dataset.food }),
      });
      const data = await r.json();
      if (!r.ok) { msg.textContent = data.detail || 'Failed'; return; }
      window.location.href = '/token';
    } catch (e) { msg.textContent = 'Network error'; }
  });
});
