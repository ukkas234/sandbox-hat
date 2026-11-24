# Riset Ronde 2 — Audit Aset Ronde 1 + Gap Tooling Sandbox

**Tanggal:** 24 November 2026
**Status:** audit + rencana saja. Tidak ada tool yang di-install, tidak ada aset yang diubah.
**Konteks:** 4 item "Midnight Gold" ronde 1 disetujui, ukkas diundang ke ronde 2. Deadline campaign: **30 November 2026** (±6 hari lagi). Target ronde 2: karya yang lebih bagus dan spektakuler.

---

## 1. Ringkasan eksekutif

- Ronde 1 **bukan karya voxel**. Fedora dibuat sebagai mesh halus di Blender; pakaian dibuat sebagai tekstur 2D prosedural (PIL + numpy), bukan model 3D. Tidak ada satu pun file `.vox`/`.vxr` di repo.
- **Temuan audit terpenting:** jumlah segitiga fedora yang sebenarnya adalah **3.196 tris, bukan 1.602** seperti tertulis di README (angka 1.602 menghitung poligon Blender sebelum triangulasi; hasil export GLB yang terukur = 3.196). Masih aman untuk ukuran aksesori, tapi ini menunjukkan tidak ada audit GLB independen sebelum submit.
- **Tool kunci yang hilang di VM:** VoxEdit, MagicaVoxel, Goxel, trimesh, pygltflib, gltf-transform, Sandbox Studio/Avatar Studio/Game Maker. Blender 5.3.0 + Python (PIL/numpy) + Node sudah ada dan cukup untuk sebagian pekerjaan.
- **Batasan struktural:** validasi dan publish final HANYA bisa dari aplikasi desktop Sandbox Studio di laptop Windows ukkas. VM hanya bisa menyiapkan aset + audit lokal.

---

## 2. Audit aset ronde 1

Lokasi: `~/workspace/sandbox-hat/` (total 15 MB, repo: `ukkas234/sandbox-hat`).

### 2.1 Inventaris file

| File | Format | Ukuran | Isi (terverifikasi) |
|---|---|---|---|
| `sandbox-fedora.glb` | glTF 2.0 binary | 179.164 byte | Aksesori kepala. 1 mesh (`CrownMesh`), 2 primitif, 2 material (`CharcoalFelt`, `GoldBand`), 1 node, **0 skin, 0 animasi**. Bounds X/Z ±0,19 m, Y 0–0,13 m. Generator: Khronos glTF Blender I/O v5.3.43. **Segitiga terukur: 3.196** |
| `set/sandbox-top.png` | PNG RGB 1024×1024 | 434.589 byte | Tekstur Top (Tailored Coat). Coverage non-hitam terukur **47,1%** |
| `set/sandbox-bottom.png` | PNG RGB 1024×1024 | 885.133 byte | Tekstur Bottom (Tailored Trousers). Coverage terukur **84,8%** |
| `set/sandbox-footwear.png` | PNG RGB 1024×1024 | 282.953 byte | Tekstur Footwear v1 (Dress Boots). Coverage terukur **45,6%** |
| `set/sandbox-footwear-v2.png` | PNG RGB 1024×1024 | 293.115 byte | Tekstur Footwear v2 (strap lebih ramping). Coverage **45,6%** |
| `sandbox-fedora.blend` | Blender | 139.151 byte | File sumber fedora |
| `set/set-preview.blend` | Blender | 164.890 byte | Scene manikin untuk preview set |
| `set/previews/*.png` | PNG | — | 4 render preview manikin (set, top, bottom, footwear) |
| `set/templates/*.png` | PNG | 6 file | Template/rekonstruksi layout shirt, pants, shoes (+ canvas) |
| `main-image-square.jpg`, `set/main-image-*.jpg` | JPG 839×839 | — | Gambar utama listing marketplace |
| `build_fedora.py`, `set/paint_set.py`, `set/render_set.py`, `render_preview.py`, `set/debug_uv.py` | Python | — | Script build/paint/render (lihat 2.2) |

### 2.2 Cara ronde 1 dibuat (faktual, dari script sumber)

