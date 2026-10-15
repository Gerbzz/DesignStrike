# DesignStrike foundation and verification

## Provenance

- Official counterpart: [DesignCraft](https://getartcraft.com/apps/designcraft), with [public Rust source](https://github.com/storytold/designcraft).
- Exact source pin: `a930276fd7462f3d9abd2fbb38544c94c0c911c8` (2026-10-15). This repository begins from a new root snapshot so restricted upstream `docs/brand/` artwork is absent from public history.
- Software licence: MIT OR Apache-2.0. The upstream NOTICE and ASSETS.md retain third-party terms. The open-licensed inherited cat app icon has a separate explicit licence. The approved PWDS bitmap is copied unchanged under its owner's terms.

## Foundation

The complete DesignCraft workspace supplies a native egui editor, headless CLI, web host, page and spread document model, threaded stories, paragraph composer, parent pages, styles, swatches, text wrap, PDF and IDML paths. These are upstream source capabilities, not DesignStrike acceptance results. The app remains on a pre-alpha publication gate in upstream [docs/gaps.md](gaps.md).

DesignStrike changes the visible native window, welcome screen, About panel, and project links, while preserving `.designcraft` document and internal package names for compatibility. The old ArtCraft mark shape was drawn in code; that code and the separately licensed `docs/brand/` files were removed before the new public root was committed.

## Verification

[Hosted Ubuntu 24.04 run 38727509672](https://github.com/Gerbzz/DesignStrike/actions/runs/38727509672) passed against code commit [`b2606033a4af5667d91aeed5c762fa9c4ccdd6e9`](https://github.com/Gerbzz/DesignStrike/commit/b2606033a4af5667d91aeed5c762fa9c4ccdd6e9). Its standard runner built the complete native desktop and CLI binaries with Rust 1.95, then passed the engine project-link test. No local Rust compilation used the shared Windows build slot.

The test launched the actual desktop editor under Xvfb/software OpenGL. It captured the [welcome screen](images/designstrike-welcome-ubuntu24.png), [About panel](images/designstrike-about-ubuntu24.png), [editor](images/designstrike-editor-ubuntu24.png), and [edited fifth page](images/designstrike-edited-page-ubuntu24.png) after native frames rendered. Starting from the code-generated four-page magazine, it appended a fifth page, placed an original text frame on that page, and saved `.designcraft`. A new CLI process reopened the saved file and exported [a five-page PDF](evidence/designstrike-synthetic-publication.pdf) plus five page PNGs. The [machine-readable report](evidence/designstrike-verification.json) records five reopened pages, one parent page, 15 paragraph styles, five PNGs, five PDF pages, selectable edited text in PDF, a five-page IDML export/reimport, and an unchanged native document hash. The [cover](images/designstrike-export-cover.png) and [fifth-page export](images/designstrike-export-page5.png) are preserved for visual review. The hosted artifact also contains the complete inspect JSON and process logs, with one-day retention.

This is a synthetic workflow check, not acceptance on a customer publication. The fifth-page PNG shows a narrow purple strip from adjacent page artwork at its left edge. Its visual clipping and PDF/print fidelity need investigation. The first two hosted iterations failed on a missing locked dependency and on proof-frame placement in the test harness; both were corrected before the passing run.

## Remaining

- Reproduce and fix the Primary Text Frame Smart Text Reflow page-deletion blocker reported in the upstream gap list.
- Validate live editing, paragraph/style behavior, overset detection, PDF quality, IDML import/export, fonts, preflight and a real multi-page publication on representative fixtures.
- Investigate the adjacent-page artwork strip in the fifth-page export and verify page clipping on both PDF and PNG output.
- Validate Windows/macOS and package naming, localized product strings and installer identity. The inherited open-licensed cat icon is temporary.
- FigStrike is the next missing Craft counterpart after this foundation.
