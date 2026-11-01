#!/usr/bin/env python3
"""Run only in a disposable Linux VM after make kernel; unloads modules it loads."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def run(*args, ok=True):
    p = subprocess.run(args, text=True, capture_output=True)
    print('$', ' '.join(args), '\n', p.stdout, p.stderr, 'exit=', p.returncode, flush=True)
    if ok and p.returncode:
        raise RuntimeError('Command failed')
    return p

def state(name='colors'):
    return json.loads(Path('/proc/kds_' + name).read_text())

def write(text):
    with open('/proc/kds_colors', 'w') as f:
        f.write(text + '\n')

def links(s):
    nodes = {0:s['head'], **{n['id']:n for n in s['nodes']}}
    for key, n in nodes.items():
        assert nodes[n['next']]['prev'] == key
        assert nodes[n['prev']]['next'] == key

def reject(text):
    before = state()
    try: write(text)
    except OSError: pass
    else: raise AssertionError('Accepted invalid command: ' + repr(text))
    assert state() == before

if __name__ == '__main__':
    if os.geteuid() != 0: raise SystemExit('Run with sudo in an isolated VM.')
    loaded = {line.split()[0] for line in Path('/proc/modules').read_text().splitlines()}
    if loaded & {'colors','collatz'}:
        raise SystemExit('Unload existing colors/collatz first; this test will not replace your state.')
    try:
        run('uname','-a'); run('gcc','--version')
        run('insmod', str(ROOT/'src/kernel/colors.ko'))
        assert len(state()['nodes']) == 4; links(state()); print('PASS initial four')
        write('ADD 10 20 30'); write('SEARCH 10 20 30'); assert state()['found'] == 5
        write('DELETE 5'); links(state()); print('PASS add/search/delete')
        for text in ['ADD -1 0 0','ADD 256 0 0','ADD 4294967296 0 0','ADD 1 2 3 extra','CLEAR\nRESET','CLEAR\0junk','DELETE 999','SEARCH 0 0 256']:
            reject(text)
        print('PASS invalid commands preserve state')
        for id in [1,3,4,2]: write('DELETE '+str(id)); links(state())
        assert state()['head'] == {'next':0,'prev':0}; print('PASS empty and boundary deletion')
        for _ in range(128): write('ADD 0 0 0')
        reject('ADD 0 0 0'); links(state()); print('PASS capacity')
        write('CLEAR'); write('RESET'); assert len(state()['nodes']) == 4
        run('rmmod','colors')
        assert not Path('/proc/kds_colors').exists()
        for start, length in [(1,1),(15,18),(25,24),(27,112)]:
            run('insmod',str(ROOT/'src/kernel/collatz.ko'),f'start={start}')
            s=state('collatz'); links(s)
            values=[int(n['value']) for n in s['nodes']]
            assert len(values)==length and values[0]==start and values[-1]==1
            for a,b in zip(values,values[1:]): assert b == (a//2 if a%2==0 else 3*a+1)
            run('rmmod','collatz'); print('PASS Collatz',start)
        for start in [0,18446744073709551615]:
            assert run('insmod',str(ROOT/'src/kernel/collatz.ko'),f'start={start}',ok=False).returncode != 0
            assert not Path('/proc/kds_collatz').exists()
        print('PASS invalid Collatz rollback')
        run('dmesg','--ctime')
        print('ALL KERNEL ACCEPTANCE CHECKS PASSED')
    finally:
        for module in ['colors','collatz']:
            if Path('/proc/kds_'+module).exists(): run('rmmod',module,ok=False)
