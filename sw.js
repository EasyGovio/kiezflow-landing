const CACHE_NAME = 'pacdi-20260814-175254';
const ASSETS = ['./'];
self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)));
});
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(cached => {
      const revalidate = fetch(e.request)
        .then(fresh => {
          if (fresh && fresh.status === 200) {
            const copy = fresh.clone();
            caches.open(CACHE_NAME).then(c => c.put(e.request, copy));
          }
          return fresh;
        })
        .catch(() => null);
      e.waitUntil(revalidate);
      if (cached) return cached;
      return revalidate.then(fresh => {
        if (fresh) return fresh;
        return new Response('Baglanti sorunu olustu, lutfen tekrar deneyin.', {
          status: 503, statusText: 'Service Unavailable',
          headers: { 'Content-Type': 'text/plain; charset=utf-8' }
        });
      });
    })
  );
});
