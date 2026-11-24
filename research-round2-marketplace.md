# Riset Mendalam The Sandbox — Marketplace Wearables & Spesifikasi Creator
## Persiapan Ronde 2 Wearable & Cosmetic Bounty

**Tanggal riset:** 24 November 2026
**Konteks:** 4 item "Midnight Gold" ronde 1 sudah SUBMIT + DISETUJUI (email Seve Menez, 24 Nov 2026 16:10 WIB). Ukkas diundang ke **Ronde 2** — kirim karya baru via form yang sama, bisa dapat hadiah 2x. Campaign berakhir **30 November 2026** (6 hari lagi).
**Sumber utama:** halaman Luma bounty (dibaca langsung 24 Nov 2026), dokumentasi resmi Sandbox Studio (`studio-docs.sandbox.game`, dibaca langsung), halaman harga resmi, dan halaman Shop sandbox.game (dibaca langsung).

---

## 1. Ringkasan eksekutif

- **Bounty:** pool **$5.000**, **$5 per item pakaian** (Top/Bottom/Footwear) dan **$10 per item Head Accessory** (topi/rambut). Dibayar **SAND di Polygon**. Sistem **first come, first served** — pool bisa habis sebelum 30 Nov.
- **Ronde 2 bukan otomatis:** "Creators whose initial submissions demonstrate strong quality… may be invited to submit another round. Approval for one round does not automatically guarantee eligibility for another." Ukkas sudah mendapat undangan itu — artinya kualitas ronde 1 lolos bar.
- **Dua jalur pembuatan (resmi, dari Luma):**
  - **Pakaian ($5): texture-mapped clothing via Avatar Studio** di dalam Sandbox Studio Editor — pakaian = tekstur 2D, BUKAN mesh 3D.
  - **Topi & rambut ($10): 3D-modeled, via Blender + rigging plugins** — satu-satunya kategori yang berupa mesh 3D.
- **Di luar bounty, ada uang kedua:** item yang sama dijual di Player Marketplace dengan harga **Silicon**. Jendela peluncuran **1 Des 2026 – 1 Mar 2027: komisi 100% = $0,007/Silicon**. Contoh resmi: item 500 Silicon × 200 pembeli = **$700**. Jadi item ronde 2 sebaiknya dipublish **sebelum 1 Des** agar masuk jendela ini.
- **Kesimpulan alat:** yang wajib adalah **Sandbox Studio + Avatar Studio** (pakaian), **Blender + Sandbox Rigify** (topi/rambut 3D), dan **image editor** (tekstur 1024×1024). VoxEdit adalah jalur lama (voxel ASSET) dan **tidak dipakai** untuk bounty ini.

---

## 2. Aturan resmi Wearable & Cosmetic Bounty (Luma, diverifikasi 24 Nov 2026)

Sumber: https://luma.com/0ci3wufr?tk=Dq96pC

| Hal | Detail |
|---|---|
| Periode campaign | **17–30 November 2026** |
| Reward pool | **$5.000**, sampai habis |
| Reward per item | **$5** pakaian (Top/Bottom/Footwear), **$10** Head Accessory (topi, hairstyle, headphone, dll) |
| Batas submit | **1 item per kategori per creator**, maks 4 item ronde 1. Ronde tambahan hanya bila diundang/di-approve |
| Seleksi | First come, first served, **subject to eligibility and quality verification** |
| Pembayaran | Setara USD dibayar **SAND di Polygon**, ke wallet di form |
| Cara ikut | 1) Buat item → 2) Publish di `create.sandbox.game/projects` (lengkapi metadata, harga dalam Silicon) → 3) Isi Google Form (link asset published + alamat wallet Polygon) |
| Harga jual | Dipatok dalam **Silicon**; panduan harga: https://studio-docs.sandbox.game/monetization/recommended-list-prices |

**Syarat item (harus dipenuhi semua):**
- Orisinal — bukan karya orang lain / bukan aset yang sudah ada.
- Kategori eligible (Top / Bottom / Footwear / Head Accessory).
- Fungsional: tekstur benar, posisi benar, rigging benar bila ada; tanpa masalah visual/teknis besar.
- Standar kualitas: kreativitas, effort, dan kualitas visual yang memadai.
- Kompatibel dengan sistem avatar Sandbox.
- Tim Sandbox secara khusus mendorong **topi dan hairstyle 3D** ("Creators are especially encouraged to explore 3D-modeled hats and hairstyles").

