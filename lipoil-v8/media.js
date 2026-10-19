const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
const films = [...document.querySelectorAll('video')];
const manuallyPaused = new WeakSet();
for (const film of films) {
  film.addEventListener('pointerdown', () => {
    if (!film.paused) manuallyPaused.add(film);
    else manuallyPaused.delete(film);
  });
}
const observer = new IntersectionObserver(entries => {
  for (const {target: film, isIntersecting} of entries) {
    if (isIntersecting && !preference.matches && !manuallyPaused.has(film)) film.play().catch(() => {});
    else film.pause();
  }
}, {threshold: 0.4});
films.forEach(film => observer.observe(film));
preference.addEventListener('change', () => { if (preference.matches) films.forEach(film => film.pause()); });
