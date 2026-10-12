(() => {
  const video = document.querySelector('.do-hero video');
  const hero = document.querySelector('.do-hero');
  const header = document.querySelector('.do-header');
  if (!video || !hero || !header) return;
  const sync = (time = video.currentTime) => {
    const ending = time >= 146 / 24;
    hero.toggleAttribute('data-film-ending', ending);
    header.toggleAttribute('data-film-ending', ending);
  };
  if ('requestVideoFrameCallback' in video) {
    const frame = (_, metadata) => {
      sync(metadata.mediaTime);
      video.requestVideoFrameCallback(frame);
    };
    video.requestVideoFrameCallback(frame);
  }
  video.addEventListener('timeupdate', () => sync());
  video.addEventListener('seeked', () => sync());
  video.addEventListener('loadeddata', () => sync());
  sync();
})();