**Yang DILARANG (diskualifikasi):**
- Low-effort, tidak selesai, kualitas buruk.
- Aset rusak, texture mapping salah, rigging salah.
- **Duplikat atau variasi minor dari aset yang sama** untuk melipatgandakan reward — ronde 2 harus benar-benar karya baru, bukan "Midnight Gold v2" dengan ganti warna.
- Menyalin karya creator lain / melanggar IP pihak ketiga.
- Submit >1 item per kategori tanpa approval ronde tambahan.
- **Mengedit form yang sudah disubmit = diskualifikasi** (apapun alasannya); kalau perlu ubah, submit entri baru.
- **Tidak boleh mengedit aset setelah submit.**
- Multi-account untuk mengakali batas = diskualifikasi / ban permanen.
- "Submissions do not guarantee rewards" — semua tunduk pada review dan approval akhir tim Sandbox.

**Ronde 2 (dari Luma):** "Additional submission rounds: Creators whose initial submissions demonstrate strong quality and meet the bounty requirements may be invited to submit another round of items. Additional rounds are subject to The Sandbox team's approval and remaining reward availability."

---

## 3. Marketplace: apa yang laris & berapa harganya

### 3.1 Dua marketplace — lama (SAND) vs baru (Silicon)

- **Marketplace lama (NFT, ERC-1155, bayar SAND):** aset dan LAND diperdagangkan sebagai NFT di Ethereum/Polygon. Halaman `sandbox.game/en/marketplace/` saat ini sudah mengarah ke landing page Sandbox Studio — marketplace lama sedang digantikan.
- **Player Marketplace baru:** meluncur bersama **Sandbox Studio pada 1 Desember 2026**. Item avatar/kosmetik dijual dengan **Silicon** (mata uang platform; pemain beli Silicon, sebagian dengan SAND + bonus 10%). Semua item bounty ronde 1/2 akan tampil di sini ("Your items will be visible on the Player Marketplace when our new platform goes live").

### 3.2 Harga nyata di Shop lama (dibaca langsung 24 Nov 2026, sandbox.game)

Contoh item wearable/avatar yang masih terdaftar (harga SAND; 1 SAND ≈ **$0,033** per 24 Nov 2026):

| Item | Harga | Catatan |
|---|---|---|
| Sandness Police Wearable Tactical Vest | 25 SAND ($0,83) | wearable vest |
| Police Dog Bruce – Off duty | 25 SAND ($0,83) | avatar |
| Police Dog Bruce – On duty | 50 SAND ($1,65) | avatar |
| Detective Sergeant Julius Anguilla – Tactical Police Harness | 50 SAND ($1,65) | harness |
| Police Constable Chive – Roads and Traffic Duties | 100 SAND ($3,31) | avatar |
| Police Constable Pelican – Traffic Duties | 100 SAND ($3,31) | avatar |
| Police Constable Pelican – Response Duties | 500 SAND ($16,55) | avatar |
| PC Big Paul – response duties | 500 SAND ($16,55) | avatar |
| meta red hat / meta blue hat | 5 SAND ($0,17) | topi sederhana |
| Police Man | 7,5 SAND ($0,25) | avatar |
| Sandness Police Extendable Baton | 5 SAND ($0,17) | aksesori |

**Pola harga:** wearable satuan 5–100 SAND; avatar lengkap 25–500 SAND. Topi sederhana hanya 5 SAND — topi polos tanpa detail **tidak laku mahal**. Item yang mahal adalah **karakter lengkap / set bertema kuat** (polisi, 100–500 SAND).

### 3.3 Harga resmi yang direkomendasikan (Silicon) — studio-docs, diverifikasi 17 Nov 2026

Sumber: https://studio-docs.sandbox.game/monetization/recommended-list-prices

| Item | Floor (Si) | Typical (Si) | Premium (Si) |
|---|---|---|---|
| Character / full avatar | 100 | 250–800 | 2.500 |
| Tops / Bottoms / Footwear: **Texture** | 10 | **25–100** | 200 |
| Tops / Bottoms / Footwear: **Mesh** (coming soon) | 10 | 75–250 | 400 |
| Body: Head | 10 | 100–250 | 500 |
| Body: full set | 50 | 250–600 | 1.000 |
| **Accessory: Head** | 10 | **80–250** | 400 |
| Accessory: Face | 10 | 75–200 | 350 |
| Accessory: Back | 10 | 125–350 | 600 |
| Accessory: Neck / Shoulders / Waist | 10 | 60–150 | 250 |

