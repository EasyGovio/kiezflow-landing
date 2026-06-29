import os, sys

domain = "example.com"
if os.path.exists("CNAME"):
    with open("CNAME") as f:
        domain = f.read().strip()

print("Domain:", domain)

ANALYTICS = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-E6ML8EDW0H"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-E6ML8EDW0H");</script>'
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8426936740213369" crossorigin="anonymous"></script>'

ASCII_MUHUR = """<!--
\u256c\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u256e
\u2551         \U0001f6e1\ufe0f  PACDI FRAMEWORK \u2014 PROTECTED WORK                  \u2551
\u2551                                                               \u2551
\u2551  \u00a9 2026 PACDI Global Yaz\u0131l\u0131m Ltd. \u015eti.                       \u2551
\u2551  FSEK Registration No : 2026/18897                            \u2551
\u2551  Trade Registry      : 23836 \u00b7 Yunusemre / Manisa, TR       \u2551
\u2551                                                               \u2551
\u2551  This work and its modular software architecture are          \u2551
\u2551  protected under PACDI Software Library FSEK registration.   \u2551
\u2551  Unauthorized copying is subject to legal action.            \u2551
\u2551                                                               \u2551
\u2551  pacdi.eu \u00b7 pacdi.de \u00b7 info@pacdi.eu                         \u2551
\u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563
-->"""

PWA_HEAD = """    <link rel="manifest" href="/manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="PACDI">
"""

PWA_SCRIPT = """<script>
(function() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(function(){});
  }

  var isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
  var isInStandalone = ('standalone' in navigator && navigator.standalone);
  var shown = sessionStorage.getItem('pwa-banner-shown');
  if (shown || isInStandalone) return;

  // iOS Safari — manuel yönlendirme
  if (isIOS) {
    setTimeout(function() {
      var bar = document.createElement('div');
      bar.id = 'pwa-banner';
      bar.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#04162E;border-top:2px solid #F6B45F;padding:14px 16px;z-index:9999;font-family:system-ui;';
      bar.innerHTML =
        '<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;">' +
          '<div>' +
            '<div style="color:#F6B45F;font-size:0.82rem;font-weight:700;margin-bottom:4px;">📲 Ana ekrana ekle</div>' +
            '<div style="color:#b0b5bf;font-size:0.75rem;line-height:1.5;">' +
              'Safari'de <strong style="color:#eaf2fb;">&#11015; Paylaş</strong> butonuna bas, ' +
              'ardından <strong style="color:#eaf2fb;">Ana Ekrana Ekle</strong> seçeneğini seç.' +
            '</div>' +
            '<div style="color:#4a6a88;font-size:0.68rem;margin-top:4px;">&#9432; iOS'ta otomatik kurulum desteklenmiyor — bu adım gerekli.</div>' +
          '</div>' +
          '<button onclick="document.getElementById('pwa-banner').remove();sessionStorage.setItem('pwa-banner-shown','1')" ' +
            'style="background:transparent;border:none;color:#7a9ab8;font-size:1.2rem;cursor:pointer;padding:0 4px;flex-shrink:0;">✕</button>' +
        '</div>';
      document.body.appendChild(bar);
      sessionStorage.setItem('pwa-banner-shown', '1');
    }, 3000);
    return;
  }

  // Android / Desktop Chrome — otomatik install prompt
  var deferredPrompt = null;
  window.addEventListener('beforeinstallprompt', function(e) {
    e.preventDefault();
    deferredPrompt = e;
    setTimeout(function() {
      if (!deferredPrompt) return;
      var bar = document.createElement('div');
      bar.id = 'pwa-banner';
      bar.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#04162E;border-top:2px solid #F6B45F;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;z-index:9999;font-family:system-ui;';
      bar.innerHTML =
        '<span style="color:#eaf2fb;font-size:0.85rem;">📲 Ana ekrana ekle &mdash; daha hızlı aç!</span>' +
        '<div style="display:flex;gap:8px;">' +
          '<button onclick="installPWA()" style="background:#F6B45F;border:none;color:#04162E;padding:6px 16px;border-radius:20px;font-weight:700;cursor:pointer;font-size:0.82rem;">Ekle</button>' +
          '<button onclick="document.getElementById(\'pwa-banner\').remove();sessionStorage.setItem(\'pwa-banner-shown\',\'1\')" style="background:transparent;border:1px solid rgba(246,180,95,0.3);color:#7a9ab8;padding:6px 12px;border-radius:20px;cursor:pointer;font-size:0.82rem;">Sonra</button>' +
        '</div>';
      document.body.appendChild(bar);
    }, 3000);
  });

  window.installPWA = function() {
    if (deferredPrompt) { deferredPrompt.prompt(); deferredPrompt.userChoice.then(function(){ deferredPrompt=null; }); }
    var b = document.getElementById('pwa-banner'); if (b) b.remove();
    sessionStorage.setItem('pwa-banner-shown', '1');
  };
})();
</script>
"""

