document.addEventListener('DOMContentLoaded', () => {

  // Mobile burger menu
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav');
  if (burger) {
    burger.addEventListener('click', () => {
      nav.classList.toggle('open');
      burger.classList.toggle('open');
    });
    document.querySelectorAll('.nav a').forEach(link => {
      link.addEventListener('click', () => nav.classList.remove('open'));
    });
  }

  // Active nav link
  const current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a').forEach(link => {
    if (link.getAttribute('href') === current) {
      link.classList.add('active');
    }
  });

  // Fade-in on scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

  // Menu tabs
  const tabs = document.querySelectorAll('.menu-tab');
  const items = document.querySelectorAll('.menu-item');
  if (tabs.length) {
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const filter = tab.dataset.filter;
        items.forEach(item => {
          if (filter === 'all' || item.dataset.category === filter) {
            item.style.display = 'flex';
          } else {
            item.style.display = 'none';
          }
        });
      });
    });
  }

  // Contact form
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      const original = btn.textContent;
      btn.textContent = '✓ Отправлено!';
      btn.style.background = '#4CAF50';
      setTimeout(() => {
        btn.textContent = original;
        btn.style.background = '';
        form.reset();
      }, 2500);
    });
  }

});
