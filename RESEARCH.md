# QNX Doctor — RESEARCH.md

> Proyek hackathon: **QNX Global Hackathon 2026** — "QNX Doctor"
> Riset ditulis: 17 Nov 2026 (WIB) · Semua fakta di bawah ini diambil dari sumber publik yang tercantum per bagian.
> Status riset: **lengkap untuk spek & rules**; SDP 8.0 belum diunduh (butuh akun myQNX Syarip — lihat §2.4).

---

## 0. Ringkasan eksekutif

| Item | Fakta |
|---|---|
| Hackathon | QNX Global Hackathon — "The power to shape the world" |
| Sponsor | BlackBerry Ltd (QNX) · Administrator: Devpost, Inc. |
| Total hadiah | **$50.000+** (tunai) + podcast, coffee chat, swag, blog feature |
| Deadline submit | **15 Des 2026 14:00 ET = 16 Des 2026 02:00 WIB** |
| Judging | 15–29 Jan 2027 · Pemenang diumumkan ~4 Feb 2027 |
| Kategori QNX Doctor | **Developer Tooling & Host Tools** (host-based tool, Linux) |
| Bonus yang dikejar | **Best use of QNX-specific Technologies ($3.500)** + **Best Codelab/Tutorial ($3.500)** |
| Syarat kunci | Repo publik (GitHub/GitLab/Bitbucket) + lisensi open-source terdeteksi + video YouTube publik < 3 menit + build/run instructions (versi QNX, target, toolchain) |
| Blocker terbesar | **Lisensi QNX SDP 8.0 gratis butuh akun myQNX + verifikasi email Syarip** (syaripdm@gmail.com). Tanpa SDP, audit tidak bisa divalidasi terhadap header/toolchain asli. |

---

## 1. Official Rules Devpost — ringkasan lengkap

Sumber utama: https://qnx.devpost.com/rules (dibaca 17 Nov 2026)
Halaman utama: https://qnx.devpost.com/

### 1.1 Timeline (Rules §1)

| Tahap | Waktu |
|---|---|
| Registration & Submission Period | 2 Nov 2026 11:00 ET – **15 Des 2026 14:00 ET** |
| Deadline dalam WIB | **16 Des 2026 02:00 WIB** (ET = UTC−5 di Desember; WIB = UTC+7; selisih 12 jam) |
| Judging Period | 15 Jan 2027 10:00 ET – 29 Jan 2027 17:00 ET |
| Public Community Voting | 15 Jan 2027 10:00 ET – 29 Jan 2027 17:00 ET |
| Winners Announced | ~4 Feb 2027 14:00 ET |

### 1.2 Eligibility (Rules §3)

- Terbuka untuk: individu **≥ 18 tahun**, tim, dan organisasi.
- Satu orang boleh ikut di lebih dari satu tim DAN ikut individual.
- **TIDAK terbuka untuk** penduduk/organisasi di negara yang dilarang hukum AS / sanksi OFAC — disebutkan eksplisit: **Brazil, Russia, Crimea, Cuba, Iran, North Korea** + negara lain yang disanksi komprehensif OFAC.
- **Indonesia TIDAK ada di daftar larangan** → Syarip eligible.
- Dilarang: karyawan/agen Sponsor & Administrator (BlackBerry/QNX, Devpost) + keluarga/household mereka, juri, dan pihak yang terlibat produksi hackathon.
- Tim/organisasi wajib menunjuk satu **Representative** yang bertindak atas nama tim.

### 1.3 Project Requirements (Rules §4)

Proyek harus berupa software yang **berjalan di / menarget QNX 8.0 (QNX Everywhere)**, salah satu:

1. Aplikasi, driver, library, atau komponen yang **berjalan di QNX 8.0 RTOS**, di hardware apa pun yang didukung QNX, **termasuk QEMU**; ATAU
2. **Host-based tool** (Windows, macOS, atau Linux) yang **build, test, analyze, atau mendukung** software yang menarget QNX 8.0.
   → **QNX Doctor masuk jalur #2** (tool analisis statis host-side, Linux).

Kategori (pilih **tepat 1** di form submit):

1. Robotics & Medical
2. Automotive & Mobility
3. Low-level Software
4. **Developer Tooling & Host Tools** ← pilihan QNX Doctor
5. Open-Source Contribution & Ports (khusus kategori ini: repo BARU dibuat selama Submission Period, berisi patch/porting layer + QNX build files + instruksi; referensikan upstream via URL, **jangan submit fork**)

Aturan lain:

- Proyek harus **baru dibuat 2 Nov–15 Des 2026**, ATAU proyek lama yang **di-update signifikan** setelah 2 Nov 2026 (dan dijelaskan update-nya).
- Proyek harus bisa di-install & jalan konsisten sesuai video/deskripsi.
- **Multiple submissions diperbolehkan**, asal tiap submission unik & berbeda secara substansial.
- Integrasi SDK/API pihak ketiga harus sah lisensinya.
- Proyek **tidak boleh** dikembangkan dengan dukungan finansial/preferensial dari Sponsor/Administrator (termasuk lisensi komersial QNX). Lisensi **QNX Everywhere non-komersial gratis TIDAK termasuk** larangan ini — itu jalur resmi yang disediakan sponsor.
- Semua materi submission **dalam bahasa Inggris** (atau disertai terjemahan Inggris).

### 1.4 Submission Requirements (Rules §4) — CHECKLIST

- [ ] **URL repo publik** GitHub / GitLab / Bitbucket — berisi SEMUA source, aset, dan instruksi build & run. Repo harus **public + open source, file lisensi terdeteksi di bagian atas halaman repo (About section)**.
- [ ] Repo harus **membuktikan proyek benar-benar build untuk / jalan di QNX 8.0** — sekadar menyebut "QNX 8.0" di README **TIDAK cukup**.
- [ ] **Satu kategori** dipilih di form.
- [ ] **Build & run instructions**: sebutkan **versi QNX, target (hardware atau QEMU), dan toolchain** yang dipakai.
- [ ] **Text description** yang menjelaskan fitur & fungsionalitas proyek.
- [ ] **Video demo < 3 menit**, footage proyek berfungsi di device/target yang dituju, **upload ke YouTube, public**, tanpa trademark/musik berhak cipta pihak ketiga tanpa izin. Juri tidak wajib menonton lebih dari 3 menit.
- [ ] (Khusus Open-Source Ports) URL upstream + URL PR bila ada — *tidak relevan untuk QNX Doctor*.
- [ ] (Bonus Codelab) URL codelab/tutorial di field yang disediakan — *rencana: ikut, lihat §5.4*.
- [ ] **Evidence of QNX use** — submission harus menjelaskan bagaimana proyek memakai/mendukung QNX. Bukti yang diterima: QNX-specific source code/API; QNX libraries, headers, **buildfiles**, toolchains, system images, config files di repo; demo jalan di QNX 8.0; atau untuk host tool: output/fungsi yang spesifik untuk build/analyze/test/deploy/debug software QNX 8.0. Daftar ini ilustratif, bukan exhaustive. **Kode POSIX-compatible tetap eligible** bila koneksi ke QNX ditunjukkan jelas. → Sebutkan file/fungsi/output/demo yang relevan di deskripsi submission.
- [ ] Submission adalah karya orisinal, dimiliki penuh oleh entrant, tidak melanggar IP pihak lain.
- [ ] Proyek tersedia **gratis tanpa restriksi** untuk testing/evaluasi oleh Sponsor, Administrator, dan Juri **sampai Judging Period berakhir**. Juri tidak wajib men-test; boleh menilai hanya dari deskripsi, gambar, dan video.
- [ ] Draft boleh disimpan sebelum deadline; **setelah deadline tidak boleh diubah** (kecuali perubahan yang diizinkan Sponsor/Devpost untuk hapus materi yang melanggar IP/PII).

### 1.5 Judging (Rules §6)

- **Stage One (pass/fail)**: proyek masuk akal sesuai tema & memakai API/SDK yang dipersyaratkan.
- **Stage Two — 4 kriteria, bobot SAMA (equally weighted)**:
  1. **Technological Implementation** — seberapa baik proyek dibangun & seberapa efektif memakai QNX 8.0; kode menunjukkan engineering effort nyata, implementasi non-trivial yang benar-benar build/jalan di QNX.
  2. **Design** — produk lengkap & koheren, bukan sekadar proof of concept.
  3. **Potential Impact** — kasus nyata & spesifik memecahkan masalah di market yang dilayani QNX, dan menjelaskan kenapa fondasi real-time seperti QNX adalah pilihan tepat.
  4. **Innovation & AI Creativity** — penggunaan QNX yang kreatif & non-obvious, plus pemahaman genuine terhadap problem space.
- Tie-break: skor kriteria pertama (Technological Implementation) tertinggi menang; bila masih seri, lanjut ke kriteria berikutnya; bila semua seri, panel juri voting.
- Penilaian bisa memakai panel ahli, peer review, **analisis otomatis berbasis AI**, atau kombinasi.

**Bonus prizes (Rules §6):**

