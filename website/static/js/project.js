document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('[data-header]');
  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');

  window.addEventListener('scroll', () => header?.classList.toggle('scrolled', window.scrollY > 30), { passive: true });
  menuButton?.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
  });
  nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    nav.classList.remove('open');
    menuButton?.setAttribute('aria-expanded', 'false');
  }));

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('visible');
      const counter = entry.target.querySelector?.('[data-count]') || (entry.target.matches?.('[data-count]') ? entry.target : null);
      if (counter && !counter.dataset.done) animateCounter(counter);
      observer.unobserve(entry.target);
    });
  }, { threshold: .15 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  function animateCounter(element) {
    element.dataset.done = 'true';
    const target = Number(element.dataset.count);
    if (reducedMotion) { element.textContent = target.toLocaleString('ja-JP'); return; }
    const start = performance.now();
    const duration = 1400;
    const tick = now => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      element.textContent = Math.floor(target * eased).toLocaleString('ja-JP');
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('[data-filter]').forEach(item => item.classList.toggle('active', item === button));
    document.querySelectorAll('[data-category]').forEach(card => {
      card.classList.toggle('hidden', button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter);
    });
  }));
});
