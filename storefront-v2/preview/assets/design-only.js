(() => {
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
