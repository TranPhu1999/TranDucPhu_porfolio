(function () {
  var root = document.documentElement;
  root.classList.remove('no-js');

  // theme toggle
  var btn = document.querySelector('.theme-toggle');
  function setTheme(t) {
    root.setAttribute('data-theme', t);
    if (btn) btn.setAttribute('aria-label', t === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  }
  setTheme(root.getAttribute('data-theme') || 'light');
  if (btn) btn.addEventListener('click', function () {
    var t = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    setTheme(t);
    try { localStorage.setItem('theme', t); } catch (e) {}
  });
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
      var saved = null; try { saved = localStorage.getItem('theme'); } catch (_) {}
      if (!saved) setTheme(e.matches ? 'dark' : 'light');
    });
  }

  // mobile menu
  var menu = document.querySelector('.menu-btn'), links = document.querySelector('.nav-links');
  if (menu && links) {
    menu.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      menu.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { links.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); }
    });
  }

  // reveal on scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('in'); }); }

  // typed text
  var typed = document.querySelector('.typed');
  if (typed) {
    var words = JSON.parse(typed.getAttribute('data-words') || '[]');
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce || !words.length) { typed.textContent = words.join(' · '); }
    else {
      var wi = 0, ci = 0, del = false;
      (function tick() {
        var w = words[wi];
        typed.textContent = w.slice(0, ci);
        if (!del && ci < w.length) ci++;
        else if (!del) { del = true; return setTimeout(tick, 1600); }
        else if (ci > 0) ci--;
        else { del = false; wi = (wi + 1) % words.length; }
        setTimeout(tick, del ? 35 : 70);
      })();
    }
  }

  // reading progress + toc highlight
  var bar = document.querySelector('.progress'), article = document.querySelector('.prose');
  if (bar && article) {
    var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
    var heads = tocLinks.map(function (a) { return document.getElementById(decodeURIComponent(a.hash.slice(1))); }).filter(Boolean);
    var onScroll = function () {
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight;
      var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 1;
      bar.style.width = (p * 100) + '%';
      var cur = null;
      heads.forEach(function (h) { if (h.getBoundingClientRect().top < 120) cur = h.id; });
      tocLinks.forEach(function (a) { a.classList.toggle('active', a.hash.slice(1) === cur); });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // copy link
  var copy = document.querySelector('[data-copy]');
  if (copy) copy.addEventListener('click', function () {
    var url = copy.getAttribute('data-copy');
    if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () {
      copy.textContent = 'Copied!'; setTimeout(function () { copy.textContent = 'Copy link'; }, 1500);
    });
  });
})();