FSEK_FOOTER = """<div id="pacdi-fsek" style="clear:both;width:100%;display:block;text-align:center;padding:28px 16px 20px;border-top:1px solid rgba(212,175,55,0.15);margin-top:32px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;box-sizing:border-box;">
  <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(212,175,55,0.06);border:1px solid rgba(212,175,55,0.25);border-radius:24px;padding:8px 20px;margin-bottom:12px;flex-wrap:wrap;justify-content:center;">
    <span style="font-size:1rem;">\U0001f6e1\ufe0f</span>
    <span style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;color:#D4AF37;text-transform:uppercase;">FSEK Registered \u00b7 PACDI Framework</span>
  </div>
  <div style="font-size:0.78rem;color:#8A8F9A;margin-bottom:4px;">Operated by AskMeAI Teknoloji Ltd. \u015eti. (TR: 23837)</div>
  <div style="font-size:0.72rem;color:#6B7280;margin-bottom:10px;">Intellectual property owned by \u00a9 2026 PACDI Global Yaz\u0131l\u0131m Ltd. \u015eti. &mdash; FSEK No: <a href="https://pacdi.eu/legal.html" style="color:#D4AF37;text-decoration:none;">2026/18897</a></div>
  <div style="font-size:0.82rem;font-style:italic;color:#6B7280;">&ldquo;Technology in the service of humanity.&rdquo;</div>
</div>"""

