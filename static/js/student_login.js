document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const msg = document.getElementById('msg');
  msg.textContent = '';
  try {
    const r = await fetch('/api/student/login', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ roll_no: fd.get('roll_no'), password: fd.get('password') }),
    });
    const data = await r.json();
    if (!r.ok) { msg.textContent = data.detail || 'Login failed'; return; }
    localStorage.setItem('student_token', data.access_token);
    localStorage.setItem('student_name', data.name);
    localStorage.setItem('student_roll', data.roll_no);
    window.location.href = data.has_selected ? '/token' : '/food';
  } catch (err) { msg.textContent = 'Network error'; }
});