- **Best Codelab / Tutorial ($3.500)**: terbuka untuk entrant mana pun yang juga submit proyek eligible. Syarat: URL codelab/tutorial **yang ditulis selama Submission Period** yang mengajarkan cara melakukan suatu task di/untuk QNX 8.0. **Tidak wajib berhubungan dengan proyek entrant.** Dinilai dengan kriteria judging yang sama.
- **Best Use of QNX-specific Technologies ($3.500)**: untuk submission yang paling kreatif/impactful/sophisticated memakai kemampuan unik platform QNX, **termasuk tapi tidak terbatas pada: native message passing, resource managers, microkernel architecture, startup and boot customization, real-time services, dan security policies**.
  → QNX Doctor sangat cocok: audit native message passing, resource manager, buildfile/startup, RT scheduling, dan (nanti) security policies.

**Community Choice**: voting publik 15–29 Jan 2027; pemenang = verified votes terbanyak (Devpost yang menentukan). Dilarang manipulasi vote (manual/otomatis, multi-email) — pelanggaran = diskualifikasi vote.

### 1.6 Hadiah & payout (Rules §8)

| Hadiah | Jumlah | Pemenang |
|---|---|---|
| Grand Prize | **$10.000** + episode podcast "Code the Future" + coffee chat dengan John Wall (CEO QNX) | 1 |
| Best of Robotics & Medical | $4.000 + coffee chat exec QNX | 1 |
| Best of Automotive & Mobility | $4.000 + coffee chat exec QNX | 1 |
| Best of Low-level Software | $4.000 + coffee chat exec QNX | 1 |
| Best of Developer Tooling & Host Tools | $4.000 + coffee chat exec QNX | 1 |
| Best of Open-Source Contribution & Ports | $4.000 + coffee chat exec QNX | 1 |
| Runner-Up (tiap kategori) | $2.000 | 1 × 5 kategori |
| Honorable Mention | $1.000 | 3 |
| Best Codelab / Tutorial | $3.500 | 1 |
| Best use of QNX-specific Technologies | $3.500 | 1 |
| Community Choice | Blog + social feature + QNX swag (tanpa uang) | 1 |

**Aturan multiple prize (penting):** satu proyek bisa menang **maksimal 1 Overall prize + 1 Bonus prize + 1 Community Choice prize**.
→ Skenario terbaik QNX Doctor: Best of Developer Tooling ($4.000) + Best use of QNX-specific Technologies ($3.500) + Community Choice = **$7.500 + swag/feature**. Grand Prize ($10.000) + bonus = $13.500 bila menang grand.

**Cara pemenang dibayar (Rules §8.3–8.4) — PAYOUT DEVPOST:**

- Hadiah dibayar ke Entrant (individu) / Representative (tim) / Organisasi.
- **Hadiah uang dikirim via pos ke alamat pemenang ATAU ditransfer elektronik ke rekening bank pemenang**, HANYA setelah **winner affidavit + formulir wajib lainnya (Required Forms) diterima lengkap**.
- **Deadline mengembalikan Required Forms: 10 hari kerja** setelah formulir dikirim ke pemenang. Info salah / telat → hadiah bisa tertunda, didiskualifikasi, atau hangus.
- **Hadiah dikirim dalam 60 hari** setelah Sponsor/Devpost menerima Required Forms yang lengkap.
- **Verifikasi identitas/kualifikasi/peran pemenang wajib** sebelum hadiah dianggap sah — pemenang belum resmi sampai affidavit terverifikasi, walau sudah diumumkan.
- **Pajak & biaya ditanggung pemenang**: wiring fee, currency exchange fee, dan pajak di yurisdiksi pemenang. Penduduk AS wajib isi **W-9**; penduduk negara lain (termasuk Indonesia) kemungkinan diminta **W-8BEN**. Sponsor/Devpost berhak memotong (withholding) sebagian hadiah sesuai hukum pajak AS / yurisdiksi pemenang.
- Hadiah **non-transferable**; sponsor boleh mengganti dengan hadiah setara/lebih tinggi.
- Bila tidak ada submission eligible untuk suatu hadiah, hadiah itu tidak diberikan.

**IP (Rules §7):** submission tetap milik entrant. Sponsor mendapat lisensi non-eksklusif untuk judging; Sponsor & Devpost berhak mempromosikan submission dan memakai nama/likeness/foto/suara kontributor untuk promosi hackathon selama periode hackathon + **3 tahun** setelahnya.

**Sengketa (Rules §13):** arbitrase final & mengikat di bawah American Arbitration Association, hukum Negara Bagian New York, AS. Tidak ada class action.

**Kontak resmi:** [email protected] (tertera di Rules §15).

### 1.7 Juri (tertera di halaman utama)

Sheridan Ethier (VP Engineering Middleware), Patrick Murtha (Sr Director Product Mgmt), Cris Sinnott (Sr Director Engineering, Open Source), Andy Gryc (Director, Developer Ecosystem), Dongkai Guo (Director, Software Development), John Dallas (Principal Academic Partnerships Manager), Morgan McKeen (Developer Engagement Marketing Manager), Mike Shane (Sr Systems Software Developer), John Hanam (Manager, Developer Relations).

---

## 2. QNX Everywhere — cara daftar gratis QNX SDP 8.0

Sumber: https://qnx.software/en/developers/get-started/qnx-everywhere (dibaca 17 Nov 2026),
https://qnx.software (homepage), https://www.qnx.com/developers/docs/8.0/com.qnx.doc.qnxsdp.quickstart/topic/about.html

### 2.1 Apa itu QNX Everywhere

Program BlackBerry/QNX (diluncurkan CES 2025) yang memberi **akses gratis QNX SDP 8.0 untuk non-commercial use** — pelajar, hobbyist, prototyper, peneliti. Lisensi **gratis dan perpetual (tidak perlu renewal)** untuk non-komersial, menurut komentar tim Developer Relations QNX. Per Jan 2026: **30.000+ lisensi** diunduh, 12.000+ lisensi diterbitkan, 120+ institusi akademik, 10.000+ learners training online, 2.500+ open-source ports.

**Yang didapat (tiga komponen):**

| Komponen | Isi |
|---|---|
| **QNX SDP 8.0** | Software Development Platform: QNX Neutrino RTOS 8.0 (microkernel), toolchain qcc/q++, QNX Software Center, Momentics IDE / QNX Toolkit for VS Code, BSP, utilitas (mkifs, mkqnximage, dll.) |
| **QNX Developer Desktop** | Self-hosted desktop yang jalan langsung di QNX 8.0 (bukan di host OS): C, C++, Python, Make, CMake, Git, terminal, browser, file manager Thunar; sample projects C/C++, Python, GTK, OpenGL ES. Dikirim sebagai **QEMU image** (host Ubuntu 22.04/24.04 LTS). |
| **QNX Hypervisor** | Hypervisor deterministik untuk mixed-criticality (termasuk QNX Hypervisor for Safety 8.0). |

Juga tersedia gratis: **training online di https://learning.qnx.com**, QNX SDP 8.0 Quick Start Guide, QNX Quick Start Target Image untuk Raspberry Pi 5, dan Codelabs di https://qnx.github.io.

**Batasan lisensi (QDL — QNX Development License, non-commercial):** hanya untuk educational / personal projects / aktivitas non-revenue. **Tidak mencakup** evaluasi atau development untuk tujuan komersial. Untuk evaluasi komersial 30 hari ada jalur terpisah. SDP 8.0 dirancang untuk SoC **4+ CPU cores**.

### 2.2 Langkah pendaftaran (dokumentasi langkah — TIDAK dilakukan di riset ini)

Langkah resmi dari halaman QNX Everywhere ("Try QNX Now for Free"):

1. **Login ke akun myQNX** — "To receive your license, you must have a myQNX account."
2. **Isi formulir lisensi QNX Everywhere** — setelah login, diminta mengisi license data untuk memulai request.
3. **Terima lisensi** — setelah request diproses, lisensi non-komersial dikirim.