# ── Legal.html content (standard — all repos except pacdi.store) ──
LEGAL_HTML = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Impressum &amp; Datenschutz</title>
    <meta name="robots" content="noindex, nofollow">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-E6ML8EDW0H"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-E6ML8EDW0H");</script>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #04162E; color: #e8edf2; padding: 40px 20px 80px; line-height: 1.75; }}
        .wrap {{ max-width: 760px; margin: 0 auto; }}
        .back {{ display: inline-flex; align-items: center; gap: 6px; color: #7a9ab8; text-decoration: none; font-size: 0.85rem; margin-bottom: 36px; }}
        .back:hover {{ color: #F6B45F; }}
        h1 {{ font-size: 1.6rem; color: #F6B45F; margin-bottom: 6px; }}
        .subtitle {{ font-size: 0.85rem; color: #7a9ab8; margin-bottom: 36px; }}
        h2 {{ font-size: 0.8rem; font-weight: 700; color: #F6B45F; margin: 28px 0 10px; text-transform: uppercase; letter-spacing: 0.06em; }}
        p {{ font-size: 0.88rem; color: #8a9ab0; margin-bottom: 10px; }}
        a {{ color: #F6B45F; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        hr {{ border: none; border-top: 1px solid rgba(246,180,95,0.1); margin: 28px 0; }}
        .box {{ background: rgba(255,255,255,0.02); border: 1px solid rgba(246,180,95,0.15); border-radius: 12px; padding: 20px 24px; margin: 12px 0; }}
        .warn {{ background: rgba(246,180,95,0.05); border-left: 4px solid #F6B45F; border-radius: 8px; padding: 14px 18px; margin: 12px 0; }}
        .warn p {{ color: #c8cdd5; margin: 0; }}
        .fsek-block {{ text-align: center; padding: 28px 0 0; }}
        .fsek-badge {{ display: inline-flex; align-items: center; gap: 8px; background: rgba(212,175,55,0.06); border: 1px solid rgba(212,175,55,0.25); border-radius: 24px; padding: 8px 20px; margin-bottom: 12px; }}
        .fsek-badge span {{ font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; color: #D4AF37; text-transform: uppercase; }}
    </style>
</head>
<body>
<div class="wrap">
<a href="/" class="back">&larr; Zur&uuml;ck</a>
<h1>Impressum &amp; Datenschutz</h1>
<p class="subtitle">Vollst&auml;ndige rechtliche Informationen: <a href="https://pacdi.eu/legal.html" target="_blank">pacdi.eu/legal.html</a></p>

<h2>Impressum</h2>
<div class="box">
    <p><strong style="color:#e8edf2;">AskMeAI Teknoloji Ltd. &Scaron;ti.</strong><br>
    Ticaret Sicil No: 23837<br>
    Ayni Ali Mah. 3317 Sk. Nur Apt No:43 I&ccedil; Kap&imath; No:3<br>
    Yunusemre / Manisa, T&uuml;rkiye<br>
    MER&Scaron;&Iuml;S: 0086178065200001</p>
    <p style="margin-top:12px;"><strong style="color:#e8edf2;">Verantwortlicher gem&auml;&szlig; &sect; 18 Abs. 2 MStV:</strong><br>
    Mehmet Ayd&imath;nl&imath;<br>
    Bernauerstr. 115, 13507 Berlin, Deutschland<br>
    E-Mail: <a href="mailto:info@askmeai.io">info@askmeai.io</a></p>
</div>

<div class="warn">
    <p>Dieses Angebot ist ein digitaler Informationsdienst und stellt keine Rechts- oder Steuerberatung dar.</p>
</div>

<hr>

<h2>Datenschutzerkl&auml;rung</h2>

<h2>1. Datenerhebung</h2>
<p>Die meisten PACDI-Tools speichern Daten ausschlie&szlig;lich lokal in Ihrem Browser (localStorage). Es werden keine pers&ouml;nlichen Daten an unsere Server &uuml;bertragen.</p>

<h2>2. Google Analytics</h2>
<p>Diese Website verwendet Google Analytics (Google Ireland Limited). IP-Adressen werden vor der Speicherung anonymisiert. Opt-out: <a href="https://tools.google.com/dlpage/gaoptout" target="_blank">Google Analytics Opt-out Add-on</a>.</p>

<h2>3. Google AdSense</h2>
<p>Diese Website zeigt Werbeanzeigen &uuml;ber Google AdSense. AdSense verwendet Cookies f&uuml;r interessenbezogene Werbung. Weitere Informationen: <a href="https://policies.google.com/privacy" target="_blank">Google Datenschutzerkl&auml;rung</a>.</p>

<h2>4. Ihre Rechte (DSGVO Art. 15&ndash;21)</h2>
<p>Auskunft, Berichtigung, L&ouml;schung, Einschr&auml;nkung, Daten&uuml;bertragbarkeit, Widerspruch. Kontakt: <a href="mailto:info@askmeai.io">info@askmeai.io</a> &mdash; Antwort innerhalb von 30 Tagen.</p>

<h2>5. Geistiges Eigentum</h2>
<p>Alle Softwarearchitekturen und Inhaltsstrukturen sind Eigentum der <strong style="color:#e8edf2;">PACDI Global Yaz&imath;l&imath;m Ltd. &Scaron;ti.</strong> (TR: 23836) und gesch&uuml;tzt unter FSEK-Registrierung Nr. 2026/18897. Betrieben durch AskMeAI Teknoloji Ltd. &Scaron;ti. im Rahmen einer Sublizenz.</p>

<hr>

<div id="pacdi-fsek" class="fsek-block">
    <div class="fsek-badge"><span>&#128737;&#65039;</span><span>FSEK Registered &middot; PACDI Framework</span></div>
    <p style="font-size:0.78rem;color:#6B7280;margin-bottom:4px;">Operated by AskMeAI Teknoloji Ltd. &Scaron;ti. (TR: 23837)</p>
    <p style="font-size:0.72rem;color:#4a6a88;margin-bottom:6px;">&copy; 2026 PACDI Global Yaz&imath;l&imath;m Ltd. &Scaron;ti. &mdash; FSEK No: 2026/18897</p>
    <p style="font-size:0.82rem;font-style:italic;color:#4a6a88;">&ldquo;Technology in the service of humanity.&rdquo;</p>
</div>
</div>
</body>
</html>'''

SKIP = ['legal.html','impressum.html','datenschutz.html','404.html','master-template.html','test.html']
SKIP_FOOTER = ['legal.html','impressum.html','datenschutz.html','404.html','master-template.html','test.html']

# ── Write standard legal.html (skip if pacdi.store) ──
if domain != 'pacdi.store':
    legal_content = LEGAL_HTML.format()
    legal_path = 'legal.html'
    # Always overwrite to keep standard
    with open(legal_path, 'w', encoding='utf-8') as f:
        f.write(legal_content)
    print('Legal updated: legal.html')
else:
    print('Skipping legal.html for pacdi.store (has custom version)')

# ── manifest.json otomatik oluştur ──
import json
manifest = {
    "name": "PACDI — " + domain,
    "short_name": "PACDI",
    "description": "PACDI Digital — Technology in the service of humanity.",
    "start_url": "./index.html",
    "display": "standalone",
    "background_color": "#04162E",
    "theme_color": "#04162E",
    "orientation": "portrait",
    "categories": ["business", "productivity", "utilities"],
    "icons": [
        {
            "src": "https://cdn-icons-png.flaticon.com/512/6849/6849232.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any maskable"
        },
        {
            "src": "https://cdn-icons-png.flaticon.com/512/6849/6849232.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any maskable"
        }
    ]
}
with open('manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print('manifest.json created:', domain)

# ── sw.js otomatik oluştur ──
sw = "const CACHE_NAME = 'pacdi-v1';\n"
sw += "const ASSETS = ['./'];\n"
sw += "self.addEventListener('install', e => e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS))));\n"
sw += "self.addEventListener('activate', e => e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))));\n"
sw += "self.addEventListener('fetch', e => e.respondWith(caches.match(e.request).then(r => {\n"
sw += "  if (r) { fetch(e.request).then(nr => { if(nr.status===200) caches.open(CACHE_NAME).then(c=>c.put(e.request,nr)); }).catch(()=>{}); return r; }\n"
sw += "  return fetch(e.request);\n"
sw += "})));\n"
with open('sw.js', 'w', encoding='utf-8') as f:
    f.write(sw)
print('sw.js created:', domain)

# ── ads.txt otomatik oluştur ──
with open('ads.txt', 'w', encoding='utf-8') as f:
    f.write('google.com, pub-8426936740213369, DIRECT, f08c47fec0942fa0\n')
print('ads.txt created:', domain)

updated = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['.git','.github']]
    for fname in files:
        if not fname.endswith('.html') or fname.startswith('google4d'):
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if '</head>' not in content:
                continue
            orig = content
            relpath = fpath.replace('./','').replace('.\\','')
            if relpath == 'index.html':
                url = 'https://' + domain + '/'
            else:
                url = 'https://' + domain + '/' + relpath

            # ── HEAD injections ──
            insert = ''
            if 'G-E6ML8EDW0H' not in content:
                insert += '    ' + ANALYTICS + '\n'
            if 'ca-pub-8426936740213369' not in content and fname not in SKIP:
                insert += '    ' + ADSENSE + '\n'
            if 'canonical' not in content:
                insert += '    <link rel="canonical" href="' + url + '" />\n'
            if 'manifest.json' not in content and fname not in SKIP:
                insert += PWA_HEAD
            if insert:
                content = content.replace('</head>', insert + '</head>', 1)

            # ── PWA Script ──
            if 'serviceWorker' not in content and '</body>' in content and fname not in SKIP_FOOTER:
                content = content.replace('</body>', PWA_SCRIPT + '\n</body>', 1)

            # ── ASCII muhur → <body> sonrasi ──
            if 'PACDI FRAMEWORK' not in content and '<body' in content:
                body_end = content.find('>', content.find('<body')) + 1
                content = content[:body_end] + '\n' + ASCII_MUHUR + '\n' + content[body_end:]

            # ── FSEK footer eski versiyon güncelle ──
            if 'pacdi-fsek' in content:
                # Eski tek satırlı versiyon → yeni iki şirketli versiyon
                content = content.replace(
                    '<div style="font-size:0.78rem;color:#8A8F9A;margin-bottom:4px;">\u00a9 2026 PACDI Global Yaz\u0131l\u0131m Ltd. \u015eti.</div>\n  <div style="font-size:0.72rem;color:#6B7280;margin-bottom:10px;">Protected under FSEK Copyright Registration No: <a href="https://pacdi.eu" style="color:#D4AF37;text-decoration:none;">2026/18897</a></div>',
                    '<div style="font-size:0.78rem;color:#8A8F9A;margin-bottom:4px;">Operated by AskMeAI Teknoloji Ltd. \u015eti. (TR: 23837)</div>\n  <div style="font-size:0.72rem;color:#6B7280;margin-bottom:10px;">Intellectual property owned by \u00a9 2026 PACDI Global Yaz\u0131l\u0131m Ltd. \u015eti. &mdash; FSEK No: <a href="https://pacdi.eu/legal.html" style="color:#D4AF37;text-decoration:none;">2026/18897</a></div>'
                )

            # ── Inline Impressum fix: PACDI Global → AskMeAI ──
            if 'Verantwortlich: PACDI Global' in content:
                content = content.replace(
                    'Verantwortlich: PACDI Global',
                    'Verantwortlicher: Mehmet Ayd\u0131nl\u0131 / AskMeAI Teknoloji Ltd. \u015eti.'
                )
                print('Fixed: inline impressum ->', fpath)

            if 'Ein Service von PACDI Global' in content:
                content = content.replace(
                    'Ein Service von PACDI Global',
                    'Ein Service von AskMeAI Teknoloji Ltd. \u015eti.'
                )

            # ── Body flex fix: mevcut FSEK yanlış yerdeyse düzelt ──
            import re as _re2
            if 'pacdi-fsek' in content:
                body_flex2 = _re2.search(r'body\s*\{[^}]*display\s*:\s*flex', content)
                if body_flex2 and 'flex-direction:column' not in content:
                    # body'ye flex-direction:column ekle
                    content = _re2.sub(
                        r'(body\s*\{[^}]*)(display\s*:\s*flex)',
                        r'\1flex-direction:column;\2',
                        content, count=1
                    )

            # ── Body flex fix: FSEK footer yan kaymasın ──
            if 'pacdi-fsek' in content and 'display:flex' in content:
                # Yeni versiyon
                content = content.replace(
                    'id="pacdi-fsek" style="clear:both;width:100%;display:block;',
                    'id="pacdi-fsek" style="clear:both;width:100%;flex-basis:100%;display:block;'
                )
                # Eski versiyon — padding ile başlayan
                import re
                content = re.sub(
                    r'id="pacdi-fsek" style="([^"]*?)"',
                    lambda m: 'id="pacdi-fsek" style="' + m.group(1) + '"' 
                        if 'flex-basis' in m.group(1) or 'clear:both' in m.group(1)
                        else 'id="pacdi-fsek" style="clear:both;width:100%;flex-basis:100%;' + m.group(1) + '"',
                    content
                )

            # ── FSEK visible footer ──
            if 'pacdi-fsek' not in content and '</body>' in content and fname not in SKIP_FOOTER:
                # Body display:flex varsa son </div> öncesine ekle (layout fix)
                import re as _re
                body_flex = _re.search(r'body\s*\{[^}]*display\s*:\s*flex', content)
                if body_flex:
                    # Son </div> + </body> pattern'ı bul
                    last_div = content.rfind('</div>')
                    if last_div > 0:
                        content = content[:last_div] + FSEK_FOOTER + '\n' + content[last_div:]
                    else:
                        content = content.replace('</body>', FSEK_FOOTER + '\n</body>', 1)
                else:
                    content = content.replace('</body>', FSEK_FOOTER + '\n</body>', 1)

            if content != orig:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated += 1
                print('Updated:', fpath)
        except Exception as e:
            print('Error:', fpath, str(e))

print('Total updated:', updated)
