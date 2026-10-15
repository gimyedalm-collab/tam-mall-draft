// User-controlled original product footage. Pause clips when leaving the screen.
const cloudVideos = document.querySelectorAll('#cloud-blush video');
cloudVideos.forEach(video => {
  video.controls = false;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'film-toggle';
  button.textContent = '영상 재생';
  button.setAttribute('aria-label', `${video.getAttribute('aria-label')} 재생`);
  button.setAttribute('aria-pressed', 'false');
  video.parentElement.after(button);
  button.addEventListener('click', async () => {
    if (!video.paused) { video.pause(); return; }
    try { await video.play(); } catch { button.textContent = '다시 재생'; video.controls = true; }
  });
  video.addEventListener('play', () => {
    button.textContent = '일시 정지';
    button.setAttribute('aria-pressed', 'true');
    button.setAttribute('aria-label', `${video.getAttribute('aria-label')} 일시 정지`);
  });
  video.addEventListener('pause', () => {
    button.textContent = '영상 재생';
    button.setAttribute('aria-pressed', 'false');
    button.setAttribute('aria-label', `${video.getAttribute('aria-label')} 재생`);
  });
});
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => { if (!entry.isIntersecting) entry.target.pause(); });
  }, { threshold: 0.1 });
  cloudVideos.forEach(video => observer.observe(video));
}
cloudVideos.forEach(video => video.addEventListener('play', () => {
  cloudVideos.forEach(other => { if (other !== video) other.pause(); });
}));
