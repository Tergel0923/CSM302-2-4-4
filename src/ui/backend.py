"""Kernel adapter and explicitly labelled practice backend; no external dependencies."""
import json
from pathlib import Path

MAX_U64 = (1 << 64) - 1
DEFAULTS = [(138, 226, 43), (255, 0, 0), (0, 255, 0), (0, 0, 255)]


def integer(value, low, high):
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError('Enter an integer.')
    text = str(value)
    if not text.isascii() or not text.isdecimal() or len(text) > 20:
        raise ValueError('Use decimal digits only.')
    n = int(text)
    if not low <= n <= high:
        raise ValueError(f'Value must be between {low} and {high}.')
    return n


def command(data):
    action = data.get('action')
    if action in ('ADD', 'SEARCH'):
        return action + ' ' + ' '.join(str(integer(data.get(k), 0, 255)) for k in ('r', 'g', 'b'))
    if action == 'DELETE':
        return 'DELETE ' + str(integer(data.get('id'), 1, (1 << 32) - 1))
    if action in ('RESET', 'CLEAR'):
        return action
    raise ValueError('Unknown action.')


def linked(nodes, kind, **metadata):
    ids = [0] + [n['id'] for n in nodes]
    result = []
    for i, node in enumerate(nodes, 1):
        result.append(dict(node, prev=ids[i - 1], next=ids[(i + 1) % len(ids)]))
    return dict(kind=kind, head={'next': ids[1] if nodes else 0, 'prev': ids[-1]}, nodes=result, **metadata)


def collatz(start):
    n = integer(start, 1, MAX_U64)
    nodes = []
    while True:
        if len(nodes) >= 4096:
            raise ValueError('Sequence exceeds 4096 nodes.')
        nodes.append({'id': len(nodes) + 1, 'value': str(n)})
        if n == 1:
            return linked(nodes, 'collatz', start=str(start))
        if n % 2 and n > (MAX_U64 - 1) // 3:
            raise ValueError('Unsigned 64-bit overflow; choose a smaller start.')
        n = n // 2 if n % 2 == 0 else 3 * n + 1


class DemoBackend:
    mode = 'PRACTICE SIMULATION — not kernel evidence'

    def __init__(self):
        self.nodes = []
        self.next_id = 1
        self.found = 0
        self.sequence = collatz(25)
        self.execute({'action': 'RESET'})

    def state(self):
        return {'mode': self.mode, 'colors': linked(self.nodes, 'colors', found=self.found),
                'collatz': self.sequence, 'collatz_error': None}

    def execute(self, data):
        if data.get('action') == 'COLLATZ':
            self.sequence = collatz(data.get('start'))
            return
        parts = command(data).split()
        action = parts[0]
        if action == 'ADD':
            if len(self.nodes) >= 128 or self.next_id > (1 << 32) - 1:
                raise ValueError('List capacity reached (128 nodes).')
            self.nodes.append(dict(zip(('r', 'g', 'b'), map(int, parts[1:])), id=self.next_id))
            self.next_id += 1
            self.found = 0
        elif action == 'SEARCH':
            rgb = list(map(int, parts[1:]))
            self.found = next((n['id'] for n in self.nodes if [n[k] for k in ('r', 'g', 'b')] == rgb), 0)
        elif action == 'DELETE':
            idx = next((i for i, n in enumerate(self.nodes) if n['id'] == int(parts[1])), None)
            if idx is None:
                raise ValueError('Node ID not found.')
            self.nodes.pop(idx)
            self.found = 0
        elif action == 'CLEAR':
            self.nodes.clear()
            self.found = 0
        elif action == 'RESET':
            self.nodes = [dict(zip(('r', 'g', 'b'), rgb), id=i) for i, rgb in enumerate(DEFAULTS, 1)]
            self.next_id, self.found = 5, 0


class KernelBackend:
    mode = 'LIVE LINUX KERNEL — /proc snapshots'

    def state(self):
        colors = json.loads(Path('/proc/kds_colors').read_text())
        try:
            sequence = json.loads(Path('/proc/kds_collatz').read_text())
            error = None
        except FileNotFoundError:
            sequence, error = None, 'Load collatz.ko with start=N in the terminal, then Refresh.'
        return {'mode': self.mode, 'colors': colors, 'collatz': sequence, 'collatz_error': error}

    def execute(self, data):
        if data.get('action') == 'COLLATZ':
            raise ValueError('Live mode: sudo rmmod collatz; sudo insmod src/kernel/collatz.ko start=N; then Refresh.')
        with open('/proc/kds_colors', 'w') as out:
            out.write(command(data) + '\n')
