#!/usr/bin/env python3
"""Орчныг өөрчлөхгүйгээр шаардлага ба цөмийн модулийн төлөвийг шалгана."""
import argparse
import os
from pathlib import Path
import platform
import shutil
import sys


def inspect(live=False):
    checks = [('Python 3.10+', sys.version_info >= (3, 10), platform.python_version())]
    if live:
        release = platform.release()
        checks += [('Linux орчин', platform.system() == 'Linux', platform.system()),
                   ('GCC хөрвүүлэгч', bool(shutil.which('gcc')), shutil.which('gcc') or 'олдсонгүй'),
                   ('Make хэрэгсэл', bool(shutil.which('make')), shutil.which('make') or 'олдсонгүй'),
                   ('Цөмийн build хавтас', Path('/lib/modules', release, 'build').exists(), release)]
        for name in ('colors', 'collatz'):
            path = Path('/proc/kds_' + name)
            print(f"Модулийн төлөв: {name}: " + ('ачаалагдсан' if path.exists() else 'ачаалагдаагүй'))
            if path.exists():
                print('  Унших эрх: ' + ('байна' if os.access(path, os.R_OK) else 'sudo шаардлагатай'))
    for name, ok, detail in checks:
        print(f"{'АМЖИЛТТАЙ' if ok else 'ШААРДЛАГАТАЙ'} | {name} | {detail}")
    print('Суулгах, ачаалах команд ажиллуулаагүй; зөвхөн орчны мэдээлэл уншив.')
    return all(ok for _, ok, _ in checks)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Төслийн орчин оношлох')
    parser.add_argument('--live', action='store_true', help='Бодит цөмийн build шаардлагыг нэмэлтээр шалгах')
    sys.exit(0 if inspect(parser.parse_args().live) else 1)