- **Fedora:** script Blender — crown dibuat dengan profil lathe (modifier Screw 64 langkah) + brim dari silinder 64 sisi yang ujungnya ditekuk ke bawah + band emas dari torus; ketiga bagian di-join jadi 1 mesh rigid; origin di (0,0,0) sebagai titik socket topi; export GLB (Y-up, satuan meter).
- **Pakaian:** script Python (PIL + numpy) yang menggambar prosedural di canvas 1024×1024: bentuk pakaian dari poligon, garis piping emas, kancing emas, monogram berlian "MG", lalu ditambah noise + pola weave kain. **Bukan hasil melukis manual di atas template asli Avatar Studio** — layout template direkonstruksi dari screenshot dokumentasi resmi, bukan byte-exact (layout sepatu paling tidak pasti; sudah terbukti butuh revisi v2 karena strap terbaca seperti sandal di preview).
- **Preview/QA:** render manikin di Blender saja. Tidak ada pengecekan live di Avatar Studio dari VM (tidak mungkin — butuh aplikasi desktop + login).

### 2.3 Penilaian jujur — kelemahan ronde 1

1. **Bukan voxel.** Di dunia yang seluruh estetikanya voxel, fedora halus (lathe + torus mulus) terlihat "asing". Aksesori voxel asli (tangga voxel, stud, band berundak) akan jauh lebih menyatu dengan dunia Sandbox.
2. **Angka teknis salah catat.** README mengklaim 1.602 tris; hasil export yang terukur 3.196 tris. Tidak fatal (masih kecil), tapi menunjukkan tidak ada audit file final sebelum submit.
3. **Pakaian = gambar datar prosedural.** Detail digambar dari primitif PIL (poligon/garis) — lekukan kaku, tanpa shading kain yang sesungguhnya (lipatan, gradasi cahaya), tanpa variasi material. Emasnya warna datar karena Paint Skin hanya membawa warna diffuse (tidak ada metallic/roughness map).
4. **Monogram generik.** "MG" memakai font DejaVu Serif bawaan sistem — bukan logo yang digambar khusus.
5. **Template tidak terverifikasi.** Layout direkonstruksi dari screenshot; risiko detail jatuh di tempat yang salah di avatar (sudah terjadi 1× pada sepatu).
6. **Satu cerita warna, tanpa kontras.** Charcoal + emas di semua item memang kohesif, tapi tidak ada elemen "wow" — tidak ada glow, tidak ada aksen kontras, tidak ada detail yang membuat orang berhenti scroll.
7. **Tanpa animasi/rigging.** Semua item statis. (Catatan: aksesori avatar di Avatar Studio pada dasarnya rigid; animasi VoxEdit berlaku untuk ASSET/NPC — jangan berasumsi aksesori bisa beranimasi sebelum dicek di Avatar Studio.)
8. **Tidak ada variasi kategori.** 4 slot terpakai (topi + 3 pakaian). Ronde 2 adalah kesempatan mengulang 4 slot itu dengan kualitas lebih tinggi, bukan menambah slot.

---

## 3. Inventaris tool di VM ini (terverifikasi 24 Nov 2026)

### 3.1 ADA

| Tool | Versi | Lokasi | Catatan |
|---|---|---|---|
| Blender | 5.3.0 | `~/.local/bin/blender` | Addon exporter glTF **aktif**. Fondasi utama ronde 2 |
| Python 3 | 3.12.3 | system + `~/workspace/tools/venv-video`, `venv-manim` | PIL 10.2.0–13.0.0, numpy 1.26.4–2.5.5, SciPy 1.11.4 (system) |
| Node.js / npm | v24.22.1 / 10.9.4 | `/usr/bin/node`, `/opt/hatch-image/bin/npm` | Jalur install gltf-transform |
| ffmpeg | 8.1.2 | `/usr/bin/ffmpeg` | Render/preview video aset |
| git / gh | — | `/usr/bin/git`, `/usr/bin/gh` | Repo sudah terhubung |
| Godot | 4.7.2 | `~/.local/bin/godot` | Bisa preview GLB; bukan tool Sandbox |
| pip | 24.0 | system + venv-video | Siap install paket Python |

