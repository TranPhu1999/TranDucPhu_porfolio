(function () {
  var list = document.getElementById('post-list');
  var input = document.getElementById('search');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.filter'));
  var count = document.getElementById('count');
  if (!list) return;
  var posts = [], topic = 'All';

  var params = new URLSearchParams(location.search);
  if (params.get('topic')) topic = params.get('topic');
  if (params.get('q')) input.value = params.get('q');

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]; }); }

  function render() {
    var q = input.value.trim().toLowerCase();
    chips.forEach(function (c) { c.setAttribute('aria-pressed', c.dataset.topic === topic ? 'true' : 'false'); });
    var shown = posts.filter(function (p) {
      var okTopic = topic === 'All' || p.topics.indexOf(topic) !== -1;
      var hay = (p.title + ' ' + p.summary + ' ' + p.tags.join(' ')).toLowerCase();
      return okTopic && (!q || hay.indexOf(q) !== -1);
    });
    list.innerHTML = shown.map(function (p) {
      return '<a class="card post-card" href="' + esc(p.slug) + '/">' +
        '<div class="meta"><time datetime="' + p.date + '">' + esc(p.date_human) + '</time> · ' + p.reading_time + ' min read</div>' +
        '<h2>' + esc(p.title) + '</h2><p>' + esc(p.summary) + '</p>' +
        '<ul class="tags">' + p.tags.map(function (t) { return '<li class="tag">' + esc(t) + '</li>'; }).join('') + '</ul></a>';
    }).join('') || '<p class="empty">No posts match. Try another search or topic.</p>';
    if (count) count.textContent = shown.length + (shown.length === 1 ? ' post' : ' posts');
  }

  chips.forEach(function (c) { c.addEventListener('click', function () { topic = c.dataset.topic; render(); }); });
  input.addEventListener('input', render);

  fetch('posts.json').then(function (r) { return r.json(); }).then(function (d) { posts = d; render(); })
    .catch(function () { /* keep server-rendered list */ });
})();