Detail pembuatan akun myQNX (sumber: http://www.qnx.com/developers/docs/qsc/com.qnx.doc.qsc.user_guide/topic/create_myqnx.html):

1. Buka www.qnx.com → klik **Sign In** di atas halaman.
2. Isi **alamat email + pilih password** → klik **Create Account**.
3. **Cek email** — ada **confirmation key**.
4. Aktivasi dengan salah satu cara: (a) klik **activation link** di email konfirmasi, atau (b) masukkan key + email di halaman pembuatan akun → Continue.

Setelah akun aktif:

- Buka profil myQNX → **Registered Products** — di sini terlihat license key, serial number, license certificate, dan license administrator per produk.
- **Catatan resmi: beri waktu hingga 1 jam** sampai lisensi QNX Everywhere muncul di profil myQNX setelah deployment dimulai. Bila lisensi tidak muncul, hubungi myqnx@blackberry.com.
- Download & install via **QNX Software Center (QSC)**: install QSC → buat instalasi QNX SDP 8.0 → (opsional) install QNX Momentics IDE atau QNX Toolkit for VS Code.
- Aktivasi license key di QNX Toolkit: masukkan **email yang terasosiasi dengan akun myQNX**; bila aktivasi remote gagal, aktivasi manual via QSC atau utilitas `qlicense`.

**Persyaratan host (Quick Start Guide SDP 8.0):**

- Host development: PC **x86, Windows atau Linux**. **QNX SDP 8.0 TIDAK mendukung macOS** dan **TIDAK didukung di host ARM**.
- Target: VM (QEMU/VMware/VirtualBox) atau board (mis. Raspberry Pi 5).
- Akun myQNX dengan lisensi SDP 8 yang valid harus sudah ter-deploy sebelum software bisa dipakai.

### 2.3 Apa yang BISA diverifikasi tanpa login (dokumen publik)

Semua ini bisa dibaca/dicek **tanpa akun** — dipakai untuk riset & spek ini:

- Dokumen SDP 8.0 lengkap: https://www.qnx.com/developers/docs/8.0/ (termasuk Quick Start Guide, System Architecture, Utilities Reference, Library Reference, BSP 8.0 docs di https://www.qnx.com/developers/docs/BSP8.0/ ...)
- Blog "QNX From The Board Up" (membuat image QNX dari nol + QEMU): https://qnx.software/en/blog/2026/qnxe-ftbu-2
- QNX Everywhere FAQ & halaman program: https://qnx.software/en/developers/get-started/qnx-everywhere
- Codelabs publik: https://qnx.github.io
- Open-source ports dashboard: https://oss.qnx.com dan repo GitHub QNX (disebut di halaman Everywhere: "open-source ports on its GitHub repository")
- Proyek Eclipse S-CORE `toolchains_qnx` (Bazel toolchain QNX 8.0 + contoh buildfile IFS + script QEMU) — publik, dipakai sebagai referensi teknis di §3.
- Devpost hackathon & Rules — publik, tanpa login.
- Komunitas: r/QNX, QNX Discord (discord.gg — link di halaman Everywhere).

**Yang TIDAK bisa tanpa login:** download SDP 8.0 itu sendiri, QNX Software Center, license key, Quick Start Target Image RPi/QEMU via QSC, dan isi myQNX License Manager.

### 2.4 ⛔ BLOKIR — langkah yang butuh Syarip

| # | Langkah | Kenapa butuh Syarip | Detail |
|---|---|---|---|
| 1 | **Buat akun myQNX** | Akun harus atas nama + email dia; password akun adalah miliknya | Email: **syaripdm@gmail.com**. Password: pakai **password default yang dia tentukan** (aturan 14 Nov 2026 — nilai TIDAK ditulis di file ini; dia kirim langsung di chat / kartu aman). |
| 2 | **Klik activation link / masukkan confirmation key dari email** | Kode verifikasi dikirim ke inbox syaripdm@gmail.com — hanya dia yang bisa buka | Cek inbox (termasuk spam) setelah daftar. |
| 3 | **Isi formulir lisensi QNX Everywhere** (login myQNX → form) | Form memakai data/identitas dia; persetujuan lisensi non-komersial atas nama dia | Setelah submit, tunggu **hingga 1 jam** sampai lisensi muncul di profil. |
| 4 | **(Opsional, nanti) Download SDP 8.0 via QNX Software Center** | Download besar (SDP 8.0 = paket ratusan MB–GB) + login myQNX; sebaiknya di VM/host Linux, bukan HP | Bisa didelegasikan ke agen SETELAH akun + lisensi aktif, dengan kredensial yang dia berikan lewat jalur aman. |
| 5 | **(Saat menang) Isi winner affidavit + W-8BEN + data bank** | Dokumen legal & data bank pribadi — hanya dia | Deadline 10 hari kerja setelah formulir dikirim; hadiah cair ≤ 60 hari setelah formulir lengkap. |

**Yang TIDAK butuh Syarip (bisa dikerjakan agen sekarang):** semua riset, penulisan spek, scaffolding repo, penulisan engine audit (parser C/buildfile) memakai spesifikasi publik di §3, penulisan codelab, dan persiapan video (setelah ada hasil audit nyata).

---

## 3. Riset teknis QNX SDP 8.0 (sumber publik)

> Semua sintaks/API di bawah ini diambil dari dokumentasi publik QNX (docs.qnx.com / www.qnx.com/developers/docs), blog resmi qnx.software, dan repo publik Eclipse S-CORE. Nomor versi yang dikutip: SDP 8.0 / Neutrino 8.0.0.

### 3.1 Buildfile mkifs — sintaks & contoh nyata

**Utilitas:** `mkifs` — "Build an OS image filesystem (QNX)".
Sintaks (Utilities Reference):

```
mkifs [-a suffix] [-l inputline] [-n[n]] [-p patchfile]
      [-r rootdir] [-s section] [-v] [buildfile [imagefile]]
```

Jalan di: QNX Neutrino, Linux, Windows. Jangan dikacaukan dengan `mkefs` (embedded FS) / `mketfs` (ETFS).

**Grammar buildfile:** tiap baris = `[attributes] file_specification`. Atribut dalam `[...]`. `#` = komentar. Tidak bisa pakai backslash untuk memecah baris. Dua jenis atribut:

- **Boolean**: prefix `+`/`-`, mis. `+compress`, `-bigendian`, `+script`, `+optional`, `+raw`.
- **Value**: `nama=nilai`, mis. `uid=5 gid=5`, `virtual=x86_64,multiboot`, `image=0x400000`, `type=link`, `data=copy`, `physical=...`, `code=...`, `module=aps`.

Atribut yang didukung mkifs (dokumen resmi): `+|-autolink`, `+|-bigendian`, `cd=path`, `chain=addr`, `code=uip_spec`, `+|-compress`, `data=uip_spec`, `gid=id_spec`, `image=addr_space_spec`, `module=module_name` (modul opsional untuk procnto, mis. `[module=aps]`), `+|-optional`, `+|-page_align`, `physical=boot_spec`, `+|-raw`, `+|-script`, `search=filename:...`, `type=file_type`, `uid=id_spec`, `virtual=boot_spec`.

**Contoh 1 — buildfile minimal x86 (dari Utilities Reference `mkifs`):**

```
[virtual=x86,bios] .bootstrap = {
    startup-bios
    PATH=/proc/boot procnto
}
[+script] .script = {
    devc-con -n9 &
    reopen /dev/con1
    [+session] esh
}
libc.so
[data=copy]
devc-con
esh
[type=link] /usr/lib/ldqnx.so.2=/proc/boot/libc.so
```

Build: `mkifs simple.bld simple.ifs`

**Contoh 2 — buildfile x86_64 multiboot untuk QEMU (dari blog resmi "QNX From The Board Up #2", qnx.software):**

```
[virtual=x86_64,multiboot] boot = {
    startup-x86 -D 8250
    procnto-smp-instr
}
[+script] init = {
    display_msg "Welcome to QNX 8.0"
    devc-ser8250 &
    reopen /dev/ser1
    [+session] /bin/sh &
}
```

Build: `mkifs image.build image.ifs`

**Contoh 3 — buildfile x86_64 dari repo Eclipse S-CORE `toolchains_qnx` (`tests/init_x86_64.build`):**

```
[image=0x400000]
[virtual=x86_64,multiboot] boot = {
    startup-x86 -v -D8250..115200 -zz
    procnto-smp-instr
}
[+script] startup-script = {
    display_msg Welcome to QNX OS 8.0 on x86_64 tweaked for S-CORE!
    SYSNAME=nto
    TERM=qansi
    devc-ser8250 &
    reopen /dev/ser1
    [+session] /bin/sh &
}
```

**Struktur buildfile (3 bagian):**

1. **Bootfile** — `[virtual=<arch>,<protocol>] .bootstrap = { startup-... ; procnto... }`. `virtual` = virtual address system; protokol umum: `multiboot`, `elf`, `bios`, `srec`. `[image=<size>]` = ukuran maksimum image (hex, mis. `0x400000` = 4 MB).
2. **Script** — `[+script] .script` / `init` = perintah yang dijalankan kernel setelah init: `display_msg`, `devc-*`, `reopen`, `[+session]`; perintah `waitfor`, `reopen`, `display_msg` adalah builtin script.
3. **Daftar file/link** — file yang dimasukkan ke image; `[type=link] /path/dest=/proc/boot/src` untuk symlink; `[data=copy]` untuk file data.

**Perintah terkait:**

- `mkqnximage --type=vmware|vbox|qemu [--build] [--clean] [--graphics[=yes|no]] [--repos=dir[:dir]...]` — generator VM image QNX Neutrino. Untuk QEMU: host Ubuntu, guest **x86-64** (kombinasi yang didukung). Snippet kustomisasi di `local/snippets/`: `system_files.custom`, `ifs_files.custom` (format buildfile mkifs), `post_start.custom` (fragmen shell — **bukan** sintaks buildfile; gotcha nyata). Filesystem image: partisi system read-only di `/system`, data read-write di `/data`; tidak ada FS yang di-mount di `/`.
- BSP generic x86_64: `make` di `$BSP_ROOT_DIR/images/generic-uefi` → `x86_64-generic-uefi.efi` (buildfile `x86_64-generic-uefi.build`); varian hypervisor `x86_64-generic-uefi-hyp.efi`; `make disk_image` → `disk.img` (mkqnx6fsimg + mkfatfsimg + diskimage). Untuk mkifs langsung, wajib `-r` untuk lokasi binary.
- RPi 5: `make ifs-rpi5.raw` di `$BSP_ROOT_DIR/images`; boot U-Boot: `fatload mmc 0 0x80000 ifs-rpi5.raw` lalu `go 0x80000 ${fdtcontroladdr}`.

### 3.2 Toolchain QNX — qcc, target, sysroot

- **Compiler driver: `qcc` (C) / `qpp` / `q++` (C++)**. QNX merekomendasikan `qcc`, bukan memanggil `gcc` langsung. `qcc -V` (tanpa argumen) menampilkan daftar compiler & platform yang didukung.
- **Target flag `-V gcc_nto<arch><endian>`**:
  - `qcc -V gcc_ntoaarch64le hello.c -o hello` (AArch64, SDP 8.0)
  - `qcc -V gcc_ntox86_64 hello.c -o hello` (x86_64)
  - Varian lama: `gcc_ntoarmv7le` (armle-v7), `gcc_ntoppcbe`, `gcc_ntox86`.
- **Environment variables (diset `qconfig` / skrip SDP):**
  - `QNX_HOST` — lokasi file host-specific (tools). Contoh instalasi: `~/qnx800/host/linux/x86_64`.
  - `QNX_TARGET` — lokasi target backends (headers + libs) di host. Header di `${QNX_TARGET}/usr/include` (termasuk `sys/`, `arpa/`, ...).
  - `QNX_CONFIGURATION` — lokasi file konfigurasi instalasi (default self-hosted: `/etc/qconfig`).
  - Lisensi: `~/.qnx/license/licenses` (atau `/opt/score_qnx/license/licenses` di CI S-CORE).
- **CMake (Qt for QNX, pola resmi):**
  ```cmake
  set(CMAKE_SYSTEM_NAME QNX)
  set(CMAKE_SYSTEM_PROCESSOR aarch64le)   # atau x86_64
  set(arch gcc_ntoaarch64le)
  set(CMAKE_C_COMPILER qcc)
  set(CMAKE_C_COMPILER_TARGET ${arch})
  set(CMAKE_CXX_COMPILER q++)
  set(CMAKE_CXX_COMPILER_TARGET ${arch})
  set(CMAKE_FIND_ROOT_PATH $ENV{QNX_TARGET};$ENV{QNX_TARGET}/${CMAKE_SYSTEM_PROCESSOR})
  set(CMAKE_SYSROOT $ENV{QNX_TARGET})
  ```
  `CMAKE_SYSTEM_VERSION`: `800` untuk SDP 8.0 (710 untuk 7.1).
- **Self-hosted vs cross-development:** self-hosted = develop & run di sistem QNX yang sama (Developer Desktop); cross = develop di host Linux/Windows, transfer & debug di target. `qcc` tanpa `-V` default ke platform host saat ini.
- **QNX Toolkit for VS Code**: butuh SDP 8.0 terinstal terpisah; setting `qnx.sdpPath`; walkthrough otomatis; bisa generate example projects ("Generate QNX Example Projects..."). Proyek: QNX Recursive Makefile, Simple Makefile, QNX CMake Project, atau None.
- **Versi toolchain**: SDP 8.0 memakai GCC-based qcc; BSP 8.0.5 adalah rilis terbaru yang terlihat di release notes (Sep–Okt 2026).

### 3.3 Header & API khusus QNX (nyata, dari Library Reference / Programmer's Guide)

| Header | API / simbol | Fungsi |
|---|---|---|
| `sys/neutrino.h` | `ChannelCreate(unsigned flags)`, `ChannelDestroy(int chid)`, `ChannelCreatePulsePool()`, `ConnectAttach(nd, pid, chid, index, flags)`, `ConnectDetach(coid)` | Channel & connection untuk message passing. Flag: `_NTO_CHF_MSG_PAUSING`, `_NTO_CHF_NET_MSG`, `_NTO_CHF_THREAD_DEATH`, `_NTO_CHF_INHERIT_RUNMASK`. |
| `sys/neutrino.h` | `MsgSend(coid, smsg, sbytes, rmsg, rbytes)`, `MsgSendv/nc`, `MsgReceive(chid, msg, nbytes, info)`, `MsgReceivePulse()`, `MsgReply(rcvid, status, msg, nbytes)`, `MsgRead/MsgWrite`, `MsgError()`, `MsgDeliverEvent()` | Message passing sinkron (copy data). Minimal set: ChannelCreate, ConnectAttach, MsgSend, MsgReceive, MsgReply. |
| `sys/neutrino.h` | `ThreadCreate()`, `ThreadCtl(_NTO_TCTL_*, ...)`, `SchedGet()`, `SchedSet()`, `SignalKill()`, `InterruptAttach()`, `InterruptAttachEvent()`, `InterruptWait()`, `InterruptUnmask()`, `InterruptMask()` | Thread & interrupt kernel calls. |
| `sys/neutrino.h` | `name_attach()`, `name_open()`, `name_close()` (via `sys/dispatch.h`) | Nama pathname untuk channel (dipakai resource manager). |
| `sys/siginfo.h` | `struct sigevent`, `SIGEV_INTR`, `SIGEV_PULSE`, `SIGEV_SIGNAL`, `SIGEV_THREAD`, `SIGEV_UNBLOCK`, `SIGEV_SIGNAL_CODE` | Event notification; pulse = pesan 8-byte non-blocking (code + value 32-bit). |
| `sys/procmgr.h` | `procmgr_ability()`, `procmgr_symlink()`, `procmgr_daemon()`, `procmgr_event_notify()` | Kemampuan proses, symlink di /proc, daemonize. |
| `sys/mman.h` | `mmap()`, `munmap()`, `mlock()`, `mlockall(MCL_CURRENT\|MCL_FUTURE)`, `shm_open()`, `mmap_device_io()`, `mmap_device_memory()` | Memory mapping; `mmap_device_io()` butuh `ThreadCtl(_NTO_TCTL_IO_PRIV, ...)` + root. |
| `sys/iofunc.h` + `sys/dispatch.h` | `resmgr_attach()`, `resmgr_connect_funcs_t`, `resmgr_io_funcs_t`, `iofunc_attr_t`, `iofunc_func_init()`, `dispatch_create()`, `dispatch_context_alloc()`, `resmgr_block()`, `resmgr_msgread()` | Resource manager framework (lapisan: iofunc → resmgr → dispatch → thread pool). **Attach butuh root.** |
| `sys/dispatch.h` | `dispatch_handler()`, `dispatch_block()`, `message_attach()` | Dispatch loop server. |
| `hw/inout.h` | `in8/in16/in32`, `out8/out16/out32`, `mmap_device_io()` | I/O port hardware access (x86). |
| `pthread.h` | `pthread_create()`, `pthread_setschedparam()`, `pthread_getschedparam()`, `pthread_attr_setschedpolicy()`, `pthread_attr_setschedparam()`, `pthread_attr_setinheritsched(PTHREAD_EXPLICIT_SCHED \| PTHREAD_INHERIT_SCHED)`, `pthread_mutexattr_setprotocol()`, `pthread_mutexattr_setprioceiling()` | POSIX threads + RT scheduling. Policy: `SCHED_FIFO`, `SCHED_RR`, `SCHED_OTHER` (di QNX, SCHED_OTHER dipetakan ke SCHED_RR). |
| `pthread.h` | `PTHREAD_PRIO_NONE`, `PTHREAD_PRIO_INHERIT`, `PTHREAD_PRIO_PROTECT` | Protokol mutex: none / priority inheritance / priority ceiling. |
| `mqueue.h` | `mq_open()`, `mq_send()`, `mq_receive()`, `mq_notify()` | POSIX message queues. |
| `sys/slog2.h` + `libslog2` | `slog2f()`, `vslog2f()`, `slog2_set_verbosity()`, `slog2_get_verbosity()`; daemon `slogger2` | System logging framework; severity levels; interface PPS opsional (`-P pps_path`, butuh PPS service jalan). |
| PPS | service `pps`; objek di `/fs/pps`; `open()` + `read()`/`write()`; objek spesial `.all`, `.notify` | Persistent Publish/Subscribe — publish async, persist across reboot; subscriber `open(O_RDONLY)`, publisher `open(O_WRONLY)`/`O_RDWR`; mode full/delta. |
| `screen/screen.h` | `screen_create_context()`, `screen_create_window()`, `screen_post_window()` | QNX Screen graphics (dipakai Developer Desktop & sample game). |
| `sys/neutrino.h` | `ClockCycles()`, `ClockTime()`, `TimerCreate()`, `TimerSettime()` | High-resolution timing; `CLOCK_MONOTONIC` untuk pengukuran. |
| `sys/aps.h` | Adaptive Partitioning Scheduler (APS) — `[module=aps]` di buildfile | Budget CPU per partisi. |
| `sys/ham.h` | High Availability Manager (HAM) | Monitoring & recovery proses. |

**Fakta scheduling penting (dari QNX docs "The scheduling thread attributes"):**

- Default `pthread_attr_setinheritsched` = `PTHREAD_INHERIT_SCHED`: thread baru **mewarisi** policy creator, dan nilai policy/priority di attr **diam-diam diabaikan** (tanpa error). Harus set `PTHREAD_EXPLICIT_SCHED` agar `setschedpolicy`/`setschedparam` berlaku.
- **Bug klasik (dokumen resmi):** set `PTHREAD_EXPLICIT_SCHED` + hanya set policy tanpa priority → `sched_priority` default = **0** = prioritas proses IDLE. "You simply cannot run a thread at priority zero."
- Hanya **root** yang bisa memberi RT scheduling parameters (SCHED_FIFO/SCHED_RR).
- Thread SCHED_FIFO yang loop tanpa block akan menahan CPU selamanya dari thread prioritas lebih rendah.
- **Priority inheritance di message passing:** Neutrino menerapkan priority inheritance pada MsgSend — server yang menerima pesan mewarisi prioritas pengirim (inheritance across message passing). Ini alasan arsitektur message-passing QNX tahan terhadap priority inversion dibanding mutex biasa.

### 3.4 Anti-pattern real-time (nyata, grounded di dokumen & praktik QNX)

| # | Anti-pattern | Kenapa berbahaya di RT | Deteksi (pola kode) |
|---|---|---|---|
| RT-01 | **`malloc`/`free`/`new`/`delete` di thread RT** (setelah init) | Alokasi heap bisa block / page fault → jitter tak terbatas; allocator memakai lock global | `malloc|calloc|realloc|free|new |delete` di dalam fungsi thread yang di-set SCHED_FIFO/RR, atau setelah `mlockall` |
| RT-02 | **Mutex tanpa priority inheritance/ceiling** | Priority inversion klasik: thread low-prio pegang lock, medium-prio preempt, high-prio kelaparan | `pthread_mutex_init(&m, NULL)` / attr tanpa `pthread_mutexattr_setprotocol(..., PTHREAD_PRIO_INHERIT \| PTHREAD_PRIO_PROTECT)` pada mutex yang dipakai lintas prioritas |
| RT-03 | **Thread tanpa schedparam eksplisit** | `PTHREAD_INHERIT_SCHED` (default) → policy/priority di attr diabaikan; atau priority 0 (= IDLE) | `pthread_create` tanpa `pthread_attr_setinheritsched(..., PTHREAD_EXPLICIT_SCHED)` + `setschedpolicy` + `setschedparam` |
| RT-04 | **Blocking call di ISR / interrupt handler** | ISR QNX harus pendek; blocking (MsgSend, mutex lock, malloc, printf) di handler = hang/latency sistem | `InterruptAttach()` handler yang memanggil `MsgSend|pthread_mutex_lock|malloc|printf|sleep|open` — pola benar: `InterruptAttachEvent()` + `SIGEV_INTR` + `InterruptWait()` di thread |
| RT-05 | **Unbounded allocation / alokasi di loop RT** | Fragmentasi + pertumbuhan heap tak terbatas → kehabisan memori di sistem embedded | `malloc` di dalam `while(1)` loop thread RT; `realloc` bertumbuh; tidak ada `mlockall(MCL_CURRENT\|MCL_FUTURE)` |
| RT-06 | **Tidak ada error check pada kernel call QNX** | `ChannelCreate`/`ConnectAttach`/`MsgSend` gagal diam-diam → perilaku undefined | Return value `ChannelCreate|ConnectAttach|MsgSend|name_attach|resmgr_attach` tidak dicek (`== -1`) |
| RT-07 | **MsgSend tanpa timeout** | Server mati/hang → client block selamanya | `MsgSend()` tanpa `TimerTimeout()` / tanpa `MsgSendnc()`; tidak ada `SIGEV_UNBLOCK` |
| RT-08 | **Prioritas sama untuk semua thread (flat priority)** | Tidak ada diferensiasi RT; thread background bisa menunda thread kritis | Semua `sched_priority` bernilai sama / tidak ada `pthread_setschedparam` sama sekali |
| RT-09 | **I/O blocking di thread RT** (read/write file, printf ke console, network) | I/O bisa block tak terbatas → deadline miss | `printf|fprintf|read|write|fopen` di path thread SCHED_FIFO |
| RT-10 | **Buildfile: tidak ada `procnto` / startup salah / file hilang** | Image tidak boot / boot hang | `[virtual=...]` tanpa `procnto`, `startup-*` tidak cocok arch, file di `[+script]` tidak ada di image |
| RT-11 | **`sched_priority` = 0** | = prioritas IDLE; thread praktis tidak pernah jalan | `sched_priority = 0` atau attr ter-init default + EXPLICIT_SCHED tanpa setschedparam |
| RT-12 | **Tidak `mlockall` untuk thread RT** | Page fault di path RT = jitter | Thread RT tanpa `mlockall(MCL_CURRENT | MCL_FUTURE)` setelah init |

### 3.5 Menjalankan QNX 8.0 di QEMU

**Jalur A — mkifs manual + QEMU x86_64 (blog resmi FTBU #2):**

```bash
mkifs image.build image.ifs
qemu-system-x86_64 -cpu max -smp 1 -display none -kernel image.ifs -serial stdio
```

Catatan: image multiboot (`[virtual=x86_64,multiboot]`), startup `startup-x86 -D 8250`, kernel `procnto-smp-instr`. Serial diarahkan ke stdio; driver `devc-ser8250` + `reopen /dev/ser1` di script.

**Jalur B — mkqnximage (resmi, termudah):**

```bash
mkqnximage --type=qemu --build
```

Lalu boot image hasil generate dengan QEMU (x86-64 guest, host Ubuntu). Kustomisasi via `local/snippets/*.custom`.

**Jalur C — aarch64 / Raspberry Pi 4 (repo Eclipse S-CORE `toolchains_qnx`, `tests/run_qemu.sh`):**

- QEMU bawaan Ubuntu 24.04 **tidak** punya machine `-M raspi4b` dengan emulasi peripheral BCM2711 → butuh **custom-built QEMU** + DTB `bcm2711-rpi-4-b.dtb`.
- x86_64: QEMU bawaan + KVM (`-accel kvm -cpu host`) + `virtio-rng` (`/dev/urandom`).
- aarch64: TCG (tanpa akselerasi), `-append` berisi parameter bootloader (`-vvv`, `-D miniuart`).
- Pola umum aarch64:
  ```bash
  qemu-system-aarch64 -M raspi4b -cpu cortex-a72 -kernel init_aarch64.ifs \
      -dtb bcm2711-rpi-4-b.dtb -serial stdio -display none
  ```
  (parameter persis mengikuti `run_qemu.sh` S-CORE; verifikasi ulang saat SDP tersedia.)

**Jalur D — Developer Desktop QEMU image:** via QNX Software Center, instal "QNX SDP 8.0 Quick Start Target Image for QEMU" (host Ubuntu 22.04/24.04).

**Jalur E — Raspberry Pi 5:** flash "QNX Quick Start Target Image for Raspberry Pi" (tersedia di halaman Everywhere); image sudah berisi demo apps open-source.

**Referensi validasi nyata:** Proyek Devpost **QNX Bootlab** (dipublish 6 Nov 2026, https://devpost.com/software/qnx-bootlab) membuktikan pola ini jalan di SDP 8.0: `bootlab doctor` / `new` / `build` / `up`; `cmd_build()` memanggil `qcc`; `cmd_up()` memanggil `mkqnximage` lalu boot `qemu-system-x86_64` (IFS sebagai kernel, serial assertion di stdio); contoh `example/probe.c` (qcc, `qnx.target.x86_64`) mencetak `uname`, `CLOCK_MONOTONIC`, checksum prima, `done rc=0`. **Ini kompetitor langsung** — QNX Doctor harus dibedakan (lihat §5.5).

### 3.6 Contoh proyek sample QNX (untuk diaudit / dijadikan fixture)

| Proyek | Sumber | Kegunaan untuk QNX Doctor |
|---|---|---|
| Eclipse S-CORE `toolchains_qnx` — `tests/init_x86_64.build`, `tests/run_qemu.sh`, `tests/BUILD` | GitHub Eclipse S-CORE (publik; didokumentasikan via DeepWiki) | **Fixture utama**: buildfile IFS + toolchain Bazel + skrip QEMU x86_64/aarch64 |
| QNX Toolkit example projects (di-generate dari VS Code: "Generate QNX Example Projects...") | QNX Toolkit for VS Code + SDP 8.0 (butuh lisensi) | Fixture proyek C/C++/CMake resmi |
| QNX Developer Desktop sample projects (C, C++, Python, GTK, OpenGL ES) | QEMU image Developer Desktop via QSC (butuh lisensi) | Fixture aplikasi self-hosted |
| Sensor Framework samples: ADAS example, Camera example, Camera MUX, Sensor example | SDP 8.0 docs ("Run sample applications") | Fixture aplikasi sensor/camera |
| QNX Cookbook samples: Web Counter resource manager, ADIOS (Analog/Digital I/O Server), RAM-disk & tar filesystem | QNX docs "Appendix: Sample Programs" (cookbook) | **Fixture resource manager** — target audit resmgr |
| screenwm — window manager berbasis QNX Screen | https://gitlab.com/elahav/screenwm (disebut di HN oleh tim QNX) | Fixture Screen API |
| QNX Bootlab (kompetitor Devpost) | https://devpost.com/software/qnx-bootlab | Referensi validasi QEMU + pola `probe.c`; JANGAN ditiru mentah-mentah |
| QNX open-source ports (2.500+) | https://oss.qnx.com + GitHub QNX | Korpus besar untuk uji audit massal |
| QNX Codelabs | https://qnx.github.io | Referensi format codelab (untuk bonus) |
| QNX SDP 8.0 Quick Start Guide | https://www.qnx.com/developers/docs/8.0/com.qnx.doc.qnxsdp.quickstart/topic/about.html | Panduan langkah-demi-langkah resmi |
| QNX "From The Board Up" series | https://qnx.software/en/blog/2026/qnxe-ftbu-2 | Referensi buildfile + QEMU |

**Catatan akses:** `gitlab.com/qnx` **tidak bisa dibuka dari environment riset ini** (domain diblokir policy — error saat fetch, 17 Nov 2026). Akses GitLab QNX harus dicoba dari environment lain / browser. GitHub QNX + oss.qnx.com tetap bisa jadi korpus.

---

## 4. QNX Doctor — konsep produk (dari riset di atas)

**Definisi:** Host-based static analyzer (CLI + CI-friendly) untuk proyek QNX 8.0 — "dokter" yang memeriksa kesehatan real-time & QNX-spesifik sebuah codebase **tanpa perlu menjalankan SDP/QEMU** (analisis statis murni atas source + buildfile), lalu memberi diagnosis + resep perbaikan + skor.

**Kenapa ini menang di kriteria judging:**

| Kriteria | Bukti yang dibangun |
|---|---|
| Technological Implementation | Parser C + parser buildfile mkifs + cross-check konsistensi (file di script ada di image? startup cocok arch?); engine aturan RT-01..RT-12; laporan SARIF + JSON; demo nyata jalan di QEMU (probe project diaudit lalu di-boot). |
| Design | CLI rapi (`qnx-doctor check`, `init`, `report`), output berwarna + HTML report, exit code CI, skor 0–100 + grade. |
| Potential Impact | Bug RT di medical/robotics/automotive = nyawa & recall; tool ini menangkap bug sebelum deployment. Market QNX = 275 jt kendaraan + medical + industrial. |
| Innovation & AI Creativity | Aturan QNX-spesifik (message-passing inheritance, buildfile, PPS, resmgr) yang tidak ada di linter generik (clang-tidy/cppcheck tidak paham Neutrino). |

**Fitur inti (v1):**

1. `qnx-doctor check <path>` — scan repo: file `.c/.h/.cpp`, `.build`/buildfile, `CMakeLists.txt`, `Makefile`.
2. 12 aturan audit RT-01..RT-12 (§3.4) + aturan buildfile BF-01..BF-05 (§5.1).
3. Output: terminal (warna + ringkasan), `--format json|sarif|html`, exit code non-zero bila ada finding High/Critical (CI-ready).
4. `qnx-doctor explain <RULE>` — penjelasan + contoh benar/salah (bahan codelab).
5. `qnx-doctor init` — scaffold proyek contoh QNX yang **sengaja berisi bug** (bad/) + versi **benar** (good/) untuk demo & video.
6. Mode `--qemu` (opsional, bila SDP tersedia): cross-compile probe dengan `qcc`, build IFS dengan `mkifs`, boot QEMU, assert serial output — membuktikan audit konsisten dengan runtime.

---

## 5. SPEK TEKNIS QNX Doctor

### 5.1 Daftar check audit (grounded — tiap check punya pola kode nyata)

**Keluarga RT — Real-time safety (file C/C++)**

| ID | Nama | Apa yang dicari | Pola kode / API | Severity | Contoh salah → benar |
|---|---|---|---|---|---|
| RT-01 | Heap allocation in RT thread | `malloc/calloc/realloc/free/new/delete` di thread SCHED_FIFO/RR (di luar init) | `malloc(`, `calloc(`, `realloc(`, `free(`, `new `, `delete` di fungsi yang reachable dari thread RT | **High** | Salah: `void *rt_loop(){ ... p = malloc(128); ... }` → Benar: alokasi sekali di `init()` sebelum `pthread_setschedparam`, lalu pakai static pool / `mlockall(MCL_CURRENT\|MCL_FUTURE)` |
| RT-02 | Mutex without priority protocol | `pthread_mutex_init` dengan attr NULL/default, atau `setprotocol` tidak dipanggil | `pthread_mutex_init(&m, NULL)`; absen `pthread_mutexattr_setprotocol(&a, PTHREAD_PRIO_INHERIT)` / `PTHREAD_PRIO_PROTECT` | **High** | Salah: `pthread_mutex_init(&m, NULL);` → Benar: `pthread_mutexattr_init(&a); pthread_mutexattr_setprotocol(&a, PTHREAD_PRIO_INHERIT); pthread_mutex_init(&m, &a);` |
| RT-03 | Thread without explicit scheduling | `pthread_create` tanpa EXPLICIT_SCHED + policy + priority | `pthread_create(` tanpa `pthread_attr_setinheritsched(..., PTHREAD_EXPLICIT_SCHED)` di sekitarnya; atau `setschedpolicy` tanpa `setschedparam` | **High** | Salah: `pthread_attr_setschedpolicy(&a, SCHED_FIFO); pthread_create(&t, &a, ...);` (priority default 0 = IDLE) → Benar: tambah `sp.sched_priority = 10; pthread_attr_setschedparam(&a, &sp);` |
| RT-04 | Blocking call in ISR | Blocking call di dalam interrupt handler `InterruptAttach()` | Di dalam fungsi handler: `MsgSend`, `pthread_mutex_lock`, `malloc`, `printf`, `sleep`, `open`, `read` | **Critical** | Salah: handler `InterruptAttach(irq, handler, ...)` yang memanggil `MsgSend(...)` → Benar: `InterruptAttachEvent(irq, &event, 0)` dengan `event.sigev_notify = SIGEV_INTR`, lalu `InterruptWait(NULL, NULL)` di thread |
| RT-05 | Unbounded allocation in RT loop | `malloc/realloc` di dalam `while(1)` thread RT | `malloc` di dalam loop tak berbatas di thread RT | **High** | Salah: `while(1){ buf = malloc(n); ... }` → Benar: pre-allocate buffer pool di init, reuse |
| RT-06 | Unchecked QNX kernel call | Return value kernel call tidak dicek | `ChannelCreate(`, `ConnectAttach(`, `MsgSend(`, `name_attach(`, `resmgr_attach(`, `InterruptAttach` tanpa `== -1` / `if (... < 0)` | **Medium** | Salah: `chid = ChannelCreate(0);` → Benar: `chid = ChannelCreate(0); if (chid == -1) { perror("ChannelCreate"); exit(EXIT_FAILURE); }` |
| RT-07 | MsgSend without timeout | `MsgSend` tanpa timeout | `MsgSend(` tanpa `TimerTimeout(_NTO_TIMEOUT_SEND, ...)` sebelumnya, atau tanpa `MsgSendnc` | **Medium** | Salah: `MsgSend(coid, ...)` mentah → Benar: `TimerTimeout(CLOCK_REALTIME, _NTO_TIMEOUT_SEND, &event, &timeout, NULL); MsgSend(...);` |
| RT-08 | Flat priority (no differentiation) | Semua thread prioritas sama / tidak ada `pthread_setschedparam` sama sekali | Tidak ada `sched_priority` yang berbeda antar thread; tidak ada `pthread_setschedparam` di repo | **Low** | Salah: semua thread default → Benar: RT kritis prio 20, background prio 10, dst. |
| RT-09 | Blocking I/O in RT thread | I/O blocking di path thread RT | `printf(`, `fprintf(`, `fopen(`, `read(`, `write(` di fungsi thread RT (ganti dengan `slog2f` / buffer) | **Medium** | Salah: `printf("tick\n");` di loop RT → Benar: `slog2f(_SLOG_SETCODE(...), _SLOG_INFO, "tick");` atau tulis ke ring buffer |
| RT-11 | Priority zero thread | `sched_priority = 0` | `sched_priority = 0` atau `sp.sched_priority = 0` | **High** | Salah: `sp.sched_priority = 0;` → Benar: `sp.sched_priority = 10;` (1–255; 0 = IDLE) |
| RT-12 | Missing mlockall in RT thread | Thread RT tanpa memory locking | Thread RT tanpa `mlockall(MCL_CURRENT \| MCL_FUTURE)` | **Low** | Salah: tidak ada `mlockall` → Benar: `mlockall(MCL_CURRENT | MCL_FUTURE);` setelah init, sebelum loop RT |

**Keluarga BF — Buildfile / image (file `.build`, `*.bld`, buildfile)**

| ID | Nama | Apa yang dicari | Pola | Severity | Contoh salah → benar |
|---|---|---|---|---|---|
| BF-01 | Missing procnto in bootstrap | `[virtual=...] .bootstrap` tanpa `procnto` | Blok `.bootstrap` tidak mengandung `procnto` | **Critical** | Salah: `boot = { startup-x86 }` → Benar: `boot = { startup-x86 -D 8250; procnto-smp-instr }` |
| BF-02 | Startup/arch mismatch | `startup-*` tidak cocok dengan `virtual=<arch>` | `virtual=x86_64` + `startup-` selain `startup-x86`; `virtual=aarch64` + bukan `startup-*` ARM | **High** | Salah: `[virtual=x86_64,multiboot]` + `startup-rpi4` → Benar: `startup-x86` |
| BF-03 | Script references missing file | File di `[+script]` tidak ada di daftar file image | Nama binary di script (mis. `devc-ser8250`, `myapp`) tidak muncul di daftar file buildfile | **High** | Salah: script jalankan `myapp &` tapi `myapp` tidak tercantum → Benar: tambahkan `myapp` ke daftar file |
| BF-04 | Missing libc / ldqnx link | Image tanpa `libc.so` atau link `ldqnx.so.2` | Tidak ada `libc.so` dan tidak ada `[type=link] /usr/lib/ldqnx.so.2=...` | **Medium** | Salah: daftar file tanpa `libc.so` → Benar: sertakan `libc.so` + `[type=link] /usr/lib/ldqnx.so.2=/proc/boot/libc.so` |
| BF-05 | Session without reopen | `[+session]` shell tanpa `reopen` console lebih dulu | `[+session] sh` tanpa `reopen /dev/con1` / `/dev/ser1` sebelumnya | **Low** | Salah: langsung `[+session] esh` → Benar: `devc-con -n9 &` + `reopen /dev/con1` dulu |

**Keluarga QNX — API QNX-spesifik (skor bonus "Best use of QNX-specific Technologies")**

| ID | Nama | Apa yang dicari | Pola | Severity |
|---|---|---|---|---|
| QX-01 | Channel without pulse pool | `ChannelCreate` untuk server yang juga butuh pulse — sarankan `ChannelCreatePulsePool` | `ChannelCreate(0)` di server | Info |
| QX-02 | PPS object without persistence check | Publish PPS tanpa cek `pps` service jalan | `open("/pps/...")` tanpa cek service | Low |
| QX-03 | Resource manager without root note | `resmgr_attach` tanpa catatan butuh root | `resmgr_attach(` | Info |
| QX-04 | `name_attach` tanpa `name_detach` / cleanup | Attach tanpa detach saat exit | `name_attach(` tanpa `name_detach(` | Low |
| QX-05 | `ThreadCtl(_NTO_TCTL_IO_PRIV)` tanpa cek | I/O privilege tanpa error check | `ThreadCtl(_NTO_TCTL_IO` | Medium |

**Total v1: 12 RT + 5 BF + 5 QX = 22 checks.** (RT-10 dilebur ke BF-01/BF-02; penomoran dipertahankan agar stabil.)

### 5.2 Format output yang disarankan

**Terminal (default):** ringkasan skor + tabel finding (severity berwarna) + file:line + snippet + saran fix satu baris.
```
QNX Doctor — report for ./sample-bad
Score: 42/100  Grade: D  (12 findings: 2 Critical, 4 High, 4 Medium, 2 Low)
[CRITICAL] RT-04  src/isr.c:23  blocking MsgSend() inside ISR handler
  → use InterruptAttachEvent() + InterruptWait() in a thread
...
```

**JSON (`--format json`):** machine-readable untuk CI & Devpost evidence:
```json
{
  "tool": "qnx-doctor", "version": "0.1.0",
  "target": "./sample-bad", "qnx_version": "8.0",
  "score": 42, "grade": "D",
  "summary": {"critical": 2, "high": 4, "medium": 4, "low": 2, "info": 0},
  "findings": [
    {"id": "RT-04", "severity": "critical", "file": "src/isr.c", "line": 23,
     "column": 5, "message": "blocking MsgSend() inside ISR handler",
     "code_snippet": "MsgSend(coid, &msg, sizeof(msg), &rpl, sizeof(rpl));",
     "recommendation": "Use InterruptAttachEvent() with SIGEV_INTR and handle in a thread via InterruptWait().",
     "references": ["https://www.qnx.com/developers/docs/8.0/..."]}
  ]
}
```

**SARIF (`--format sarif`):** SARIF 2.1.0 — bisa di-upload ke GitHub Code Scanning (tab Security) → bukti "real engineering" untuk juri.
**HTML (`--format html`):** laporan satu file, grafik skor, daftar finding collapsible — dipakai di video & README.
**Exit code:** `0` bila tidak ada finding ≥ High; `1` bila ada High/Critical (CI gate); `2` bila error tool (path tidak ada, parse gagal).

### 5.3 Daftar file contoh yang harus dibuat

**Repo (publik, lisensi MIT — terdeteksi di About GitHub):**

```
qnx-doctor/
├── LICENSE                      # MIT
├── README.md                    # deskripsi + evidence QNX (file/fungsi/output) + build/run instructions (QNX 8.0, QEMU x86_64, qcc)
├── CONTRIBUTING.md
├── .gitignore
├── pyproject.toml               # Python 3.11+, stdlib-only (tanpa dependensi) — jalan di host Linux tanpa SDP
├── src/qnx_doctor/
│   ├── __init__.py
│   ├── __main__.py              # CLI: check / init / explain / report
│   ├── cli.py
│   ├── rules.py                 # definisi 22 checks (id, severity, pola, rekomendasi, referensi docs)
│   ├── c_parser.py              # tokenizer/parser C ringan (tanpa libclang — stdlib only)
│   ├── buildfile_parser.py      # parser buildfile mkifs ([attributes], .bootstrap, [+script])
│   ├── analyzer.py              # orkestrasi: thread RT detection → aturan RT; buildfile → BF; API → QX
│   ├── reporters.py             # terminal / json / sarif / html
│   └── qemu.py                  # (opsional) wrapper mkifs+qcc+QEMU bila SDP tersedia
├── tests/
│   ├── test_rules.py
│   ├── test_buildfile_parser.py
│   └── fixtures/
│       ├── bad/                 # proyek contoh BERBUG (12+ finding)
│       │   ├── src/isr_bad.c        # RT-04: MsgSend di ISR
│       │   ├── src/mutex_bad.c      # RT-02: mutex tanpa PI
│       │   ├── src/thread_bad.c     # RT-03/RT-11: tanpa EXPLICIT_SCHED, prio 0
│       │   ├── src/heap_bad.c       # RT-01/RT-05: malloc di loop RT
│       │   └── image_bad.build      # BF-01..BF-05
│       └── good/                # proyek contoh BENAR (0 finding, skor 100)
│           ├── src/isr_good.c
│           ├── src/mutex_good.c
│           ├── src/thread_good.c
│           ├── src/heap_good.c
│           └── image_good.build
├── examples/
│   ├── probe.c                  # program QNX nyata (qcc, qnx.target.x86_64): uname + CLOCK_MONOTONIC + checksum — untuk boot QEMU
│   └── probe.build              # buildfile x86_64 multiboot (pola FTBU #2)
├── docs/
│   ├── CODELAB.md               # codelab bonus: "Audit your first QNX project with QNX Doctor" (untuk Best Codelab/Tutorial)
│   ├── RULES.md                 # dokumentasi semua 22 checks + contoh benar/salah
│   └── ARCHITECTURE.md
├── .github/workflows/ci.yml     # CI: jalankan qnx-doctor pada fixtures (bad harus FAIL, good harus PASS) + SARIF upload
├── demo/
│   └── demo.sh                  # skrip demo terminal untuk video
└── video/
    └── SCRIPT.md                # naskah video < 3 menit
```

**File kunci yang harus ada sebelum submit (checklist build):**

- [ ] `src/qnx_doctor/` lengkap + `qnx-doctor check` jalan di Linux tanpa SDP (stdlib-only).
- [ ] `tests/fixtures/bad/` menghasilkan ≥ 12 findings (termasuk 2 Critical) & `tests/fixtures/good/` skor 100.
- [ ] `examples/probe.c` + `probe.build` — cross-compile `qcc -V gcc_ntox86_64`, `mkifs`, boot QEMU, serial assert (bila SDP sudah didapat; bila belum, tandai sebagai "validated after SDP" — JANGAN klaim sudah divalidasi).
- [ ] `docs/CODELAB.md` — codelab lengkap (untuk bonus $3.500).
- [ ] `README.md` — build/run instructions: QNX 8.0, target QEMU x86_64, toolchain qcc; evidence QNX: daftar file/fungsi.
- [ ] Video YouTube publik < 3 menit (naskah di `video/SCRIPT.md`).
- [ ] Repo publik + LICENSE MIT + CI hijau + SARIF ter-upload.

### 5.4 Strategi bonus

- **Best use of QNX-specific Technologies ($3.500):** tekankan di README + deskripsi Devpost: aturan QX-01..QX-05 (message passing, resource manager, PPS, buildfile/startup, RT services) + parser buildfile mkifs + validasi QEMU. Ini "unique capabilities of the QNX platform" persis seperti yang disebut Rules §6.
- **Best Codelab / Tutorial ($3.500):** `docs/CODELAB.md` (atau dipublish sebagai halaman GitHub Pages) — "Audit your first QNX project with QNX Doctor": langkah 1) install SDP 8.0 via QNX Everywhere, 2) buat proyek contoh, 3) jalankan qnx-doctor, 4) perbaiki tiap finding, 5) boot di QEMU & lihat skor naik. Codelab **tidak wajib** berhubungan dengan proyek — tapi di sini berhubungan, makin kuat. Isi field URL codelab di form submit.
- **Community Choice:** promosikan submission setelah 15 Jan 2027 (voting) — jangan manipulasi vote.