### 3.2 HILANG

| Tool | Status | Dampak |
|---|---|---|
| VoxEdit | ❌ tidak ada | **Kritis.** Satu-satunya tool resmi yang bisa membuat aset voxel untuk Marketplace |
| MagicaVoxel | ❌ tidak ada | Editor voxel ringan, alternatif VoxEdit untuk modelling `.vox` |
| Goxel | ❌ tidak ada | Editor voxel open-source; **satu-satunya editor voxel yang jalan native di Linux** |
| trimesh / pygltflib / py-vox-io | ❌ tidak ada di semua venv | Audit GLB + konversi mesh→voxel + baca/tulis `.vox` tidak bisa dilakukan |
| gltf-transform / gltfpack | ❌ tidak ada | Validasi + optimasi GLB tidak bisa dilakukan |
| ImageMagick / GIMP / Inkscape | ❌ tidak ada | Painting tekstur manual (PIL saja yang ada) |
| Wine | ❌ tidak ada | Menutup jalur menjalankan tool Windows di VM |
| Sandbox Studio / Avatar Studio / Game Maker | ❌ tidak ada (Windows/macOS only) | Validasi + publish final **mustahil dari VM** |

### 3.3 Sumber daya VM

- Disk: **101 GB kosong** (34% terpakai) — cukup.
- RAM: total 7,9 GB, **hanya ~0,8 GB free saat pengecekan** — ketat; jangan jalankan banyak render berat paralel.
- CPU: 4 core (shared 1,5 vCPU efektif). Render Blender/ffmpeg lambat tapi jalan.

---

## 4. Tool/skill spesifik yang dibutuhkan untuk wearable spektakuler

| Kebutuhan | Tool yang tepat | Status di VM |
|---|---|---|
| **Voxel authoring (inti)** | VoxEdit (resmi, Modeler + Animator + Block Editor; satu-satunya yang export ke Marketplace) | ❌ — hanya Windows/macOS; jalan di laptop ukkas |
| Voxel authoring alternatif | Goxel (Linux native, export `.vox`/`.glb`/`.obj`) atau MagicaVoxel (Windows/macOS) | ❌ — Goxel bisa di-install di VM (lihat §5.2) |
| **Mesh → voxel** | Blender Remesh modifier mode Blocks; atau trimesh `voxel` + py-vox-io; atau import mesh ke Goxel | ⚠️ Blender ada; trimesh belum ada |
| **Rigging / animasi** | VoxEdit Animator (untuk ASSET/NPC). Aksesori avatar = rigid GLB, tanpa skin/animasi | ❌ — VoxEdit tidak ada; dan animasi aksesori **perlu verifikasi** di Avatar Studio |
| **Texture painting (pakaian)** | Template ASLI dari Avatar Studio (menu Paint Skin → Open Folder for Live Editing) + GIMP/Krita/PIL. Paint Skin = diffuse-only, 1024×1024 | ⚠️ PIL ada; GIMP tidak ada; template asli hanya ada di laptop ukkas |
| **Preview** | Avatar Studio live preview (laptop) + render manikin Blender (VM, sudah ada `set-preview.blend`) | ⚠️ sebagian |
| **Validasi** | Validator Avatar Studio (saat import) + audit lokal: trimesh/gltf-transform (tris, bounds, origin, material, ukuran file) | ❌ — validator hanya di laptop; audit lokal belum ada toolnya |
| **Konversi antar-format** | VoxBridge CLI (tool DAO untuk GLB hasil VoxEdit: cleanup tekstur, reduksi poligon, atlas, laporan validasi) | ❌ — belum di-install (opsional) |

**Angka skala Sandbox (dari riset web):** 1 meter = 32×32×32 voxel; avatar setinggi 2 meter. Artinya aksesori kepala yang baik dibangun dalam grid ~32 voxel per meter — detail voxel terasa kalau dirancang pada grid ini, bukan ditempel dari mesh halus.

