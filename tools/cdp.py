"""Drive headless Chrome over the DevTools protocol, with the standard library.

Used by tools/screenshots.py and tools/check_browser.py. No package is
installed for it: a minimal WebSocket client (RFC 6455, text frames only,
client to server masked) carries the protocol's JSON messages, and Chrome
is the one already on the machine or the GitHub runner (ADR-0010).

  with Chrome() as chrome:
      page = chrome.new_page(1366, 900)
      page.goto(url)
      page.evaluate("document.title")

Each Chrome runs with a new, empty profile in a temporary folder, which is
deleted afterwards; it never touches the user's own browser or profiles.
A missing Chrome is a hard failure naming what was looked for, never a
skip (ADR-0008, gate D).
"""

from __future__ import annotations

import base64
import collections
import functools
import hashlib
import http.server
import json
import os
import platform
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from urllib.parse import urlsplit


class MissingTool(Exception):
    """Chrome is not installed where it was looked for."""


class CDPError(Exception):
    """The browser answered a command with an error, or stopped answering."""


# Chrome's locations, in the order they are tried. PG_CHROME overrides them.
# On Windows they are built from the system's own folder variables, so no
# drive letter is written here (gate A refuses one in any committed file).
_WINDOWS_CHROME = Path("Google") / "Chrome" / "Application" / "chrome.exe"
CANDIDATES = {
    "Windows": [str(Path(os.environ[v]) / _WINDOWS_CHROME)
                for v in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA") if os.environ.get(v)],
    "Darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"],
    "Linux": ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"],
}


def find_chrome() -> str:
    override = os.environ.get("PG_CHROME")
    if override:
        if Path(override).is_file():
            return override
        raise MissingTool(f"PG_CHROME is set to {override}, which is not a file")
    tried = CANDIDATES.get(platform.system(), [])
    for candidate in tried:
        found = shutil.which(candidate) or (candidate if Path(candidate).is_file() else None)
        if found:
            return found
    raise MissingTool("Chrome was not found. Looked for: " + ", ".join(tried) +
                      ". Install Google Chrome, or set PG_CHROME to its path")


