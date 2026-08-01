// KIEZ ÖNERİ SİSTEMİ — bağımsız modül
// server.js bunu tek satırla çağırır, server.js'in kendisine dokunmaz.
module.exports = function(app, db, checkAuth, rateLimit) {

  db.exec(`
    CREATE TABLE IF NOT EXISTS kiez_oneriler (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      isletme_adi TEXT NOT NULL,
      sokak TEXT,
      not_metni TEXT,
      oneren_isim TEXT,
      oneren_iletisim TEXT,
      durum TEXT DEFAULT 'bekliyor',
      created_at TEXT DEFAULT (datetime('now')),
      onaylanma_tarihi TEXT
    );
  `);

  const kiezLimiter = rateLimit({
    windowMs: 60 * 60 * 1000,
    max: 10,
    standardHeaders: true,
    legacyHeaders: false,
    message: { ok: false, error: 'Saatlik öneri limitine ulaşıldı, lütfen sonra tekrar deneyin.' }
  });

  app.post('/api/kiez/oneri', kiezLimiter, (req, res) => {
    const { isletme_adi, sokak, not_metni, oneren_isim, oneren_iletisim } = req.body || {};
    if (!isletme_adi || typeof isletme_adi !== 'string') {
      return res.status(400).json({ ok: false, error: 'İşletme adı zorunlu' });
    }
    db.prepare(`INSERT INTO kiez_oneriler (isletme_adi, sokak, not_metni, oneren_isim, oneren_iletisim)
                VALUES (?, ?, ?, ?, ?)`)
      .run(isletme_adi, sokak || null, not_metni || null, oneren_isim || null, oneren_iletisim || null);
    res.json({ ok: true, mesaj: 'Öneriniz alındı, incelendikten sonra yayınlanacak. Teşekkürler!' });
  });

  app.get('/api/kiez/oneriler/onayli', (req, res) => {
    const rows = db.prepare(`SELECT id, isletme_adi, sokak, not_metni, oneren_isim, onaylanma_tarihi
                              FROM kiez_oneriler WHERE durum = 'onaylandi' ORDER BY onaylanma_tarihi DESC`).all();
    res.json({ ok: true, oneriler: rows });
  });

  app.get('/api/kiez/oneriler', checkAuth, (req, res) => {
    const rows = db.prepare(`SELECT * FROM kiez_oneriler ORDER BY created_at DESC`).all();
    res.json({ ok: true, oneriler: rows });
  });

  app.put('/api/kiez/oneriler/:id/onayla', checkAuth, (req, res) => {
    db.prepare(`UPDATE kiez_oneriler SET durum = 'onaylandi', onaylanma_tarihi = datetime('now') WHERE id = ?`)
      .run(req.params.id);
    res.json({ ok: true });
  });

  app.delete('/api/kiez/oneriler/:id', checkAuth, (req, res) => {
    db.prepare(`DELETE FROM kiez_oneriler WHERE id = ?`).run(req.params.id);
    res.json({ ok: true });
  });

  console.log('Kiez öneri sistemi yüklendi (/api/kiez/...)');
};
