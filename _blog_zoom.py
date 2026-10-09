# -*- coding: utf-8 -*-
"""Shared Mermaid click-to-zoom markup for Hermes blog generators."""

ZOOM_CSS = """
    /* Click-to-zoom for diagrams */
    .mermaid { cursor: zoom-in; }
    .zoom-overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,.85);
      display: none; align-items: center; justify-content: center;
      z-index: 9999; padding: 40px; cursor: zoom-out;
    }
    .zoom-overlay.open { display: flex; }
    .zoom-overlay svg {
      max-width: 95vw; max-height: 90vh; width: auto; height: auto;
      background: var(--surface); border-radius: 12px; padding: 24px;
    }
"""

ZOOM_SNIPPET = """  <div class="zoom-overlay" id="zoomOverlay" aria-hidden="true"></div>
  <script>
    (function () {
      var zoomOverlay = document.getElementById('zoomOverlay');
      if (!zoomOverlay) return;
      function closeZoom() {
        zoomOverlay.classList.remove('open');
        zoomOverlay.innerHTML = '';
        zoomOverlay.setAttribute('aria-hidden', 'true');
      }
      document.querySelectorAll('.mermaid').forEach(function (el) {
        el.addEventListener('click', function () {
          var svg = el.querySelector('svg');
          if (!svg) return;
          zoomOverlay.innerHTML = '';
          zoomOverlay.appendChild(svg.cloneNode(true));
          zoomOverlay.classList.add('open');
          zoomOverlay.setAttribute('aria-hidden', 'false');
        });
      });
      zoomOverlay.addEventListener('click', closeZoom);
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeZoom();
      });
    })();
  </script>
"""