**Catatan batas resmi:** angka batas segitiga/ukuran file resmi Avatar Studio **tidak ditemukan** di hasil pencarian web (hasil pencarian didominasi Roblox/dokumen platform lain). Jangan pakai angka pihak ketiga sebagai patokan — **cek validator di Avatar Studio saat import**; itu satu-satunya sumber kebenaran.

---

## 5. Gap + langkah setup konkret (per tool yang hilang)

> Instruksi di bawah ini rencana setup, **bukan eksekusi**. Tidak ada yang di-install dalam audit ini.

### 5.1 VoxEdit — KRITIS, di laptop Windows ukkas (tidak bisa di VM)

- Download resmi dari situs VoxEdit / hub Sandbox Studio. Ukuran file ±200 MB, gratis, Windows 10+ / macOS.
- File installer Windows bernama `VoxEdit_WIN_latest.zip` (versi terbaru).
- Install → login dengan akun Sandbox ukkas → modul Modeler (voxel), Animator (rig/animasi), Block Editor.
- **Kenapa tidak di VM:** tidak ada build Linux resmi dari The Sandbox (daftar platform resmi: Windows, macOS). Menjalankan via Wine tidak disarankan (Wine belum terpasang; install Wine berat dan VoxEdit belum tentu stabil di Wine).

### 5.2 Goxel 0.15.1 — editor voxel untuk VM Linux (prioritas install #1 di VM)

- Prebuilt: unduh dari `goxel.xyz` (halaman download resmi; pilih build Linux).
- Atau build dari source (butuh dependensi sistem):
  ```bash
  sudo apt install scons pkg-config libglfw3-dev libgtk-3-dev
  git clone https://github.com/guillaumechereau/goxel
  cd goxel && make release
  ```
- Ukuran kecil (source + deps ± puluhan MB). Lisensi GPL, gratis.
- Format: baca/tulis `.vox` (MagicaVoxel), export `.glb`/`.gltf`/`.obj`/`.ply`/`.qb`/PNG. Punya layers, symmetry, dan sculpting — cukup untuk membuat aksesori voxel hero di VM, lalu finalisasi di VoxEdit/Avatar Studio.

### 5.3 MagicaVoxel — opsional, di laptop Windows/macOS

- Download dari situs resmi ephtracy (`ephtracy.github.io`), gratis, ukuran kecil (±10 MB).
- Windows/macOS only. Di Linux hanya lewat Wine — **tidak direkomendasikan** di VM ini.

### 5.4 trimesh + pygltflib + py-vox-io — audit & konversi GLB/voxel (prioritas install #2 di VM)

```bash
~/workspace/tools/venv-video/bin/python -m pip install trimesh pygltflib py-vox-io
```

- Ukuran kecil (beberapa MB; numpy sudah ada). Kegunaan: hitung tris/bounds/origin/material dari GLB secara independen (temuan §2.1 soal 3.196 tris didapat dengan cara ini), voxelisasi mesh (`trimesh.voxel`), dan baca/tulis file `.vox`.

### 5.5 gltf-transform CLI — validasi & optimasi GLB (prioritas install #3 di VM)

```bash
npm install -g @gltf-transform/cli
```

- Node/npm sudah ada (v24/10.9). Kegunaan: `gltf-transform inspect` (statistik file), `validate`, `optimize` (dedup, prune, resize tekstur). Alternatif: **gltfpack** (satu binary dari GitHub releases `zeux/meshoptimizer`, ±10 MB).

### 5.6 ImageMagick — opsional (PIL sudah cukup)

```bash
sudo apt install imagemagick
```

- Hanya bila butuh operasi batch tekstur di CLI (resize, composite, montage preview). Untuk painting, PIL yang sudah ada + GIMP di laptop sudah memadai.

### 5.7 Sandbox Studio (+ Avatar Studio + Game Maker) — KRITIS, di laptop Windows ukkas

- Download dari `create.sandbox.game` → install di Windows 10+ → login akun ukkas → menu hamburger → Avatar Studio.
- **Ini satu-satunya tempat untuk:** mengambil template Paint Skin asli, live preview, validator aksesori, export, dan publish. Semua langkah ini tidak bisa dikerjakan dari VM.
- Game Maker (satu paket dengan Sandbox Studio) dipakai untuk preview aset di dunia game bila diperlukan.

