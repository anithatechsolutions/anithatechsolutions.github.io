/* Anitha Techsolutions — site interactions: header, mobile menu, reveal, 3D tilt, contact form, install-as-app. */
(function () {
  var header = document.querySelector('.site-header');
  var hasHero = document.querySelector('.hero, .page-hero');
  function onScroll() { if (header) header.classList.toggle('solid', window.scrollY > 40 || !hasHero); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  var toggle = document.querySelector('.menu-toggle'), nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) header.classList.add('solid'); else onScroll();
    });
    nav.addEventListener('click', function (e) { if (e.target.tagName === 'A') { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); } });
  }

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('in'); }); }

  // 3D tilt on cards (pointer devices only)
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduced && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('[data-tilt]').forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = 'perspective(900px) rotateY(' + (x * 10) + 'deg) rotateX(' + (-y * 10) + 'deg) translateY(-4px)';
      });
      card.addEventListener('pointerleave', function () { card.style.transform = ''; });
    });
  }

  // Contact form -> opens the visitor's email app with the details filled in
  var form = document.getElementById('contact-form');
  if (form) {
    var status = document.getElementById('form-status');
    var button = form.querySelector('button[type="submit"]');
    var buttonHTML = button.innerHTML;
    function show(kind, html) { status.className = 'form-status ' + kind; status.innerHTML = html; status.hidden = false; }
    function mailtoFallback(f) {
      var subject = 'Enquiry: ' + f.service.value + ' - ' + f.name.value;
      var body = 'Name: ' + f.name.value + '\nEmail: ' + f.email.value + '\nCompany: ' + (f.company.value || '-') +
        '\nPhone: ' + (f.phone.value || '-') + '\nService: ' + f.service.value + '\n\n' + f.message.value;
      return 'mailto:' + form.dataset.to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var f = form.elements;
      if (f.website.value) { form.reset(); show('ok', 'Thank you — your message has been sent.'); return; } // bot
      var data = {
        name: f.name.value, email: f.email.value, company: f.company.value || '-', phone: f.phone.value || '-',
        service: f.service.value, message: f.message.value,
        _subject: 'Website enquiry: ' + f.service.value + ' - ' + f.name.value,
        _replyto: f.email.value, _template: 'table', _captcha: 'false'
      };
      button.disabled = true; button.textContent = 'Sending…'; status.hidden = true;
      fetch(form.dataset.endpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data)
      }).then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (j) {
          if (!res.ok || j.success === 'false' || j.success === false || j.errors) throw new Error(j.message || 'Send failed');
        });
      }).then(function () {
        form.reset();
        show('ok', '<b>Thank you!</b> Your message has been sent. We will reply within one business day.');
      }).catch(function () {
        show('err', 'Sorry, the message could not be sent. Please <a href="' + mailtoFallback(f) + '">send it by email instead</a> or write to <a href="mailto:' + form.dataset.to + '">' + form.dataset.to + '</a>.');
      }).then(function () { button.disabled = false; button.innerHTML = buttonHTML; });
    });
  }


  // Typing line in the hero: types a word, pauses like a person would, erases, moves on
  var typed = document.querySelector('.typed');
  if (typed && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var words = typed.getAttribute('data-words').split('|'), wi = 0, ci = words[0].length, deleting = true;
    function tick() {
      var w = words[wi];
      ci += deleting ? -1 : 1;
      typed.textContent = w.slice(0, ci);
      var delay = deleting ? 45 : 85 + Math.random() * 70;
      if (!deleting && ci === w.length) { deleting = true; delay = 1800; }
      else if (deleting && ci === 0) { deleting = false; wi = (wi + 1) % words.length; delay = 350; }
      setTimeout(tick, delay);
    }
    setTimeout(tick, 2600);
  }

  // Year
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Install as app (PWA)
  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    window.addEventListener('load', function () { navigator.serviceWorker.register('/sw.js').catch(function () {}); });
  }
  var deferred, bar = document.getElementById('install-bar');
  function dismissed() { try { return localStorage.getItem('installDismissed') === '1'; } catch (e) { return false; } }
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault(); deferred = e;
    if (bar && !dismissed()) setTimeout(function () { bar.hidden = false; requestAnimationFrame(function () { bar.classList.add('show'); }); }, 4000);
  });
  if (bar) {
    bar.querySelector('.btn').addEventListener('click', function () {
      bar.classList.remove('show');
      if (deferred) { deferred.prompt(); deferred = null; }
    });
    bar.querySelector('.x').addEventListener('click', function () {
      bar.classList.remove('show');
      try { localStorage.setItem('installDismissed', '1'); } catch (e) {}
    });
  }
})();
