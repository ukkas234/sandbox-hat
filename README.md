# sandbox-hat — Sandbox Wearable & Cosmetic Bounty, set "Midnight Gold"

4 items for the Sandbox Wearable & Cosmetic Bounty (17–30 Nov 2026, pool $5,000, FCFS, paid in SAND on Polygon). Max $25: Head Accessory $10 + Top $5 + Bottom $5 + Footwear $5.

## Files

- `sandbox-fedora.glb` — Item 1, Head Accessory. Charcoal fedora + gold band, one rigid mesh, Hat socket, 1602 tris, no skin/animation. `preview.png` is its render. Built by `build_fedora.py` (Blender).
- `set/sandbox-top.png` — Item 2, Top. Tailored Coat texture, 1024×1024 PNG.
- `set/sandbox-bottom.png` — Item 3, Bottom. Tailored Trousers texture, 1024×1024 PNG.
- `set/sandbox-footwear.png` — Item 4, Footwear. Dress Boots texture, 1024×1024 PNG.
- `set/previews/` — Blender manikin previews of the full set.
- `set/SET.md` — design notes per item (read before working on clothing).
- `submit-prompt.md` — the full submit prompt: login → Avatar Studio → publish → Google Form, one item at a time. Give it as-is to the agent doing the submission.

## Notes

- Clothing is a 2D texture ("Paint Skin") in Avatar Studio, NOT GLB. One separate skin per garment.
- Template alignment was reconstructed from official docs screenshots, not byte-exact. Shoes layout is the least certain. Always check the Avatar Studio live preview before exporting.
- Never edit an asset after submitting it — editing = disqualification.
- The Polygon wallet address for the form is in `submit-prompt.md`. The wallet private key is NOT in this repo (never commit `polygon-wallet.json`).