class WebSocket:
    """Just enough of RFC 6455 for the DevTools protocol."""

    def __init__(self, url: str, timeout: float = 30) -> None:
        parts = urlsplit(url)
        self.sock = socket.create_connection((parts.hostname, parts.port), timeout=timeout)
        self.buffer = b""
        key = base64.b64encode(os.urandom(16)).decode()
        request = (f"GET {parts.path} HTTP/1.1\r\nHost: {parts.hostname}:{parts.port}\r\n"
                   f"Upgrade: websocket\r\nConnection: Upgrade\r\n"
                   f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
        self.sock.sendall(request.encode())
        while b"\r\n\r\n" not in self.buffer:
            self._fill()
        head, self.buffer = self.buffer.split(b"\r\n\r\n", 1)
        lines = head.decode("latin-1").split("\r\n")
        if " 101 " not in lines[0] + " ":
            raise CDPError(f"WebSocket upgrade refused: {lines[0]}")
        expected = base64.b64encode(hashlib.sha1(
            (key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()).decode()
        headers = {k.lower(): v.strip() for k, _, v in (line.partition(":") for line in lines[1:])}
        if headers.get("sec-websocket-accept") != expected:
            raise CDPError("WebSocket upgrade answered with the wrong accept key")

    def _fill(self) -> None:
        chunk = self.sock.recv(1 << 20)
        if not chunk:
            raise CDPError("the browser closed the connection")
        self.buffer += chunk

    def _take(self, n: int) -> bytes:
        while len(self.buffer) < n:
            self._fill()
        data, self.buffer = self.buffer[:n], self.buffer[n:]
        return data

    def _send_frame(self, opcode: int, payload: bytes) -> None:
        header = bytes([0x80 | opcode])
        length = len(payload)
        if length < 126:
            header += bytes([0x80 | length])
        elif length < 1 << 16:
            header += bytes([0x80 | 126]) + struct.pack(">H", length)
        else:
            header += bytes([0x80 | 127]) + struct.pack(">Q", length)
        mask = os.urandom(4)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(header + mask + masked)

    def send(self, text: str) -> None:
        self._send_frame(0x1, text.encode("utf-8"))

    def recv(self, timeout: float) -> str:
        self.sock.settimeout(timeout)
        message = b""
        while True:
            first, second = self._take(2)
            opcode, final = first & 0x0F, first & 0x80
            length = second & 0x7F
            if length == 126:
                length = struct.unpack(">H", self._take(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", self._take(8))[0]
            if second & 0x80:
                mask = self._take(4)
                payload = bytes(b ^ mask[i % 4] for i, b in enumerate(self._take(length)))
            else:
                payload = self._take(length)
            if opcode == 0x8:
                raise CDPError("the browser closed the connection")
            if opcode == 0x9:
                self._send_frame(0xA, payload)
                continue
            if opcode == 0xA:
                continue
            message += payload
            if final:
                return message.decode("utf-8")

    def close(self) -> None:
        try:
            self._send_frame(0x8, b"")
        except OSError:
            pass
        self.sock.close()


class Chrome:
    """One headless Chrome with a fresh profile, and its protocol connection."""

    def __init__(self, accessibility: bool = False, flags: tuple[str, ...] = ()) -> None:
        self.binary = find_chrome()
        self.profile = tempfile.mkdtemp(prefix="pg-chrome-")
        args = [self.binary, "--headless=new", "--remote-debugging-port=0",
                f"--user-data-dir={self.profile}", "--no-first-run",
                "--no-default-browser-check", "--disable-extensions",
                "--disable-background-networking", "--disable-sync",
                "--disable-component-update", "--disable-default-apps",
                "--disable-features=Translate,MediaRouter,OptimizationHints",
                "--metrics-recording-only", "--mute-audio", "--hide-scrollbars",
                "--password-store=basic", "--use-mock-keychain", *flags]
        if accessibility:
            # As a screen reader switches it on: the full accessibility tree
            # from the first load.
            args.append("--force-renderer-accessibility")
        # On the GitHub runner, Ubuntu 24.04 restricts the user namespaces
        # Chrome's sandbox uses; the workflows set PG_CHROME_NO_SANDBOX=1
        # there only, in jobs that hold no write token (ADR-0010).
        if os.environ.get("PG_CHROME_NO_SANDBOX") == "1":
            args.append("--no-sandbox")
        args.append("about:blank")
        self.process = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.next_id = 0
        self.events: collections.deque = collections.deque()
        try:
            port, path = self._debugging_port(Path(self.profile) / "DevToolsActivePort")
            self.ws = WebSocket(f"ws://127.0.0.1:{port}{path}")
        except BaseException:
            # A Chrome that started must not outlive a failed start.
            if self.process.poll() is None:
                self._kill_tree()
            self._cleanup()
            raise

    def _debugging_port(self, port_file: Path) -> list[str]:
        deadline = time.monotonic() + 30
        while True:
            try:
                fields = port_file.read_text().split() if port_file.is_file() else []
            except OSError:
                # Windows refuses the read while Chrome still holds the file
                # open (seen 2026-10-16); a later pass reads it whole.
                fields = []
            if len(fields) >= 2:
                return fields[:2]
            if self.process.poll() is not None:
                raise CDPError(f"Chrome exited at start with code {self.process.returncode}")
            if time.monotonic() > deadline:
                raise CDPError("Chrome did not open its debugging port within 30 s")
            time.sleep(0.05)

    def version(self) -> str:
        return self.send("Browser.getVersion")["product"]

    def send(self, method: str, params: dict | None = None, session: str | None = None,
             timeout: float = 60) -> dict:
        self.next_id += 1
        message = {"id": self.next_id, "method": method, "params": params or {}}
        if session:
            message["sessionId"] = session
        self.ws.send(json.dumps(message))
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise CDPError(f"{method}: no answer within {timeout} s")
            data = json.loads(self.ws.recv(remaining))
            if data.get("id") == self.next_id:
                if "error" in data:
                    raise CDPError(f"{method}: {data['error'].get('message')}")
                return data.get("result", {})
            if "method" in data:
                self.events.append(data)

    def wait_event(self, method: str, session: str | None = None, timeout: float = 30) -> dict:
        """The first event of this kind, from the queue or the wire."""
        for event in list(self.events):
            if event["method"] == method and event.get("sessionId") == session:
                self.events.remove(event)
                return event.get("params", {})
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise CDPError(f"no {method} within {timeout} s")
            data = json.loads(self.ws.recv(remaining))
            if data.get("method") == method and data.get("sessionId") == session:
                return data.get("params", {})
            if "method" in data:
                self.events.append(data)

    def drain(self, seconds: float) -> None:
        """Read events for a while, keeping them, so time passes for the page
        while the connection stays serviced."""
        deadline = time.monotonic() + seconds
        while (remaining := deadline - time.monotonic()) > 0:
            try:
                data = json.loads(self.ws.recv(remaining))
            except (socket.timeout, TimeoutError):
                break
            if "method" in data:
                self.events.append(data)

    def take_events(self, method: str, session: str | None = None) -> list[dict]:
        taken = [e for e in self.events if e["method"] == method and e.get("sessionId") == session]
        for event in taken:
            self.events.remove(event)
        return [e.get("params", {}) for e in taken]

    def new_page(self, width: int, height: int, *, dark: bool = False, reduced: bool = False,
                 scripts: bool = True) -> "Page":
        """A tab in its own fresh browsing context: no cache, no storage."""
        context = self.send("Target.createBrowserContext")["browserContextId"]
        target = self.send("Target.createTarget", {"url": "about:blank",
                                                   "browserContextId": context})["targetId"]
        session = self.send("Target.attachToTarget", {"targetId": target, "flatten": True})["sessionId"]
        page = Page(self, session, target, context)
        for domain in ("Page", "Runtime", "Network", "Log"):
            page.send(f"{domain}.enable")
        page.send("Emulation.setDeviceMetricsOverride",
                  {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False})
        page.send("Emulation.setEmulatedMedia", {"features": [
            {"name": "prefers-color-scheme", "value": "dark" if dark else "light"},
            {"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}]})
        if not scripts:
            page.send("Emulation.setScriptExecutionDisabled", {"value": True})
        return page

    def _cleanup(self) -> None:
        for _ in range(20):
            try:
                shutil.rmtree(self.profile)
                return
            except FileNotFoundError:
                return
            except OSError:
                time.sleep(0.25)

    def close(self) -> None:
        try:
            self.send("Browser.close", timeout=5)
        except Exception:
            pass
        try:
            self.ws.close()
        except Exception:
            pass
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self._kill_tree()
        self._cleanup()

    def _kill_tree(self) -> None:
        """Stop Chrome and every process it started. Never raises: by now the
        check's result is in, and a stuck exit must not turn it into a fail."""
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(self.process.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            self.process.kill()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            # Seen once, with a Chrome that ran across the machine sleeping
            # (2026-10-16): say so, so it can be stopped by hand.
            print(f"cdp: Chrome, process {self.process.pid}, did not exit; stop it by hand",
                  file=sys.stderr)

    def __enter__(self) -> "Chrome":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


class Page:
    def __init__(self, chrome: Chrome, session: str, target: str, context: str) -> None:
        self.chrome, self.session, self.target, self.context = chrome, session, target, context

    def send(self, method: str, params: dict | None = None, timeout: float = 60) -> dict:
        return self.chrome.send(method, params, session=self.session, timeout=timeout)

    def goto(self, url: str, settle: float = 0.0) -> None:
        self.chrome.take_events("Page.loadEventFired", self.session)
        self.send("Page.navigate", {"url": url})
        self.chrome.wait_event("Page.loadEventFired", self.session, timeout=60)
        if settle:
            self.chrome.drain(settle)

    def evaluate(self, expression: str, await_promise: bool = False):
        result = self.send("Runtime.evaluate", {"expression": expression, "returnByValue": True,
                                                "awaitPromise": await_promise})
        if "exceptionDetails" in result:
            details = result["exceptionDetails"]
            text = details.get("exception", {}).get("description") or details.get("text")
            raise CDPError(f"page script failed: {text}")
        return result["result"].get("value")

    def key(self, key: str) -> None:
        codes = {"Tab": 9, "Enter": 13, "Escape": 27}
        base = {"key": key, "code": key, "windowsVirtualKeyCode": codes[key],
                "nativeVirtualKeyCode": codes[key]}
        down = {**base, "type": "keyDown"}
        if key == "Enter":
            down["text"] = "\r"
        self.send("Input.dispatchKeyEvent", down)
        self.send("Input.dispatchKeyEvent", {**base, "type": "keyUp"})

    def ax_tree(self) -> list[dict]:
        return self.send("Accessibility.getFullAXTree")["nodes"]

    def screenshot(self, width: int, height: int, scale: float, quality: int = 82) -> bytes:
        data = self.send("Page.captureScreenshot", {
            "format": "webp", "quality": quality, "captureBeyondViewport": False,
            "clip": {"x": 0, "y": 0, "width": width, "height": height, "scale": scale}})["data"]
        return base64.b64decode(data)

    def close(self) -> None:
        self.chrome.send("Target.closeTarget", {"targetId": self.target})
        self.chrome.send("Target.disposeBrowserContext", {"browserContextId": self.context})


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    # Every type the built site serves, as GitHub Pages serves it. Python's
    # own table depends on the machine: on the seat's Windows it had no
    # .webp, so a link to a picture downloaded it instead of opening it
    # (2026-10-23); images inside a page loaded anyway, by sniffing.
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".webp": "image/webp", ".woff2": "font/woff2", ".js": "text/javascript",
                      ".css": "text/css", ".html": "text/html", ".json": "application/json",
                      ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".pdf": "application/pdf"}

    def log_message(self, *args) -> None:
        pass

    def end_headers(self) -> None:
        # Never let a check pass on a cached copy of an older build.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


class Server:
    """Serves a built folder on 127.0.0.1 at a free port, in a thread."""

    def __init__(self, folder: Path) -> None:
        handler = functools.partial(QuietHandler, directory=str(folder))
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.origin = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def __enter__(self) -> "Server":
        return self

    def __exit__(self, *exc) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
