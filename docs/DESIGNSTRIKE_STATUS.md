# DesignStrike foundation and verification

## Provenance

- Official counterpart: [DesignCraft](https://getartcraft.com/apps/designcraft), with [public Rust source](https://github.com/storytold/designcraft).
- Exact source pin: `a930276fd7462f3d9abd2fbb38544c94c0c911c8` (2026-10-15). This repository begins from a new root snapshot so restricted upstream `docs/brand/` artwork is absent from public history.
- Software licence: MIT OR Apache-2.0. The upstream NOTICE and ASSETS.md retain third-party terms. The open-licensed inherited cat app icon has a separate explicit licence. The approved PWDS bitmap is copied unchanged under its owner's terms.

## Foundation

The complete DesignCraft workspace supplies a native egui editor, headless CLI, web host, page and spread document model, threaded stories, paragraph composer, parent pages, styles, swatches, text wrap, PDF and IDML paths. These are upstream source capabilities, not DesignStrike acceptance results. The app remains on a pre-alpha publication gate in upstream [docs/gaps.md](gaps.md).

DesignStrike changes the visible native window, welcome screen, About panel, and project links, while preserving `.designcraft` document and internal package names for compatibility. The old ArtCraft mark shape was drawn in code; that code and the separately licensed `docs/brand/` files were removed before the new public root was committed.

## Verification

Pending a bounded hosted Linux build and workflow run. No local Rust compilation will use the shared Windows build slot. The intended check uses the real application and CLI to create or open a multi-page layout, change it, save and reopen the native document, export PDF and pages, inspect the output, and capture the native UI after rendering settles. Exact run, commit and images will be linked here after verification.

## Remaining

- Reproduce and fix the Primary Text Frame Smart Text Reflow page-deletion blocker reported in the upstream gap list.
- Validate live editing, paragraph/style behavior, overset detection, PDF quality, IDML import/export, fonts, preflight and a real multi-page publication on representative fixtures.
- Validate Windows/macOS and package naming, localized product strings and installer identity. The inherited open-licensed cat icon is temporary.
- FigStrike is the next missing Craft counterpart after this foundation.
