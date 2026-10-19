(() => {
  const video = document.querySelector('#texture-film');
  const button = document.querySelector('#cloud-blush .film-toggle');
  if (!video || !button) return;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const chapters = document.querySelector('#cloud-blush .film-chapters');
  const chapterButtons = [...(chapters?.querySelectorAll('button') || [])];
  let inView = false;
  let userPaused = false;
  let activeChapter = -1;
  const canAutoplay = () => !reducedMotion.matches && !navigator.connection?.saveData;
  const play = async () => {
    try { await video.play(); }
    catch { button.textContent = '영상 재생'; }
  };
  const updateChapter = () => {
    const index = chapterButtons.reduce((current, item, i) => video.currentTime >= Number(item.dataset.start) ? i : current, 0);
    if (index === activeChapter || !chapterButtons.length) return;
    activeChapter = index;
    chapterButtons.forEach((item, i) => item.setAttribute('aria-pressed', String(i === index)));
  };
  const enableChapters = () => {
    if (chapters && Number.isFinite(video.duration) && video.duration > 7.4) chapters.hidden = false;
    updateChapter();
  };
  video.controls = false;
  button.hidden = false;
  button.addEventListener('click', () => {
    if (video.paused) { userPaused = false; play(); }
    else { userPaused = true; video.pause(); }
  });
  chapterButtons.forEach(item => item.addEventListener('click', () => {
    userPaused = true;
    video.pause();
    video.currentTime = Number(item.dataset.start) + 0.08;
    updateChapter();
  }));
  const updateButton = () => {
    button.textContent = video.paused ? '영상 재생' : '일시 정지';
    button.setAttribute('aria-pressed', String(!video.paused));
    button.setAttribute('aria-label', video.paused ? '크림투파우더 영상 재생' : '크림투파우더 영상 일시 정지');
  };
  video.addEventListener('play', updateButton);
  video.addEventListener('pause', updateButton);
  video.addEventListener('loadedmetadata', enableChapters);
  video.addEventListener('timeupdate', updateChapter);
  video.addEventListener('seeked', updateChapter);
  video.addEventListener('error', () => {
    video.controls = true;
    button.hidden = true;
    if (chapters) chapters.hidden = true;
  });
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
  if (video.readyState >= 1) enableChapters();
  updateButton();
})();
