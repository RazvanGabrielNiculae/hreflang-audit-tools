#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import sys
class P(HTMLParser):
 def __init__(self): super().__init__(); self.lang=""; self.canon=[]; self.alt=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=="html": self.lang=d.get("lang","")
  if t=="link" and d.get("rel","").lower()=="canonical": self.canon.append(d.get("href",""))
  if t=="link" and d.get("rel","").lower()=="alternate" and d.get("hreflang"): self.alt.append((d.get("hreflang"),d.get("href","")))
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path("examples/en.html"); x=P(); x.feed(p.read_text(encoding="utf-8")); errors=[]
if not x.lang: errors.append("missing html lang")
if len(x.canon)!=1: errors.append(f"expected one canonical, got {len(x.canon)}")
if not x.alt: errors.append("no hreflang alternates")
for lang,url in x.alt:
 if not lang.strip() or not url.strip(): errors.append("empty hreflang or href")
print(f"lang={x.lang or '-'} canonical={len(x.canon)} alternates={len(x.alt)} errors={len(errors)}")
for e in errors: print("ERROR",e)
sys.exit(bool(errors))
