# Kernel Structure Lab
## Хэрэглэгчийн ба operational гарын авлага
F.CSM302 · Бие даалт 1 · II-4-4
2026-11-01 · Repository: Tergel0923/CSM302-II-4-4
## Зорилго
Дөрвөн өнгийн kernel linked list болон параметртэй Collatz list-ийн бүтцийг харж, нэмэх, устгах, хайх, reset хийх туршилтыг гүйцэтгэнэ.
## Горим сонгох
| Горим | Орчин | Зориулалт |
| Practice | Windows/Linux/macOS, Python 3.10+ | UI болон алгоритмтай танилцах |
| Live kernel | Ubuntu VM, kernel 5.6+, headers | Assignment-ийн бодит kernel ажиллагаа |
Practice дээрх амжилт нь kernel module ажилласны нотолгоо биш. UI-ийн дээд талд горим байнга харагдана.
## Хурдан эхлэх: practice
ZIP-ийг задлаад CSM302-II-4-4 хавтас дотор terminal нээнэ.
```bash
python3 src/ui/server.py --mode demo
```
Windows PowerShell дээр:
```powershell
py src/ui/server.py --mode demo
```
Browser дээр http://127.0.0.1:8765 нээнэ. Local server-ийг Ctrl+C дарж зогсооно. Refresh page нь серверийн state-ийг хадгална; server restart нь practice state-ийг шинээр үүсгэнэ.
---PAGE---
# 1. Live kernel суулгах
Дэмжих зорилтот орчин: Ubuntu 22.04 LTS эсвэл 24.04 LTS VM. GCC, Make, Python 3.10+, kernel-ийн яг тохирох headers. Browser нь VM дотроос localhost-д хандана. Native Windows дээр kernel module ажиллахгүй. WSL2-д өөр kernel/header setup шаардлагатай тул VM нь илүү хялбар.
```bash
git clone https://github.com/Tergel0923/CSM302-II-4-4.git
cd CSM302-II-4-4
sudo apt update
sudo apt install build-essential linux-headers-$(uname -r) python3 git
uname -r
gcc --version
python3 --version
make kernel
sudo insmod src/kernel/colors.ko
sudo insmod src/kernel/collatz.ko start=15
sudo python3 src/ui/server.py --mode kernel
```
Нээх хаяг: http://127.0.0.1:8765. Browser-ийг root-оор ажиллуулахгүй. Server нь root-only /proc interface-д хандах учраас live горимд sudo ашигласан. Энэ нь тусгаарласан сургалтын VM-д зориулсан.
## Command line-аар шалгах
```bash
sudo cat /proc/kds_colors
sudo cat /proc/kds_collatz
printf 'ADD 10 20 30\n' | sudo tee /proc/kds_colors
sudo dmesg | grep -E 'kds_colors|kds_collatz'
```
Хэрэв repository-д шинэ файлууд хараахан push хийгдээгүй бол clone хийсний дараа өгсөн багцын файлуудыг repo root-д хуулна. GitHub upload зааврыг docs/SUBMISSION.md-ээс харна.
---PAGE---
# 2. UI ашиглах
Structure сонголтоос Part I Color list эсвэл Part II Collatz list сонгоно. Graph нь node-ийн logical ID, value, prev/next утгыг харуулна. Inspector хүснэгтээр холбоосыг давхар шалгана.
| Тэмдэг / товч | Үүрэг |
| HEAD / ID 0 | Sentinel, өгөгдлийн node биш |
| Ногоон сум | next холбоос |
| Цэнхэр сум | prev холбоос |
| Шар хүрээ | SEARCH-ийн эхний match |
| Add | RGB 0–255 шинэ node нэмэх |
| Delete | Оруулсан ID-тай node устгах |
| Search RGB | Эхний тохирох RGB; байхгүй бол мэдээлэл |
| Reset four | Анхны 4 өнгө, ID 1–4 |
| Clear | List-ийг хоослох |
| Refresh | /proc-оос шинэ snapshot унших |
| Export JSON | Current state ба command history татах |
Reset four нь анхны RGB (138,226,43), (255,0,0), (0,255,0), (0,0,255) үүсгэнэ. Эхний утга нь номын red/blue/green field-ийн жишээг RGB дараалалд хөрвүүлсэн утга юм.
## Жишээ 1: add/search/delete
1. Reset four дарна: count=4, HEAD.next=1, HEAD.prev=4.
2. R=10, G=20, B=30 оруулж Add: count=5, шинэ ID=5.
3. Search RGB: match ID=5, node шар хүрээтэй.
4. ID=5 оруулаад Delete: count=4; 4.next=0 ба HEAD.prev=4.
5. Search RGB: No matching RGB value. CLEAR хийвэл HEAD-ийн хоёр холбоос 0 болно.
---PAGE---
# 3. Collatz туршилт ба lifecycle
## Жишээ 2: start=15
Practice mode-д start=15 оруулаад Generate practice sequence дарна. Live mode-д дараах terminal команд ашиглана:
```bash
sudo rmmod collatz
sudo insmod src/kernel/collatz.ko start=15
```
Хэрэв өмнө нь модуль ачаалаагүй бол rmmod алхмыг алгасана. UI-д Part II сонгоод Refresh дарна. 18 node; эхний value=15, сүүлийн value=1 байна.
Хүлээгдсэн дараалал: 15,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1.
## Жишээ 3: параметр ба захын утга
start=1 → 1 node. start=25 → 24 nodes. start=27 → 112 nodes. start=0 болон overflow болох ULL_MAX нь татгалзана. Хэрэв invalid live load хийсэн бол module ачаалагдахгүй; зөв start-аар дахин insmod хийнэ.
## Зогсоох / cleanup
UI terminal дээр Ctrl+C дарна. Энэ нь module-ийг unload хийхгүй. Дараа нь:
```bash
sudo rmmod collatz
sudo rmmod colors
sudo dmesg | grep -E 'kds_colors|kds_collatz'
```
Log-д removed N nodes; list empty=1 гарна. /proc/kds_colors болон /proc/kds_collatz арилсан байна. Шинэ туршилт эхлэхдээ insmod командуудаа дахин ажиллуулна.
## History-ийн хязгаар
History нь зөвхөн тухайн browser tab-ийн амжилттай командуудыг бүртгэнэ. Өөр terminal эсвэл өөр tab-ийн үйлдлүүдийг автоматаар poll хийхгүй; Refresh хийж одоогийн төлөвийг уншина. Page reload хийвэл browser history арилна; Export-оор өмнө нь хадгална.
---PAGE---
# 4. Operational тест ба нотолгоо
## Локал automation
```bash
make test
```
Python tests нь input validation, model invariant, Collatz, HTTP token/origin/host шалгалтуудыг гүйцэтгэнэ. C test нь module-ийн shared arithmetic header-ийг GCC + ASan/UBSan-тай compile хийж шалгана. LeakSanitizer нь container/ptrace орчинд ажиллахгүй бол зөвхөн тэр орчинд ASAN_OPTIONS=detect_leaks=0 make test ажиллуулна.
## Бодит kernel acceptance
Өмнө ачаалсан colors/collatz байхгүй үед:
```bash
make kernel
sudo python3 tests/kernel_acceptance.py | tee docs/evidence/kernel-acceptance.txt
```
Script нь одоо ачаалагдсан модуль байвал state-ийг дарж устгахгүйгээр зогсоно. Өөрөө ачаалсан module-уудаа finally хэсэгт unload хийнэ. Тестийн төгсгөлд ALL KERNEL ACCEPTANCE CHECKS PASSED гарах ёстой. Алдаа гарвал log-ийг хадгалж, тухайн алхмыг зассаны дараа дахин шалгана.
## Screenshot checklist
- Live mode badge + анхны дөрвөн өнгө.
- ADD/SEARCH дараах ID 5 ба холбоосууд.
- CLEAR дараах HEAD self-links.
- Collatz start=15, node count 18 ба inspector.
- dmesg-ийн load traversal ба unload cleanup.
- uname -a, GCC/Python version, make kernel output.
Screenshot-уудыг docs/evidence/ дотор хадгалж Report.md-д тайлбартай нэмнэ. Practice screenshot-ийг live гэж нэрлэхгүй.
## PDF дахин үүсгэх
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install reportlab
python3 tools/build_docs.py
```
PDF generator нь DejaVu Sans font ашиглана. Ubuntu дээр шаардлагатай бол fonts-dejavu-core суулгана. Markdown эхийг өөрчилсний дараа PDF-ийн бүх хуудсыг шалгана.
---PAGE---
# 5. Алдаа ба шийдэл
| Шинж | Шалтгаан / шийдэл |
| /lib/modules/.../build missing | Running kernel-тэй тохирох headers суулга |
| Invalid module format | Өөр kernel-д build хийсэн; matching headers-тай rebuild |
| Key was rejected | VM-ийн module signing/Secure Boot тохиргоог шалга |
| Operation not permitted | sudo/CAP_SYS_MODULE эсвэл VM/container limitation |
| /proc/kds_colors missing | colors.ko ачаалаагүй; insmod ба dmesg шалга |
| Permission denied | Live server-ийг sudo-оор ажиллуул |
| File exists on insmod | Модуль ачаалагдсан; эхлээд rmmod |
| RGB error | Бүхэл 0–255; хоосон/бутархай утгагүй |
| Node not found | Одоогийн inspector-оос ID шалга |
| Capacity reached | 128 limit; delete/clear хий |
| Address already in use | --port 8766; шинэ URL-ийг ашигла |
| Invalid Host / 403 | localhost биш 127.0.0.1 URL; page reload |
## Known issues / validation boundary
Ubuntu 6.8.0-138-generic headers дээр хоёр module compile/link амжилттай (W=1). Kernel load болон live screenshot энэ багцыг бэлтгэсэн container-д баталгаажаагүй. Target VM дээр tests/kernel_acceptance.py болон UI checklist-ийг заавал ажиллуулна. Browser visual test мөн бэлтгэлийн орчинд browser binary татагдаагүй учраас pending.
Module reload нь state-ийг шинээр үүсгэнэ. Persistent database байхгүй. Том sequence дээр graph scroll урт болно. Simultaneous browser/terminal өөрчлөлтөд Refresh шаардлагатай. Local server-ийг internet-д expose хийхээр зохиогоогүй.
## Хүлээлгэн өгөх
Бодит log/screenshot нэмээд Report-ийн үр дүнг шинэчилнэ. README, source, tests, docs-оо commit/push хийж, шалгасан commit дээр tag гаргана. MS Teams-д Report + Manual + repo link-ээ нэг post-д хавсаргана. IV-2-7-ийн шүүмж нь тусдаа ажил бөгөөд тэдний материал хэрэгтэй.
