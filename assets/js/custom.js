/**
 * Reading progress bar — thin fixed bar at page top
 */
(function () {
  if (typeof window === 'undefined') return;

  function init() {
    var bar = document.createElement('div');
    bar.id = 'reading-progress';
    document.body.prepend(bar);

    var ticking = false;
    function update() {
      var scrollTop = window.scrollY || document.documentElement.scrollTop;
      var docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      if (docHeight <= 0) return;
      bar.style.width = Math.min((scrollTop / docHeight) * 100, 100) + '%';
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(update);
        ticking = true;
      }
    }, { passive: true });

    update();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
