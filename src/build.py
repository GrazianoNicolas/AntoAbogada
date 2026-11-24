#!/usr/bin/env python3
"""Arma el sitio de varias páginas a partir de src/.

Uso, desde la raíz del repositorio:
    python3 src/build.py .
    python3 src/build.py . --prototipo ruta/prototipo.html   (además, el prototipo de revisión en un solo archivo)
"""
import datetime, html, json, os, re, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
PROTOTIPO = sys.argv[sys.argv.index('--prototipo') + 1] if '--prototipo' in sys.argv else None

DOMINIO = 'https://www.pliegoestudio.com.ar/'   # provisorio: reemplazar por el dominio real
SITIO = 'Pliego Estudio Jurídico'

# Una entrada por página. "slug" es la carpeta donde se publica (vacío para el inicio) y "archivo" es su fuente en src/paginas/.
PAGINAS = [
    {'slug': '', 'archivo': 'inicio', 'nombre': 'Inicio',
     'title': 'Licitaciones en Corrientes: obras y tecnología | Pliego',
     'desc': 'Licitaciones de obras, mantenimiento y tecnología en Corrientes, analizadas por una abogada. '
             'Descárguelas gratis y pida asesoría para presentar su oferta.'},
    {'slug': 'licitaciones', 'archivo': 'licitaciones', 'nombre': 'Licitaciones',
     'title': 'Licitaciones abiertas en Corrientes, por rubro | Pliego',
     'desc': 'Licitaciones abiertas de la Provincia de Corrientes y sus municipios: obras, mantenimiento, tecnología y software. '
             'Elija su rubro y descargue el pliego gratis.'},
    {'slug': 'planes', 'archivo': 'planes', 'nombre': 'Planes',
     'title': 'Asesoría para presentarse a una licitación | Pliego',
     'desc': 'Tres planes para su empresa o pyme en Corrientes: descarga gratuita de licitaciones, asesoría para presentar '
             'su oferta y seguimiento completo del proceso.'},
    {'slug': 'guia', 'archivo': 'guia', 'nombre': 'Guía',
     'title': 'Cómo es una licitación pública en Corrientes | Pliego',
     'desc': 'Guía paso a paso de una licitación pública en Corrientes: llamado, pliego, oferta, apertura, adjudicación y cobro, '
             'con la norma que rige cada etapa.'},
    {'slug': 'quien-soy', 'archivo': 'quien-soy', 'nombre': 'Quién soy',
     'title': 'Abogada que analiza licitaciones en Corrientes | Pliego',
     'desc': 'Soy abogada y analizo procesos de licitación en la Provincia de Corrientes. Trabajé con licitaciones de obras, '
             'de mantenimiento y de tecnología.'},
    {'slug': 'preguntas', 'archivo': 'preguntas', 'nombre': 'Preguntas',
     'title': 'Preguntas frecuentes sobre licitaciones | Pliego',
     'desc': 'Respuestas sobre las licitaciones en Corrientes y los planes: qué se publica, cuánto cuesta, qué incluye la asesoría, '
             'garantías y Registro de Proveedores.'},
    {'slug': 'contacto', 'archivo': 'contacto', 'nombre': 'Contacto',
     'title': 'Contacto y pedido de asesoría | Pliego',
     'desc': 'Pida asesoría para presentarse a una licitación en Corrientes. Cuénteme a qué se dedica su empresa y qué licitación '
             'le interesa. La consulta llega por WhatsApp.'},
]

FUENTES_GOOGLE = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Besley:wght@500;600;700'
                  '&family=IBM+Plex+Mono:wght@400;500&family=Public+Sans:wght@400;500;600;700&display=swap">')
UR = ('U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,'
      'U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD')
ARCHIVOS_FUENTE = ('besley.woff2', 'public-sans.woff2', 'plex-mono-400.woff2', 'plex-mono-500.woff2')
RESET = ('<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
         'img{max-width:100%}[hidden]{display:none!important}</style>')


