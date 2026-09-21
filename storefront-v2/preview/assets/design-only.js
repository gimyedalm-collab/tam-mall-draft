(() => {
  const header = document.querySelector('.do-header');
  const menuButton = document.querySelector('.mobile-nav-toggle');
  if (header && menuButton) {
    const setMenu = (open) => {
      header.toggleAttribute('data-nav-open', open);
      menuButton.setAttribute('aria-expanded', String(open));
    };
    menuButton.addEventListener('click', () => setMenu(!header.hasAttribute('data-nav-open')));
    header.querySelector('nav').addEventListener('click', (event) => {
      if (event.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && header.hasAttribute('data-nav-open')) {
        setMenu(false);
        menuButton.focus();
      }
    });
    document.addEventListener('pointerdown', (event) => {
      if (!header.contains(event.target)) setMenu(false);
    });
    matchMedia('(max-width:760px)').addEventListener('change', () => setMenu(false));
  }
  const video = document.querySelector('.do-hero video');
  const filmButton = document.querySelector('.film-toggle');
  if (!video || !filmButton) return;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const syncVideo = () => {
    filmButton.textContent = video.paused ? '영상 재생' : '영상 멈춤';
    filmButton.setAttribute('aria-label', video.paused ? '브랜드 영상 재생' : '브랜드 영상 일시정지');
    filmButton.setAttribute('aria-pressed', String(video.paused));
  };
  filmButton.addEventListener('click', () => {
    if (video.paused) video.play().catch(syncVideo); else video.pause();
  });
  video.addEventListener('play', syncVideo);
  video.addEventListener('pause', syncVideo);
  const applyMotion = () => { if (motion.matches) video.pause(); syncVideo(); };
  motion.addEventListener('change', applyMotion);
  if (motion.matches) { video.autoplay = false; video.pause(); }
  applyMotion();
})();
/* 전 페이지 공통: 따라다니는 카카오톡 채널 버튼 */
(function(){var s=document.createElement('script');s.src='assets/channel-button.js?v=1';s.defer=true;document.head.appendChild(s);})();
