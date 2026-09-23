import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; TOOL=ROOT/'tools'/'audit_hreflang.py'
class CLI(unittest.TestCase):
 def run_case(self,rel): return subprocess.run([sys.executable,str(TOOL),str(ROOT/rel)],capture_output=True,text=True)
 def test_valid(self): self.assertEqual(self.run_case('examples/en.html').returncode,0)
 def test_missing_lang(self): self.assertNotEqual(self.run_case('tests/fixtures/missing-lang.html').returncode,0)
 def test_multiple_canonical(self): self.assertNotEqual(self.run_case('tests/fixtures/multiple-canonical.html').returncode,0)
 def test_no_alternates(self): self.assertNotEqual(self.run_case('tests/fixtures/no-alternates.html').returncode,0)
if __name__=='__main__': unittest.main()
