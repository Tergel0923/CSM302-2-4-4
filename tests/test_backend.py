import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/ui'))
from backend import DemoBackend, command, collatz, MAX_U64

class BackendTests(unittest.TestCase):
    def setUp(self): self.b = DemoBackend()
    def check_links(self, s):
        nodes = {0: s['head'], **{n['id']: n for n in s['nodes']}}
        for id, n in nodes.items():
            self.assertEqual(nodes[n['next']]['prev'], id)
            self.assertEqual(nodes[n['prev']]['next'], id)
    def test_initial_four(self):
        s = self.b.state()['colors']; self.assertEqual(len(s['nodes']), 4); self.check_links(s)
    def test_add_search_delete(self):
        self.b.execute(dict(action='ADD', r='1', g='2', b='3'))
        self.b.execute(dict(action='SEARCH', r='1', g='2', b='3'))
        self.assertEqual(self.b.found, 5)
        self.b.execute(dict(action='DELETE', id=5)); self.check_links(self.b.state()['colors'])
    def test_delete_first_middle_last(self):
        for id in [1,3,4,2]:
            self.b.execute(dict(action='DELETE', id=id)); self.check_links(self.b.state()['colors'])
        self.assertEqual(self.b.state()['colors']['head'], {'next':0, 'prev':0})
    def test_missing_delete(self):
        with self.assertRaises(ValueError): self.b.execute(dict(action='DELETE', id=999))
    def test_search_miss(self):
        self.b.execute(dict(action='SEARCH', r=1,g=2,b=3)); self.assertEqual(self.b.found,0)
    def test_duplicate_first_match(self):
        self.b.execute(dict(action='ADD',r=255,g=0,b=0));self.b.execute(dict(action='SEARCH',r=255,g=0,b=0));self.assertEqual(self.b.found,2)
    def test_clear_reset(self):
        self.b.execute({'action':'CLEAR'});self.check_links(self.b.state()['colors'])
        self.b.execute({'action':'RESET'});self.assertEqual(len(self.b.nodes),4)
    def test_bad_rgb(self):
        for value in [-1,256,'abc','1.0',True,None,'1\nCLEAR',2**40]:
            with self.subTest(value=value), self.assertRaises(ValueError): command(dict(action='ADD',r=value,g=0,b=0))
    def test_capacity(self):
        for _ in range(124): self.b.execute(dict(action='ADD',r=0,g=0,b=0))
        with self.assertRaises(ValueError): self.b.execute(dict(action='ADD',r=0,g=0,b=0))
        self.assertEqual(len(self.b.nodes),128)
    def test_collatz_15(self):
        s=collatz(15); self.assertEqual([int(n['value']) for n in s['nodes']],[15,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1]); self.check_links(s)
    def test_collatz_25(self): self.assertEqual(len(collatz(25)['nodes']),24)
    def test_collatz_one(self): self.assertEqual(len(collatz(1)['nodes']),1)
    def test_collatz_27(self): self.assertEqual(len(collatz(27)['nodes']),112)
    def test_invalid_collatz(self):
        for value in [0,-1,MAX_U64,MAX_U64+1,'hello']:
            with self.subTest(value=value), self.assertRaises(ValueError): collatz(value)
    def test_failed_generation_preserves_state(self):
        old=self.b.sequence
        with self.assertRaises(ValueError):self.b.execute(dict(action='COLLATZ',start=0))
        self.assertIs(self.b.sequence,old)

if __name__=='__main__': unittest.main()
