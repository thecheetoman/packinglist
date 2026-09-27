(function () {
  var btn = document.getElementById('install-btn');
  var bar = document.getElementById('ios-shortcut');
  var hint = document.getElementById('ios-hint');
  var deferred = null;

  function isStandalone() {
    return window.matchMedia('(display-mode: standalone)').matches ||
      window.matchMedia('(display-mode: fullscreen)').matches ||
      window.navigator.standalone === true;
  }

  function isIOS() {
    return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  }

  function hide() {
    if (btn) btn.hidden = true;
    if (bar) bar.hidden = true;
  }

  if (isStandalone()) {
    hide();
    return;
  }

  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferred = e;
    if (btn) {
      btn.hidden = false;
    }
  });

  if (btn) {
    btn.addEventListener('click', function () {
      if (!deferred) return;
      btn.hidden = true;
      deferred.prompt();
      deferred.userChoice.then(function (choice) {
        if (choice.outcome === 'accepted') hide();
        deferred = null;
      });
    });
  }

  window.addEventListener('appinstalled', function () {
    deferred = null;
    hide();
  });

  if (isIOS()) {
    if (bar) {
      bar.hidden = false;
      bar.addEventListener('click', function () {
        bar.hidden = true;
        if (hint) hint.hidden = false;
      });
    }
    if (hint) {
      hint.addEventListener('click', function () {
        hint.hidden = true;
      });
    }
  }
})();
