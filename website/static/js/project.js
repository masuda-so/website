document.addEventListener('DOMContentLoaded', () => {
  const root = document.documentElement;
  const header = document.querySelector('[data-header]');
  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');
  const mobileQuery = window.matchMedia('(max-width: 900px)');

  const updateHeader = () => header?.classList.toggle('scrolled', window.scrollY > 30);
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  if (menuButton && nav) {
    const setMenuState = (isOpen, restoreFocus = false) => {
      nav.classList.toggle('open', isOpen);
      menuButton.setAttribute('aria-expanded', String(isOpen));
      menuButton.setAttribute('aria-label', isOpen ? 'メニューを閉じる' : 'メニューを開く');
      document.body.classList.toggle('menu-open', isOpen);

      if (isOpen) {
        window.requestAnimationFrame(() => nav.querySelector('a')?.focus());
      } else if (restoreFocus) {
        menuButton.focus();
      }
    };

    menuButton.addEventListener('click', () => {
      setMenuState(menuButton.getAttribute('aria-expanded') !== 'true');
    });

    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => setMenuState(false));
    });

    document.addEventListener('keydown', event => {
      const menuIsOpen = menuButton.getAttribute('aria-expanded') === 'true';
      if (event.key === 'Escape' && menuIsOpen) {
        setMenuState(false, true);
        return;
      }

      if (event.key === 'Tab' && menuIsOpen) {
        const focusableElements = [menuButton, ...nav.querySelectorAll('a')];
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (event.shiftKey && document.activeElement === firstElement) {
          event.preventDefault();
          lastElement.focus();
        } else if (!event.shiftKey && document.activeElement === lastElement) {
          event.preventDefault();
          firstElement.focus();
        }
      }
    });

    const resetMenuAtDesktop = event => {
      if (!event.matches) setMenuState(false);
    };
    if (mobileQuery.addEventListener) {
      mobileQuery.addEventListener('change', resetMenuAtDesktop);
    } else {
      mobileQuery.addListener(resetMenuAtDesktop);
    }
    root.classList.add('menu-ready');
  }

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealElements = [...document.querySelectorAll('.reveal')];
  const counters = [...document.querySelectorAll('[data-count]')];

  const showImmediately = () => {
    root.classList.remove('motion-ready');
    revealElements.forEach(element => element.classList.add('visible'));
    counters.forEach(counter => {
      counter.textContent = Number(counter.dataset.count).toLocaleString('ja-JP');
    });
  };

  const animateCounter = element => {
    if (element.dataset.done) return;
    element.dataset.done = 'true';
    const target = Number(element.dataset.count);
    if (!Number.isFinite(target)) return;

    element.textContent = '0';
    const start = performance.now();
    const duration = 1400;
    const tick = now => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      element.textContent = Math.floor(target * eased).toLocaleString('ja-JP');
      if (progress < 1) window.requestAnimationFrame(tick);
    };
    window.requestAnimationFrame(tick);
  };

  if (!reducedMotion && 'IntersectionObserver' in window) {
    try {
      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('visible');
          const counter = entry.target.matches('[data-count]')
            ? entry.target
            : entry.target.querySelector('[data-count]');
          if (counter) animateCounter(counter);
          observer.unobserve(entry.target);
        });
      }, { threshold: 0.15 });

      root.classList.add('motion-ready');
      revealElements.forEach(element => observer.observe(element));
    } catch (error) {
      showImmediately();
    }
  } else {
    showImmediately();
  }

  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const projectCards = [...document.querySelectorAll('[data-category]')];
  const filterStatus = document.querySelector('[data-filter-status]');

  const applyFilter = selectedButton => {
    const selectedFilter = selectedButton.dataset.filter;
    filterButtons.forEach(button => {
      const isSelected = button === selectedButton;
      button.classList.toggle('active', isSelected);
      button.setAttribute('aria-pressed', String(isSelected));
    });

    projectCards.forEach(card => {
      card.hidden = selectedFilter !== 'all' && card.dataset.category !== selectedFilter;
      card.classList.remove('wide');
    });

    const visibleCards = projectCards.filter(card => !card.hidden);
    if (visibleCards.length === 1) visibleCards[0].classList.add('wide');
    if (filterStatus) filterStatus.textContent = `${visibleCards.length}つの事業領域を表示中`;
  };

  filterButtons.forEach(button => {
    button.addEventListener('click', () => applyFilter(button));
  });

  const activeFilter = filterButtons.find(button => button.classList.contains('active'));
  if (activeFilter) {
    applyFilter(activeFilter);
    root.classList.add('filter-ready');
  }
});
