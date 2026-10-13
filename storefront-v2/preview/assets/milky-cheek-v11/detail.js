(() => {
  const root = document.getElementById('milky-cheek-detail');
  if (!root) return;
  const video = root.querySelector('video');
  const button = root.querySelector('.mc-play');
  if (!video || !button) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let visible = false;
  let pausedByUser = false;
  video.controls = false;
  button.hidden = false;
  const sync = () => {
    button.textContent = video.paused ? '재생' : '일시정지';
    button.setAttribute('aria-label', video.paused ? '사용법 영상 재생' : '사용법 영상 일시정지');
    button.setAttribute('aria-pressed', String(!video.paused));
  };
  const play = () => video.play().catch(() => sync());
  const update = () => {
    if (visible && !document.hidden && !reduced.matches && !pausedByUser) play();
    else video.pause();
  };
  video.addEventListener('play', sync);
  video.addEventListener('pause', sync);
  button.addEventListener('click', () => {
    if (video.paused) { pausedByUser = false; play(); }
    else { pausedByUser = true; video.pause(); }
  });
  new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    update();
  }, { threshold: 0.25 }).observe(root.querySelector('.mc-film'));
  reduced.addEventListener('change', update);
  document.addEventListener('visibilitychange', update);
})();
