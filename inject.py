import os, sys, re

# ══════════════════════════════════════════════════════════════════
# PACDI ÇOK DİLLİLİK STANDARDI — Temmuz 2026'dan itibaren zorunlu
# ══════════════════════════════════════════════════════════════════
# Çok dilli bir sayfa yazılırken TEK doğru kalıp:
#
#   <div data-lang="de">...Almanca içerik...</div>
#   <div data-lang="tr">...Türkçe içerik...</div>
#   (satır içi metinler için: <span data-lang-inline="de">...</span>)
#
#   Dil değiştirme butonları <div class="lang-bar"> içinde olmalı.
#   JS SADECE .style.display ile blokları gösterip gizlemeli;
#   ASLA .innerText / .innerHTML ile metin YAZMAMALI — bu, içeriği
#   Google'a görünmez kılar (bkz. Temmuz 2026 SEO denetimi: grundrente.io
#   ve türevleri bu yüzden aylarca indexlenmedi).
#
#   Neden: data-lang bloklarının ikisi de ham HTML'de gerçekten var
#   olur, JS sadece görünürlüğü değiştirir — Google her iki dili de
#   kaynak kodda görür. innerText/innerHTML ile JS-obje swap'inde ise
#   ikinci dil hiçbir zaman HTML kaynağında yer almaz, sadece tarayıcı
#   çalışırken üretilir — Google bunu görmez.
#
#   Bu standarda uymayan sayfalar aşağıdaki lint tarafından otomatik
#   tespit edilip konsola uyarı olarak basılır (dosya OTOMATIK
#   DÜZELTİLMEZ — batch_split_lang.py ile elle/yarı-otomatik taşınması
#   gerekir).
# ══════════════════════════════════════════════════════════════════

_NONCOMPLIANT_MARKERS = [
    (re.compile(r'\.innerText\s*=\s*t\.'),
     "JS obje (L[lang]) ile innerText swap — SEO görünmezliği riski"),
    (re.compile(r'\.innerHTML\s*=\s*t\.'),
     "JS obje (L[lang]) ile innerHTML swap — SEO görünmezliği riski"),
    (re.compile(r'var\s+L\s*=\s*\{'),
     "Dil objesi (var L = {...}) tespit edildi — data-lang bloklarına taşınmalı"),
]

_lint_hits = []

def lint_multilingual(fpath, content):
    """Standart dışı çok dillilik kalıplarını tespit eder, dosyayı değiştirmez."""
    if 'data-lang=' in content or 'data-i18n=' in content:
        return  # zaten standart (veya standarda yakın) bir kalıp kullanıyor
    for pattern, reason in _NONCOMPLIANT_MARKERS:
        if pattern.search(content):
            _lint_hits.append((fpath, reason))
            break

domain = "example.com"
if os.path.exists("CNAME"):
    with open("CNAME") as f:
        domain = f.read().strip()

print("Domain:", domain)

ANALYTICS = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-E6ML8EDW0H"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-E6ML8EDW0H");</script>'
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8426936740213369" crossorigin="anonymous"></script>'

ASCII_MUHUR = """<!--
╬═══════════════════════════════════════════════════════════════╮
║         🛡️  PACDI FRAMEWORK — PROTECTED WORK                  ║
║                                                               ║
║  © 2026 PACDI Global Yazılım Ltd. Şti.                       ║
║  FSEK Registration No : 2026/18897                            ║
║  Trade Registry      : 23836 · Yunusemre / Manisa, TR       ║
║                                                               ║
║  This work and its modular software architecture are          ║
║  protected under PACDI Software Library FSEK registration.   ║
║  Unauthorized copying is subject to legal action.            ║
║                                                               ║
║  pacdi.eu · pacdi.de · info@pacdi.eu                         ║
╠═══════════════════════════════════════════════════════════════╣
-->"""

PWA_HEAD = """    <link rel="manifest" href="/manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="PACDI">
"""

LANG_DETECT_SCRIPT = """<script>
(function(){
  if (sessionStorage.getItem('autoLang')) return;
  var bl = (navigator.language || navigator.userLanguage || 'en').substring(0,2).toLowerCase();
  var supported = ['tr','de','en'];
  var lang = supported.indexOf(bl) > -1 ? bl : 'en';
  sessionStorage.setItem('autoLang', lang);
})();
</script>
"""

