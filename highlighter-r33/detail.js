(() => {
  const root = document.getElementById('beam-highlighter-r33');
  if (!root) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const items = [...root.querySelectorAll('[data-motion]')].map(frame => ({
    frame, button: frame.querySelector('button'), video: frame.querySelector('video'),
    image: frame.querySelector('img'), visible: false, pausedByUser: false, playing: false
  }));
  const sync = item => {
    const playing = item.video ? !item.video.paused : item.playing;
    item.button.textContent = playing ? '일시정지' : '재생';
    item.button.setAttribute('aria-label', `${item.button.dataset.name} ${playing ? '일시정지' : '재생'}`);
    item.button.setAttribute('aria-pressed', String(playing));
  };
  const pause = item => {
    if (item.video) item.video.pause();
    else { item.image.src = item.image.dataset.still; item.playing = false; }
    sync(item);
  };
  const play = item => {
    if (item.video) {
      if (!item.video.getAttribute('src')) item.video.src = item.video.dataset.src;
      item.video.play().catch(() => sync(item));
    } else { item.image.src = item.image.dataset.animated; item.playing = true; sync(item); }
  };
  const update = item => item.visible && !document.hidden && !reduced.matches && !item.pausedByUser ? play(item) : pause(item);
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      const item = items.find(item => item.frame === entry.target);
      item.visible = entry.isIntersecting; update(item);
    }
  }, { threshold: .25 });
  for (const item of items) {
    item.button.hidden = false;
    if (item.video) {
      item.video.controls = false;
      item.video.addEventListener('play', () => sync(item));
      item.video.addEventListener('pause', () => sync(item));
    }
    item.button.addEventListener('click', () => {
      const playing = item.video ? !item.video.paused : item.playing;
      item.pausedByUser = playing;
      if (playing) pause(item); else play(item);
    });
    observer.observe(item.frame);
  }
  document.addEventListener('visibilitychange', () => items.forEach(update));
  reduced.addEventListener('change', () => items.forEach(update));
})();