Catatan resmi: "Mesh tops, bottoms, and footwear are Coming soon" — saat ini pakaian mesh belum tersedia; pakaian = tekstur.

### 3.4 Contoh nyata dari bounty yang sama

- **"The Surveyor Set"** (creator @blocknbull, dipost 20 Nov 2026): Surveyor Field Jacket, Parcel Cargo Pants, Waypoint Runners, Surveyor Hard Hat — satu set bertema utuh (jaket lapangan + celana kargo + sepatu + helm), dipublish **100 Silicon per item**. Proses: tekstur dilukis di Studio; mesh helm dibuat dengan Python. Ini contoh pesaing langsung di bounty yang sama — set bertema + harga 100 Si.
  Sumber: https://www.instagram.com/p/Df9WIWNISHC/
- **Community Avatar Design Contest** (Feb 2026): 100+ submission, 10 pemenang, tiap avatar edisi 250, harga **29 SAND** (~$2,40). Bukti: desain komunitas orisinal yang rapi bisa terjual sebagai edisi terbatas.
- **Koleksi brand:** Atari, Bruce Lee, Terminator, Black Mirror, Steve Aoki, Snoop Dogg — IP besar mendominasi harga tertinggi, tapi **dilarang** untuk bounty (IP pihak ketiga = diskualifikasi). Pelajaran: tiru **kualitas dan kohesi temanya**, bukan IP-nya.

### 3.5 Uang di luar bounty — komisi Silicon (penting!)

Sumber: https://studio-docs.sandbox.game/monetization/silicon-and-creator-earnings.md

- **Jendela peluncuran 1 Des 2026 – 1 Mar 2027:** komisi **100% dari Silicon yang dibelanjakan pemain, $0,007 per Silicon** (untuk avatar cosmetics dan in-game purchases). Berlaku untuk $1 juta komisi pertama lintas semua creator.
- **Tarif standar dari 1 Mar 2027:** avatar cosmetics **50%**, $0,005 per Silicon.
- Contoh resmi: item 500 Si × 200 pembeli = 100.000 Si → **$700**.
- Komisi clear **30 hari** setelah penjualan (**60 hari** untuk creator baru); payout minimal **$100** komisi yang sudah clear; dibayar fiat via **Tipalti** (transfer bank dll); perlu verifikasi identitas + info pajak.
- Pemain yang beli Silicon pakai SAND dapat **bonus 10% Silicon** — bonus itu ikut dihitung ke komisimu.
- **Implikasi:** publish item ronde 2 **sebelum 1 Des 2026** agar mendapat tarif penuh $0,007/Si selama mungkin. Harga 100 Si (seperti Surveyor Set) = $0,70 per penjualan di jendela peluncuran.

---

## 4. Spesifikasi resmi pembuatan wearable

### 4.1 Pakaian — Avatar Studio "Paint Skin" (tekstur 2D, bukan mesh)

Sumber: https://studio-docs.sandbox.game/avatars/how-to-paint-avatar-clothing.md

- **Skin = satu set tekstur 2D pakaian:** Top + Bottom + Shoes. File kerja `.avatar-skin.json` di `assets/avatars/`.
- **Cara buka:** menu hamburger → **Avatar Studio… → Paint Skin** → isi Skin Name → Create.
- **Template (pilih kombinasi lengan + celana):**

| Outfit | Jumlah part |
|---|---|
| Long Sleeves, Short Pants | 8 |
| Long Sleeves, Long Pants | 8 |
| Short Sleeves, Short Pants | 6 |
| Short Sleeves, Long Pants | 6 |

- **Layout tekstur (kritis — ini yang paling sering salah):**
  - **Top:** bagian **depan baju = setengah ATAS** tekstur; **belakang = setengah BAWAH**.
  - **Bottom:** **depan = setengah KIRI**; **belakang = setengah KANAN**.
  - **Shoes:** satu tekstur berisi kedua sepatu + sol; bentuk sepatu **atas = sepatu kanan**, **bawah = sepatu kiri**; sol adalah island terpisah.
