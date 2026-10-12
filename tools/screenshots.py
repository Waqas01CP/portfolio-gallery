"""Take each design's preview for the gallery, from its live demo.

  python tools/screenshots.py [_site]

Reads a gallery built by `python build.py --gallery`, serves it on
127.0.0.1, opens each design's demo in headless Chrome and saves the first
screen, 1366 by 900 CSS pixels at half size, as designs/<name>/preview.webp
in the built folder. Motion is reduced, so the capture shows the page at
rest, and the light setting is used, so every preview is taken alike.

Previews are made here, by the deploy workflow, never supplied by a
contributor, so a preview cannot misrepresent its design (ADR-0006). The
workflow runs this in a job of its own that holds no write token, and the
next job takes only the .webp files from it (ADR-0010).

Exit 0 when every design has its preview; 1 when one failed, named; 2 when
the folder is not a built gallery. Chrome missing is exit 1, naming where
it was looked for (ADR-0008, gate D).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cdp import CDPError, Chrome, MissingTool, Server  # noqa: E402
from build import PREVIEW_FILE, PREVIEW_SIZE  # noqa: E402

WIDTH, HEIGHT = 1366, 900
SCALE = PREVIEW_SIZE[0] / WIDTH


def main(argv: list[str]) -> int:
    folder = Path(argv[0] if argv else "_site").resolve()
    demos = sorted(p.parent for p in (folder / "designs").glob("*/index.html"))
    if not (folder / "index.html").is_file() or not demos:
        print(f"{folder} is not a built gallery; run python build.py --gallery first",
              file=sys.stderr)
        return 2
    failed = []
    try:
        with Server(folder) as server, Chrome() as chrome:
            print(f"{chrome.version()}: {len(demos)} demo(s)")
            for demo in demos:
                page = chrome.new_page(WIDTH, HEIGHT, reduced=True)
                try:
                    page.goto(f"{server.origin}/designs/{demo.name}/index.html", settle=1.0)
                    page.evaluate("document.fonts.ready.then(() => true)", await_promise=True)
                    chrome.drain(1.0)
                    image = page.screenshot(WIDTH, HEIGHT, SCALE)
                    if image[:4] != b"RIFF" or image[8:12] != b"WEBP":
                        raise CDPError("the capture is not a WebP image")
                    (demo / PREVIEW_FILE).write_bytes(image)
                    print(f"  {demo.name}: {len(image)} bytes")
                except CDPError as error:
                    failed.append(f"{demo.name}: {error}")
                finally:
                    page.close()
    except MissingTool as error:
        print(f"missing tool: {error}", file=sys.stderr)
        return 1
    for failure in failed:
        print(f"  FAILED {failure}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
