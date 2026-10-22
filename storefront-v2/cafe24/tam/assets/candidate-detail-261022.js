/* Candidate-only delivery preview; native options, cart and Snap stay intact.
 * Product25 is intentionally excluded until its 00 gloss/oil composition is
 * reconciled. Product-description registration remains a separate live step.
 */
(() => {
  'use strict';
  if (!/^\/skin-skin21(?:\/|$)/.test(location.pathname)) return;
  const target = document.getElementById('tam-candidate-detail');
  if (!target) return;
  const query = new URL(location.href).searchParams.get('product_no');
  const path = location.pathname.match(/\/product\/[^/]+\/(\d+)(?:\/|$)/);
  const product = Number(query || path?.[1]);
  if (![24, 102, 109, 110, 111, 118].includes(product)) return;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  target.dataset.deliveryStatus = 'loading';
  fetch(`/tam-detail-20261022/product-${product}.html`, {signal: controller.signal})
    .then(response => {
      if (!response.ok) throw new Error('Detail unavailable');
      return response.text();
    })
    .then(html => {
      const fragment = document.createElement('template');
      fragment.innerHTML = html;
      const media = [...fragment.content.querySelectorAll('img')];
      if (!media.length || fragment.content.querySelector('script,iframe,object,form') ||
          media.some(img => !img.getAttribute('src')?.startsWith(`/tam-detail-20261022/p${product}-`))) {
        throw new Error('Unexpected detail content');
      }
      target.replaceChildren(fragment.content);
      target.dataset.deliveryStatus = 'ready';
      target.dataset.deliveryProduct = String(product);
    })
    .catch(() => { target.dataset.deliveryStatus = 'original-fallback'; })
    .finally(() => clearTimeout(timeout));
})();