- **Alur kerja:** pilih garment (Top/Bottom/Shoes) → **Open Folder for Live Editing** → edit file tekstur di image editor → save menimpa file → Avatar Studio menampilkan perubahan **live** di avatar. `Reset to Original` menghapus semua paint.
- **Hanya garment yang dilukis yang diekspor.** Export menghasilkan folder berisi tekstur + material garment yang dilukis.
- **Ronde 1 ukkas memakai cara ini:** Top/Bottom/Footwear berupa PNG **1024×1024** (lihat `~/workspace/sandbox-hat/set/`). Template alignment direkonstruksi dari screenshot docs resmi — bukan byte-exact; layout sepatu paling tidak pasti. **Selalu cek live preview di Avatar Studio sebelum export.**
- **Keterbatasan:** pakaian tekstur **tidak bisa beranimasi sendiri** dan tidak mengubah siluet — spektakulernya harus datang dari kualitas lukisan tekstur (shading, highlight, detail kain, bordir, pola).

### 4.2 Head Accessory / topi & rambut — mesh 3D via Blender (satu-satunya kategori 3D)

Sumber: https://studio-docs.sandbox.game/avatars/how-to-create-an-avatar-accessory.md

- **Aksesori = satu mesh 3D pada SATU socket.** Topi memakai socket **Hat**. Aksesori mengikuti tulang itu **sebagai satu kesatuan kaku — tidak menekuk mengikuti badan**.
- **Siapkan mesh di Blender / Maya / tool 3D lain. Export SATU file `.glb`, dalam satuan meter, semua transform di-apply (di Maya: freeze transformations). Origin diletakkan di titik attachment (untuk topi = puncak kepala). Hapus Armature modifier. Cek posisi terhadap socket dengan Sandbox Rigify sebelum import.**
- **Import checks di Avatar Studio** (otomatis): mesh ada, **rigid** (mesh ber-skin/ber-armature **memblokir export**), ukuran, jarak dari socket, socket tersedia di avatar, dan **triangle count**.
  - Yang memblokir export: mesh hilang, atau mesh ber-skin (skinned mesh).
  - Masalah lain dilaporkan beserta cara memperbaikinya.
- **Adjust (opsional):** geser/putar/skala dengan gizmo atau ketik angka; avatar dalam pose rest saat langkah ini. `Reset to the Imported Origin` mengembalikan ke origin .glb. File `.glb` baru yang di-drop akan **mempertahankan placement** yang sudah diatur.
- **Export:** nama aksesori → **Export Accessory…** → placement tertulis ke dalam `.glb`. Hasil: folder berisi **item pack recipe + .glb**. File kerja `.avatar-accessory.json` di `assets/avatars/`.
- **Ronde 1 ukkas:** fedora Blender `.glb`, **1.602 tris**, satu rigid mesh, Hat socket, tanpa skin/animasi (`~/workspace/sandbox-hat/sandbox-fedora.glb`, dibuat `build_fedora.py`).
- **Keterbatasan:** aksesori **rigid** — tidak ada animasi per-aksesori (tidak ada kain berkibar, rambut bergerak, dll). Spektakulernya datang dari **siluet, detail geometri, dan material**.

### 4.3 Avatar lengkap (konteks — kalau mau naik level ke full character)

Sumber: https://studio-docs.sandbox.game/avatars/how-to-create-an-avatar.md

- Rig karakter di Blender dengan **Sandbox Rigify add-on** sebelum mulai. Export satu `.glb` untuk seluruh karakter, atau **Export Parts** (satu `.glb` per body slot).
- **15 slot tubuh:** `Head`, `UpperTorso`, `LowerTorso`, `Left/RightUpperArm`, `Left/RightLowerArm`, `Left/RightHand`, `Left/RightUpperLeg`, `Left/RightLowerLeg`, `Left/RightFoot`.
- **Validate:** cek body parts, skinned meshes, Sandbox rig, finger bones, ukuran, wajah, dan socket **Hat**. `Try Expressions` memutar **Neutral, Happy, Sad, Angry, Blink** (contoh di docs: 53 dari 53 face expressions).
- **Surfaces (mapping material):** Body, T-Shirt, Sleeves, Shorts, Legs, Shoes (6 of 6 mapped). **Template** menyimpan layout UV platform sebagai PNG untuk di-unwrap.
- **Try On:** preview outfit + aksesori (mis. headphone di socket Hat). Preview ini **tidak memindahkan socket** — socket dipindah di Sandbox Rigify lalu export ulang.
- Export: folder `parts/` (15 `.glb`) + `recipes/` (parts recipe JSON). Harga jual tipikal full avatar **250–800 Silicon** (premium 2.500).

