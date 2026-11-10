/* Anitha Techsolutions — 3D hero: many systems integrating into one platform.
   Real Odoo app icons orbit a central core; data pulses flow from each app into the platform.
   Requires three.js (global THREE). Falls back silently to the CSS background. */
(function () {
  var canvas = document.getElementById('hero3d');
  if (!canvas || !window.THREE) return;

  var renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, powerPreference: 'low-power' });
  } catch (e) { return; }

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var BLUE = 0x2F5BEA, BLUE2 = 0x5F86FF, GOLD = 0xC6A15B;
  var apps = [];
  try { apps = JSON.parse(canvas.getAttribute('data-apps') || '[]'); } catch (e) { apps = []; }

  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
  camera.position.set(0, 0, 14);
  var world = new THREE.Group();
  scene.add(world);

  function easeOut(x) { return 1 - Math.pow(1 - Math.min(Math.max(x, 0), 1), 3); }

  // Soft round glow texture
  var glowTex = (function () {
    var c = document.createElement('canvas'); c.width = c.height = 128;
    var g = c.getContext('2d'), grd = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    grd.addColorStop(0, 'rgba(160,190,255,1)'); grd.addColorStop(0.35, 'rgba(47,91,234,.5)'); grd.addColorStop(1, 'rgba(47,91,234,0)');
    g.fillStyle = grd; g.fillRect(0, 0, 128, 128);
    return new THREE.CanvasTexture(c);
  })();
  function glow(size, opacity) {
    var s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: opacity }));
    s.scale.set(size, size, 1);
    return s;
  }

  // Core platform
  var core = new THREE.Group();
  world.add(core);
  var ico = new THREE.Mesh(new THREE.IcosahedronGeometry(1.6, 1),
    new THREE.MeshBasicMaterial({ color: BLUE2, wireframe: true, transparent: true, opacity: 0.5 }));
  var inner = new THREE.Mesh(new THREE.IcosahedronGeometry(1.0, 2), new THREE.MeshBasicMaterial({ color: BLUE, transparent: true, opacity: 0.92 }));
  core.add(ico); core.add(inner); core.add(glow(7, 1));

  // Orbit rings
  var RADII = [2.9, 3.9, 4.9], rings = [];
  [[1.15, 0.3], [-0.55, 0.85], [0.35, -0.5]].forEach(function (rot, i) {
    var ring = new THREE.Mesh(new THREE.TorusGeometry(RADII[i], 0.012, 8, 180),
      new THREE.MeshBasicMaterial({ color: i === 2 ? GOLD : BLUE2, transparent: true, opacity: 0.28 }));
    ring.rotation.set(rot[0], rot[1], 0);
    world.add(ring); rings.push(ring);
  });

  // App card texture: white rounded tile with the real app icon + label underneath
  function appTexture(app, done) {
    var W = 256, H = 300, c = document.createElement('canvas'); c.width = W; c.height = H;
    var g = c.getContext('2d');
    function draw(img) {
      g.clearRect(0, 0, W, H);
      g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 24; g.shadowOffsetY = 8;
      g.fillStyle = '#ffffff';
      var x = 48, y = 18, s = 160, r = 36;
      g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + s, y, x + s, y + s, r); g.arcTo(x + s, y + s, x, y + s, r);
      g.arcTo(x, y + s, x, y, r); g.arcTo(x, y, x + s, y, r); g.closePath(); g.fill();
      g.shadowColor = 'transparent';
      if (img) g.drawImage(img, x + 26, y + 26, s - 52, s - 52);
      g.font = '700 34px Montserrat, system-ui, sans-serif'; g.textAlign = 'center';
      g.fillStyle = 'rgba(14,27,51,.85)'; g.fillText(app.label, W / 2 + 2, 246);
      g.fillStyle = '#ffffff'; g.fillText(app.label, W / 2, 244);
      done(new THREE.CanvasTexture(c));
    }
    var img = new Image();
    img.onload = function () { draw(img); };
    img.onerror = function () { draw(null); };
    img.src = app.src;
  }

  // Nodes on orbits
  var nodes = [];
  var COUNT = Math.max(apps.length, 9);
  for (var i = 0; i < COUNT; i++) {
    var ringIdx = i % 3;
    var holder = new THREE.Group();
    var spriteMat = new THREE.SpriteMaterial({ transparent: true, depthWrite: false, opacity: 0 });
    var sprite = new THREE.Sprite(spriteMat);
    sprite.scale.set(1.25, 1.46, 1);
    sprite.renderOrder = 10;                      // cards always drawn above lines and pulses
    spriteMat.depthTest = false;
    holder.add(glow(1.6, 0.35));
    holder.add(sprite);
    world.add(holder);
    if (apps[i]) {
      (function (m) {
        appTexture(apps[i], function (tex) {
          try { m.map = tex; m.needsUpdate = true; } catch (e) { /* tainted canvas (file://): keep glow only */ }
        });
      })(spriteMat);
    }
    nodes.push({ holder: holder, mat: spriteMat, ring: rings[ringIdx], radius: RADII[ringIdx],
                 angle: Math.floor(i / 3) * (Math.PI * 2 / Math.ceil(COUNT / 3)) + ringIdx * 1.05, speed: [0.07, -0.05, 0.035][ringIdx] });
  }

  // Connection lines + travelling data pulses
  var linePos = new Float32Array(COUNT * 6);
  var lineGeo = new THREE.BufferGeometry();
  lineGeo.setAttribute('position', new THREE.BufferAttribute(linePos, 3));
  var lineMat = new THREE.LineBasicMaterial({ color: BLUE2, transparent: true, opacity: 0, blending: THREE.AdditiveBlending });
  world.add(new THREE.LineSegments(lineGeo, lineMat));
  var pulses = nodes.map(function (n, k) {
    var p = glow(0.55, 0.95); world.add(p);
    return { sprite: p, phase: k / COUNT };
  });

  // Particle field
  var PCOUNT = window.innerWidth < 700 ? 300 : 700, pPos = new Float32Array(PCOUNT * 3);
  for (var q = 0; q < PCOUNT; q++) {
    var rr = 6 + Math.random() * 18, th = Math.random() * Math.PI * 2, ph = Math.acos(2 * Math.random() - 1);
    pPos[q * 3] = rr * Math.sin(ph) * Math.cos(th);
    pPos[q * 3 + 1] = rr * Math.sin(ph) * Math.sin(th) * 0.6;
    pPos[q * 3 + 2] = rr * Math.cos(ph) - 6;
  }
  var pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
  var particles = new THREE.Points(pGeo, new THREE.PointsMaterial({ color: 0x9FB6FF, size: 0.04, transparent: true, opacity: 0.6, depthWrite: false }));
  scene.add(particles);

  var tmp = new THREE.Vector3(), narrow = false;
  function place(t, intro) {
    for (var k = 0; k < nodes.length; k++) {
      var n = nodes[k], a = n.angle + t * n.speed;
      tmp.set(Math.cos(a) * n.radius, Math.sin(a) * n.radius, 0).applyEuler(n.ring.rotation);
      n.holder.position.copy(tmp);
      // each app appears one after another during the intro
      var appear = easeOut((intro - 0.15 - k * 0.07) / 0.5);
      n.holder.scale.setScalar(0.6 + 0.4 * appear);
      n.mat.opacity = appear * (narrow ? 0.14 : 1);
      linePos[k * 6] = 0; linePos[k * 6 + 1] = 0; linePos[k * 6 + 2] = 0;
      linePos[k * 6 + 3] = tmp.x; linePos[k * 6 + 4] = tmp.y; linePos[k * 6 + 5] = tmp.z;
      // data pulse: travels from the app to the core, then repeats
      var f = ((t * 0.28 + pulses[k].phase) % 1);
      pulses[k].sprite.position.copy(tmp).multiplyScalar(1 - easeOut(f));
      pulses[k].sprite.material.opacity = appear * Math.sin(Math.PI * f) * 0.95;
    }
    lineGeo.attributes.position.needsUpdate = true;
    lineMat.opacity = 0.3 * easeOut((intro - 0.4) / 0.6);
  }

  function layout() {
    var w = canvas.clientWidth, h = canvas.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    narrow = w <= 920;
    world.position.set(narrow ? 0 : 3.7, narrow ? 2.4 : 0.2, 0);
    world.userData.baseScale = narrow ? 0.62 : 0.95;
  }

  var mouseX = 0, mouseY = 0;
  window.addEventListener('pointermove', function (e) {
    mouseX = (e.clientX / window.innerWidth) * 2 - 1;
    mouseY = (e.clientY / window.innerHeight) * 2 - 1;
  }, { passive: true });

  var running = true, start = performance.now();
  function frame(now) {
    var t = (now - start) / 1000, intro = Math.min(t / 2.2, 1);
    world.scale.setScalar(world.userData.baseScale * (0.85 + 0.15 * easeOut(intro)));
    core.rotation.y = t * 0.18; core.rotation.x = Math.sin(t * 0.25) * 0.15;
    ico.rotation.z = t * 0.07;
    inner.scale.setScalar(1 + Math.sin(t * 1.2) * 0.035);   // slow "breathing"
    place(t, intro);
    particles.rotation.y = t * 0.008;
    world.rotation.y += ((mouseX * 0.28) - world.rotation.y) * 0.03;
    world.rotation.x += ((mouseY * 0.16) - world.rotation.x) * 0.03;
    renderer.render(scene, camera);
    if (running && !reduced) requestAnimationFrame(frame);
  }

  layout();
  window.addEventListener('resize', layout);
  if (reduced) {
    world.scale.setScalar(world.userData.baseScale);
    place(0, 1);
    setTimeout(function () { renderer.render(scene, camera); }, 600);   // after textures load
    return;
  }

  var visible = true;
  function setRunning(on) {
    if (on && !running) { running = true; requestAnimationFrame(frame); }
    else if (!on) running = false;
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; setRunning(visible && !document.hidden); }).observe(canvas);
  }
  document.addEventListener('visibilitychange', function () { setRunning(visible && !document.hidden); });
  requestAnimationFrame(frame);
})();
