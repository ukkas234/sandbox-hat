# BUILD REPORT — Sandbox Wearable & Cosmetic Bounty, Ronde 2

**Status: kedua set selesai + ter-QC (24 Nov 2026). Belum ada yang di-submit — submit + form dilakukan ukkas sendiri dari laptop.**

Aturan bounty yang berlaku: maks 1 item per kategori per ronde (4 item). **Neon Ronin = set submit ronde 2. Royal Peacock = ditahan** untuk Player Marketplace (buka 1 Des 2026, komisi 100%) atau ronde 3 bila diundang. Jangan pernah submit kedua set sekaligus ke ronde yang sama.

---

## SET 1 — NEON RONIN (set submit ronde 2)

Dir: `~/workspace/sandbox-hat/round2/neon-ronin/`

| File | Isi / ukuran |
|---|---|
| `neon-ronin-kabuto.glb` | Head Accessory hero — 53 KB |
| `kabuto.vox.json` / `kabuto.vox` | Definisi voxel grid / MagicaVoxel .vox |
| `neon-ronin-kabuto.blend` | File sumber Blender |
| `neon-ronin-top.png` | Top 1024×1024 — 412 KB |
| `neon-ronin-bottom.png` | Bottom 1024×1024 — 893 KB |
| `neon-ronin-footwear.png` | Footwear 1024×1024 — 182 KB |
| `kabuto_voxels.py`, `build_kabuto.py`, `paint_ronin.py`, `render_ronin.py`, `render_kabuto.py` | Script build (reproducible) |

**Kabuto — angka terukur (Blender + trimesh, sama persis):** 156 voxel (grid 32 voxel/meter), 470 face → **940 segitiga**. gltf-transform validate: 0 warning. Bounds X ±0,1875 m, Y ±0,156 m, Z 0–0,25 m. Origin (0,0,0) = puncak kepala (Hat socket), rigid, tanpa armature/modifier, 4 material (plate/charcoal/cyan emissive/magenta). Desain: kubah berundak berongga + tanduk kuwagata 2×2 (ujung cyan) + maedate (stripe cyan + jewel magenta) + fukigaeshi + peak depan. Mesh sengaja tidak watertight (bawah terbuka, helm duduk di atas kepala) — bukan blocker.

**Tekstur:** footprint identik ronde 1 (coverage non-hitam: top 46,9% / bottom 84,8% / footwear 45,6%). Top: kimono wrap + sash diagonal + circuit cyan + emblem torii + crest diamond punggung. Bottom: hakama + trim cyan di hem. Footwear: boots tabi (split-toe) + jahitan cyan + gesper silver. Bug yang diperbaiki saat build: warna gelap (8,8,12) terlalu dekat hitam murni → coverage sepatu sempat 34,8%; diperbaiki ke (16,16,20).

**Preview:** 9 render di `previews/` (set depan/belakang, top depan/belakang, bottom, footwear, kabuto depan/samping/atas). 2 masalah diperbaiki: tanduk v1 terlalu tipis (1 voxel, ujung cyan tampak melayang) → ditebalkan 2×2, maedate dipersempit 4→2 voxel; framing full-set memotong tanduk → kamera ditarik mundur.

---

## SET 2 — ROYAL PEACOCK (ditahan — marketplace / ronde 3)

Dir: `~/workspace/sandbox-hat/round2/royal-peacock/`

| File | Isi / ukuran |
|---|---|
| `royal-peacock-crown.glb` | Head Accessory hero — 45 KB |
| `crown.vox.json` / `crown.vox` | Definisi voxel grid (612 byte .vox) / MagicaVoxel .vox |
| `royal-peacock-crown.blend` | File sumber Blender |
| `royal-peacock-top.png` | Top 1024×1024 — 399 KB |
| `royal-peacock-bottom.png` | Bottom 1024×1024 — 937 KB |
| `royal-peacock-footwear.png` | Footwear 1024×1024 — 288 KB |
| `crown_voxels.py`, `build_crown.py`, `paint_peacock.py`, `render_peacock.py`, `render_crown.py` | Script build (reproducible) |