### 5.5 Kompetitor langsung — QNX Bootlab (sudah submit di Devpost)

- Proyek: **QNX Bootlab** — https://devpost.com/software/qnx-bootlab — dipublish **6 Nov 2026**.
- Konsep: one-command "cross-compile → rebuild image → boot QEMU → check serial console": `bootlab doctor`, `bootlab new/build/up`; Python stdlib; memakai `qcc`, `mkqnximage`, `qemu-system-x86_64`; contoh `probe.c`.
- **Diferensiasi QNX Doctor (wajib ditegaskan di deskripsi):**
  1. Bootlab = **build & boot orchestration** (apakah image jalan); QNX Doctor = **static audit kesehatan RT & QNX-spesifik** (apakah kode BENAR secara real-time) — komplementer, bukan duplikat.
  2. QNX Doctor **tidak butuh SDP/QEMU untuk jalan** (analisis statis murni) → bisa dipakai di CI mana pun, bahkan sebelum SDP terinstal.
  3. 22 aturan grounded (RT + buildfile + API QNX), output SARIF/HTML, skor 0–100 — Bootlab tidak punya.
  4. Codelab + fixture bad/good sebagai materi edukasi.
- Risiko: juri bisa menganggap keduanya "tooling QEMU". Mitigasi: demo video QNX Doctor fokus pada **finding audit + fix**, bukan pada boot QEMU; sebutkan Bootlab sebagai tool komplementer di README (fair, jujur).

