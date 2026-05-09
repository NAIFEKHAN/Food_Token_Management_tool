document.getElementById('adminLogin').addEventListener('submit', async (e) => {
  e.preventDefault(); // This must be the very first line
  
  const fd = new FormData(e.target);
  const msg = document.getElementById('msg');
  if (msg) msg.textContent = ''; // Ensure the element exists before writing to it

  try {
    const r = await fetch('/api/admin/login', {
      method: 'POST', 
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: fd.get('username'), password: fd.get('password') }),
    });
    
    const data = await r.json();
    if (!r.ok) { 
      if (msg) msg.textContent = data.detail || 'Login failed'; 
      return; 
    }
    
    localStorage.setItem('admin_token', data.access_token);
    window.location.href = '/admin/dashboard';
  } catch (error) {
    if (msg) msg.textContent = 'Connection error. Please try again.';
    console.error('Login Error:', error);
  }
});