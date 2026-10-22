/* Native skin21 navigation and live catalog prices; no preview checkout handlers. */
(() => {
  'use strict';
  if (!document.body.classList.contains('tam-candidate-home')) return;
  const menu = document.querySelector('.ux-links');
  const toggle = document.querySelector('.ux-menu-toggle');
  const close = () => { menu?.classList.remove('is-open'); toggle?.setAttribute('aria-expanded', 'false'); };
  toggle?.addEventListener('click', () => {
    const open = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  menu?.addEventListener('click', e => { if (e.target.closest('a')) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu?.classList.contains('is-open')) { close(); toggle.focus(); } });
  document.addEventListener('pointerdown', e => { if (!e.target.closest('.ux-header')) close(); });
  matchMedia('(min-width:901px)').addEventListener('change', close);

  const cards = [...document.querySelectorAll('[data-native-product]')];
  const hydrate = async () => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 10000);
    try {
      const response = await fetch('/skin-skin21/product/list.html?cate_no=74', { signal: controller.signal });
      if (!response.ok) throw new Error('catalog unavailable');
      const catalog = new DOMParser().parseFromString(await response.text(), 'text/html');
      for (const card of cards) {
        const product = catalog.getElementById(`anchorBoxId_${card.dataset.nativeProduct}`);
        const price = product?.dataset.price;
        if (!price || !/^\d+(?:\.\d+)?$/.test(price)) continue;
        card.querySelector('.ux-product-price').textContent = Number(price).toLocaleString('ko-KR') + '원';
        card.dataset.priceSource = 'cafe24-native-catalog';
      }
    } catch (_) { /* The product link retains access to authoritative pricing. */ }
    finally { clearTimeout(timer); }
  };
  const section = document.querySelector('.do-products');
  if (section && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) { observer.disconnect(); hydrate(); }
    }, { rootMargin: '400px' });
    observer.observe(section);
  } else hydrate();
})();
