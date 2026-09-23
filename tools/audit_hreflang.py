#!/usr/bin/env python3
import argparse,re,sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
LANG=re.compile(r'^(?:[A-Za-z]{2,3})(?:-[A-Za-z]{2}|-[0-9]{3})?$')
class P(HTMLParser):
 def __init__(self): super().__init__(); self.lang=''; self.canon=[]; self.alt=[]
 def handle_starttag(self,t,a):
  d=dict(a); rel=(d.get('rel') or '').lower()
  if t=='html': self.lang=d.get('lang','') or ''
  if t=='link' and rel=='canonical': self.canon.append(d.get('href','') or '')
  if t=='link' and rel=='alternate' and d.get('hreflang') is not None: self.alt.append((d.get('hreflang') or '',d.get('href','') or ''))
def parse(path):
 x=P(); x.feed(Path(path).read_text(encoding='utf-8')); return x
def audit_page(path,page_url=None,require_x_default=False):
 x=parse(path); e=[]; page_url=page_url or (x.canon[0] if len(x.canon)==1 else '')
 if not x.lang: e.append('missing html lang')
 elif not LANG.match(x.lang): e.append(f'invalid html lang: {x.lang}')
 if len(x.canon)!=1: e.append(f'expected one canonical, got {len(x.canon)}')
 langs=[]
 if not x.alt: e.append('no hreflang alternates')
 for lang,url in x.alt:
  l=lang.strip(); u=url.strip(); langs.append(l.lower())
  if not l or not u: e.append('empty hreflang or href')
  elif l.lower()!='x-default' and not LANG.match(l): e.append(f'invalid hreflang: {l}')
 if page_url and not any(urljoin(page_url,u)==page_url and l.lower()==x.lang.lower() for l,u in x.alt): e.append('missing self-referencing hreflang')
 if require_x_default and 'x-default' not in langs: e.append('missing x-default')
 return x,e
def audit_pair(a_path,a_url,b_path,b_url):
 a,ea=audit_page(a_path,a_url); b,eb=audit_page(b_path,b_url); e=[f'A: {x}' for x in ea]+[f'B: {x}' for x in eb]
 amap={(l.lower(),urljoin(a_url,u)) for l,u in a.alt}; bmap={(l.lower(),urljoin(b_url,u)) for l,u in b.alt}
 if not any(u==b_url and l==b.lang.lower() for l,u in amap): e.append('A does not reference B with B language')
 if not any(u==a_url and l==a.lang.lower() for l,u in bmap): e.append('B does not reciprocate A with A language')
 return e
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('html'); ap.add_argument('--url'); ap.add_argument('--require-x-default',action='store_true'); ap.add_argument('--peer'); ap.add_argument('--peer-url'); n=ap.parse_args()
 if n.peer:
  if not n.url or not n.peer_url: ap.error('--peer requires --url and --peer-url')
  e=audit_pair(n.html,n.url,n.peer,n.peer_url)
 else:
  x,e=audit_page(n.html,n.url,n.require_x_default); print(f'lang={x.lang or "-"} canonical={len(x.canon)} alternates={len(x.alt)} errors={len(e)}')
 for z in e: print('ERROR',z)
 return 1 if e else 0
if __name__=='__main__': raise SystemExit(main())
