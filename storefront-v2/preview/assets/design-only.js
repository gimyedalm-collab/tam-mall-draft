(() => {
  const band = document.querySelector('.do-marquee');
  const group = band.querySelector('.marquee-group');
  const track = band.querySelector('.marquee-track');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const button = band.querySelector('button');
  const measure = () => {
    // Identical groups; travel one group at 22 CSS pixels per second.
    track.style.setProperty('--marquee-duration', String(group.getBoundingClientRect().width / 22) + 's');
    band.dataset.ready = 'true';
  };
  document.fonts.ready.then(() => { measure(); new ResizeObserver(measure).observe(group); });
  button.addEventListener('click', () => {
    const paused = band.dataset.paused !== 'true';
    band.dataset.paused = String(paused);
    button.setAttribute('aria-pressed', String(paused));
    button.setAttribute('aria-label', paused ? '흐르는 문구 재생' : '흐르는 문구 일시정지');
    button.textContent = paused ? '▷' : 'Ⅱ';
  });
  const video = document.querySelector('.do-hero video');
  const filmButton = document.querySelector('.film-toggle');
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
