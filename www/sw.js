// Offline app-shell cache for the web/PWA version (skipped inside the Android app).
const CACHE = 'valiryan-v1';
const SHELL = ['./', './index.html', './manifest.webmanifest', './vendor/jsmediatags.min.js',
  './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png', './favicon.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(k => Promise.all(k.filter(x => x !== CACHE).map(x => caches.delete(x)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET' || new URL(r.url).origin !== location.origin) return;
  e.respondWith(caches.match(r).then(hit => hit || fetch(r).then(res => {
    const copy = res.clone(); caches.open(CACHE).then(c => c.put(r, copy)); return res;
  }).catch(() => caches.match('./index.html'))));
});
