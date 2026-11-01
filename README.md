# Цөмийн өгөгдлийн бүтэц — II-4-4

**F.CSM302 · Бие даалт 1 · Operating System Concepts (2018), Chapter 3, Project 4**

Бодит Linux kernel-ийн circular doubly linked list болон түүнийг `/proc`-оор уншдаг interactive graph.

## Хэрэгжүүлсэн зүйл

- **Part I / colors.ko:** ачаалахад 4 RGB элемент; kernel log-д traversal; unload үед safe deletion + kfree.
- **Part II / collatz.ko:** `start=25` default; параметрээс Collatz sequence үүсгэж linked list-д хадгалах, traversal/log, unload cleanup.
- **UI:** add, delete by ID, search RGB, clear/reset, next/prev graph, HEAD sentinel, snapshot inspector, JSON export, operation history.
- Хязгаар: RGB 0–255; colors 128 nodes; Collatz 4096 nodes, unsigned 64-bit overflow guard.
- Live mode хэзээ ч автоматаар simulation руу шилжихгүй. Practice mode нь kernel proof биш.

## Түргэн эхлэх: дадлага (Windows, Linux, macOS)

Python 3.10+ суулгана. Сан нэмж суулгахгүй.

```bash
git clone https://github.com/Tergel0923/CSM302-II-4-4.git
cd CSM302-II-4-4
python3 src/ui/server.py --mode demo
```

Windows: `py src/ui/server.py --mode demo`.
Нээх: **http://127.0.0.1:8765**. Зогсоох: Ctrl+C.

## Түргэн эхлэх: бодит цөм (Ubuntu VM)

Ubuntu 22.04/24.04 VM, kernel 5.6+, Python 3.10+, GCC/Make, running kernel-тэй ижил headers шаардлагатай.
Доорх командуудыг repository root-оос ажиллуулна:

```bash
sudo apt update
sudo apt install build-essential linux-headers-$(uname -r) python3 git
make kernel
sudo insmod src/kernel/colors.ko
sudo insmod src/kernel/collatz.ko start=15
sudo python3 src/ui/server.py --mode kernel
```

Browser-ийг энгийн хэрэглэгчээр VM дотор нээнэ: http://127.0.0.1:8765.
Proc файлууд root-only, write нь CAP_SYS_ADMIN шалгана. Сургалтын тусгаарласан VM ашиглана.
HTTP server нь зөвхөн loopback хаяг дээр ажиллана. Public network-д бүү байршуул.

```bash
# UI terminal-д Ctrl+C дарсны дараа:
sudo dmesg | grep -E 'kds_colors|kds_collatz'
sudo rmmod collatz
sudo rmmod colors
sudo dmesg | grep -E 'kds_colors|kds_collatz'
```

Collatz параметр солих:
```bash
sudo rmmod collatz
sudo insmod src/kernel/collatz.ko start=27
```
Дараа нь UI-ийн Шинэчлэх товчийг дарна. Windows/ердийн WSL2 дээр `.ko` ачаалах нь native Ubuntu VM-тэй адил биш; kernel headers/module support шаардлагатай.

## Туршилт ба баталгаажуулалтын төлөв

```bash
make test
# Disposable VM дээр make kernel-ийн дараа, модуль ачаалаагүй үед:
sudo python3 tests/kernel_acceptance.py | tee docs/evidence/kernel-acceptance.txt
```

2026-11-01: **22 Python test АМЖИЛТТАЙ**, shared C arithmetic test АМЖИЛТТАЙ (ASan/UBSan; container-д leak detector disabled), JavaScript syntax АМЖИЛТТАЙ.
`docs/evidence/local-tests.txt` нь бодит гаралт. **colors.ko болон collatz.ko нь Ubuntu 6.8.0-138-generic headers дээр W=1 build амжилттай** (docs/evidence/kernel-build.txt). Host kernel нь 6.18.57 тул module load хийгээгүй. **Kernel runtime болон browser visual acceptance хараахан баталгаажаагүй**. Энэ нь бүх төсөл acceptance давсан гэсэн үг биш.

Container-ийн LeakSanitizer ptrace алдаа гарвал зөвхөн тухайн орчинд `ASAN_OPTIONS=detect_leaks=0 make test` ашиглаж болно; VM дээр эхлээд `make test` хэвээр ажиллуул.

## Бүтэц

| Зам | Агуулга |
|---|---|
| src/kernel/ | colors.c, collatz.c, shared arithmetic, Kbuild |
| src/ui/ | stdlib Python server, backend, HTML/SVG interactive UI |
| tests/ | model, HTTP, arithmetic, real kernel acceptance tests |
| docs/ | Mongolian report/manual, review template, evidence and submission checklist |
| tools/build_docs.py | PDF-ийг эх Markdown-оос дахин гаргах |

## Баримт бичиг

- [Тайлан](docs/II-4-4_BD1_Report.pdf) — хэрэгжилт, онол, бодит local test, үлдсэн validation.
- [Manual](docs/II-4-4_Manual.pdf) — user болон operational заавар.
- [Peer-review template](docs/II-4-4_Review_IV-2-7_TEMPLATE.pdf) — бөглөөгүй загвар; гүйцэтгэсэн шүүмж биш.
- [Submission checklist](docs/SUBMISSION.md).

## Баг ба AI ашиглалт

Баг II-4-4. Өмнөх README-д байсан гишүүд: Тэргэл, Булгантамир, Төгөлдөр, Зэлмэ, Амина, Наранбат.
Гишүүн тус бүрийн ажил/commit-ийг баталгаажуулж оруулаагүй; хийсэн бодит ажлаар нөхнө.
Код, UI, тест, баримт бичгийг ChatGPT/Codex-ийн тусламжтай боловсруулсан. Баг кодыг судалж, VM дээр туршиж, үр дүнг нягталж хамгаална. Гишүүдийн commit history, screenshot, kernel test үр дүнг зохиомлоор үүсгээгүй.

## Эх сурвалж

- Silberschatz, Galvin, Gagne. *Operating System Concepts*, 10th ed., 2018. Chapter 3, Programming Project 4, printed P-19–P-22.
- https://docs.kernel.org/core-api/list.html
- https://docs.kernel.org/filesystems/seq_file.html
- https://docs.kernel.org/kbuild/modules.html
- F.CSM302: BD1 Guide, Topic and Peer Review Allocation, Peer Review Guide (өгсөн PDF).

Шүүмжлэх баг: **IV-2-7 — Fork-Join Sorting Application**. Тэдний post, code, Report, Manual шаардлагатай.
