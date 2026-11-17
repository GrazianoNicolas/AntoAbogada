# Pliego, estudio jurídico

Sitio web de un estudio jurídico dedicado a licitaciones y contrataciones públicas en la Provincia de Corrientes, Argentina.

Es un sitio estático: no necesita instalación, servidor ni base de datos. La raíz del repositorio es el sitio publicable, así que funciona tal cual en GitHub Pages, Netlify, Vercel, Cloudflare Pages o cualquier hosting común.

## Estructura

| Ruta | Qué es |
| --- | --- |
| `index.html` | La página completa, con estilos y script incluidos. **Se genera, no se edita a mano.** |
| `robots.txt`, `sitemap.xml` | Para que Google recorra el sitio. También se generan. |
| `fuentes/` | Tipografías del sitio (Besley, Public Sans, IBM Plex Mono; licencia OFL). |
| `marca/` | Logo en PNG e isotipo en SVG y PNG. |
| `og-image.png`, `favicon.svg` | Imagen para compartir en redes e ícono de la pestaña. |
| `src/pliego-web.html` | Fuente de la página: textos, estilos y script. **Acá se edita.** |
| `src/build.py` | Arma `index.html` con las etiquetas de SEO y los datos estructurados. |

## Cómo hacer un cambio

1. Editar `src/pliego-web.html`.
2. Regenerar el sitio desde la raíz del repositorio:

   ```
   python3 src/build.py .
   ```

3. Abrir `index.html` en el navegador para revisar y subir los cambios.

El título, la descripción y el dominio del sitio se cambian al principio de `src/build.py`. Los datos estructurados de las preguntas frecuentes se arman solos a partir del contenido de la página.

## Datos que hay que completar antes de publicar

En `src/pliego-web.html` están marcados con `class="completar"`:

1. Nombre y apellido de la abogada, matrícula y formación (sección "El estudio").
2. WhatsApp, correo, dirección y horario (sección "Contacto").
3. Número de WhatsApp del formulario: al final del archivo, `var WHATSAPP = ''`. Va en formato internacional sin signos, por ejemplo `5493794000000`.
4. Foto de la abogada, en lugar del recuadro punteado.
5. Dominio: en `src/build.py` figura `https://www.pliegoestudio.com.ar/` como provisorio. Hay que reemplazarlo por la dirección real del sitio antes de publicarlo, porque se usa en la URL canónica, el `robots.txt` y el `sitemap.xml`.

## Revisión legal pendiente

Los textos citan la Ley 5571, el Decreto 3056/04, la Ley 3079 y la Ley 3460 a partir de los textos publicados por organismos oficiales de Corrientes. La abogada tiene que validar cada artículo y cada plazo antes de publicar.

## Diseño

- Se adapta a celular, tablet y computadora. Por debajo de 900 px de ancho el menú pasa a un botón desplegable.
- Tiene tema claro y oscuro, según la configuración del dispositivo.
- Las animaciones usan sólo CSS y unas líneas de JavaScript. Se desactivan si la persona tiene activada la opción de reducir movimiento, y sin JavaScript todo el contenido queda visible.

## SEO

Ya está hecho:

- Título y descripción pensados para la búsqueda "abogada licitaciones Corrientes".
- Un solo H1 y subtítulos con las búsquedas principales: proveedor del Estado, Registro de Proveedores, licitación pública, obra pública, impugnaciones.
- Datos estructurados para Google: estudio jurídico, sitio y preguntas frecuentes.
- Etiquetas para compartir en redes, idioma es-AR y ubicación en Corrientes.
- Página liviana, sin librerías, con tipografías propias precargadas para que el texto no salte al cargar.

Falta después de publicar:

1. Registrar el dominio y publicar el sitio con HTTPS.
2. Crear el Perfil de Empresa en Google con el mismo nombre, dirección y teléfono que figuran en la web.
3. Dar de alta el sitio en Google Search Console y enviar el `sitemap.xml`.
4. Sumar páginas de guía, una por tema: cómo inscribirse como proveedor, cómo impugnar una preadjudicación, garantías, obra pública.