### 5.6 Risiko & hal yang belum terverifikasi

| # | Risiko / gap | Dampak | Mitigasi |
|---|---|---|---|
| 1 | **SDP 8.0 belum diunduh** — butuh akun myQNX + verifikasi email Syarip (§2.4) | Aturan belum tervalidasi terhadap header/toolchain asli; `probe.c` belum pernah di-boot di QEMU | Kerjakan engine dari spek publik dulu; validasi QEMU setelah lisensi aktif; JANGAN klaim validasi yang belum dilakukan |
| 2 | `gitlab.com` **terblokir** di environment riset ini (policy) | Sample project GitLab QNX tidak bisa di-fetch di sini | Pakai GitHub QNX, oss.qnx.com, S-CORE, docs.qnx.com; coba GitLab dari browser/VM lain |
| 3 | QEMU aarch64 butuh **custom QEMU** (raspi4b) | Demo aarch64 lebih rumit | Fokus demo di **x86_64** (QEMU bawaan + KVM/TCG) — sudah cukup untuk Rules |
| 4 | Video < 3 menit harus menunjukkan proyek berfungsi | Butuh rekaman terminal + (bila ada) boot QEMU | Rekam `qnx-doctor check` pada fixture bad→good; bila QEMU belum ada, tunjukkan audit + SARIF/HTML report sebagai bukti fungsi |
| 5 | Pemenang non-AS kena **W-8BEN + withholding** | Hadiah bersih < nominal | Catat di planning; siapkan data bank & dokumen saat menang (§2.4 #5) |
| 6 | Deadline 16 Des 2026 02:00 WIB — ~29 hari dari riset ini | Waktu ketat bila SDP lambat | Jalur kritis: myQNX (Syarip, hari ini) → engine (agen) → fixture → codelab → video → submit 2–3 hari sebelum deadline |

---

## 6. Checklist submit (ringkas — salin ke tracking)

- [ ] Akun myQNX dibuat + email terverifikasi (Syarip — §2.4)
- [ ] Lisensi QNX Everywhere muncul di profil myQNX (tunggu ≤ 1 jam)
- [ ] (Opsional tapi kuat) SDP 8.0 terinstal; `qcc -V gcc_ntox86_64` jalan; `mkifs` + QEMU boot probe berhasil
- [ ] Repo GitHub publik `qnx-doctor` + LICENSE MIT terdeteksi di About
- [ ] Engine 22 checks + fixtures bad/good + CI hijau + SARIF
- [ ] `docs/CODELAB.md` selesai (bonus Codelab)
- [ ] README: build/run instructions (QNX 8.0, QEMU x86_64, qcc) + evidence QNX
- [ ] Video YouTube publik < 3 menit
- [ ] Daftar Devpost (Join Hackathon) + isi form: repo URL, deskripsi (EN), video URL, kategori **Developer Tooling & Host Tools**, URL codelab
- [ ] Submit **sebelum 16 Des 2026 02:00 WIB** (target internal: 13 Des 2026)
- [ ] (Bila menang) affidavit + W-8BEN + data bank dalam 10 hari kerja

---

## 7. Sumber (semua URL diverifikasi dibaca 17 Nov 2026)

**Hackathon & Rules**
- https://qnx.devpost.com/ — halaman utama (prize, kategori, judging criteria)
- https://qnx.devpost.com/rules — Official Rules lengkap (§1–§15)
- https://devpost.com/software/qnx-bootlab — kompetitor QNX Bootlab (publish 6 Nov 2026)

**QNX Everywhere & akun**
- https://qnx.software — homepage QNX
- https://qnx.software/en/developers/get-started/qnx-everywhere — langkah lisensi gratis, FAQ, komponen (SDP 8.0 / Developer Desktop / Hypervisor)
- https://qnx.software/en/press-release/2026/qnx-everywhere-expands-global-developer-ecosystem-through-education-innovation-and-open-collaboration — statistik program (30K+ lisensi, dsb.)
- http://www.qnx.com/developers/docs/qsc/com.qnx.doc.qsc.user_guide/topic/create_myqnx.html — Create Your myQNX Account (email + confirmation key)
- http://www.qnx.com/developers/docs/qsc/com.qnx.doc.qsc.user_guide/topic/using_license_manager.html — myQNX License Manager
- https://www.qnx.com/developers/docs/8.0/com.qnx.doc.qnxtoolkit.user_guide/topic/licensing.html — aktivasi license key QNX Toolkit

**Dokumentasi SDP 8.0**
- https://www.qnx.com/developers/docs/8.0/ — index dokumentasi SDP 8.0
- https://www.qnx.com/developers/docs/8.0/com.qnx.doc.qnxsdp.quickstart/topic/about.html — QNX SDP 8.0 Quick Start Guide
- https://www.qnx.com/developers/docs/8.0/com.qnx.doc.qnxsdp.quickstart/topic/install_host.html — instalasi host (Windows/Linux x86; tanpa macOS/ARM)
- https://www.qnx.com/developers/docs/8.0/com.qnx.doc.qnxtoolkit.user_guide/topic/quickstart_guide.html — Quickstart Guidelines QNX Toolkit
- https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.prog/topic/devel_SELFORCROSS.html — Cross-development (qcc -V gcc_ntoaarch64le)
- https://www.qnx.com/developers/docs/7.1/com.qnx.doc.neutrino.utilities/topic/m/mkqnximage.html — mkqnximage
- https://www.qnx.com/developers/docs/BSP8.0/com.qnx.doc.bsp_x86_64.generic_8.0/topic/build_commandline.html — build BSP generic x86_64 (make, .build, disk_image)
- https://www.qnx.com/developers/docs/BSP8.0/com.qnx.doc.bsp_raspberrypi.bcm2712.rpi5_8.0/topic/build_ifs_uboot.html — build IFS RPi 5 + boot U-Boot
- https://www.qnx.com/developers/docs/7.1/com.qnx.doc.neutrino.lib_ref/topic/c/channelcreate.html — ChannelCreate()
- https://www.qnx.com/developers/docs/7.1/com.qnx.doc.neutrino.getting_started/topic/s1_procs_Thread_attributes_scheduling.html — scheduling thread attributes (bug priority 0)
- https://qnx.com/developers/docs/7.1/com.qnx.doc.neutrino.utilities/topic/s/slogger2.html — slogger2 / slog2
- http://www.qnx.com/developers/docs/6.5.0SP1/neutrino/sys_arch/pps.html — PPS
- https://www.qnx.com/developers/docs/6.4.0/neutrino/getting_started/s1_msg.html — Message Passing
- https://www.qnx.com/developers/docs/6.3.0SP3/neutrino/utilities/m/mkifs.html — mkifs (sintaks & atribut)
- https://doc.qt.io/qt-6/building-qt-for-qnx.html — CMake toolchain file QNX (qcc, QNX_TARGET, arch)

**Blog & komunitas**
- https://qnx.software/en/blog/2026/qnxe-ftbu-2 — "QNX From The Board Up #2 — Create a Basic Image" (buildfile x86_64 + QEMU)
- https://www.mikecramer.com/qnx/qnx_6.1_docs/neutrino/sys_arch/kernel.html — Neutrino microkernel (ThreadCtl, SchedSet, IPC)
- https://www.mikecramer.com/qnx/qnx_6.1_docs/neutrino/prog/resmgr.html — Writing a Resource Manager (resmgr_attach, InterruptAttachEvent)
- https://news.ycombinator.com/item?id=42079460 — QNX Everywhere gratis + RPi image (lisensi perpetual, screenwm)

**Repo & tooling publik**
- https://deepwiki.com/eclipse-score/toolchains_qnx/3-qcc-toolchain — QCC toolchain (QNX_HOST/QNX_TARGET, qcc/qpp)
- https://deepwiki.com/eclipse-score/toolchains_qnx/4.2-ifs-build-files — IFS build files (init_x86_64.build)
- https://deepwiki.com/eclipse-score/toolchains_qnx/6-testing-with-qemu — Testing with QEMU (x86_64 KVM, aarch64 custom QEMU + DTB)
- https://oss.qnx.com — Open-source ports dashboard QNX
- https://qnx.github.io — QNX Codelabs

**Tidak berhasil diakses dari environment ini (dicatat, bukan diasumsikan):**
- https://gitlab.com/qnx — **diblokir policy** (browser.open gagal); coba dari browser/VM lain.
- https://info.devpost.com/terms — Terms of Service Devpost (dirujuk Rules §14); isi payout mengikuti Rules §8 yang sudah dibaca penuh.
