/* Opt-in UI. Preview adapter below never submits a real order or issues coupons. */
(() => {
  'use strict';
  const preview = document.body.hasAttribute('data-tam-purchase-preview');
  const config = window.TAM_PURCHASE_CONFIG || (preview ? {
    channelUrl: 'https://pf.kakao.com/_nxhIxhn', popupEnabled: true,
    popupDelay: 12000, couponAmount: 3000, dispatch: { enabled: false }
  } : null);
  if (!config || !window.TamPurchasePolicy) return;
  const policy = window.TamPurchasePolicy;
  const detail = document.querySelector('[data-preview-product]');
  const create = (tag, cls, text) => {
    const el = document.createElement(tag); el.className = cls;
    if (text) el.textContent = text; return el;
  };
  const info = create('div', 'tam-purchase-info');
  if (preview && detail) {
    document.body.classList.add('tam-purchase');
    const product = (window.TAM_CATALOG || []).find(p => p.id === Number(detail.dataset.previewProduct));
    const shippingText = create('p', 'tam-shipping-text');
    const progress = create('progress', 'tam-shipping-progress');
    progress.max = 30000; progress.setAttribute('aria-label', '무료배송 기준까지 선택한 상품 금액');
    const note = create('small', '', '상품 할인 적용 후, 쿠폰 사용 전 금액 기준 · 3만원 이상 무료배송');
    const update = () => {
      const select = detail.querySelector('select'), qty = Number(detail.querySelector('input[type=number]').value);
      const subtotal = select.value && Number.isInteger(qty) && qty >= 1 && qty <= 99 && product ? product.price * qty : 0;
      const state = policy.shipping(subtotal);
      shippingText.textContent = subtotal === 0 ? '배송비 3,000원 · 3만원 이상 무료배송' :
        state.remaining > 0 ? `${state.remaining.toLocaleString('ko-KR')}원 더 담으면 무료배송` : '무료배송 · 쿠폰을 사용해도 유지됩니다';
      progress.value = Math.min(subtotal, 30000);
    };
    info.append(shippingText, progress, note);
    const dispatch = create('p', 'tam-dispatch-title', '평일 오후 2시 이전 결제 완료 시 당일 출고');
    dispatch.style.marginTop = '16px';
    info.append(dispatch, create('small', '', '출고 안내 미리보기 · 주말·공휴일 및 예약·품절 상품 제외'));
    detail.before(info);
    detail.addEventListener('input', update); detail.addEventListener('change', update); update();
  }
  // Native skin supplies stock eligibility and a verified fulfillment calendar.
  const nativeDispatch = document.querySelector('[data-tam-dispatch]');
  if (!preview && nativeDispatch) {
    const updateDispatch = () => {
      const state = policy.dispatch(new Date(), config.dispatch);
      nativeDispatch.textContent = state.title; nativeDispatch.dataset.state = state.state;
    };
    updateDispatch(); setInterval(updateDispatch, 30000);
    document.addEventListener('visibilitychange', updateDispatch);
  }
  if (!config.popupEnabled || !/^https:\/\/pf\.kakao\.com\/[\w-]+\/?$/.test(config.channelUrl || '')) return;
  // Never automatically solicit during cart, checkout or account tasks.
  if (/(basket|checkout|orderform|login|join|coupon|myshop)/i.test(location.pathname)) return;
  // Preview follows the current product-page offer. Live amounts need admin confirmation.
  const amount = Number.isInteger(config.couponAmount) && config.couponAmount > 0 &&
    (preview || config.couponAmountVerified === true) ? config.couponAmount.toLocaleString('ko-KR') + '원' : null;
  const panel = create('aside', 'tam-channel-panel'); panel.hidden = true;
  panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-modal', 'false');
  panel.setAttribute('aria-labelledby', 'tam-channel-title');
  const close = create('button', 'tam-channel-close', '닫기'); close.type = 'button';
  const label = create('p', 'tam-channel-label', 'TAM BEAUTY');
  const title = create('h2', '', amount ? `채널 추가 시 ${amount} 쿠폰` : '카카오톡 채널 쿠폰'); title.id = 'tam-channel-title';
  const copy = create('p', 'tam-channel-copy', amount ?
    `탐뷰티 카카오톡 채널 추가 시 ${amount} 쿠폰.\n사용 조건은 채널 쿠폰 안내에서 확인해 주세요.` :
    '탐뷰티 카카오톡 채널에서 쿠폰과 사용 조건을 확인해 주세요.');
  const link = create('a', 'tam-channel-link', '채널 추가하고 쿠폰 받기');
  link.href = config.channelUrl; link.target = '_blank'; link.rel = 'noopener noreferrer';
  link.setAttribute('aria-label', '카카오톡 채널 추가하고 쿠폰 받기 (새 창)');
  const snooze = create('button', 'tam-channel-snooze', '24시간 보지 않기'); snooze.type = 'button';
  panel.append(close, label, title, copy, link, snooze); document.body.append(panel);
  const key = 'tam-channel-prompt-v1'; let shown = false, opener = null;
  const read = (storage, suffix) => { try { return window[storage].getItem(key + suffix); } catch { return null; } };
  const write = (storage, suffix, value) => { try { window[storage].setItem(key + suffix, value); } catch {} };
  const hide = () => { panel.hidden = true; if (panel.contains(document.activeElement)) opener?.focus(); };
  const show = manual => {
    if (!panel.hidden) return;
    opener = document.activeElement; panel.hidden = false; shown = true;
    write('sessionStorage', '-shown', '1');
    if (manual) close.focus();
  };
  close.addEventListener('click', hide);
  snooze.addEventListener('click', () => { write('localStorage', '-until', String(Date.now() + 86400000)); hide(); });
  link.addEventListener('click', () => { write('localStorage', '-until', String(Date.now() + 86400000)); hide(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !panel.hidden) hide(); });
  const trigger = create('button', 'tam-channel-trigger'); trigger.type = 'button';
  const mark = create('span', 'tam-channel-mark', '카카오톡');
  const benefit = create('span', 'tam-channel-benefit');
  benefit.append(create('span', 'tam-channel-condition', '채널 추가 시'),
    create('strong', 'tam-channel-value', amount ? `${amount} 쿠폰` : '쿠폰 혜택 확인'));
  const arrow = create('span', 'tam-channel-arrow', '→'); arrow.setAttribute('aria-hidden', 'true');
  trigger.append(mark, benefit, arrow);
  trigger.setAttribute('aria-label', amount ? `카카오톡 채널 추가 시 ${amount} 쿠폰 안내 열기` : '카카오톡 채널 쿠폰 안내 열기');
  trigger.setAttribute('aria-haspopup', 'dialog'); trigger.addEventListener('click', () => show(true));
  const triggerHost = info.isConnected ? info : document.querySelector('[data-tam-channel-trigger-host], .do-footer, footer');
  if (triggerHost) triggerHost.append(trigger);
  if (read('sessionStorage', '-shown') || Number(read('localStorage', '-until')) > Date.now()) return;
  const started = Date.now();
  const attempt = () => {
    if (shown || read('sessionStorage', '-shown') || Number(read('localStorage', '-until')) > Date.now()) return;
    if (Date.now() - started < (config.popupDelay ?? 12000) || document.hidden || scrollY < 320) return;
    if (document.activeElement?.matches('input,select,textarea,button')) return;
    if (document.querySelector('dialog[open], [aria-modal="true"]:not([hidden]), .mobile-nav.open, .do-header[data-nav-open]')) return;
    const protectedArea = document.querySelector('.detail-product, .xans-product-detail, .do-hero');
    if (protectedArea && protectedArea.getBoundingClientRect().bottom > 0) return;
    show(false);
  };
  const timer = setInterval(() => { attempt(); if (shown) clearInterval(timer); }, 1000);
})();
