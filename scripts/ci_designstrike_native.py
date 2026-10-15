"""Drive DesignStrike's running native desktop through its loopback control API."""

import json
from pathlib import Path
import os
import socket
import struct
import sys
import time


OUT = Path(sys.argv[1]).resolve()
PID = int(sys.argv[2])
PORT = 18950
MARKER = "DesignStrike synthetic publication proof"


def request(method, params=None):
    payload = {"id": 1, "method": method, "params": params or {}}
    with socket.create_connection(("127.0.0.1", PORT), timeout=3) as connection:
        connection.settimeout(60)
        connection.sendall((json.dumps(payload) + "\n").encode())
        with connection.makefile("r", encoding="utf-8") as lines:
            reply = json.loads(lines.readline())
    if reply.get("ok") is not True:
        raise RuntimeError(f"{method} failed: {reply}")
    return reply.get("result")


def screenshot(name):
    path = OUT / name
    request("ui.screenshot", {"path": str(path), "focus": False})
    png = path.read_bytes()
    assert png.startswith(b"\x89PNG\r\n\x1a\n") and png[12:16] == b"IHDR"
    assert struct.unpack(">II", png[16:24]) == (1440, 900), name
    assert len(png) > 30000, f"{name}: suspiciously small UI image"
    print(f"Native {name}: {len(png)} bytes")


deadline = time.monotonic() + 120
while time.monotonic() < deadline:
    try:
        # POSIX signal 0 checks liveness. On Windows, os.kill(pid, 0) can
        # terminate the process; the control request below proves liveness.
        if os.name != "nt":
            os.kill(PID, 0)
        state = request("ui.inspect")
        if state.get("window", [0, 0])[0] >= 1400:
            break
    except (OSError, RuntimeError, ValueError, KeyError):
        pass
    time.sleep(1)
else:
    raise SystemExit("Native DesignStrike window/control server did not become ready")

screenshot("welcome.png")
request("ui.menu.invoke", {"command": "help.about", "params": {"open": True}})
screenshot("about.png")
request("ui.menu.invoke", {"command": "help.about", "params": {"open": False}})

request("engine.execute", {"command": "file.newSample", "params": {}})
sample = request("document.inspect")
assert sample["pageCount"] == 4, sample.get("pageCount")
assert sample["parents"] and sample["paragraphStyles"] and sample["stories"]
assert any(parent["items"] > 0 for parent in sample["parents"])
request("engine.execute", {"command": "layout.pages.insert", "params": {"count": 1}})
expanded = request("document.inspect")
assert expanded["pageCount"] == 5
last_spread = expanded["spreads"][-1]
spread = last_spread["index"]
last_page = last_spread["pages"][-1]
assert last_page["index"] == 4
page_x = last_page["bounds"][0]
request(
    "engine.execute",
    {
        "command": "frame.create",
        "params": {
            "spread": spread,
            "rect": [page_x + 60, 80, page_x + 485, 150],
            "content": "text",
            "text": MARKER,
            "caret": False,
        },
    },
)
edited = request("document.inspect")
assert edited["pageCount"] == 5
assert any(MARKER in story["preview"] and not story["overset"] for story in edited["stories"])
native_path = OUT / "publication.designcraft"
request("engine.execute", {"command": "file.saveAs", "params": {"path": str(native_path)}})
assert native_path.is_file() and native_path.stat().st_size > 10000


def settled_page(page):
    request("ui.set", {"page": page, "fit": "page"})
    observed = []
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        state = request("ui.inspect")
        if state.get("currentPage") == page - 1 and state.get("canvasRect") and state.get("perf", {}).get("renderMs", 0) > 0:
            observed.append(state)
            if len(observed) >= 3:
                time.sleep(0.5)
                return observed[-1]
        else:
            observed.clear()
        time.sleep(0.4)
    raise RuntimeError(f"page {page} did not settle: {observed[-1] if observed else state}")


editor = settled_page(3)
screenshot("editor.png")
last = settled_page(5)
screenshot("edited-page.png")
(OUT / "native-inspect.json").write_text(
    json.dumps({"sample": {"pageCount": sample["pageCount"], "styles": len(sample["paragraphStyles"])}, "edited": edited, "editorUi": editor, "lastUi": last}, indent=2),
    encoding="utf-8",
)
print(f"Saved native {native_path.name}: {native_path.stat().st_size} bytes, {edited['pageCount']} pages")
