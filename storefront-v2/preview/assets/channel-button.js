/* 전 페이지 공통: 화면을 따라다니는 카카오톡 채널 버튼 (2026-09-21)
   운영 몰의 오른쪽 아래 퀵메뉴 채널 버튼을 그대로 잇는다. tam.js / design-only.js 가 이 파일을 불러온다.
   카페24에서는 스킨 레이아웃(또는 기존 배너매니저 퀵메뉴)이 이 자리를 맡는다. */
(function () {
  var CHANNEL_URL = 'https://pf.kakao.com/_nxhIxhn';
  if (document.querySelector('.tam-channel-fab')) return;

  var style = document.createElement('style');
  style.textContent =
    '.tam-channel-fab{position:fixed;right:24px;bottom:24px;z-index:39;display:flex;align-items:center;justify-content:center;' +
    'width:52px;height:52px;border-radius:50%;background:#fee500;box-shadow:0 6px 18px rgba(0,0,0,.14);transition:transform .15s ease}' +
    '.tam-channel-fab:hover{transform:translateY(-2px)}' +
    '.tam-channel-fab:focus-visible{outline:2px solid #181818;outline-offset:3px}' +
    '.tam-channel-fab svg{width:30px;height:30px;display:block}' +
    /* 채널 안내 패널이 같은 구석에 떠 있는 동안에는 숨김 */
    'body:has(.tam-channel-panel:not([hidden])) .tam-channel-fab{display:none}' +
    '@media (max-width:760px){.tam-channel-fab{right:16px;bottom:calc(16px + env(safe-area-inset-bottom));width:48px;height:48px}' +
    '.tam-channel-fab svg{width:28px;height:28px}}' +
    '@media (prefers-reduced-motion:reduce){.tam-channel-fab{transition:none}.tam-channel-fab:hover{transform:none}}' +
    '@media print{.tam-channel-fab{display:none}}';
  document.head.appendChild(style);

  var link = document.createElement('a');
  link.className = 'tam-channel-fab';
  link.href = CHANNEL_URL;
  link.target = '_blank';
  link.rel = 'noopener';
  link.setAttribute('aria-label', '카카오톡 채널 추가 (새 창)');
  link.innerHTML =
    '<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false">' +
    '<path fill="#191919" d="M16 5C9.4 5 4 9.3 4 14.5c0 3.3 2.2 6.3 5.6 8l-1.1 4.1c-.1.5.4.8.8.6l4.9-3.2c.6.1 1.2.1 1.8.1 6.6 0 12-4.3 12-9.6S22.6 5 16 5z"/>' +
    '<text x="16" y="18.4" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="9.5" font-weight="700" fill="#fee500">Ch</text>' +
    '</svg>';
  document.body.appendChild(link);
})();
