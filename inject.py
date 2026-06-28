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

FSEK_FOOTER = """<div id="pacdi-fsek" style="text-align:center;padding:28px 16px 20px;border-top:1px solid rgba(212,175,55,0.15);margin-top:32px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(212,175,55,0.06);border:1px solid rgba(212,175,55,0.25);border-radius:24px;padding:8px 20px;margin-bottom:12px;">
    <span style="font-size:1rem;">\U0001f6e1\ufe0f</span>
    <span style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;color:#D4AF37;text-transform:uppercase;">FSEK Registered \u00b7 PACDI Framework</span>
  </div>
  <div style="font-size:0.78rem;color:#8A8F9A;margin-bottom:4px;">Operated by AskMeAI Teknoloji Ltd. \u015eti. (TR: 23837)</div>
  <div style="font-size:0.72rem;color:#6B7280;margin-bottom:10px;">Intellectual property owned by \u00a9 2026 PACDI Global Yaz\u0131l\u0131m Ltd. \u015eti. &mdash; FSEK No: <a href="https://pacdi.eu/legal.html" style="color:#D4AF37;text-decoration:none;">2026/18897</a></div>
  <div style="font-size:0.82rem;font-style:italic;color:#6B7280;">&ldquo;Technology in the service of humanity.&rdquo;</div>
</div>"""

SKIP = ['legal.html','impressum.html','datenschutz.html','404.html','master-template.html','test.html']
SKIP_FOOTER = ['legal.html','impressum.html','datenschutz.html','404.html','master-template.html','test.html']

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
            if insert:
                content = content.replace('</head>', insert + '</head>', 1)

            # ── ASCII muhur → <body> opening'in hemen sonrasi ──
            if 'PACDI FRAMEWORK' not in content and '<body' in content:
                # body tag'inden sonra ekle
                body_end = content.find('>', content.find('<body')) + 1
                content = content[:body_end] + '\n' + ASCII_MUHUR + '\n' + content[body_end:]

            # ── FSEK visible footer → </body>'den once ──
            if 'pacdi-fsek' not in content and '</body>' in content and fname not in SKIP_FOOTER:
                content = content.replace('</body>', FSEK_FOOTER + '\n</body>', 1)

            if content != orig:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated += 1
                print('Updated:', fpath)
        except Exception as e:
            print('Error:', fpath, str(e))

print('Total updated:', updated)
