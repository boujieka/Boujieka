"""Turn raw PDFs into page-marked text for extraction agents.
Usage: prepare.py <work_dir>   (expects <work_dir>/raw/*.pdf; OCR output may already sit in <work_dir>/text/<name>.txt)
Writes <work_dir>/text/*.txt, <work_dir>/paged/*.txt ("=== PAGE n ===" markers = PDF page numbers) and sha256.txt."""
import sys, os, subprocess, hashlib
W = sys.argv[1]
os.makedirs(f'{W}/text', exist_ok=True); os.makedirs(f'{W}/paged', exist_ok=True)
with open(f'{W}/sha256.txt', 'w') as h:
    for f in sorted(os.listdir(f'{W}/raw')):
        if not f.endswith('.pdf'): continue
        n = f[:-4]; p = f'{W}/raw/{f}'
        h.write(hashlib.sha256(open(p, 'rb').read()).hexdigest() + '  ' + f + '\n')
        t = f'{W}/text/{n}.txt'
        if not os.path.exists(t) or os.path.getsize(t) < 1000:
            subprocess.run(['pdftotext', '-layout', p, t], check=False)
        pages = open(t, encoding='utf-8', errors='replace').read().split('\f')
        with open(f'{W}/paged/{n}.txt', 'w') as o:
            for i, pg in enumerate(pages, 1):
                if pg.strip(): o.write(f'\n=== PAGE {i} ===\n{pg}')
        print(n, len(pages), 'pages', os.path.getsize(t), 'chars')
