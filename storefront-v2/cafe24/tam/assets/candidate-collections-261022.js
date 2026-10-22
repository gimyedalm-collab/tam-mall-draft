/* Candidate collection views filter the native SHOP assortment, preserving SKUs. */
(() => {
  'use strict';
  if (!/^\/skin-skin21\/product\/list\.html$/.test(location.pathname)) return;
  const params = new URLSearchParams(location.search);
  const collection = params.get('tam_collection');
  const label = {jelly:'더 젤리',cloud:'더 클라우드'}[collection];
  if (!label || params.get('cate_no') !== '74') return;
  const list = document.querySelector('.xans-product-listnormal .prdList');
  if (!list) return;
  const heading = document.querySelector('.titleArea h2');
  if (heading) heading.textContent = label;
  const filter = () => {
    let count = 0;
    for (const item of list.children) {
      const name = item.querySelector('.name')?.textContent || '';
      if (name.includes(label)) { item.style.removeProperty('display'); count++; }
      else item.style.setProperty('display','none','important');
    }
    const counter = document.querySelector('.prdCount');
    if (counter) counter.textContent = `${count} items`;
  };
  filter();
  new MutationObserver(filter).observe(list,{childList:true});
  // Native sorting keeps its original semantics and the selected collection.
  for (const a of document.querySelectorAll('a[href*="sort_method="]')) {
    const url = new URL(a.href);
    if (url.origin !== location.origin || url.pathname !== location.pathname) continue;
    url.searchParams.set('tam_collection',collection);
    a.href = url.href;
  }
  document.body.dataset.tamCollection = collection;
})();
