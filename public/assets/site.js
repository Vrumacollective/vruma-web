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


// Contact: formulario → mail (FormSubmit)
const cf = document.getElementById('cform');
if (cf) {
  const btn = cf.querySelector('button[type=submit]'), err = cf.querySelector('.err'), sent = cf.querySelector('.sent');
  cf.addEventListener('submit', async ev => {
    ev.preventDefault();
    if (cf.elements._honey.value || cf.classList.contains('sending')) return;
    err.hidden = true; btn.disabled = true; cf.classList.add('sending');
    const f = cf.elements;
    const body = JSON.stringify({name: f.name.value, email: f.email.value, message: f.message.value,
      _subject: 'Nuevo mensaje desde vrumacollective.com — ' + f.name.value, _template: 'table', _captcha: 'false'});
    const showSent = () => { if (!cf.classList.contains('done')) { cf.classList.add('done'); sent.hidden = false; } };
    // FormSubmit tarda en responder: confirmamos a los 2 s y el envío sigue en segundo plano (keepalive)
    const early = setTimeout(showSent, 2000);
    try {
      const r = await fetch(cf.dataset.endpoint, {method: 'POST', keepalive: true, headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}, body});
      const d = await r.json().catch(() => ({}));
      if (!r.ok || String(d.success) === 'false') throw 0;
      clearTimeout(early); showSent(); cf.reset();
    } catch (e) {
      clearTimeout(early); cf.classList.remove('done'); sent.hidden = true; err.hidden = false;
    }
    btn.disabled = false; cf.classList.remove('sending');
  });
  cf.querySelector('.again').addEventListener('click', () => { cf.classList.remove('done'); sent.hidden = true; cf.elements.name.focus(); });
}