**Crown — angka terukur (Blender + trimesh, sama persis):** 124 voxel (grid 32 voxel/meter), 372 face → **744 segitiga**. gltf-transform validate v2: **No errors, No warnings, No hints**. Bounds X ±0,1719 m, Y ±0,125 m, Z 0–0,25 m. Origin (0,0,0) = puncak kepala (Hat socket), rigid, tanpa armature/modifier, 6 material (gold / gold light / gold dark / teal emissive / peacock blue emissive / emerald emissive). Desain: band emas 2 ring + spikes gold + jewel emerald di depan + 5 kipas bulu merak dari busur belakang, tiap bulu berujung eye-spot (teal–biru–emas). Mesh sengaja tidak watertight (band berongga, bawah terbuka) — bukan blocker.

**Revisi desain v1 → v2 (hasil QC):** v1 bulu terlalu tinggi (7–9 voxel) dengan eye-spot kecil → di render close-up terbaca seperti tiang pagar, dari samping jadi dinding teal padat. v2: bulu dipendekkan (5–7 voxel) + eye fan diperbesar jadi 3 baris (biru lebar + pusat emas + rim emerald) sehingga mata merak mendominasi siluet. Render ulang terverifikasi: depan + set-front terbaca jelas sebagai mahkota kipas bulu merak; samping tetap slab teal (bawaan bulu 1 voxel tebal) tapi berundak, bukan dinding rata.

**Tekstur:** footprint identik ronde 1 (coverage non-hitam terukur: **top 47,1% / bottom 84,8% / footwear 45,6%** — sama dengan ronde 1). Top: jas brokat emas + 2 mata merak di dada + kancing emas + piping teal + mata merak raksasa di punggung (pusat punggung). Bottom: celana formal emas + waistband emerald + stripe teal + mata merak di paha. Footwear: sepatu formal emas + toe cap mengkilap + jahitan teal + mata merak di lidah + strap gesper emas.

**Preview:** 9 render di `previews/` (peacock-set-front/back, peacock-top-front/back, peacock-bottom, peacock-footwear, crown-front/side/top). Semua dicek visual.

---

## Tooling yang terinstall (dipakai kedua set)

- trimesh 5.2.2 + pygltflib 1.16.5 + py-vox-io di `~/workspace/tools/venv-video/`
- gltf-transform CLI 4.5.1 di `~/.npm-global/bin/gltf-transform`
- Goxel 0.15.1 AppImage di `~/workspace/tools/goxel/` (verifikasi .vox)
- Blender 5.3.0 di `~/.local/bin/blender` (bukan di PATH — pakai path penuh)
- Wine TIDAK diinstall.

## Catatan preview (artefak manikin — BUKAN cacat)

- **Gap helm–kepala:** kepala manikin bola vs dasar helm datar. Preview ronde 1 menunjukkan gap yang sama dengan fedora yang disetujui; kepala avatar Sandbox asli kotak berdatar atas, jadi helm/mahkota akan duduk rapat.
- **Sepatu tampak boxy / area insole gelap di atas sepatu:** keterbatasan manikin kotak, sama seperti preview ronde 1 yang disetujui; detail jahitan/gesper/emblem jatuh di tempat yang benar.
- **Strip hitam tipis di bawah jaket (depan/belakang):** latar hitam tekstur di bawah poligon pakaian, terpeta ke dasar kotak torso manikin. Bukan bagian tekstur pakaian.
- **Bagian dalam band mahkota terlihat dari belakang-bawah:** band berongga; di avatar asli tertutup kepala.

## Checklist sisi laptop (HANYA bisa di Windows ukkas)

1. Buka template asli Avatar Studio → bandingkan layout tekstur (khususnya sepatu — template ronde 1 adalah rekonstruksi dari screenshot docs, bukan template asli).
2. Import .glb ke Avatar Studio → jalankan validator (rigid / ukuran / jarak / tris).
3. Live preview di avatar → cek helm duduk rapat, tidak clipping, tekstur tidak terbalik.
4. Publish ke Creator Hub (Neon Ronin dulu — 4 item).
5. Isi Google Form ronde 2 (form yang sama seperti ronde 1) — **jangan edit form/asset setelah submit (edit = DQ)**.
6. Royal Peacock: tahan sampai marketplace buka 1 Des (harga saran 100 Silicon/item) atau sampai undangan ronde 3 datang.
7. Simpan bukti: screenshot Creator Hub LIVE + konfirmasi form, seperti ronde 1.
