(function(){
  // Número de WhatsApp en formato internacional, sin signos ni espacios. Ejemplo: 5493794000000
  var WHATSAPP = '';
  var anio = document.getElementById('anio');
  if (anio) anio.textContent = new Date().getFullYear();
  var cada = function(lista, fn){ Array.prototype.forEach.call(lista, fn); };

  // Sombra del encabezado al bajar
  var top = document.querySelector('.top');
  var alScroll = function(){ if (top) top.classList.toggle('baja', window.scrollY > 8); };
  window.addEventListener('scroll', alScroll, { passive: true });
  alScroll();

  // Menú desplegable en celular y tablet
  var boton = document.getElementById('menu-btn');
  var cerrar = function(){ if (top && boton) { top.classList.remove('abierto'); boton.setAttribute('aria-expanded', 'false'); boton.setAttribute('aria-label', 'Abrir el menú'); } };
  if (top && boton) {
    boton.addEventListener('click', function(){
      var abre = !top.classList.contains('abierto');
      top.classList.toggle('abierto', abre);
      boton.setAttribute('aria-expanded', abre ? 'true' : 'false');
      boton.setAttribute('aria-label', abre ? 'Cerrar el menú' : 'Abrir el menú');
    });
    document.getElementById('menu').addEventListener('click', function(e){ if (e.target.closest('a')) cerrar(); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape') cerrar(); });
    document.addEventListener('click', function(e){ if (!top.contains(e.target)) cerrar(); });
    window.addEventListener('resize', cerrar);
  }

  // Listado: el rubro elegido pasa primero y queda marcado como cercano a la empresa
  var RUBROS = { obras: 'Obras', mantenimiento: 'Mantenimiento', tecnologia: 'Tecnología', software: 'Software y soporte' };
  var lista = document.getElementById('lista');
  if (lista) {
    var cuerpo = lista.tBodies[0];
    var filas = Array.prototype.slice.call(cuerpo.rows);
    // Un llamado deja de mostrarse al día siguiente de su apertura, aunque el listado no se haya vuelto a armar
    if (!lista.hasAttribute('data-ejemplo')) {
      var d = new Date();
      var hoy = d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
      filas = filas.filter(function(f){
        var abre = (f.getAttribute('data-apertura') || '').slice(0, 10);
        if (abre && abre < hoy) { cuerpo.removeChild(f); return false; }
        return true;
      });
    }
    // Aviso cuando no queda ningún llamado abierto, en total o del rubro elegido
    var vacia = document.getElementById('lista-vacia');
    var avisar = function(rubro){
      if (!vacia) return;
      var hay = filas.some(function(f){ return rubro === 'todas' || f.getAttribute('data-rubro') === rubro; });
      lista.parentNode.hidden = !filas.length;
      vacia.hidden = hay;
      if (!hay) document.getElementById('vacia-txt').textContent = filas.length && RUBROS[rubro]
        ? 'En este momento no hay llamados abiertos del rubro ' + RUBROS[rubro] + ' en el listado.'
        : 'En este momento no hay llamados abiertos en el listado.';
    };
    avisar('todas');
    // En celular las filas se muestran como tarjetas; estos roles mantienen la lectura como tabla
    lista.setAttribute('role', 'table');
    cada(lista.querySelectorAll('thead, tbody'), function(g){ g.setAttribute('role', 'rowgroup'); });
    cada(lista.rows, function(f){ f.setAttribute('role', 'row'); });
    cada(lista.querySelectorAll('thead th'), function(c){ c.setAttribute('role', 'columnheader'); });
    cada(lista.querySelectorAll('tbody th'), function(c){ c.setAttribute('role', 'rowheader'); });
    cada(lista.querySelectorAll('td'), function(c){ c.setAttribute('role', 'cell'); });
    // El pedido de asesoría de cada fila lleva también el rubro de esa licitación
    filas.forEach(function(f){
      var a = f.querySelector('a[data-licitacion]');
      if (a) a.setAttribute('data-rubro', RUBROS[f.getAttribute('data-rubro')] || '');
    });
    var chips = document.querySelectorAll('.chip');
    cada(chips, function(chip){
      chip.addEventListener('click', function(){
        var rubro = chip.getAttribute('data-rubro');
        cada(chips, function(c){ c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
        var cerca = [], resto = [];
        filas.forEach(function(f){
          var afin = rubro !== 'todas' && f.getAttribute('data-rubro') === rubro;
          f.classList.toggle('afin', afin);
          f.classList.toggle('lejos', rubro !== 'todas' && !afin);
          (afin ? cerca : resto).push(f);
        });
        cerca.concat(resto).forEach(function(f){ cuerpo.appendChild(f); });
        avisar(rubro);
      });
    });
    // Si se llega desde un rubro del inicio, el listado abre con ese rubro elegido
    var filtrar = function(){
      var pedido = '';
      try { pedido = new URLSearchParams(window.location.search).get('rubro') || ''; } catch (err) {}
      try {
        var guardado = sessionStorage.getItem('pliego-rubro');
        if (guardado) { pedido = guardado; sessionStorage.removeItem('pliego-rubro'); }
      } catch (err) {}
      cada(chips, function(c){ if (pedido && c.getAttribute('data-rubro') === pedido) c.click(); });
    };
    filtrar();
    window.addEventListener('hashchange', filtrar);
    var nota = document.getElementById('nota-lista');
    lista.addEventListener('click', function(e){
      if (nota && e.target.closest('button.bajar')) nota.textContent = 'Estas licitaciones son de ejemplo. Cuando se carguen las reales, este botón descarga el pliego oficial.';
    });
  }

  // Los enlaces que piden una consulta llevan su dato al formulario: la licitación, el rubro o el tema.
  // Entre páginas viaja en la dirección; en el prototipo, que es un solo archivo, se guarda en la pestaña.
  var CAMPOS = ['licitacion', 'rubro', 'tema'];
  cada(document.querySelectorAll('a[data-licitacion], a[data-tema]'), function(a){
    var href = a.getAttribute('href') || '';
    var datos = {};
    CAMPOS.forEach(function(c){ var v = a.getAttribute('data-' + c); if (v) datos[c] = v; });
    if (href.charAt(0) === '#') {
      a.addEventListener('click', function(){ try { sessionStorage.setItem('pliego-consulta', JSON.stringify(datos)); } catch (err) {} });
    } else {
      var partes = [];
      for (var c in datos) partes.push(c + '=' + encodeURIComponent(datos[c]));
      a.setAttribute('href', href + '?' + partes.join('&'));
    }
  });

  cada(document.querySelectorAll('a[data-filtro]'), function(a){
    var href = a.getAttribute('href') || '';
    var rubro = a.getAttribute('data-filtro');
    if (href.charAt(0) === '#') {
      a.addEventListener('click', function(){ try { sessionStorage.setItem('pliego-rubro', rubro); } catch (err) {} });
    } else {
      a.setAttribute('href', href + '?rubro=' + encodeURIComponent(rubro));
    }
  });

  var quieto = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !quieto) {
    // Aparición suave de cada bloque al entrar en pantalla. El título de cada página no espera al script.
    var bloques = document.querySelectorAll('.wrap > .sec-head, .clientes article, .filtros, .cob, .munis, .plan, .pasos li, .sigue, .etapas li, .sub, .tabla, .faq-grupo, .estudio > *, .contacto > *, .cierre .wrap > *');
    var ver = new IntersectionObserver(function(entradas){
      entradas.forEach(function(en){
        if (en.isIntersecting || en.boundingClientRect.top < 0) { en.target.classList.add('visto'); ver.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.05 });
    cada(bloques, function(el){
      if (el.querySelector('h1')) return;
      var i = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.style.setProperty('--d', (i % 4) * 0.08 + 's');
      el.classList.add('rv');
      ver.observe(el);
    });
    document.documentElement.classList.add('anim');
  }

  var form = document.getElementById('consulta');
  if (!form) return;
  // Con el número cargado, el WhatsApp de la lista de datos abre la conversación
  var viaWa = document.getElementById('via-wa');
  if (WHATSAPP && viaWa) {
    var directo = document.createElement('a');
    directo.href = 'https://wa.me/' + WHATSAPP;
    directo.rel = 'noopener';
    directo.textContent = viaWa.textContent;
    viaWa.textContent = '';
    viaWa.appendChild(directo);
  }
  var pedida = '';
  var elegir = function(select, valor){
    cada(select.options, function(o){ if (o.text === valor) select.value = o.value || o.text; });
  };
  var cargarPedido = function(){
    var datos = {};
    try {
      var q = new URLSearchParams(window.location.search);
      CAMPOS.forEach(function(c){ if (q.get(c)) datos[c] = q.get(c); });
    } catch (err) {}
    try {
      var guardado = sessionStorage.getItem('pliego-consulta');
      if (guardado) {
        datos = JSON.parse(guardado) || datos;
        sessionStorage.removeItem('pliego-consulta');
        pedida = '';
        document.getElementById('elegida').hidden = true;
      }
    } catch (err) {}
    if (datos.licitacion) {
      pedida = String(datos.licitacion).slice(0, 200);
      document.getElementById('elegida-txt').textContent = pedida;
      document.getElementById('elegida').hidden = false;
      elegir(document.getElementById('c-tema'), 'Quiero asesoría para una licitación');
    }
    if (datos.rubro) elegir(document.getElementById('c-rubro'), datos.rubro);
    if (datos.tema) elegir(document.getElementById('c-tema'), datos.tema);
  };
  cargarPedido();
  window.addEventListener('hashchange', cargarPedido);

  form.addEventListener('submit', function(e){
    e.preventDefault();
    var v = function(id){ return (document.getElementById(id).value || '').trim(); };
    var lineas = ['Hola, le escribo desde la web del estudio.'];
    if (v('c-nombre')) lineas.push('Nombre: ' + v('c-nombre'));
    if (v('c-empresa')) lineas.push('Empresa: ' + v('c-empresa'));
    if (v('c-rubro')) lineas.push('Rubro: ' + v('c-rubro'));
    lineas.push('Tema: ' + v('c-tema'));
    if (pedida) lineas.push('Licitación: ' + pedida);
    if (v('c-msj')) lineas.push('Consulta: ' + v('c-msj'));
    var texto = lineas.join('\n');
    if (WHATSAPP) {
      window.location.href = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(texto);
    } else {
      document.getElementById('previa-txt').textContent = texto;
      document.getElementById('previa').hidden = false;
    }
  });
})();
