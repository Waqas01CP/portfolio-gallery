"""Take each design's preview for the gallery, from its live demo, and make
each showcase entry's served copies from its author's screenshot.

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

Then the showcase (ADR-0016; Changes, 2026-10-20): each entry's screenshot,
as its author's tool saved it, is decoded once by a second headless Chrome
with the GPU off, and drawn into two served copies, WebP at quality
SHOWCASE_QUALITY, never enlarged, each the size build.py's
showcase_shapes() gives and the gallery's HTML reserves: card.webp, the
picture in its own shape at most SHOWCASE_CARD_WIDTH wide, with
transparent bands beyond the shape limits, and full.webp, fitting 2560 by
2560, written to showcase/<login>/ in the built folder. When Chrome reads
the screenshot at another size than the build did, as a quarter turn in
its EXIF that one of them ignores would give, the copies are not made and
the entry fails, named. A canvas holds pixels only, so the copies carry none of the
screenshot's metadata, and the copy's container is rewritten to hold its
image chunks alone, without even the colour profile Chrome's encoder
adds; the next job checks that too (tools/ci.py assemble). The
screenshot itself is never published. With the GPU on,
drawing a large capture in headless Chrome hung or came out blank on the
seat's machine (2026-10-20); with it off, five runs of each method gave
the same bytes.

Exit 0 when every design has its preview and every entry its copies; 1
when one failed, named; 2 when the folder is not a built gallery. Chrome
missing is exit 1, naming where it was looked for (ADR-0008, gate D).
"""

from __future__ import annotations

import base64
import json
import struct
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cdp import CDPError, Chrome, MissingTool, Server  # noqa: E402
from build import (PREVIEW_FILE, PREVIEW_SIZE, SHOWCASE, SHOWCASE_CARD,  # noqa: E402
                   SHOWCASE_FULL, SHOWCASE_QUALITY, BuildError, load_showcase)

WIDTH, HEIGHT = 1366, 900
SCALE = PREVIEW_SIZE[0] / WIDTH

# Decode once, then draw each copy at the size and place the build gave it;
# what the picture leaves of the canvas stays transparent.
SERVE = """async (src, shown, shapes, quality) => {
  const response = await fetch(src);
  if (!response.ok) throw new Error('could not read the file, ' + response.status);
  const bitmap = await createImageBitmap(await response.blob());
  if (bitmap.width !== shown[0] || bitmap.height !== shown[1]) {
    throw new Error('Chrome reads it as ' + bitmap.width + 'x' + bitmap.height + ', the build as ' +
                    shown[0] + 'x' + shown[1]);
  }
  const copies = {};
  for (const [name, {size: [width, height], at: [x, y, w, h]}] of Object.entries(shapes)) {
    const canvas = new OffscreenCanvas(width, height);
    const context = canvas.getContext('2d');
    context.imageSmoothingQuality = 'high';
    context.drawImage(bitmap, x, y, w, h);
    const blob = await canvas.convertToBlob({type: 'image/webp', quality: quality});
    const bytes = new Uint8Array(await blob.arrayBuffer());
    let text = '';
    for (let i = 0; i < bytes.length; i += 0x8000) {
      text += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    }
    copies[name] = {width: width, height: height, data: btoa(text)};
  }
  return {width: bitmap.width, height: bitmap.height, copies: copies};
}"""


IMAGE_CHUNKS = (b"VP8 ", b"VP8L", b"ALPH")


def image_only(data: bytes) -> bytes:
    """The WebP with its image chunks and nothing else. Chrome's encoder
    adds its own sRGB colour profile (ICCP) to what a canvas holds; the
    pixels are sRGB already, which browsers assume without a profile."""
    chunks, pos = [], 12
    while pos + 8 <= len(data):
        kind, length = struct.unpack("<4sI", data[pos:pos + 8])
        chunks.append((kind, data[pos + 8:pos + 8 + length]))
        pos += 8 + length + (length & 1)
    kept = [(kind, body) for kind, body in chunks if kind in IMAGE_CHUNKS]
    header = next((body for kind, body in chunks if kind == b"VP8X"), None)
    if header and any(kind == b"ALPH" for kind, _ in kept):
        # An alpha channel needs the extended header; keep its alpha flag only.
        kept.insert(0, (b"VP8X", bytes([header[0] & 0x10]) + header[1:]))
    body = b"WEBP" + b"".join(kind + struct.pack("<I", len(part)) + part + b"\0" * (len(part) & 1)
                              for kind, part in kept)
    return b"RIFF" + struct.pack("<I", len(body)) + body


def previews(folder: Path, demos: list[Path], failed: list[str]) -> None:
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


def served_copies(folder: Path, entries: list[dict], failed: list[str]) -> None:
    with Server(SHOWCASE) as server, Chrome(flags=("--disable-gpu",)) as chrome:
        print(f"{chrome.version()}, GPU off: {len(entries)} showcase entr{'y' if len(entries) == 1 else 'ies'}")
        page = chrome.new_page(800, 600)
        try:
            # A page of the same origin, so the canvas may be read back.
            page.goto(f"{server.origin}/", settle=0.2)
            for entry in entries:
                source = urllib.parse.quote(entry["screenshot"].removeprefix("showcase/"))
                shapes = {Path(name).stem: shape for name, shape in entry["shapes"].items()}
                try:
                    result = page.send("Runtime.evaluate", {
                        "expression": f"({SERVE})({json.dumps(source)}, {json.dumps(entry['shown'])}, "
                                      f"{json.dumps(shapes)}, {SHOWCASE_QUALITY})",
                        "awaitPromise": True, "returnByValue": True}, timeout=120)
                    if "exceptionDetails" in result:
                        details = result["exceptionDetails"]
                        raise CDPError((details.get("exception") or {}).get("description") or details.get("text"))
                    value = result["result"]["value"]
                    sizes = []
                    for name in (SHOWCASE_CARD, SHOWCASE_FULL):
                        copy = value["copies"][Path(name).stem]
                        data = base64.b64decode(copy["data"])
                        if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
                            raise CDPError(f"the {name} drawn is not a WebP image")
                        data = image_only(data)
                        target = folder / entry["card"].rsplit("/", 1)[0] / name
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(data)
                        sizes.append(f"{name} {copy['width']}x{copy['height']} {len(data)} bytes")
                    print(f"  {entry['screenshot']} ({value['width']}x{value['height']}): {'; '.join(sizes)}")
                except CDPError as error:
                    failed.append(f"{entry['screenshot']}: Chrome could not read it as an image ({error})")
        finally:
            page.close()


def main(argv: list[str]) -> int:
    # A screenshot's name can hold characters the console cannot write, as
    # a Mac's narrow no-break space on Windows; write them escaped.
    sys.stdout.reconfigure(errors="backslashreplace")
    sys.stderr.reconfigure(errors="backslashreplace")
    folder = Path(argv[0] if argv else "_site").resolve()
    demos = sorted(p.parent for p in (folder / "designs").glob("*/index.html"))
    if not (folder / "index.html").is_file() or not demos:
        print(f"{folder} is not a built gallery; run python build.py --gallery first",
              file=sys.stderr)
        return 2
    failed: list[str] = []
    try:
        previews(folder, demos, failed)
        entries = load_showcase()
        if entries:
            served_copies(folder, entries, failed)
    except MissingTool as error:
        print(f"missing tool: {error}", file=sys.stderr)
        return 1
    except BuildError as error:
        print(f"the showcase cannot be read: {error}", file=sys.stderr)
        return 1
    for failure in failed:
        print(f"  FAILED {failure}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
