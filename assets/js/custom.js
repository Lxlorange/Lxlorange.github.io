/**
 * Custom enhancements for 柚子的笔记
 * - Reading progress bar
 * - Image click interaction enhancement
 * - Smooth scroll for anchor links
 */
(function () {
  if (typeof window === 'undefined') return;

  function init() {
    initProgressBar();
    initImageInteraction();
  }

  /* ================================================================
     Reading Progress Bar
     ================================================================ */
  function initProgressBar() {
    var bar = document.createElement('div');
    bar.id = 'reading-progress';
    document.body.prepend(bar);

    var ticking = false;
    function update() {
      var scrollTop = window.scrollY || document.documentElement.scrollTop;
      var docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      if (docHeight <= 0) return;
      var progress = Math.min((scrollTop / docHeight) * 100, 100);
      bar.style.width = progress + '%';
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(update);
        ticking = true;
      }
    }, { passive: true });

    // Initial call
    update();
  }

  /* ================================================================
     Image Interaction — click feedback for popup images
     ================================================================ */
  function initImageInteraction() {
    // Add cursor pointer class to content images — GLightbox handles the rest
    document.addEventListener('click', function (e) {
      var img = e.target.closest('.content img');
      if (!img) return;
      // GLightbox in Chirpy handles the popup via refactor-content.js.
      // We just ensure the cursor feedback is there.
    });
  }

  /* ================================================================
     Smooth scroll for same-page anchor links
     ================================================================ */
  document.addEventListener('click', function (e) {
    var anchor = e.target.closest('a[href^="#"]');
    if (!anchor) return;
    var href = anchor.getAttribute('href');
    if (!href || href === '#') return;
    var target = document.querySelector(href);
    if (!target) return;

    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    // Update URL without jump
    history.pushState(null, null, href);
  });

  /* ================================================================
     Start
     ================================================================ */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
