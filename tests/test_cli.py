import importlib.util,pathlib,tempfile,unittest
P=pathlib.Path(__file__).parents[1]/'tools'/'audit_hreflang.py'; s=importlib.util.spec_from_file_location('m',P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def f(body): q=tempfile.NamedTemporaryFile('w',delete=False,suffix='.html'); q.write(body); q.close(); return q.name
def page(lang,url,alts,rel='alternate'):
 links=''.join(f'<link rel="{rel}" hreflang="{l}" href="{u}">' for l,u in alts); return f'<html lang="{lang}"><head><link rel="canonical" href="{url}">{links}</head></html>'
class T(unittest.TestCase):
 def test_self_reference(self): self.assertEqual(m.audit_page(f(page('en','https://x/en',[('en','https://x/en'),('ro','https://x/ro')])), 'https://x/en')[1],[])
 def test_invalid_lang(self): self.assertTrue(any('invalid hreflang' in x for x in m.audit_page(f(page('en','https://x/en',[('zzzz','https://x/z')])), 'https://x/en')[1]))
 def test_rel_without_value_does_not_crash(self): self.assertIsInstance(m.audit_page(f('<html lang="en"><link rel><link rel="canonical" href="https://x/en"><link rel="alternate" hreflang="en" href="https://x/en">'),'https://x/en')[1],list)
 def test_reciprocity(self):
  a=f(page('en','https://x/en',[('en','https://x/en'),('ro','https://x/ro')])); b=f(page('ro','https://x/ro',[('ro','https://x/ro'),('en','https://x/en')]))
  self.assertEqual(m.audit_pair(a,'https://x/en',b,'https://x/ro'),[])
 def test_missing_xdefault(self): self.assertTrue(any('x-default' in x for x in m.audit_page(f(page('en','https://x/en',[('en','https://x/en')])), 'https://x/en',True)[1]))
if __name__=='__main__': unittest.main()