def leer(*ruta):
    with open(os.path.join(AQUI, *ruta), encoding='utf-8') as f:
        return f.read()


def escribir(ruta, texto):
    os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(texto)


CSS = leer('estilos.css')
JS = leer('sitio.js')
CABECERA = leer('partes', 'cabecera.html')
PIE = leer('partes', 'pie.html')
CLAVES = {p['slug'] or 'inicio' for p in PAGINAS}
e = html.escape
limpio = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s)).strip()
url = lambda p: DOMINIO + (p['slug'] + '/' if p['slug'] else '')


def enlazar(texto, pref=None):
    """Resuelve href="@pagina". Con pref arma rutas relativas; sin pref, las anclas del prototipo."""
    def uno(m):
        clave = m.group(1)
        assert clave in CLAVES, f'enlace a una página que no existe: @{clave}'
        if pref is None:
            return f'href="#{clave}"'
        if clave == 'inicio':
            return f'href="{pref or "./"}"'
        return f'href="{pref}{clave}/"'
    return re.sub(r'href="@([a-z-]+)"', uno, texto)


def miga(p):
    return ('<nav class="miga" aria-label="Ruta de navegación"><ol><li><a href="@inicio">Inicio</a></li>'
            f'<li aria-current="page">{e(p["nombre"])}</li></ol></nav>')


def contenido(p):
    return leer('paginas', p['archivo'] + '.html').replace('<!--MIGA-->', miga(p)).strip()


def cabecera(p):
    """Marca en el menú la página en la que se está."""
    clave = p['slug'] or 'inicio'
    cab = CABECERA.replace(f'class="lnk" href="@{clave}"', f'class="lnk activo" aria-current="page" href="@{clave}"')
    if clave == 'contacto':
        cab = cab.replace('btn--chico" href="@contacto"', 'btn--chico" aria-current="page" href="@contacto"')
    return cab.strip()


def datos_estructurados(p, cuerpo):
    if not p['slug']:
        return [
            {"@context": "https://schema.org", "@type": "LegalService", "@id": DOMINIO + "#estudio",
             "name": SITIO, "description": p['desc'], "url": DOMINIO,
             "image": DOMINIO + "og-image.png", "logo": DOMINIO + "marca/isotipo.png",
             "address": {"@type": "PostalAddress", "addressLocality": "Corrientes", "addressRegion": "Corrientes",
                         "addressCountry": "AR"},
             "areaServed": {"@type": "AdministrativeArea", "name": "Provincia de Corrientes, Argentina"},
             "knowsAbout": ["Licitaciones públicas", "Licitaciones de obra pública",
                            "Licitaciones de servicios de mantenimiento", "Licitaciones de tecnología",
                            "Licitaciones de desarrollo de software y soporte", "Contrataciones públicas"],
             "availableLanguage": "es"},
            {"@context": "https://schema.org", "@type": "WebSite", "name": SITIO, "url": DOMINIO, "inLanguage": "es-AR"},
        ]
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": DOMINIO},
        {"@type": "ListItem", "position": 2, "name": p['nombre'], "item": url(p)}]}]
    faqs = re.findall(r'<summary><h2>(.*?)</h2></summary>\s*<p>(.*?)</p>', cuerpo, re.S)
    if p['slug'] == 'preguntas':
        assert len(faqs) >= 10, len(faqs)
    if faqs:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": limpio(q), "acceptedAnswer": {"@type": "Answer", "text": limpio(a)}}
            for q, a in faqs]})
    return ld


