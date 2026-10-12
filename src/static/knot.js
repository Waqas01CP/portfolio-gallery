/* The torus knot: a wireframe drawn on a 2D canvas, with no library, in a
   worker. The page hands this worker the canvas, so neither starting the
   knot nor drawing it ever runs on the page's main thread: the first draw
   in a fresh browser costs tens of milliseconds, and on the main thread
   that alone took the site this engine was copied from near its limit for
   blocked time (docs/reference/provenance.md). The knot carries no words.
   A design shows it, or turns it off with --pg-knot: 0.

   Messages from site.js:
     start    the canvas, its colour, size, pixel ratio, and whether motion
              is reduced or the knot is off screen
     size     a new size and pixel ratio
     pointer  where the pointer is over the Intro, from -0.5 to 0.5
     visible  whether the knot is on screen and the tab is shown
     reduced  whether motion is reduced
   Under reduced motion it is drawn once and left still, and no frame is
   requested. If the device draws it too slowly it stops for good. */
"use strict";

const raf = self.requestAnimationFrame
  ? self.requestAnimationFrame.bind(self)
  : (fn) => setTimeout(() => fn(performance.now()), 16);
const caf = self.cancelAnimationFrame ? self.cancelAnimationFrame.bind(self) : clearTimeout;

let canvas = null;
let ctx = null;
let shape = null;
let colour = "#C6F135";
let ratio = 1;
let t = 0, px = 0, py = 0, tx = 0, ty = 0;
let visible = true, reduced = false, still = false, frame = 0;

function build() {
  const p = 2, q = 3, N = 200, M = 9, R = 1, r = 0.46, tube = 0.15, TAU = Math.PI * 2;
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const unit = (a) => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
  const curve = [];
  for (let i = 0; i < N; i += 1) {
    const s = (i / N) * TAU, c = R + r * Math.cos(q * s);
    curve.push([c * Math.cos(p * s), c * Math.sin(p * s), r * Math.sin(q * s)]);
  }
  const V = new Float32Array(N * M * 3);
  for (let i = 0; i < N; i += 1) {
    const s = (i / N) * TAU, c = curve[i];
    const T = unit(sub(curve[(i + 1) % N], curve[(i - 1 + N) % N]));
    let n = unit(sub(c, [R * Math.cos(p * s), R * Math.sin(p * s), 0]));
    const B = unit(cross(T, n));
    n = cross(B, T);
    for (let j = 0; j < M; j += 1) {
      const a = (j / M) * TAU, ca = Math.cos(a), sa = Math.sin(a), o = (i * M + j) * 3;
      V[o] = c[0] + tube * (ca * n[0] + sa * B[0]);
      V[o + 1] = c[1] + tube * (ca * n[1] + sa * B[1]);
      V[o + 2] = c[2] + tube * (ca * n[2] + sa * B[2]);
    }
  }
  shape = { V, N, M, P: new Float32Array(N * M * 3) };
}

function resize(width, pixelRatio) {
  if (!canvas || !width) return;
  ratio = Math.min(1.5, pixelRatio || 1, 1100 / width);
  const side = Math.round(width * ratio);
  if (canvas.width !== side) canvas.width = canvas.height = side;
}

function draw() {
  if (!ctx || !shape) return;
  const { V, N, M, P } = shape, w = canvas.width, h = canvas.height, s = w * 0.27;
  px += (tx - px) * 0.04;
  py += (ty - py) * 0.04;
  const ay = t * 0.16 + px * 0.5, ax = 0.9 + Math.sin(t * 0.09) * 0.18 + py * 0.35, az = t * 0.05;
  const cy = Math.cos(ay), sy = Math.sin(ay), cx = Math.cos(ax), sx = Math.sin(ax), cz = Math.cos(az), sz = Math.sin(az);
  for (let i = 0; i < V.length; i += 3) {
    const x = V[i] * cz - V[i + 1] * sz, y = V[i] * sz + V[i + 1] * cz, z = V[i + 2];
    const x1 = x * cy + z * sy, z1 = -x * sy + z * cy;
    const y2 = y * cx - z1 * sx, z2 = y * sx + z1 * cx;
    const f = 3.2 / (3.2 + z2);
    P[i] = w / 2 + x1 * s * f;
    P[i + 1] = h / 2 + y2 * s * f;
    P[i + 2] = z2;
  }
  ctx.clearRect(0, 0, w, h);
  const paths = [new Path2D(), new Path2D(), new Path2D(), new Path2D()];
  const seg = (a, b) => {
    const depth = (P[a + 2] + P[b + 2]) * 0.5;
    const path = paths[Math.max(0, Math.min(3, Math.floor(((depth + 1.6) / 3.2) * 4)))];
    path.moveTo(P[a], P[a + 1]);
    path.lineTo(P[b], P[b + 1]);
  };
  for (let i = 0; i < N; i += 1) {
    for (let j = 0; j < M; j += 1) {
      const a = (i * M + j) * 3;
      seg(a, (((i + 1) % N) * M + j) * 3);
      if (i % 4 === 0) seg(a, (i * M + ((j + 1) % M)) * 3);
    }
  }
  ctx.lineWidth = ratio;
  ctx.strokeStyle = colour;
  const alpha = [0.62, 0.4, 0.22, 0.09];
  for (let b = 3; b >= 0; b -= 1) {
    ctx.globalAlpha = alpha[b];
    ctx.stroke(paths[b]);
  }
  ctx.globalAlpha = 1;
}

function stop() {
  if (frame) caf(frame);
  frame = 0;
}

function loop() {
  if (frame || still || reduced || !visible || !ctx) return;
  let last = performance.now(), slow = 0;
  const step = (now) => {
    frame = 0;
    if (still || reduced || !visible) return;
    if (now - last >= 32) {
      t += Math.min(64, now - last) / 1000;
      last = now;
      const began = performance.now();
      draw();
      slow = performance.now() - began > 14 ? slow + 1 : 0;
      if (slow > 8) { still = true; return; }
    }
    frame = raf(step);
  };
  frame = raf(step);
}

self.onmessage = (event) => {
  const m = event.data;
  if (m.type === "start") {
    canvas = m.canvas;
    ctx = canvas.getContext("2d");
    colour = m.colour || colour;
    reduced = m.reduced;
    visible = m.visible;
    build();
    resize(m.width, m.ratio);
    draw();
    loop();
  } else if (m.type === "size") {
    resize(m.width, m.ratio);
    draw();
  } else if (m.type === "pointer") {
    tx = m.x;
    ty = m.y;
  } else if (m.type === "visible") {
    visible = m.value;
    if (visible) loop(); else stop();
  } else if (m.type === "reduced") {
    reduced = m.value;
    if (reduced) { stop(); draw(); } else loop();
  }
};
