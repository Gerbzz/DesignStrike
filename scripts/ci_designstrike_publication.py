"""Reopen the native synthetic magazine and verify its PDF/page exports."""

import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys


CLI = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
MARKER = "DesignStrike synthetic publication proof"
native = OUT / "publication.designcraft"
pdf = OUT / "publication.pdf"
idml = OUT / "publication.idml"
pages = OUT / "pages"
before_hash = hashlib.sha256(native.read_bytes()).hexdigest()


def call(args):
    result = subprocess.run(args, capture_output=True, text=True, timeout=180, check=False)
    with (OUT / "cli.log").open("a", encoding="utf-8") as log:
        log.write("$ " + " ".join(map(str, args)) + "\n")
        log.write(result.stdout + "\n" + result.stderr + "\n")
    if result.returncode:
        raise RuntimeError(f"{args[0]} exited {result.returncode}: {result.stderr[-1600:]}")
    return result.stdout


stdout = call([str(CLI), "run", "--in", str(native), "--cmd", "document.inspect={}", "--export", str(pdf), "--all-pages", str(pages)])
reopened = json.loads(stdout.splitlines()[0])
(OUT / "reopened-inspect.json").write_text(json.dumps(reopened, indent=2), encoding="utf-8")
assert reopened["pageCount"] == 5
assert reopened["dirty"] is False
assert len(reopened["spreads"]) >= 3
assert reopened["parents"] and reopened["paragraphStyles"]
assert any(MARKER in story["preview"] and not story["overset"] for story in reopened["stories"])
assert hashlib.sha256(native.read_bytes()).hexdigest() == before_hash, "reopen/export changed the native original"

all_pages = sorted(pages.glob("page-*.png"))
assert len(all_pages) == 5, [p.name for p in all_pages]
for page in all_pages:
    data = page.read_bytes()
    assert data.startswith(b"\x89PNG\r\n\x1a\n") and data[12:16] == b"IHDR"
    width, height = struct.unpack(">II", data[16:24])
    assert width >= 500 and height >= 500 and len(data) > 1000, (page.name, width, height, len(data))

info = call(["pdfinfo", str(pdf)])
match = re.search(r"^Pages:\s+(\d+)$", info, flags=re.MULTILINE)
assert match and int(match.group(1)) == 5, info
text = call(["pdftotext", "-layout", str(pdf), "-"])
assert MARKER in " ".join(text.split()), "the edited story is missing from selectable PDF text"

idml_check = {"attempted": True, "roundTripPassed": False}
try:
    stdout = call([str(CLI), "run", "--in", str(native), "--export", str(idml)])
    assert idml.is_file() and idml.stat().st_size > 1000
    stdout = call([str(CLI), "run", "--in", str(idml), "--cmd", "document.inspect={}"])
    imported = json.loads(stdout.splitlines()[0])
    (OUT / "idml-inspect.json").write_text(json.dumps(imported, indent=2), encoding="utf-8")
    idml_check["roundTripPassed"] = imported["pageCount"] == 5 and any(MARKER in story["preview"] for story in imported["stories"])
    idml_check["pageCount"] = imported["pageCount"]
except (RuntimeError, AssertionError, IndexError, json.JSONDecodeError) as error:
    idml_check["error"] = str(error)

report = {
    "nativeSha256Unchanged": before_hash,
    "reopenedPages": reopened["pageCount"],
    "parentCount": len(reopened["parents"]),
    "paragraphStyleCount": len(reopened["paragraphStyles"]),
    "pngPages": len(all_pages),
    "pdfPages": int(match.group(1)),
    "pdfSelectableEdit": True,
    "idml": idml_check,
}
(OUT / "verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
