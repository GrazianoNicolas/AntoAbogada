// Sólo para el prototipo de revisión: muestra de a una página dentro de un mismo archivo.
// En el sitio publicado cada página tiene su propia dirección y este script no se usa.
(function(){
  var vistas = document.querySelectorAll('[data-vista]');
  var enlaces = document.querySelectorAll('.top a[href^="#"]');
  var primera = true;
  var mostrar = function(){
    var pedido = (window.location.hash || '').slice(1);
    var actual = 'inicio';
    Array.prototype.forEach.call(vistas, function(v){ if (v.getAttribute('data-vista') === pedido) actual = pedido; });
    var cambiar = function(){
      Array.prototype.forEach.call(vistas, function(v){ v.hidden = v.getAttribute('data-vista') !== actual; });
      Array.prototype.forEach.call(enlaces, function(a){
        var es = a.getAttribute('href') === '#' + actual && !a.classList.contains('logo');
        a.classList.toggle('activo', es && a.classList.contains('lnk'));
        if (es) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
      });
      window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
    };
    var quieto = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!primera && !quieto && document.startViewTransition) document.startViewTransition(cambiar); else cambiar();
    primera = false;
  };
  window.addEventListener('hashchange', mostrar);
  mostrar();
})();