### 4.4 Animasi — apa yang bisa dan tidak bisa

- **Pakaian (tekstur):** tidak beranimasi. Mengikuti animasi avatar (jalan, lari, idle) karena menempel pada rig, tapi tidak punya gerakan sendiri.
- **Aksesori (mesh):** rigid, mengikuti satu bone/socket. Tidak menekuk, tidak berkibar.
- **Avatar/karakter:** BISA beranimasi — file `.glb` berisi bones + clips; klip bisa dari file yang sama atau `.glb` lain; ada **skeleton profile** (`.skeleton-profile.json`: bone name → role seperti `Hips`, `RightHand`; `hipBoneName` wajib untuk root-motion) dan **animation config** (`.animconfig.json`: states, transitions) yang digerakkan **Animation State Machine Node**. Klip in-place (kaki bersepeda, pinggul diam) lebih aman daripada root-motion. Sumber: https://studio-docs.sandbox.game/the-editor/how-to-import-a-rigged-character-and-animation-clips.md
- **Implikasi untuk bounty:** jangan menjanjikan/mengharapkan animasi pada pakaian/topi. "Spektakuler" di kategori ini = **detail visual statis + kesesuaian gerak avatar**.

### 4.5 Jalur lama — VoxEdit (voxel ASSET, BUKAN untuk bounty ini)

- VoxEdit (gratis, Windows/Mac) untuk membuat aset voxel NFT (ERC-1155) di marketplace lama: model → rig → animasi → mint.
- **Batas teknis resmi (kontes VoxEdit):** maks **5.000 faces**, maks **175 nodes**, tinggi maks **512 voxel (16 meter)**, floor print maks **512 × 512 × 512** (termasuk animasi). Format submit: **.vox** (+ .qb di beberapa kontes).
- **Equipment template** (topi, kacamata, masker, baju, celana, sepatu) wajib dipakai agar wearable pas di tubuh avatar; ada batas polygon dan ukuran/orientasi per body part.
- **Kriteria juri kontes VoxEdit (bobot):** Creativity 20% / Usability 40% / Optimisation 20% / Aesthetics 20%. Usability paling berat — aset harus bekerja di banyak game/scene, skala adaptif, collider bagus.
- **Catatan:** bounty Wearable & Cosmetic memakai **Avatar Studio + Blender**, bukan VoxEdit. VoxEdit relevan hanya bila ukkas mau membuat aset voxel klasik terpisah (mis. untuk dijual sebagai ASSET NFT di marketplace lama).

---

## 5. Tools & skill spesifik yang dibutuhkan

| # | Tool / skill | Fungsi spesifik | Untuk kategori | Status / catatan |
|---|---|---|---|---|
| 1 | **Sandbox Studio** (baru, beta 2026; launch publik 1 Des 2026) + **Avatar Studio** di dalamnya | Paint Skin (pakaian), Create Accessory (topi), Create Avatar; publish via Creator Hub | Semua | **Wajib.** Update engine 20 Nov 2026 "unblocks the creation of Avatar cosmetics". Target Unity/Unreal devs; AI-native. |
| 2 | **Blender** (+ **Sandbox Rigify** add-on) | Model topi/rambut 3D; rig karakter; cek posisi vs socket; export `.glb` meter, transforms applied, tanpa Armature modifier | Head Accessory ($10), full avatar | **Wajib untuk $10.** Sandbox Rigify = add-on khusus Sandbox (bukan stock Rigify Blender); dipakai untuk cek socket & rig sesuai docs. |
| 3 | **Image editor** (Photoshop / GIMP / Krita) — atau Python PIL | Lukis tekstur 1024×1024 (Top/Bottom/Shoes) sesuai layout depan/belakang; shading, pola kain, bordir, efek emas | Top/Bottom/Footwear ($5) | **Wajib.** Kualitas lukisan = satu-satunya pembeda di kategori pakaian. |
| 4 | **Creator Hub** (`create.sandbox.game/projects`) | Publish item, lengkapi metadata, patok harga Silicon | Semua | **Wajib.** Item tampil di Player Marketplace saat platform baru live. |
| 5 | **Meshy AI** (terintegrasi di Studio) | Generate mesh 3D bertekstur dari teks/gambar; export FBX/OBJ → bersihkan di Blender → `.glb` | Head Accessory (akselerator) | Opsional, mempercepat. Wajib QC: origin, skala meter, triangle count, rigid. |
| 6 | **Python** (Blender scripting / PIL) | Build prosedural (contoh ronde 1: `build_fedora.py`; pesaing Surveyor Set: mesh helm dibuat dengan Python); batch texture | Head Accessory, tekstur | Opsional, sudah terbukti di ronde 1. |
| 7 | **VoxEdit** | Aset voxel klasik (.vox), rig + animasi voxel | Bukan bounty ini | Legacy — hanya bila mau jual ASSET NFT terpisah. Batas: 5.000 faces / 175 nodes / 512 voxel. |
| 8 | **Google Form** (link di Luma) + **wallet Polygon** | Submit entri: link asset published + alamat wallet | Semua | **Wajib.** Satu form per pengajuan; edit form = diskualifikasi. |

