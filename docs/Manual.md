# ГАРЫН АВЛАГА — Kernel Data Structures

**ШИНЖЛЭХ УХААН ТЕХНОЛОГИЙН ИХ СУРГУУЛЬ**
**МЭДЭЭЛЭЛ, ХОЛБООНЫ ТЕХНОЛОГИЙН СУРГУУЛЬ**

ҮЙЛДЛИЙН СИСТЕМ (F.CSM302) · 2026–2027 оны хичээлийн жилийн намар

**Баг:** II-4-4  
**Сэдэв:** Kernel Data Structures  
**Багш:** Г. Ганбат /F.CS10/  
**Огноо:** 2026-11-01

| Гишүүн | Оюутны код |
| --- | --- |
| --- | --- |
| Э.Тэргэл | B210930801 |
| Б.Булгантамир | B241940123 |
| Т.Төгөлдөр | B242270050 |
| И.Зэлмэ | B231940158 |
| О.Амина | B241910800 |
| М.Наранбат | B242270801 |

**Repository:** [Tergel0923/CSM302-II-4-4](https://github.com/Tergel0923/CSM302-II-4-4)

**PDF хувилбар:** [II_4_4_Manual.pdf](II_4_4_Manual.pdf)

## Гарчиг

- [1.1 Хэрэглэгчийн заавар](#11-хэрэглэгчийн-заавар)
- [1.2 Operational заавар](#12-operational-заавар)

## 1. Manual

Хэрэглэгчийн ба ажиллуулах гарын авлага.

## 1.1 Хэрэглэгчийн заавар

### 1.1.1 Програмын зорилго

Дөрвөн өнгийн kernel linked list болон параметртэй Collatz list-ийн бүтцийг харж, нэмэх, устгах, хайх, reset хийх туршилтыг гүйцэтгэнэ.

### 1.1.2 Дэмжих орчин

| Горим | Орчин | Зориулалт |
| --- | --- | --- |
| Practice | Windows/Linux/macOS, Python 3.10+ | UI болон алгоритмтай танилцах |
| Live kernel | Ubuntu VM, kernel 5.6+, headers | Assignment-ийн бодит kernel ажиллагаа |

Practice дээрх амжилт нь kernel module ажилласны нотолгоо биш. UI-ийн дээд талд горим байнга харагдана.

### 1.1.3 Суулгах эсвэл нээх алхам

ZIP-ийг задлаад CSM302-II-4-4 хавтас дотор terminal нээнэ.
```bash
python3 src/ui/server.py --mode demo
```
Windows PowerShell дээр:
```powershell
py src/ui/server.py --mode demo
```
Browser дээр http://127.0.0.1:8765 нээнэ. Local server-ийг Ctrl+C дарж зогсооно. Шинэчлэх page нь серверийн state-ийг хадгална; server restart нь practice state-ийг шинээр үүсгэнэ.

### 1.1.4 Оролт ба тохиргоо

Structure сонголтоос Part I Color list эсвэл Part II Collatz list сонгоно. Graph нь node-ийн logical ID, value, prev/next утгыг харуулна. Inspector хүснэгтээр холбоосыг давхар шалгана.

### 1.1.5 Ажиллуулах, зогсоох, reset хийх

UI-ийн серверийг терминал дээр `Ctrl+C` дарж зогсооно. Энэ нь kernel module-ийг unload хийхгүй. **Шинэчлэх (Refresh)** товч одоогийн төлөвийг уншина. **Анхны 4 элементийг сэргээх (Reset four)** товч анхны дөрвөн өнгийг сэргээнэ. Module-ийг буулгах командыг 1.2.4 хэсгээс харна.

### 1.1.6 Дүрслэлийн тэмдэг, өнгө, төлөв

| Тэмдэг / товч |Үүрэг |
| --- | --- |
| HEAD / 0 дугаар | Sentinel, өгөгдлийн node биш |
| Ногоон сум | next холбоос |
| Цэнхэр сум | prev холбоос |
| Шар хүрээ | SEARCH-ийн эхний match |
| Нэмэх | RGB 0–255 шинэ node нэмэх |
| Устгах | Оруулсан ID-тай node устгах |
| RGB утгаар хайх | Эхний тохирох RGB; байхгүй бол мэдээлэл |
| Анхны 4 элементийг сэргээх | Анхны 4 өнгө, ID 1–4 |
| Хоослох | List-ийг хоослох |
| Шинэчлэх | /proc-оос шинэ snapshot унших |
| JSON файл татах | Current state ба command history татах |

Анхны 4 элементийг сэргээх нь анхны RGB (138,226,43), (255,0,0), (0,255,0), (0,0,255) үүсгэнэ. Эхний утга нь номын red/blue/green field-ийн жишээг RGB дараалалд хөрвүүлсэн утга юм.

### 1.1.7 Хоёроос доошгүй жишээ

#### Жишээ 1: add/search/delete

1. Анхны 4 элементийг сэргээх дарна: count=4, HEAD.next=1, HEAD.prev=4.
2. R=10, G=20, B=30 оруулж Нэмэх: count=5, шинэ ID=5.
3. RGB утгаар хайх: match ID=5, node шар хүрээтэй.
4. ID=5 оруулаад Устгах: count=4; 4.next=0 ба HEAD.prev=4.
5. RGB утгаар хайх: Тохирох RGB утга олдсонгүй. CLEAR хийвэл HEAD-ийн хоёр холбоос 0 болно.

#### Жишээ 2: Collatz sequence (start=15)

Practice mode-д start=15 оруулаад Дадлагын дараалал үүсгэх дарна. Live mode-д дараах terminal команд ашиглана:
```bash
sudo rmmod collatz
sudo insmod src/kernel/collatz.ko start=15
```
Хэрэв өмнө нь модуль ачаалаагүй бол rmmod алхмыг алгасана. UI-д Part II сонгоод Шинэчлэх товч дарна. 18 node; эхний value=15, сүүлийн value=1 байна.
Хүлээгдсэн дараалал: 15,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1.

#### Жишээ 3: параметр ба захын утга

start=1 → 1 node. start=25 → 24 nodes. start=27 → 112 nodes. start=0 болон overflow болох ULL_MAX нь татгалзана. Хэрэв invalid live load хийсэн бол module ачаалагдахгүй; зөв start-аар дахин insmod хийнэ.

### 1.1.8 Түгээмэл алдаа ба шийдэл

| Шинж | Шалтгаан / шийдэл |
| --- | --- |
| /lib/modules/.../build missing | Running kernel-тэй тохирох headers суулга |
| Invalid module format | Өөр kernel-д build хийсэн; matching headers-тай rebuild |
| Key was rejected | VM-ийн module signing/Secure Boot тохиргоог шалга |
| Operation not permitted | sudo/CAP_SYS_MODULE эсвэл VM/container limitation |
| /proc/kds_colors missing | colors.ko ачаалаагүй; insmod ба dmesg шалга |
| Permission denied | Live server-ийг sudo-оор ажиллуул |
| File exists on insmod | Модуль ачаалагдсан; эхлээд rmmod |
| RGB error | Бүхэл 0–255; хоосон/бутархай утгагүй |
| Node not found | Одоогийн inspector-оос ID шалга |
| Багтаамж reached | 128 limit; delete/clear хий |
| Address already in use | --port 8766; шинэ URL-ийг ашигла |
| Invalid Host / 403 | localhost биш 127.0.0.1 URL; page reload |

## 1.2 Operational заавар

### 1.2.1 Repository clone хийх

Дэмжих зорилтот орчин: Ubuntu 22.04 LTS эсвэл 24.04 LTS VM. Native Windows дээр kernel module ажиллахгүй. WSL2-д тохирох kernel болон headers шаардлагатай тул VM ашиглаж болно.

```bash
git clone https://github.com/Tergel0923/CSM302-II-4-4.git
cd CSM302-II-4-4
```

### 1.2.2 OS, compiler/runtime, version

GCC, Make, Python 3.10+ болон ажиллаж буй kernel-тэй яг тохирох headers шаардлагатай.

```bash
sudo apt update
sudo apt install build-essential linux-headers-$(uname -r) python3 git
uname -r
gcc --version
python3 --version
```

### 1.2.3 Dependency суулгах

UI нь Python стандарт сан ашиглана. PDF дахин үүсгэхэд `reportlab` суулгана.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install reportlab
```

### 1.2.4 Build ба Run команд

```bash
make kernel
sudo insmod src/kernel/colors.ko
sudo insmod src/kernel/collatz.ko start=15
sudo python3 src/ui/server.py --mode kernel
```

Нээх хаяг: http://127.0.0.1:8765. Browser-ийг root эрхээр ажиллуулахгүй. Live server нь root-only `/proc` интерфейсэд хандахын тулд `sudo` ашиглана. Энэ нь тусгаарласан сургалтын VM-д зориулсан.

#### Терминалаас шалгах

```bash
sudo cat /proc/kds_colors
sudo cat /proc/kds_collatz
printf 'ADD 10 20 30\n' | sudo tee /proc/kds_colors
sudo dmesg | grep -E 'kds_colors|kds_collatz'
```

#### Зогсоох / санах ойг чөлөөлөх

Эхлээд UI-ийн серверийг `Ctrl+C` дарж зогсооно. Дараа нь:
```bash
sudo rmmod collatz
sudo rmmod colors
sudo dmesg | grep -E 'kds_colors|kds_collatz'
```
Log-д removed N nodes; list empty=1 гарна. /proc/kds_colors болон /proc/kds_collatz арилсан байна. Шинэ туршилт эхлэхдээ insmod командуудаа дахин ажиллуулна.

### 1.2.5 Үндсэн тестийн өгөгдөл

```bash
make test
```
Python tests нь input validation, model invariant, Collatz, HTTP token/origin/host шалгалтуудыг гүйцэтгэнэ. C test нь module-ийн shared arithmetic header-ийг GCC + ASan/UBSan-тай compile хийж шалгана. LeakSanitizer нь container/ptrace орчинд ажиллахгүй бол зөвхөн тэр орчинд ASAN_OPTIONS=detect_leaks=0 make test ажиллуулна.

### 1.2.6 Нэмэлт boundary/error test

Өмнө ачаалсан colors/collatz байхгүй үед:
```bash
make kernel
mkdir -p docs/evidence
sudo python3 tests/kernel_acceptance.py | tee docs/evidence/kernel-acceptance.txt
```
Script нь одоо ачаалагдсан модуль байвал state-ийг дарж устгахгүйгээр зогсоно. Өөрөө ачаалсан module-уудаа finally хэсэгт unload хийнэ. Тестийн төгсгөлд ALL KERNEL ACCEPTANCE CHECKS PASSED гарах ёстой. Алдаа гарвал log-ийг хадгалж, тухайн алхмыг зассаны дараа дахин шалгана.

### 1.2.7 Хүлээгдсэн үр дүн

- Live mode badge + анхны дөрвөн өнгө.
- ADD/SEARCH дараах ID 5 ба холбоосууд.
- CLEAR дараах HEAD self-links.
- Collatz start=15, node count 18 ба inspector.
- dmesg-ийн load traversal ба unload cleanup.
- uname -a, GCC/Python version, make kernel output.
Live туршилтын нотолгоог `docs/evidence/` дотор хадгалж, [Report.md](Report.md)-д тайлбартай нэмнэ. Одоогийн practice зургууд [screenshots/](screenshots/) хавтаст байна. Practice screenshot-ийг live гэж нэрлэхгүй.

### 1.2.8 Known issues

Ubuntu 6.8.0-138-generic headers дээр хоёр module compile/link амжилттай (W=1). Kernel load болон live screenshot энэ багцыг бэлтгэсэн container-д баталгаажаагүй. Target VM дээр tests/kernel_acceptance.py болон UI checklist-ийг заавал ажиллуулна. Browser visual test мөн бэлтгэлийн орчинд browser binary татагдаагүй учраас шалгахаар хүлээгдэж буй.
Module reload нь state-ийг шинээр үүсгэнэ. Persistent database байхгүй. Том sequence дээр graph scroll урт болно. Simultaneous browser/terminal өөрчлөлтөд Шинэчлэх шаардлагатай. Local server-ийг internet-д expose хийхээр зохиогоогүй.

#### Үйлдлийн түүхийн хязгаар

History нь зөвхөн тухайн browser tab-ийн амжилттай командуудыг бүртгэнэ. Өөр terminal эсвэл өөр tab-ийн үйлдлүүдийг автоматаар poll хийхгүй; Шинэчлэх хийж одоогийн төлөвийг уншина. Page reload хийвэл browser history арилна; Export-оор өмнө нь хадгална.