### 5.8 Yang TIDAK perlu di-install

- **Wine** — berat (±1 GB+), tidak stabil untuk VoxEdit; lebih baik kerjakan VoxEdit langsung di laptop Windows.
- **Substance Painter / Marvelous Designer** — berbayar dan overkill untuk Paint Skin 1024² (diffuse-only). GIMP/Krita gratis sudah cukup untuk painting manual.
- **Blender add-on voxel khusus** — Remesh Blocks bawaan Blender sudah cukup untuk mesh→voxel dasar.

---

## 6. Rencana ronde 2 yang direkomendasikan

### 6.1 Alur kerja

1. **Konsep (1 hari):** pilih 1 tema kuat untuk keempat item (lihat 6.2). Tentukan hero piece di slot aksesori kepala ($10 — nilai terbesar).
2. **Voxel hero accessory:** bangun di Goxel (VM) atau VoxEdit (laptop) pada grid 32 voxel/meter. Detail bertingkat, aksen emas voxel, elemen kontras (mis. permata/bulu/api voxel).
3. **Finishing mesh:** rapikan di Blender 5.3 (origin di titik socket, skala meter, Y-up), export GLB, lalu audit lokal dengan trimesh + gltf-transform (tris, bounds, material, ukuran file) — jangan ulangi kesalahan catat angka ronde 1.
4. **Pakaian:** ambil template ASLI dari Avatar Studio di laptop (Paint Skin → Open Folder for Live Editing), lukis di atas template itu (GIMP/Krita/PIL) — jangan rekonstruksi dari screenshot lagi. Perbaiki kelemahan ronde 1: shading lipatan bergradasi, highlight/shadow emas yang meyakinkan meski diffuse-only, monogram yang digambar khusus.
5. **Validasi + publish:** import ke Avatar Studio di laptop → cek live preview per item → validator lolos → export → publish → form. **Jangan edit aset setelah submit.**

### 6.2 Arah konsep (supaya "spektakuler", bukan sekadar rapi)

- **Tema warisan Indonesia** (selaras dengan proyek dokumenter ukkas): set "Golden Garuda" — mahkota/topi Garuda voxel, coat batik mega mendung emas-hitam, celana songket, boots ukir. Cerita budaya = nilai tambah di mata reviewer.
- **Satu elemen kontras per item:** emas + satu warna aksen (merah delima / hijau zamrud) supaya tidak monoton charcoal-emas.
- **Detail voxel yang "terbaca" dari jauh:** silhouette kuat (tanduk/mahkota/jambul), bukan detail halus yang hilang di kejauhan.
- **Glow/emissive:** voxel bercahaya (mata Garuda, rune) — **wajib cek dulu** apakah Avatar Studio/marketplace mendukung material emissive pada aksesori; jangan berasumsi.

### 6.3 Prioritas mengingat deadline 30 Nov (±6 hari)

1. Hero accessory voxel (slot $10) — dampak terbesar.
2. Top + Bottom dengan template asli — perbaikan paling terasa.
3. Footwear — iterasi terakhir (layout sepatu sudah paling rawan; alokasikan waktu preview ekstra).
4. Jangan kejar animasi di ronde ini — aksesori avatar rigid; animasi butuh verifikasi dan waktu.

---

## 7. Batasan & hal yang belum terverifikasi

- Validasi/publish final hanya dari laptop Windows ukkas (Sandbox Studio). VM tidak bisa menggantikannya.
- Angka batas resmi (tris, ukuran file, tekstur) Avatar Studio tidak ditemukan lewat pencarian web — patokan akhirnya adalah validator di Avatar Studio.
- Apakah aksesori bisa membawa animasi/emissive: **belum terverifikasi**, harus dicek di Avatar Studio/VoxEdit.
- Email undangan ronde 2 (dari Seve Menez) tidak ditemukan di Gmail yang terhubung ke VM — kemungkinan masuk akun lain di HP ukkas. Link form ronde 2 = formulir yang sama dengan ronde 1 (per isi email).