**Yang TIDAK dibutuhkan:** Game Maker (untuk game, bukan wearable), LAND, Catalyst/Gem (untuk ASSET NFT lama), KYC (hanya untuk pemenang top-3 kontes VoxEdit tertentu — tidak disebut di bounty ini).

---

## 6. Standar kualitas — biasa vs spektakuler

### 6.1 Apa yang dinilai (dari aturan bounty + kriteria juri Sandbox)

- **Orisinalitas:** tema/konsep sendiri, bukan tiruan, bukan IP orang lain.
- **Usability (bobot terbesar di kontes Sandbox, 40%):** pas di avatar, tidak clipping, socket benar, bekerja di semua pose/animasi avatar.
- **Optimasi (20%):** face/triangle count efisien, tekstur rapi.
- **Estetika (20%):** geometri, proporsi, palet warna, tekstur, level detail.
- **Kreativitas (20%):** tema, storytelling, kohesi set.
- **Kelengkapan:** depan DAN belakang dirancang (banyak submission hanya bagus dari depan; back adalah pembeda mudah).

### 6.2 Ciri item biasa vs spektakuler (di kategori ini)

| Aspek | Biasa (lolos minimal) | Spektakuler (menonjol) |
|---|---|---|
| Topi (3D) | Bentuk dasar, satu warna, polos | Siluet khas + detail geometri berlapis (pita, emblem, aksen logam), material kontras (matte vs metallic gold) |
| Top (tekstur) | Warna datar, tanpa shading | Shading + highlight, tekstur kain (weave/denim/kulit), bordir/pola, kancing/saku/resleting digambar, desain belakang |
| Bottom (tekstur) | Celana polos | Lipatan kain, saku, sabuk, gradasi warna, pola konsisten dengan top |
| Footwear (tekstur) | Sepatu satu warna | Sol kontras, tali/gesper, highlight kulit, logo kecil |
| Set | 4 item tidak nyambung | **Satu tema kuat, palet konsisten, terasa satu outfit** (contoh: Surveyor Set, Sandness Police) |
| Presentasi | Screenshot seadanya | Preview depan + belakang + dipakai avatar (seperti carousel Surveyor Set) |

### 6.3 Harga sebagai sinyal kualitas

- Topi polos (meta red/blue hat): **5 SAND** — harga terendah, jangan ditiru.
- Wearable vest tematik: **25 SAND**; avatar tematik lengkap: **100–500 SAND**.
- Panduan resmi Silicon: aksesori kepala tipikal **80–250 Si** (premium 400); tekstur pakaian tipikal **25–100 Si** (premium 200). Item spektakuler dipatok di ujung atas Typical — bukan Floor.
- "The Surveyor Set" mematok **100 Si per item** — patokan realistis untuk ronde 2.

---

## 7. Rencana ronde 2 — rekomendasi konkret

### 7.1 Prinsip

1. **Tema baru total** — bukan variasi Midnight Gold (duplikat/variasi minor = diskualifikasi). Satu tema kuat untuk keempat item.
2. **Hero piece = Head Accessory ($10):** satu-satunya kategori 3D — di sinilah geometri bisa "wow". Alokasikan effort terbesar ke sini.
3. **Pakaian = lukisan tekstur terbaik:** 1024×1024, shading + detail kain + desain belakang. Palet konsisten dengan topi.
4. **Publish sebelum 1 Des 2026** → masuk jendela komisi $0,007/Si. Harga **100 Silicon/item** (dalam Typical untuk semua kategori).
5. **Submit secepatnya** — FCFS + pool $5.000 bisa habis; jangan over-polish sampai kehabisan slot.

### 7.2 Opsi tema (pilih satu)

