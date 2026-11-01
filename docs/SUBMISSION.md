# II-4-4 — Хүлээлгэн өгөх шалгах хуудас

## GitHub хувилбар

Эх код, тест, PDF болон editable эхүүд repository-д орсон. Эхний бэлтгэлийн үед connection read-only байсан; repository owner account холбосноор upload хийх эрх нээгдсэн.

Өөрийн компьютерт авах:
```bash
git clone https://github.com/Tergel0923/CSM302-II-4-4.git
cd CSM302-II-4-4
```
Хэрэв өмнө clone хийсэн бол өөрийн өөрчлөлтийг хадгалсны дараа `git pull --ff-only` ашиглана.

## Нийтлэхийн өмнө

- [ ] Ubuntu VM дээр make kernel амжилттай.
- [ ] make test болон sudo python3 tests/kernel_acceptance.py амжилттай; raw log хадгалсан.
- [ ] Live UI: 4 nodes, add/search/delete, empty HEAD, Collatz 15 ба 27 шалгасан.
- [ ] docs/evidence/ дотор live screenshot, uname/compiler output, dmesg load/unload хадгалсан.
- [ ] Report-ийн "баталгаажуулаагүй" хэсгийг зөвхөн бодит үр дүнгээр шинэчилсэн.
- [ ] Гишүүдийн бодит нэр/ажил, commit холбоосыг оруулсан.
- [ ] docs PDF-үүдийг шинэчилж git commit/push хийсэн.
- [ ] Release/tag: шалгалт давсны дараа `git tag -a v1.0.0 -m "II-4-4 verified BD1 submission"` ба `git push origin v1.0.0`.
- [ ] MS Teams БД1 - Submissions and Reviews сувагт нэг post, Report + Manual + GitHub.
- [ ] IV-2-7-ийн ажилд бодит build/run, үндсэн + нэмэлт тест; Review PDF-г тэдний post-д Reply.

## Post-ийн бэлэн текст (validation хийсний дараа үр дүнг нэмж засна)

II-4-4 – Kernel Data Structures

Код: II-4-4
Төсөл: Kernel Data Structures
Товч үр дүн: Linux kernel-ийн circular doubly linked list дээр дөрвөн өнгийн элемент болон параметртэй Collatz sequence хэрэгжүүлэв. Interactive UI нь /proc-оос next/prev холбоог уншиж, нэмэх, устгах, RGB хайх, reset хийх боломжтой. Туршилтын баталгаажуулалтын төлөв болон хязгаарлалтыг тайланд тэмдэглэв.
GitHub: https://github.com/Tergel0923/CSM302-II-4-4
Хавсралт: II-4-4_BD1_Report.pdf, II-4-4_Manual.pdf
Туршиж үзэх: README-ийн Түргэн эхлэх.

Энэ post-ийг автоматаар илгээгээгүй. Нийтлэх хувилбар болон screenshot-ийг баг өөрөө баталгаажуулна.
