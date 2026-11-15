// AetherTune website interactions
(function () {
  'use strict';
  // Smooth anchor scrolling via Lenis if available
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      if (id.length > 1) {
        const el = document.querySelector(id);
        if (el) { e.preventDefault(); el.scrollIntoView({ behavior: 'smooth' }); }
      }
    });
  });

  // Theme toggle (light/dark) stored in localStorage
  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      document.body.classList.toggle('light');
      localStorage.setItem('theme', document.body.classList.contains('light') ? 'light' : 'dark');
    });
    if (localStorage.getItem('theme') === 'light') document.body.classList.add('light');
  }
})();
