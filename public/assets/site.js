// Idioma (EN por defecto, se recuerda por visitante)
const root = document.documentElement;
document.getElementById('langBtn').onclick = () => {
  root.lang = root.lang === 'es' ? 'en' : 'es';
  try { localStorage.setItem('vruma-lang', root.lang); } catch (e) {}
};

// Loops de la grilla: cargan y se reproducen solo cuando están en pantalla
const vo = new IntersectionObserver(es => es.forEach(e => {
  const v = e.target;
  if (e.isIntersecting) { if (!v.src) v.src = v.dataset.src; v.play().catch(() => {}); }
  else v.pause();
}), { threshold: .35 });
document.querySelectorAll('.media video').forEach(v => vo.observe(v));

// Hero: 1080p en pantallas grandes, 720p en celulares o conexiones lentas
const reel = document.getElementById('reel');
if (reel) {
  const c = navigator.connection;
  const slow = c && (c.saveData || /2g|3g/.test(c.effectiveType || ''));
  reel.src = (innerWidth * devicePixelRatio >= 1600 && !slow) ? '/media/loop1080.mp4' : '/media/loop720.mp4';
  reel.play().catch(() => {});
  const pl = document.getElementById('player'), full = document.getElementById('full');
  document.getElementById('watch').onclick = () => { pl.classList.add('on'); reel.pause(); full.currentTime = 0; full.play().catch(() => {}); };
  document.getElementById('close').onclick = () => { full.pause(); pl.classList.remove('on'); reel.play().catch(() => {}); };
}