**Opsi A — "Neon Ronin" (cyber-samurai):** Top: kimono/jaket hitam + neon cyan circuit; Bottom: hakama gelap + neon trim; Footwear: boots hitam + sol neon; Head: kabuto/helm samurai 3D dengan tanduk + aksen neon. Kontras gelap-neon sangat terbaca di voxel world.

**Opsi B — "Arctic Explorer":** Top: parka putih/biru es + bulu; Bottom: celana cargo salju; Footwear: boots salju cokelat; Head: ushanka/topi bulu 3D atau helm es. Palet dingin, tekstur bulu lewat shading.

**Opsi C — "Royal Peacock" (emas-hijau mewah):** Top: jas brokat emas-hijau; Bottom: celana formal emas; Footwear: sepatu formal mengkilap; Head: mahkota/topi formal 3D dengan bulu merak. Lanjutan natural dari Midnight Gold tapi tema dan bentuk berbeda total — hati-hati tetap terasa baru, bukan variasi.

### 7.3 Checklist QC sebelum submit (wajib)

- [ ] Live preview di Avatar Studio: depan, belakang, samping — **tidak ada clipping** ke tubuh avatar.
- [ ] Topi: origin di puncak kepala, socket Hat, rigid, triangle count lolos checks.
- [ ] Tekstur: depan/belakang tidak tertukar (Top: depan=atas; Bottom: depan=kiri; Shoes: atas=kanan).
- [ ] Keempat item satu palet/tema; nama + metadata lengkap.
- [ ] Publish di Creator Hub → harga **100 Silicon** → salin link asset.
- [ ] Isi Google Form (link + wallet Polygon) → **jangan edit form atau aset setelah submit**.
- [ ] Submit sebelum 30 Nov 2026, idealnya sebelum 1 Des untuk jendela komisi.

### 7.4 Risiko

- **Pool habis duluan (FCFS):** submit cepat lebih penting daripada sempurna.
- **Diskualifikasi karena edit:** setelah submit, jangan sentuh aset/form.
- **Duplikat:** jangan kirim variasi Midnight Gold.
- **IP:** jangan pakai logo/karakter pihak ketiga.
- **Kualitas:** tim Sandbox me-review tiap item; low-effort = ditolak tanpa reward.

---

## 8. Sumber

- Bounty (Luma, dibaca 24 Nov 2026): https://luma.com/0ci3wufr?tk=Dq96pC
- Harga resmi (Silicon): https://studio-docs.sandbox.game/monetization/recommended-list-prices
- Komisi & earnings: https://studio-docs.sandbox.game/monetization/silicon-and-creator-earnings.md
- Paint avatar clothing: https://studio-docs.sandbox.game/avatars/how-to-paint-avatar-clothing.md
- Create avatar accessory: https://studio-docs.sandbox.game/avatars/how-to-create-an-avatar-accessory.md
- Create avatar: https://studio-docs.sandbox.game/avatars/how-to-create-an-avatar.md
- Import rigged character & animasi: https://studio-docs.sandbox.game/the-editor/how-to-import-a-rigged-character-and-animation-clips.md
- Indeks docs: https://studio-docs.sandbox.game/llms.txt
- Creator Hub: https://create.sandbox.game/projects
- Contoh Shop (harga SAND): https://www.sandbox.game/tr/assets/sandness-police-wearable-custodian-hat/0c193466-80b1-4735-b578-f3ea7693675e/
- Contoh pesaing "The Surveyor Set": https://www.instagram.com/p/Df9WIWNISHC/
- Studio launch 1 Des 2026: https://www.tradingview.com/news/coinmarketcal:b639625d7094b:0-the-sandbox-the-sandbox-studio-launches-01-dec-2026/
- Tutorial wearables VoxEdit: https://nftartonmeta.com/nft-wearables-on-voxedit/
- SAND ≈ $0,033 (24 Nov 2026, Bybit/OKX)

*Catatan: halaman marketplace lama (`sandbox.game/en/marketplace/`) saat ini mengarah ke landing Sandbox Studio — marketplace lama sedang digantikan Player Marketplace baru yang live 1 Des 2026. Harga SAND di atas diambil dari halaman Shop (masih live). Link download Sandbox Rigify tidak ditemukan di docs publik — add-on dirujuk di docs resmi sebagai bagian alur Avatar Studio; verifikasi di dalam Studio saat mulai bekerja.*
