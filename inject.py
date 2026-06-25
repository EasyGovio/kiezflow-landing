import os, sys

domain = "example.com"
if os.path.exists("CNAME"):
    with open("CNAME") as f:
        domain = f.read().strip()

print("Domain:", domain)

ANALYTICS = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-E6ML8EDW0H"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-E6ML8EDW0H");</script>'
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8426936740213369" crossorigin="anonymous"></script>'
SKIP = ['legal.html','impressum.html','datenschutz.html','404.html','master-template.html','test.html']

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
            insert = ''
            if 'G-E6ML8EDW0H' not in content:
                insert += '    ' + ANALYTICS + '\n'
            if 'ca-pub-8426936740213369' not in content and fname not in SKIP:
                insert += '    ' + ADSENSE + '\n'
            if 'canonical' not in content:
                insert += '    <link rel="canonical" href="' + url + '" />\n'
            if insert:
                content = content.replace('</head>', insert + '</head>', 1)
            if content != orig:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated += 1
                print('Updated:', fpath)
        except Exception as e:
            print('Error:', fpath, str(e))

print('Total updated:', updated)
