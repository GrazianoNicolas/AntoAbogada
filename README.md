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
| `src/licitaciones.json` | Los llamados del listado. **Acá se cargan las licitaciones.** |
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
6. Licitaciones: `src/licitaciones.json` ya tiene llamados reales, tomados de las publicaciones oficiales el 24/11/2026. Hay que volver a cargarlo cada vez que se publiquen llamados nuevos. Cómo hacerlo está más abajo, en "Cargar las licitaciones".
7. Municipios que cubre el listado: los tres de `src/licitaciones.json` son de ejemplo y figuran como "A confirmar". Hay que reemplazarlos por los que indique la abogada.
8. Dominio: en `src/build.py` figura `https://www.pliegoestudio.com.ar/` como provisorio. Hay que reemplazarlo por la dirección real del sitio antes de publicarlo, porque se usa en las URL canónicas, el `robots.txt` y el `sitemap.xml`.

## Cargar las licitaciones

El listado de `/licitaciones/` se arma con `src/licitaciones.json`. Cada llamado es un bloque con estos datos:

| Dato | Qué va |
| --- | --- |
| `rubro` | `obras`, `mantenimiento`, `tecnologia` o `software`. |
| `objeto` | El objeto del llamado, como figura en la publicación. |
| `organismo` | El organismo o municipio que llama. |
| `procedimiento` | Tipo y número, por ejemplo `Licitación Pública N° 14/2026`. Puede quedar vacío. |
| `detalle` | Una línea con el presupuesto oficial y el valor del pliego, si se conocen. Puede quedar vacío. |
| `apertura` | Fecha de apertura como `2026-12-03`, o con hora como `2026-12-03T10:00`. |
| `pliego` | Enlace al pliego oficial. Con este dato la fila muestra "Descargar pliego". |
| `fuente` | Enlace a la publicación oficial. Si no hay enlace al pliego, la fila muestra "Ver publicación oficial". |

Arriba del archivo, `"ejemplo"` tiene que pasar a `false` cuando los llamados sean reales y `"actualizado"` lleva la fecha de la última carga, que se muestra al pie del listado. Después hay que regenerar el sitio.

El orden lo pone el sitio, de la apertura más próxima a la más lejana. Con llamados reales, cada uno deja de mostrarse al día siguiente de su apertura aunque nadie actualice el archivo, y si no queda ninguno abierto, en total o en un rubro, el listado lo avisa.

### De dónde se toman los llamados

- Contaduría General de la Provincia: <https://www.cgpcorrientes.gob.ar/licitaciones-component>. Publica las licitaciones públicas del Poder Ejecutivo. La fecha de apertura, el presupuesto oficial y el valor del pliego están en el PDF del llamado.
- Boletín Oficial de la Provincia: <https://www.corrientes.gob.ar/boletinoficial>. Cada edición trae una sección "Licitaciones" con los llamados del Poder Judicial, de entes y de municipios.
- Poder Judicial: <https://www.juscorrientes.gov.ar/servicio-administrativo-financiero/servicio-compras/licitaciones-2026/>.

Sólo se cargan los llamados que todavía no abrieron y que entran en los cuatro rubros del estudio.

### Organismos y municipios que cubre el listado

La sección "Cobertura" de la misma página sale del bloque `"cobertura"` del archivo:

- `fuentes`: cada organismo con `nombre`, `detalle`, `fuente` (el nombre de la publicación), `enlace`, `estado` y, si corresponde, `norma`.
- `municipios`: cada municipio con `nombre` y `estado`.

`estado` puede ser `habilitado`, `proximamente` o `confirmar`. Mientras algún municipio esté en `confirmar`, la lista se muestra marcada como ejemplo.

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
