(() => {
  const video = document.querySelector('#texture-film');
  const button = document.querySelector('#cloud-blush .film-toggle');
  if (!video || !button) return;
  const stages = [...document.querySelectorAll('#cloud-blush .texture-stages li')];
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let inView = false;
  let userPaused = false;
  const canAutoplay = () => !reducedMotion.matches && !navigator.connection?.saveData;
  const play = async () => {
    try { await video.play(); }
    catch { button.textContent = '영상 재생'; }
  };
  video.controls = false;
  button.hidden = false;
  button.addEventListener('click', () => {
    if (video.paused) { userPaused = false; play(); }
    else { userPaused = true; video.pause(); }
  });
  const updateButton = () => {
    button.textContent = video.paused ? '영상 재생' : '일시 정지';
    button.setAttribute('aria-pressed', String(!video.paused));
    button.setAttribute('aria-label', video.paused ? '크림투파우더 영상 재생' : '크림투파우더 영상 일시 정지');
  };
  const updateStages = () => stages.forEach((stage, index) => {
    const active = video.currentTime >= Number(stage.dataset.start) &&
      (index === stages.length - 1 || video.currentTime < Number(stages[index + 1].dataset.start));
    stage.classList.toggle('active', active);
    if (active) stage.setAttribute('aria-current', 'step');
    else stage.removeAttribute('aria-current');
  });
  video.addEventListener('play', updateButton);
  video.addEventListener('pause', updateButton);
  video.addEventListener('timeupdate', updateStages);
  video.addEventListener('error', () => { video.controls = true; button.hidden = true; });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      inView = entries[0].intersectionRatio >= 0.35;
      if (!inView) video.pause();
      else if (!userPaused && canAutoplay() && !document.hidden) play();
    }, { threshold: [0, 0.35] });
    observer.observe(video);
  }
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) video.pause();
    else if (inView && !userPaused && canAutoplay()) play();
  });
  reducedMotion.addEventListener('change', () => { if (reducedMotion.matches) video.pause(); });
  updateButton();
  updateStages();
})();
