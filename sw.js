const CACHE_NAME = 'pacdi-v1';
const ASSETS = ['./'];
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS))));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))));
self.addEventListener('fetch', e => e.respondWith(caches.match(e.request).then(r => {
  if (r) { fetch(e.request).then(nr => { if(nr.status===200) caches.open(CACHE_NAME).then(c=>c.put(e.request,nr)); }).catch(()=>{}); return r; }
  return fetch(e.request);
})));
