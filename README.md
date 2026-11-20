# vruma-web

Sitio web de Vruma Collective — https://vrumacollective.com

## Estructura

- `data/projects.json` — los proyectos de la grilla, en orden. Cada uno tiene título (`t`), cliente (`c`), año (`y`), tipos (`k`: Film, Foto, IA, Cobertura), descripción en español (`d`) e inglés (`de`), videos de Vimeo (`vm`: id y nombre), si es spec (`spec`) y, en proyectos de fotos, cantidad de fotos de la galería (`gal`).
- `data/i18n.json` — todos los textos fijos del sitio, en inglés y español.
- `src/` — diseño (`site.css`), comportamiento (`site.js`) y el generador (`build.py`).
- `public/` — el sitio listo para publicar. **No se edita a mano**: se genera con el build.
- `public/media/` — videos y fotos. Cada proyecto usa `<v>.mp4` (loop de la grilla) y `<v>.jpg` (miniatura).

## Cómo hacer un cambio

1. Editar `data/projects.json` o `data/i18n.json` (o agregar los archivos del proyecto en `public/media/`).
2. Correr `python3 src/build.py`.
3. Subir los cambios a `main`. Cloudflare publica solo en un minuto.

## Publicación

Cloudflare (Workers con archivos estáticos), conectado a este repositorio. La configuración está en `wrangler.jsonc`: publica la carpeta `public` tal cual, sin build.
- Build command: vacío
- Deploy command: `npx wrangler deploy`