BETA_UNLOCK_SCRIPT = """<script>
(function(){
  var params = new URLSearchParams(window.location.search);
  if (params.get('beta') === 'pacdi2026') {
    try { sessionStorage.setItem('betaUnlock', '1'); } catch(e) {}
  }
  window.isBetaUnlocked = function() {
    try { return sessionStorage.getItem('betaUnlock') === '1'; } catch(e) { return false; }
  };
})();
</script>
"""

# ── Blog makaleleri için: tarayıcı çevirisi ipucu kutusu ──
TRANSLATE_TIP = """        <div class="info-box" style="background:#eef6ff;border-color:#a8cff0;border-left-color:#2a7de1;">
            <p><strong>🌍 In Ihrer Sprache lesen?</strong> Bu sayfayı kendi dilinizde okumak isterseniz / Want to read this in your language: <strong>iPhone/Safari</strong> — Adressleiste antippen → "aA" → Übersetzen. <strong>Android/Chrome</strong> — Menü (⋮) → Übersetzen. Die Übersetzung erfolgt direkt im Browser, kostenlos.</p>
        </div>

"""

# ── FIXED: tek tırnak kaçışı düzgün, daha önce defalarca tespit edilen bug giderildi ──
PWA_SCRIPT = """<script>
(function() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(function(){});
  }

  var isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
  var isInStandalone = ('standalone' in navigator && navigator.standalone);
  var shown = sessionStorage.getItem('pwa-banner-shown');
  if (shown || isInStandalone) return;

  if (isIOS) {
    setTimeout(function() {
      var bar = document.createElement('div');
      bar.id = 'pwa-banner';
      bar.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#04162E;border-top:2px solid #F6B45F;padding:14px 16px;z-index:9999;font-family:system-ui;';
      bar.innerHTML =
        '<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;">' +
          '<div>' +
            '<div style="color:#F6B45F;font-size:0.82rem;font-weight:700;margin-bottom:4px;">📲 Ana ekrana ekle</div>' +
            '<div style="color:#b0b5bf;font-size:0.75rem;line-height:1.5;">Safari\\'de <strong style="color:#eaf2fb;">&#11015; Paylaş</strong> butonuna bas, ardından <strong style="color:#eaf2fb;">Ana Ekrana Ekle</strong> seçeneğini seç.</div>' +
            '<div style="color:#4a6a88;font-size:0.68rem;margin-top:4px;">&#9432; iOS\\'ta otomatik kurulum desteklenmiyor — bu adım gerekli.</div>' +
          '</div>' +
          '<button onclick="document.getElementById(\\'pwa-banner\\').remove();sessionStorage.setItem(\\'pwa-banner-shown\\',\\'1\\')" style="background:transparent;border:none;color:#7a9ab8;font-size:1.2rem;cursor:pointer;padding:0 4px;flex-shrink:0;">✕</button>' +
        '</div>';
      document.body.appendChild(bar);
      sessionStorage.setItem('pwa-banner-shown', '1');
    }, 3000);
    return;
  }

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
          '<button onclick="document.getElementById(\\'pwa-banner\\').remove();sessionStorage.setItem(\\'pwa-banner-shown\\',\\'1\\')" style="background:transparent;border:1px solid rgba(246,180,95,0.3);color:#7a9ab8;padding:6px 12px;border-radius:20px;cursor:pointer;font-size:0.82rem;">Sonra</button>' +
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

SHARE_BAR_HEAD = '    <style>\n    .pacdi-share-bar{margin-top:24px;padding:16px;background:rgba(246,180,95,0.05);border:1px solid rgba(246,180,95,0.15);border-radius:10px;text-align:center;font-family:-apple-system,BlinkMacSystemFont,sans-serif;box-sizing:border-box;}\n    .pacdi-share-label{font-size:0.8rem;color:#7a9ab8;margin-bottom:10px;font-weight:600;}\n    .pacdi-share-btns{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;}\n    .pacdi-share-btn{display:inline-flex;align-items:center;gap:4px;font-size:0.78rem;padding:7px 14px;border-radius:20px;border:1px solid rgba(246,180,95,0.3);background:transparent;color:#F6B45F;text-decoration:none;cursor:pointer;font-family:inherit;}\n    .pacdi-share-btn:hover{background:rgba(246,180,95,0.1);}\n    </style>\n'

def page_is_light_by_default(content):
    """body arkaplanı zaten koyuysa (ör. #04162E lacivert) invert-tabanlı
    gece modu TERSİNE işler (koyu sayfa açılır). Sadece açık arkaplanlı
    sayfalara (kremli/beyaz blog vb.) gece modu enjekte edilmeli."""
    import re as _re5
    m = _re5.search(r'body\s*\{[^}]*background(?:-color)?\s*:\s*#([0-9a-fA-F]{6})', content)
    hexval = None
    if m:
        hexval = m.group(1)
    else:
        m3 = _re5.search(r'body\s*\{[^}]*background(?:-color)?\s*:\s*#([0-9a-fA-F]{3})\b', content)
        if m3:
            hexval = ''.join(c * 2 for c in m3.group(1))
    if not hexval:
        return True  # arkaplan bulunamadıysa varsayılan tarayıcı beyazı kabul et
    r, g, b = int(hexval[0:2], 16), int(hexval[2:4], 16), int(hexval[4:6], 16)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance > 128  # eşik: 128 üstü "açık" sayılır


DARKMODE_HEAD = """<style>
    [data-theme="dark"]:not([data-pacdi-native-theme]) { filter: invert(1) hue-rotate(180deg); background: #fff; }
    [data-theme="dark"]:not([data-pacdi-native-theme]) img,
    [data-theme="dark"]:not([data-pacdi-native-theme]) svg,
    [data-theme="dark"]:not([data-pacdi-native-theme]) video,
    [data-theme="dark"]:not([data-pacdi-native-theme]) picture,
    [data-theme="dark"]:not([data-pacdi-native-theme]) iframe { filter: invert(1) hue-rotate(180deg); }
    .pacdi-theme-toggle { position: fixed; top: 10px; right: 10px; z-index: 99999; width: 2.1rem; height: 2.1rem;
      border: none; border-radius: 50%; background: rgba(0,0,0,0.08); font-size: 1.05rem; cursor: pointer;
      display: flex; align-items: center; justify-content: center; backdrop-filter: blur(4px); }
    .pacdi-theme-toggle:hover { background: rgba(0,0,0,0.16); }
    </style>
"""

DARKMODE_SCRIPT = """<script>
(function(){
  var KEY = 'pacdi-theme';
  function apply(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    var btn = document.getElementById('pacdiThemeToggle');
    if (btn) btn.textContent = theme === 'dark' ? '\\u2600\\uFE0F' : '\\uD83C\\uDF19';
  }
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch(e) {}
  var preferred = (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
  apply(saved || preferred);
  function addBtn() {
    if (document.getElementById('pacdiThemeToggle')) return;
    var btn = document.createElement('button');
    btn.id = 'pacdiThemeToggle';
    btn.className = 'pacdi-theme-toggle';
    btn.setAttribute('aria-label', 'Koyu/Acik mod');
    btn.textContent = document.documentElement.getAttribute('data-theme') === 'dark' ? '\\u2600\\uFE0F' : '\\uD83C\\uDF19';
    btn.onclick = function() {
      var cur = document.documentElement.getAttribute('data-theme');
      var next = cur === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(KEY, next); } catch(e) {}
      apply(next);
    };
    document.body.appendChild(btn);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addBtn);
  } else {
    addBtn();
  }
})();
</script>
"""

SHARE_BAR_SCRIPT = '<div class="pacdi-share-bar" id="pacdiShareBar" style="clear:both;width:100%;flex-basis:100%;"></div>\n<script>\n(function(){\n  var pageTitle = (document.title.split(\'|\')[0] || document.title).trim();\n  var pageUrl = window.location.href;\n  var shareText = \'Bu \' + pageTitle + \' aracını faydalı buldum, senin de işine yarayabilir:\';\n\n  var bar = document.getElementById(\'pacdiShareBar\');\n  if (!bar) return;\n  bar.innerHTML =\n    \'<div class="pacdi-share-label">🔗 Bu aracı paylaş</div>\' +\n    \'<div class="pacdi-share-btns">\' +\n      \'<button class="pacdi-share-btn" id="pacdiShareNative" style="display:none;">📤 Paylaş</button>\' +\n      \'<a class="pacdi-share-btn" target="_blank" rel="noopener" href="https://api.whatsapp.com/send?text=\' + encodeURIComponent(shareText + \' \' + pageUrl) + \'">💬 WhatsApp</a>\' +\n      \'<a class="pacdi-share-btn" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=\' + encodeURIComponent(shareText) + \'&url=\' + encodeURIComponent(pageUrl) + \'">𝕏</a>\' +\n      \'<a class="pacdi-share-btn" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u=\' + encodeURIComponent(pageUrl) + \'">Facebook</a>\' +\n      \'<a class="pacdi-share-btn" target="_blank" rel="noopener" href="https://www.linkedin.com/sharing/share-offsite/?url=\' + encodeURIComponent(pageUrl) + \'">LinkedIn</a>\' +\n      \'<button class="pacdi-share-btn" id="pacdiShareCopy">🔗 Kopyala</button>\' +\n    \'</div>\';\n\n  if (navigator.share) {\n    var nativeBtn = document.getElementById(\'pacdiShareNative\');\n    nativeBtn.style.display = \'inline-flex\';\n    nativeBtn.onclick = function(){\n      navigator.share({ title: pageTitle, text: shareText, url: pageUrl }).catch(function(){});\n    };\n  }\n\n  var copyBtn = document.getElementById(\'pacdiShareCopy\');\n  copyBtn.onclick = function(){\n    navigator.clipboard.writeText(pageUrl).then(function(){\n      var old = copyBtn.textContent;\n      copyBtn.textContent = \'✓ Kopyalandı!\';\n      setTimeout(function(){ copyBtn.textContent = old; }, 2000);\n    }).catch(function(){});\n  };\n})();\n</script>\n'

FSEK_FOOTER = """<div id="pacdi-fsek" style="clear:both;width:100%;flex-basis:100%;text-align:center;padding:28px 16px 20px;border-top:1px solid rgba(212,175,55,0.15);margin-top:32px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;box-sizing:border-box;">
  <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(212,175,55,0.06);border:1px solid rgba(212,175,55,0.25);border-radius:24px;padding:8px 20px;margin-bottom:12px;flex-wrap:wrap;justify-content:center;">
    <span style="font-size:1rem;">🛡️</span>
    <span style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;color:#D4AF37;text-transform:uppercase;">FSEK Registered · PACDI Framework</span>
  </div>
  <div style="font-size:0.78rem;color:#8A8F9A;margin-bottom:4px;">Operated by AskMeAI Teknoloji Ltd. Şti. (TR: 23837)</div>
  <div style="font-size:0.72rem;color:#6B7280;margin-bottom:10px;">Intellectual property owned by © 2026 PACDI Global Yazılım Ltd. Şti. &mdash; FSEK No: <a href="https://pacdi.eu/legal.html" style="color:#D4AF37;text-decoration:none;">2026/18897</a></div>
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
<!--
╬═══════════════════════════════════════════════════════════════╮
║         🛡️  PACDI FRAMEWORK — PROTECTED WORK                  ║
║                                                               ║
║  © 2026 PACDI Global Yazılım Ltd. Şti.                       ║
║  FSEK Registration No : 2026/18897                            ║
║  Trade Registry      : 23836 · Yunusemre / Manisa, TR       ║
║                                                               ║
║  This work and its modular software architecture are          ║
║  protected under PACDI Software Library FSEK registration.   ║
║  Unauthorized copying is subject to legal action.            ║
║                                                               ║
║  pacdi.eu · pacdi.de · info@pacdi.eu                         ║
╠═══════════════════════════════════════════════════════════════╣
-->

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

# ── Kişisel/özel dosyalar — inject edilmez ──
PRIVATE_PREFIXES = ('mein-', 'private-', 'pacdi-sunum', 'personal-', 'intern-')

def is_private(filename):
    return any(filename.startswith(p) for p in PRIVATE_PREFIXES)

# ── Diğer repolar için: pacdi.eu/legal.html'e gerçek yönlendirme sayfası ──
LEGAL_REDIRECT = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Impressum &amp; Datenschutz</title>
    <meta name="robots" content="noindex, follow">
    <link rel="canonical" href="https://pacdi.eu/legal.html" />
    <meta http-equiv="refresh" content="0; url=https://pacdi.eu/legal.html">
    <script>window.location.replace('https://pacdi.eu/legal.html');</script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #04162E; color: #e8edf2; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 20px; text-align: center; }
        a { color: #F6B45F; }
    </style>
</head>
<body>
    <p>Weiterleitung zu <a href="https://pacdi.eu/legal.html">pacdi.eu/legal.html</a> &hellip;</p>
</body>
</html>
'''

# ── legal.html: domain'e göre üç farklı davranış ──
if domain == 'pacdi.store':
    print('Skipping legal.html for pacdi.store (has custom version)')
elif domain == 'pacdi.eu':
    legal_content = LEGAL_HTML.format()
    with open('legal.html', 'w', encoding='utf-8') as f:
        f.write(legal_content)
    print('Legal updated (full content, canonical source): legal.html')
else:
    with open('legal.html', 'w', encoding='utf-8') as f:
        f.write(LEGAL_REDIRECT)
    print('Legal updated (redirect to pacdi.eu): legal.html')

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
        {"src": "https://cdn-icons-png.flaticon.com/512/6849/6849232.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
        {"src": "https://cdn-icons-png.flaticon.com/512/6849/6849232.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
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
        if is_private(fname):
            print('Skipped (private):', fname)
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            lint_multilingual(fpath, content)
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
            if 'autoLang' not in content and fname not in SKIP:
                insert += '    ' + LANG_DETECT_SCRIPT
            if 'betaUnlock' not in content and fname not in SKIP:
                insert += '    ' + BETA_UNLOCK_SCRIPT
            if 'pacdiShareBar' not in content and fname not in SKIP_FOOTER:
                insert += SHARE_BAR_HEAD
            if ('pacdiThemeToggle' not in content and 'data-pacdi-native-theme' not in content
                    and fname not in SKIP and page_is_light_by_default(content)):
                insert += '    ' + DARKMODE_HEAD
                insert += '    ' + DARKMODE_SCRIPT

            # ── ÖZEL: index.html giriş butonu CSS düzeltmesi ──
            if fname == 'index.html' and '#userPanel .btn-sm' not in content:
                insert += '    <style>#userPanel .btn-sm { background: transparent !important; color: var(--gold) !important; border: 1px solid var(--gold) !important; } #userPanel .btn-sm:hover { background: rgba(246,180,95,0.1) !important; }</style>\n'

            if insert:
                content = content.replace('</head>', insert + '</head>', 1)

            # ── ÖZEL: pruefprotokoll.html beta override — BODY SONUNA, handlePDF tanımlandıktan SONRA ──
            if fname == 'pruefprotokoll.html' and 'pacdi2026' not in content:
                override_script = '''<script>
(function() {
  var params = new URLSearchParams(window.location.search);
  var urlBeta = params.get('beta') === 'pacdi2026';
  var sessionBeta = false;
  try { sessionBeta = sessionStorage.getItem('betaUnlock') === '1'; } catch(e) {}
  if (!urlBeta && !sessionBeta) return;
  var origHandle = window.handlePDF;
  window.handlePDF = function() {
    if (typeof generatePDF === 'function') { generatePDF(); return; }
    if (origHandle) origHandle();
  };
})();
</script>
'''
                if '</body>' in content:
                    content = content.replace('</body>', override_script + '</body>', 1)

            # ── PWA Script ──
            if 'serviceWorker' not in content and '</body>' in content and fname not in SKIP_FOOTER:
                content = content.replace('</body>', PWA_SCRIPT + '\n</body>', 1)

            # ── PWA Script eski (bozuk) versiyon güncelle ──
            if 'pwa-banner' in content and (
                "Safari'de" in content or
                "iOS'ta otomatik" in content or
                "getElementById('pwa-banner').remove()" in content
            ):
                import re as _re3
                _pwa_block_re = _re3.compile(
                    r'<script>\s*\(function\(\)\s*\{\s*if \(\'serviceWorker\' in navigator\).*?\}\)\(\);\s*</script>',
                    _re3.S
                )
                if _pwa_block_re.search(content):
                    content = _pwa_block_re.sub(PWA_SCRIPT.strip(), content, count=1)
                    print('Fixed: stale/broken PWA banner ->', fpath)

            # ── Blog makaleleri: çeviri ipucu kutusu ──
            if 'blog' in root.split(os.sep) and 'In Ihrer Sprache lesen' not in content:
                import re as _re4
                _disclaimer_re = _re4.compile(r'(<div class="disclaimer">.*?</div>\n)', _re4.S)
                if _disclaimer_re.search(content):
                    content = _disclaimer_re.sub(lambda m: m.group(1) + '\n' + TRANSLATE_TIP, content, count=1)
                    print('Added translation tip ->', fpath)

            # ── ASCII muhur → <body> sonrasi ──
            if 'PACDI FRAMEWORK' not in content and '<body' in content:
                body_end = content.find('>', content.find('<body')) + 1
                content = content[:body_end] + '\n' + ASCII_MUHUR + '\n' + content[body_end:]

            # ── FSEK footer eski versiyon güncelle ──
            if 'pacdi-fsek' in content:
                content = content.replace(
                    '<div style="font-size:0.78rem;color:#8A8F9A;margin-bottom:4px;">© 2026 PACDI Global Yazılım Ltd. Şti.</div>\n  <div style="font-size:0.72rem;color:#6B7280;margin-bottom:10px;">Protected under FSEK Copyright Registration No: <a href="https://pacdi.eu" style="color:#D4AF37;text-decoration:none;">2026/18897</a></div>',
                    '<div style="font-size:0.78rem;color:#8A8F9A;margin-bottom:4px;">Operated by AskMeAI Teknoloji Ltd. Şti. (TR: 23837)</div>\n  <div style="font-size:0.72rem;color:#6B7280;margin-bottom:10px;">Intellectual property owned by © 2026 PACDI Global Yazılım Ltd. Şti. &mdash; FSEK No: <a href="https://pacdi.eu/legal.html" style="color:#D4AF37;text-decoration:none;">2026/18897</a></div>'
                )

            # ── Inline Impressum fix: PACDI Global → AskMeAI ──
            if 'Verantwortlich: PACDI Global' in content:
                content = content.replace(
                    'Verantwortlich: PACDI Global',
                    'Verantwortlicher: Mehmet Aydınlı / AskMeAI Teknoloji Ltd. Şti.'
                )
                print('Fixed: inline impressum ->', fpath)

            if 'Ein Service von PACDI Global' in content:
                content = content.replace(
                    'Ein Service von PACDI Global',
                    'Ein Service von AskMeAI Teknoloji Ltd. Şti.'
                )

            # ── Body flex fix ──
            import re as _re2
            if 'pacdi-fsek' in content:
                body_flex2 = _re2.search(r'body\s*\{[^}]*display\s*:\s*flex', content)
                if body_flex2 and 'flex-direction:column' not in content:
                    content = _re2.sub(
                        r'(body\s*\{[^}]*)(display\s*:\s*flex)',
                        r'\1flex-direction:column;\2',
                        content, count=1
                    )
                content = content.replace(
                    'id="pacdi-fsek" style="clear:both;width:100%;display:block;',
                    'id="pacdi-fsek" style="clear:both;width:100%;flex-basis:100%;display:block;'
                )
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
                import re as _re
                body_flex = _re.search(r'body\s*\{[^}]*display\s*:\s*flex', content)
                if body_flex:
                    last_div = content.rfind('</div>')
                    if last_div > 0:
                        content = content[:last_div] + FSEK_FOOTER + '\n' + content[last_div:]
                    else:
                        content = content.replace('</body>', FSEK_FOOTER + '\n</body>', 1)
                else:
                    content = content.replace('</body>', FSEK_FOOTER + '\n</body>', 1)

            # ── PACDI paylaşım çubuğu — eski (flex-basis'siz) sürümü otomatik onar ──
            # Bu düzeltmeden önce eklenmiş sayfalarda çubuk stilsiz div ile duruyordu;
            # flex kapsayıcılarda diğer öğelerle yan yana sıkışmasına sebep oluyordu.
            if '<div class="pacdi-share-bar" id="pacdiShareBar"></div>' in content:
                content = content.replace(
                    '<div class="pacdi-share-bar" id="pacdiShareBar"></div>',
                    '<div class="pacdi-share-bar" id="pacdiShareBar" style="clear:both;width:100%;flex-basis:100%;"></div>',
                    1
                )
                print('Fixed: stale share-bar (missing flex-basis) ->', fpath)

            # ── PACDI paylaşım çubuğu — her modülün altına, FSEK footer'ın hemen üstüne ──
            if ('pacdiShareBar' not in content and fname not in SKIP_FOOTER
                    and '<div id="pacdi-fsek"' in content):
                content = content.replace('<div id="pacdi-fsek"', SHARE_BAR_SCRIPT + '\n<div id="pacdi-fsek"', 1)

            if content != orig:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated += 1
                print('Updated:', fpath)
        except Exception as e:
            print('Error:', fpath, str(e))

print('Total updated:', updated)

if _lint_hits:
    print()
    print('⚠️  ÇOK DİLLİLİK STANDART DIŞI SAYFALAR (' + str(len(_lint_hits)) + '):')
    for fpath, reason in _lint_hits:
        print('   -', fpath, '—', reason)
    print('   → Bu sayfalar batch_split_lang.py ile gerçek ayrı dil')
    print('     sayfalarına taşınmalı (bkz. PACDI çok dillilik standardı).')
else:
    print('✓ Çok dillilik standardı: tüm sayfalar uyumlu (ya da tek dilli).')
