import re, json, os, html, sys
SRC = os.path.join(os.path.dirname(__file__), 'pliego-web.html')
OUT = sys.argv[1]
DOMINIO = 'https://www.pliegoestudio.com.ar/'   # provisorio: reemplazar por el dominio real
TITLE = 'Abogada en licitaciones públicas en Corrientes | Pliego'
DESC = ('Estudio jurídico en Corrientes dedicado a licitaciones y contrataciones públicas: '
        'inscripción como proveedor del Estado, armado de ofertas, impugnaciones y cobro.')
src = open(SRC, encoding='utf-8').read()
head, body = src.split('<!--BODY-->')
style = re.search(r'<style>.*?</style>', head, re.S).group(0)
fonts = re.search(r'<link rel="stylesheet"[^>]+>', head).group(0)
# En el sitio publicado las tipografías se sirven desde la misma carpeta y se precargan: evita el salto de texto al cargar.
UR = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
face = lambda fam, w, f: f'@font-face{{font-family:"{fam}";font-style:normal;font-weight:{w};font-display:swap;src:url(fuentes/{f}) format("woff2");unicode-range:{UR}}}'
fonts = ('<link rel="preload" href="fuentes/besley.woff2" as="font" type="font/woff2" crossorigin>\n'
         '<link rel="preload" href="fuentes/public-sans.woff2" as="font" type="font/woff2" crossorigin>\n'
         '<style>' + face('Besley','500 700','besley.woff2') + face('Public Sans','400 700','public-sans.woff2')
         + face('IBM Plex Mono','400','plex-mono-400.woff2') + face('IBM Plex Mono','500','plex-mono-500.woff2') + '</style>')
body = re.sub(r'<!--PROTO-->.*?<!--/PROTO-->\n?', '', body, flags=re.S)
reset = ('<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
         'img{max-width:100%}[hidden]{display:none!important}</style>')
strip = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s)).strip()
faqs = re.findall(r'<summary><h3>(.*?)</h3></summary>\s*<p>(.*?)</p>', body, re.S)
assert len(faqs) >= 10, len(faqs)
ld = [
 {"@context":"https://schema.org","@type":"LegalService","@id":DOMINIO+"#estudio",
  "name":"Pliego Estudio Jurídico","description":DESC,"url":DOMINIO,
  "image":DOMINIO+"og-image.png","logo":DOMINIO+"marca/isotipo.png",
  "address":{"@type":"PostalAddress","addressLocality":"Corrientes","addressRegion":"Corrientes","addressCountry":"AR"},
  "areaServed":{"@type":"AdministrativeArea","name":"Provincia de Corrientes, Argentina"},
  "knowsAbout":["Licitaciones públicas","Contrataciones públicas","Registro de Proveedores del Estado",
                "Obra pública","Derecho administrativo","Impugnación de licitaciones"],
  "availableLanguage":"es"},
 {"@context":"https://schema.org","@type":"WebSite","name":"Pliego Estudio Jurídico","url":DOMINIO,"inLanguage":"es-AR"},
 {"@context":"https://schema.org","@type":"FAQPage",
  "mainEntity":[{"@type":"Question","name":strip(q),"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q,a in faqs]},
]
e = html.escape
doc = f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESC)}">
<link rel="canonical" href="{DOMINIO}">
<meta name="robots" content="index, follow">
<meta name="geo.region" content="AR-W">
<meta name="geo.placename" content="Corrientes">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="Pliego Estudio Jurídico">
<meta property="og:title" content="{e(TITLE)}">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:url" content="{DOMINIO}">
<meta property="og:image" content="{DOMINIO}og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0F4A3C">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="marca/isotipo.png">
{fonts}
{reset}
{style}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{body.strip()}
</body>
</html>
'''
os.makedirs(OUT, exist_ok=True)
import shutil
os.makedirs(os.path.join(OUT,'fuentes'), exist_ok=True)
for f in ('besley.woff2','public-sans.woff2','plex-mono-400.woff2','plex-mono-500.woff2'):
    shutil.copy(os.path.join(os.path.dirname(__file__),'fonts',f), os.path.join(OUT,'fuentes',f))
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(doc)
open(os.path.join(OUT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nDisallow: /src/\n\nSitemap: {DOMINIO}sitemap.xml\n')
open(os.path.join(OUT,'sitemap.xml'),'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{DOMINIO}</loc><lastmod>2026-11-16</lastmod></url>\n</urlset>\n')
print('ok', len(doc), 'bytes;', len(faqs), 'faqs; title', len(TITLE), 'desc', len(DESC))
