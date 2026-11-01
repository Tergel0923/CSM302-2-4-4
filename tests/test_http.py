import http.client
import json
import re
import socket
import subprocess
import sys
import time
import unittest
from pathlib import Path

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with socket.socket() as s:
            s.bind(('127.0.0.1',0)); cls.port=s.getsockname()[1]
        cls.proc=subprocess.Popen([sys.executable,str(Path(__file__).resolve().parents[1]/'src/ui/server.py'),'--mode','demo','--port',str(cls.port)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                c=http.client.HTTPConnection('127.0.0.1',cls.port,timeout=1);c.request('GET','/');r=c.getresponse();page=r.read().decode();c.close()
                cls.token=re.search("const token='([^']+)'",page)[1];break
            except OSError: time.sleep(.02)
        else: cls.proc.terminate();cls.proc.wait();raise RuntimeError('Server did not start')
    @classmethod
    def tearDownClass(cls):cls.proc.terminate();cls.proc.wait(timeout=5)
    def call(self,method,path,data=None,headers=None):
        c=http.client.HTTPConnection('127.0.0.1',self.port,timeout=3)
        c.request(method,path,body=json.dumps(data) if data is not None else None,headers=headers or {})
        r=c.getresponse();body=r.read();status=r.status;c.close();return status,body
    def auth(self):return {'Origin':f'http://127.0.0.1:{self.port}','X-KDS-Token':self.token,'Content-Type':'application/json'}
    def test_state(self):
        status,body=self.call('GET','/api/state');self.assertEqual(status,200);self.assertIn('PRACTICE',json.loads(body)['mode'])
    def test_authenticated_command(self):
        status,body=self.call('POST','/api/command',{'action':'RESET'},self.auth());self.assertEqual(status,200);self.assertEqual(len(json.loads(body)['colors']['nodes']),4)
    def test_missing_token(self):self.assertEqual(self.call('POST','/api/command',{'action':'CLEAR'})[0],403)
    def test_foreign_origin(self):
        h=self.auth();h['Origin']='https://example.com';self.assertEqual(self.call('POST','/api/command',{'action':'CLEAR'},h)[0],403)
    def test_bad_host(self):self.assertEqual(self.call('GET','/api/state',headers={'Host':'example.com'})[0],403)
    def test_invalid_input(self):self.assertEqual(self.call('POST','/api/command',{'action':'ADD','r':999,'g':0,'b':0},self.auth())[0],400)
    def test_unknown_route(self):self.assertEqual(self.call('GET','/missing')[0],404)
