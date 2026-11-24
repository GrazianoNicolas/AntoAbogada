# Pliego, estudio jurídico

Sitio web de una abogada que analiza licitaciones de obras, mantenimiento y tecnología en la Provincia de Corrientes, Argentina. Muestra un listado de licitaciones por rubro, tres planes (básico gratuito, asesoría y seguimiento completo) y el contacto.

Es un sitio estático de siete páginas: no necesita instalación, servidor ni base de datos. La raíz del repositorio es el sitio publicable, así que funciona tal cual en GitHub Pages, Netlify, Vercel, Cloudflare Pages o cualquier hosting común.

## Páginas

| Dirección | Qué tiene | Fuente |
| --- | --- | --- |
| `/` | Presentación, rubros y cómo funciona | `src/paginas/inicio.html` |
| `/licitaciones/` | Listado de licitaciones con filtro por rubro | `src/paginas/licitaciones.html` |
| `/planes/` | Los tres planes | `src/paginas/planes.html` |
| `/guia/` | Cómo es una licitación pública en Corrientes | `src/paginas/guia.html` |
| `/quien-soy/` | Presentación de la abogada | `src/paginas/quien-soy.html` |
| `/preguntas/` | Preguntas frecuentes | `src/paginas/preguntas.html` |
| `/contacto/` | Formulario que arma la consulta por WhatsApp | `src/paginas/contacto.html` |

Cada página es corta a propósito, para que en el celular no haya que desplazarse tanto. Todas terminan con una banda que lleva a la consulta.

## Estructura

| Ruta | Qué es |
| --- | --- |
| `index.html` y las carpetas de cada página | El sitio ya armado, con estilos y script incluidos. **Se genera, no se edita a mano.** |
| `robots.txt`, `sitemap.xml` | Para que Google recorra el sitio. También se generan. |
| `fuentes/` | Tipografías del sitio (Besley, Public Sans, IBM Plex Mono; licencia OFL). |
| `marca/` | Logo en PNG e isotipo en SVG y PNG. |
| `og-image.png`, `favicon.svg` | Imagen para compartir en redes e ícono de la pestaña. |
| `src/paginas/` | El contenido de cada página. **Acá se editan los textos.** |
| `src/partes/` | Encabezado con el menú y pie, compartidos por todas las páginas. |
| `src/estilos.css`, `src/sitio.js` | Estilos y script compartidos. |
| `src/build.py` | Arma las páginas con sus etiquetas de SEO y sus datos estructurados. |
| `src/prototipo.js` | Sólo para el prototipo de revisión en un archivo. El sitio publicado no lo usa. |

## Cómo hacer un cambio

1. Editar el archivo que corresponda dentro de `src/`.
2. Regenerar el sitio desde la raíz del repositorio:

   ```
   python3 src/build.py .
   ```

3. Para revisarlo, levantar un servidor local y abrir `http://localhost:8000`:

   ```
   python3 -m http.server 8000
   ```

   Abrir `index.html` con doble clic no alcanza, porque los enlaces entre páginas apuntan a carpetas.

4. Subir los cambios.

En las fuentes, los enlaces entre páginas se escriben `href="@planes"`, `href="@contacto"`, etc., y `build.py` los convierte en la ruta correcta. El título, la descripción y el dominio se cambian al principio de `src/build.py`, donde hay una entrada por página. Para sumar una página nueva hay que agregar su entrada ahí, crear su archivo en `src/paginas/` y enlazarla desde el menú o el pie.

## Datos que hay que completar antes de publicar

En las páginas están marcados con `class="completar"`:

1. Nombre y apellido de la abogada, matrícula y formación (`src/paginas/quien-soy.html`).
2. WhatsApp, correo, dirección y horario (`src/paginas/contacto.html`).
3. Número de WhatsApp del formulario: al principio de `src/sitio.js`, `var WHATSAPP = ''`. Va en formato internacional sin signos, por ejemplo `5493794000000`. Mientras esté vacío, el formulario sólo muestra cómo quedaría el mensaje.
4. Foto de la abogada, en lugar del recuadro punteado.
5. Precio del plan Asesoría (`src/paginas/planes.html`) y, si se va a cobrar en línea, el enlace de pago o de reserva al que lleva el botón "Pedir asesoría".
6. Licitaciones reales: las filas de la tabla `id="lista"` en `src/paginas/licitaciones.html` son de ejemplo. Cada fila lleva `data-rubro` con `obras`, `mantenimiento`, `tecnologia` o `software`, el botón "Descargar" tiene que pasar a ser un enlace al pliego oficial, y el enlace "Quiero presentarme" lleva en `data-licitacion` el objeto de esa licitación.
7. Dominio: en `src/build.py` figura `https://www.pliegoestudio.com.ar/` como provisorio. Hay que reemplazarlo por la dirección real del sitio antes de publicarlo, porque se usa en las URL canónicas, el `robots.txt` y el `sitemap.xml`.

## Camino hasta la consulta

- El botón "Consultar" del encabezado queda siempre a la vista.
- En el listado, cada licitación tiene "Quiero presentarme": abre el contacto con esa licitación y su rubro ya cargados.
- El formulario arma el mensaje y abre WhatsApp. No pide teléfono, porque llega con el mensaje.
- En celular el listado se muestra como tarjetas, para que las acciones se vean sin desplazar hacia el costado, y en el contacto el formulario va antes que los datos.

## Revisión legal pendiente

Los textos citan la Ley 5571, el Decreto 3056/04, la Ley 3079 y la Ley 3460 a partir de los textos publicados por organismos oficiales de Corrientes. La abogada tiene que validar cada artículo y cada plazo antes de publicar.

## Diseño

- Se adapta a celular, tablet y computadora. Por debajo de 900 px de ancho el menú pasa a un botón desplegable.
- Tiene tema claro y oscuro, según la configuración del dispositivo.
- Las animaciones usan sólo CSS y unas líneas de JavaScript, incluido el fundido al pasar de una página a otra. Se desactivan si la persona tiene activada la opción de reducir movimiento, y sin JavaScript todo el contenido queda visible.

## SEO

Ya está hecho:

- Cada página tiene su título, su descripción y su URL canónica, pensados para búsquedas como "licitaciones Corrientes", "licitaciones abiertas en Corrientes", "cómo es una licitación pública en Corrientes" y "asesoría para presentarse a una licitación".
- Un solo H1 por página y subtítulos con las búsquedas principales.
- Datos estructurados para Google: estudio jurídico y sitio en el inicio, ruta de navegación en las páginas internas y preguntas frecuentes en su página. Los de las preguntas se arman solos a partir del contenido.
- `sitemap.xml` con las siete páginas.
- Etiquetas para compartir en redes, idioma es-AR y ubicación en Corrientes.
- Páginas livianas, sin librerías, con tipografías propias precargadas para que el texto no salte al cargar.

Falta después de publicar:

1. Registrar el dominio y publicar el sitio con HTTPS.
2. Crear el Perfil de Empresa en Google con el mismo nombre, dirección y teléfono que figuran en la web.
3. Dar de alta el sitio en Google Search Console y enviar el `sitemap.xml`.
4. Dar a cada licitación su propia página, con el objeto y el organismo en el título: son las búsquedas que más visitas traen.
5. Sumar páginas de guía por rubro: cómo presentarse a una licitación de obra, de mantenimiento o de tecnología en Corrientes.
6. Medir las consultas: cuántas personas tocan "Quiero presentarme" y cuántas envían el formulario.
