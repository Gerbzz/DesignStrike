# DesignStrike foundation and verification

## Provenance

- Official counterpart: [DesignCraft](https://getartcraft.com/apps/designcraft), with [public Rust source](https://github.com/storytold/designcraft).
- Exact source pin: `a930276fd7462f3d9abd2fbb38544c94c0c911c8` (2026-10-15). This repository begins from a new root snapshot so restricted upstream `docs/brand/` artwork is absent from public history.
- Software licence: MIT OR Apache-2.0. The upstream NOTICE and ASSETS.md retain third-party terms. The open-licensed inherited cat app icon has a separate explicit licence. The approved PWDS bitmap is copied unchanged under its owner's terms.

## Foundation

The complete DesignCraft workspace supplies a native egui editor, headless CLI, web host, page and spread document model, threaded stories, paragraph composer, parent pages, styles, swatches, text wrap, PDF and IDML paths. These are upstream source capabilities, not DesignStrike acceptance results. The app remains on a pre-alpha publication gate in upstream [docs/gaps.md](gaps.md).

DesignStrike changes the visible native window, welcome screen, About panel, and project links, while preserving `.designcraft` document and internal package names for compatibility. The old ArtCraft mark shape was drawn in code; that code and the separately licensed `docs/brand/` files were removed before the new public root was committed.

## Verification

[Hosted Ubuntu 24.04 run 38729864589](https://github.com/Gerbzz/DesignStrike/actions/runs/38729864589) passed against fix commit [`1d5172420b5fc97022ad9a5020eeb25292a33860`](https://github.com/Gerbzz/DesignStrike/commit/1d5172420b5fc97022ad9a5020eeb25292a33860). Its standard runner built the complete native desktop and CLI binaries with Rust 1.95, passed the engine project-link test, the three focused regressions, 565 engine library tests (one ignored), and 35 renderer library tests. No local Rust compilation used the shared Windows build slot.

The test launched the actual desktop editor under Xvfb/software OpenGL. It captured the [welcome screen](images/designstrike-welcome-ubuntu24.png), [About panel](images/designstrike-about-ubuntu24.png), [editor](images/designstrike-editor-ubuntu24.png), and [edited fifth page](images/designstrike-edited-page-ubuntu24.png) after native frames rendered. Starting from the code-generated four-page magazine, it appended a fifth page, placed an original text frame on that page, and saved `.designcraft`. A new CLI process reopened the saved file and exported [a five-page PDF](evidence/designstrike-synthetic-publication.pdf) plus five page PNGs. The [machine-readable report](evidence/designstrike-verification.json) records five reopened pages, one parent page, 15 paragraph styles, five PNGs, five PDF pages, five rasterized PDF pages, selectable edited text in PDF, a five-page IDML export/reimport, and an unchanged native document hash. The hosted artifact also contains inspect JSON and process logs, with one-day retention.

All five exported PNG pages and all five rasterized PDF pages were visually inspected. They contain the expected cover, article spreads, color page, edited fifth page and folios; the adjacent-page purple strip is absent. Review the PNG exports for pages [1](images/designstrike-export-cover.png), [2](images/designstrike-export-page2.png), [3](images/designstrike-export-page3.png), [4](images/designstrike-export-page4.png), and [5](images/designstrike-export-page5.png), and the PDF renders for pages [1](evidence/designstrike-pdf-page1.png), [2](evidence/designstrike-pdf-page2.png), [3](evidence/designstrike-pdf-page3.png), [4](evidence/designstrike-pdf-page4.png), and [5](evidence/designstrike-pdf-page5.png). Visual inspection here is qualitative, not a typography or print-fidelity metric.

The [unfixed regression run 38729078701](https://github.com/Gerbzz/DesignStrike/actions/runs/38729078701) failed exactly three expected assertions: manual deletion immediately recreated a primary-story page or frame, and a newly facing fifth sample page inherited inside bleed. Its [red test log](evidence/designstrike-before-regressions.log) and the [original page-five export](evidence/designstrike-before-page5.png) remain in the repository. The [passing regression log](evidence/designstrike-regressions-after.log) shows those tests green. The fix gates Smart Text Reflow on a relevant primary-story/layout change and corrects the generated magazine's inside bleed and page-four background boundary. The upstream [issue #165](https://github.com/storytold/designcraft/issues/165) and inherited `docs/gaps.md` remain open; this validates the reproduced deletion cases, not every text-flow scenario.

## Remaining

- Continue validating Primary Text Frame threading, overset, page removal and flow on representative publications, beyond the three focused regressions.
- Validate live editing, paragraph/style behavior, overset detection, PDF quality, IDML import/export, fonts, preflight and a real multi-page publication on representative fixtures.
- Check intended cross-page artwork and inside bleed behavior on real documents; the fixed synthetic sample is not a general clipping proof.
- Validate Windows/macOS and package naming, localized product strings and installer identity. The inherited open-licensed cat icon is temporary.
- FigStrike is the next missing Craft counterpart after this foundation.