def pagina(p):
    pref = '../' if p['slug'] else ''
    cuerpo = contenido(p)
    cara = lambda fam, peso, f: (f'@font-face{{font-family:"{fam}";font-style:normal;font-weight:{peso};font-display:swap;'
                                 f'src:url({pref}fuentes/{f}) format("woff2");unicode-range:{UR}}}')
    # Las tipografías se sirven desde el mismo sitio y se precargan: evita el salto de texto al cargar.
    fuentes = (f'<link rel="preload" href="{pref}fuentes/besley.woff2" as="font" type="font/woff2" crossorigin>\n'
               f'<link rel="preload" href="{pref}fuentes/public-sans.woff2" as="font" type="font/woff2" crossorigin>\n'
               '<style>' + cara('Besley', '500 700', 'besley.woff2') + cara('Public Sans', '400 700', 'public-sans.woff2')
               + cara('IBM Plex Mono', '400', 'plex-mono-400.woff2') + cara('IBM Plex Mono', '500', 'plex-mono-500.woff2')
               + '</style>')
    ld = datos_estructurados(p, cuerpo)
    doc = f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['desc'])}">
<link rel="canonical" href="{url(p)}">
<meta name="robots" content="index, follow">
<meta name="geo.region" content="AR-W">
<meta name="geo.placename" content="Corrientes">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="{e(SITIO)}">
<meta property="og:title" content="{e(p['title'])}">
<meta property="og:description" content="{e(p['desc'])}">
<meta property="og:url" content="{url(p)}">
<meta property="og:image" content="{DOMINIO}og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0F4A3C">
<link rel="icon" href="{pref}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pref}marca/isotipo.png">
{fuentes}
{RESET}
<style>
{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="salto" href="#contenido">Saltar al contenido</a>
{cabecera(p)}

<main id="contenido">
{cuerpo}
</main>

{PIE.strip()}

<script>
{JS}</script>
</body>
</html>
'''
    return enlazar(doc, pref)


def prototipo():
    """Todas las páginas en un solo archivo, para revisar en claude.ai. Se muestra de a una, como en el sitio."""
    vistas = []
    for i, p in enumerate(PAGINAS):
        clave = p['slug'] or 'inicio'
        vistas.append(f'<main data-vista="{clave}"{"" if i == 0 else " hidden"}>\n{contenido(p)}\n</main>')
    doc = f'''<title>{e(SITIO)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FUENTES_GOOGLE}
<style>
{CSS}</style>
<div class="aviso"><div class="wrap">Prototipo para revisión. Los datos con <span class="completar">subrayado punteado</span> son provisorios y hay que reemplazarlos por los reales.</div></div>

{CABECERA.strip()}

{chr(10).join(vistas)}

{PIE.strip()}

<script>
{JS}</script>
<script>
{leer('prototipo.js')}</script>
'''
    return enlazar(doc)


os.makedirs(os.path.join(OUT, 'fuentes'), exist_ok=True)
for f in ARCHIVOS_FUENTE:
    shutil.copy(os.path.join(AQUI, 'fonts', f), os.path.join(OUT, 'fuentes', f))

for p in PAGINAS:
    assert len(p['title']) <= 60 and len(p['desc']) <= 160, (p['archivo'], len(p['title']), len(p['desc']))
    doc = pagina(p)
    assert doc.count('<h1') == 1, (p['archivo'], 'cada página lleva un solo H1')
    escribir(os.path.join(OUT, p['slug'], 'index.html'), doc)
    print(f"{(p['slug'] or '(inicio)') + '/':16} {len(doc):6} bytes   título {len(p['title'])}   descripción {len(p['desc'])}")

hoy = datetime.date.today().isoformat()
escribir(os.path.join(OUT, 'robots.txt'), f'User-agent: *\nAllow: /\nDisallow: /src/\n\nSitemap: {DOMINIO}sitemap.xml\n')
escribir(os.path.join(OUT, 'sitemap.xml'),
         '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
         + ''.join(f'  <url><loc>{url(p)}</loc><lastmod>{hoy}</lastmod></url>\n' for p in PAGINAS) + '</urlset>\n')

if PROTOTIPO:
    escribir(PROTOTIPO, prototipo())
    print('prototipo:', PROTOTIPO)
