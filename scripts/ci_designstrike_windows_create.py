"""Create a five-page synthetic native document through the Windows CLI."""

import json
from pathlib import Path
import subprocess
import sys


CLI = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
NATIVE = OUT / "publication.designcraft"
MARKER = "DesignStrike synthetic publication proof"


def run(*args):
    command = [str(CLI), "run", *args]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=180, check=False)
    if result.returncode:
        raise RuntimeError(f"{command!r} failed: {result.stderr}\n{result.stdout}")
    return result.stdout


stdout = run("--sample", "--cmd", 'layout.pages.insert={"count":1}', "--cmd", "document.inspect={}")
inspect = json.loads(stdout.splitlines()[-1])
assert inspect["pageCount"] == 5
last_spread = inspect["spreads"][-1]
last_page = last_spread["pages"][-1]
assert last_page["index"] == 4
page_x = last_page["bounds"][0]
frame = {
    "spread": last_spread["index"],
    "rect": [page_x + 60, 80, page_x + 485, 150],
    "content": "text",
    "text": MARKER,
    "caret": False,
}
run(
    "--sample",
    "--cmd", 'layout.pages.insert={"count":1}',
    "--cmd", "frame.create=" + json.dumps(frame, separators=(",", ":")),
    "--cmd", "file.saveAs=" + json.dumps({"path": str(NATIVE)}, separators=(",", ":")),
)
assert NATIVE.stat().st_size > 10000
reopened = json.loads(run("--in", str(NATIVE), "--cmd", "document.inspect={}").splitlines()[0])
assert reopened["pageCount"] == 5
assert any(MARKER in story["preview"] and not story["overset"] for story in reopened["stories"])
(OUT / "cli-created-inspect.json").write_text(json.dumps(reopened, indent=2), encoding="utf-8")
print(json.dumps({"creation": "Windows CLI", "pages": reopened["pageCount"], "native_bytes": NATIVE.stat().st_size}))
