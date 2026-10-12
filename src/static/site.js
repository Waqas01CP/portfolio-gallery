/* Enhancement for the page. Every word is already in the HTML, and the
   page works without this file: it only reveals, filters and animates
   (scope floor line 3). It stores nothing on the visitor's device, sets no
   cookie and makes no request but for its own knot.js (scope floor
   line 2).

   Under prefers-reduced-motion nothing moves and no animation frame is
   requested: the knot is drawn once and left still, the strip does not
   start, cards do not tilt, and the scroll effects are off. The knot
   itself is knot.js, beside this file, in a worker.

   The same file serves every design. A design turns the four heavy
   effects and the theme switch on or off with custom properties on :root,
   1 or 0 (docs/reference/design-contract.md); this file reads them once
   the styles are in. */
(() => {
  "use strict";

  const doc = document;
  const root = doc.documentElement;
  // Where this file was loaded from, so the worker beside it is found at
  // any address the site is served from (ADR-0007).
  const here = doc.currentScript ? doc.currentScript.src : location.href;
  // The design's switches. Unset means on.
  const designSays = (name) => getComputedStyle(root).getPropertyValue(name).trim() !== "0";
  const HEAVY = { knot: true, tilt: true, strip: true, scroll: true };
  const $ = (selector, scope = doc) => scope.querySelector(selector);
  const $$ = (selector, scope = doc) => Array.from(scope.querySelectorAll(selector));
  const motionQuery = matchMedia("(prefers-reduced-motion: reduce)");
  const darkQuery = matchMedia("(prefers-color-scheme: dark)");
  const wideQuery = matchMedia("(min-width: 1180px)");
  let reduced = motionQuery.matches;

  // A frame for work driven by scrolling. Under reduced motion a timer
  // stands in, so no animation frame is ever requested.
  const nextFrame = (fn) => (reduced ? setTimeout(fn, 50) : requestAnimationFrame(fn));

  // Shows or hides an element inside the sections. A section that skips
  // its layout (content-visibility in base.css) has no style yet, and at
  // load Chromium's full accessibility tree, the one a screen reader reads,
  // then exposes what `hidden` or CSS hides there, the closed "In depth"
  // panels among it. aria-hidden is read from the DOM, so it holds there,
  // and it changes with `hidden`; a shown element carries none. Measured on
  // the site this engine was copied from (docs/reference/provenance.md),
  // and checked for every design by tools/check_browser.py.
  const setShown = (el, shown) => {
    el.hidden = !shown;
    if (shown) el.removeAttribute("aria-hidden");
    else el.setAttribute("aria-hidden", "true");
  };

  // Controls that need a script start hidden, and inside the sections also
  // aria-hidden. The rail outside them keeps its aria-hidden: decoration.
  root.classList.add("js");
  $$("[data-js]").forEach((el) => {
    if (el.closest("[data-section]")) setShown(el, true);
    else el.hidden = false;
  });

  /* Theme. The page follows the device; the switch overrides it for this
     visit only, by an attribute on <html> that a reload discards. A design
     with one theme sets --pg-theme to 0, and the switch stays hidden. */
  const switches = $$("[data-theme-switch]");
  if (!designSays("--pg-theme")) switches.forEach((s) => { s.hidden = true; });
  const pageDark = () => (root.dataset.theme ? root.dataset.theme === "dark" : darkQuery.matches);
  const syncTheme = () => switches.forEach((s) => s.setAttribute("aria-checked", String(pageDark())));
  switches.forEach((s) => s.addEventListener("click", () => {
    root.dataset.theme = pageDark() ? "light" : "dark";
    syncTheme();
  }));
  darkQuery.addEventListener("change", syncTheme);
  syncTheme();

  /* Section menu: the section in view is marked, and the menu takes the
     Intro's dark colours while the Intro is in view. */
  const sections = $$("[data-section]");
  const navLinks = $$("[data-nav-link]");
  const navBoxes = $$("[data-nav-box]");
  const activeN = $("[data-active-n]");
  const activeLabel = $("[data-active-label]");
  const mnav = $("[data-mnav]");
  const ticks = $$("[data-tick]");
  const labelOf = (id) => {
    const link = navLinks.find((a) => a.dataset.navLink === id);
    return link ? link.lastChild.textContent.trim() : id;
  };
  function setActive(id) {
    navLinks.forEach((a) => {
      if (a.dataset.navLink === id) a.setAttribute("aria-current", "location");
      else a.removeAttribute("aria-current");
    });
    const index = sections.findIndex((s) => s.id === id);
    if (activeN) activeN.textContent = String(index + 1).padStart(2, "0");
    if (activeLabel) activeLabel.textContent = labelOf(id);
    navBoxes.forEach((box) => box.classList.toggle("dark", id === "intro"));
    ticks.forEach((t) => t.classList.toggle("on", t.dataset.tick === id));
  }
  const sectionWatch = new IntersectionObserver((entries) => {
    entries.forEach((entry) => { if (entry.isIntersecting) setActive(entry.target.id); });
  }, { rootMargin: "-45% 0px -50% 0px" });
  sections.forEach((s) => sectionWatch.observe(s));
  // Which sections are on screen at all, for the scroll effects below.
  const sectionWatchFx = new IntersectionObserver((changes) => {
    changes.forEach((c) => { if (c.isIntersecting) onScreen.add(c.target); else onScreen.delete(c.target); });
  });

  if (mnav) {
    $$("a", mnav).forEach((a) => a.addEventListener("click", () => { mnav.open = false; }));
    doc.addEventListener("click", (e) => { if (mnav.open && !mnav.contains(e.target)) mnav.open = false; });
  }

  /* Progress: the rail on a wide screen, the bar's underline on a phone. */
  const pcts = $$("[data-pct]");
  const railFill = $("[data-rail-fill]");
  const pill = $("[data-mbar-pill]");
  function placeTicks() {
    const height = root.scrollHeight - innerHeight;
    if (height <= 0) return;
    ticks.forEach((t) => {
      const section = doc.getElementById(t.dataset.tick);
      if (!section) return;
      const at = (section.getBoundingClientRect().top + scrollY) / height;
      t.style.setProperty("--t", Math.min(1, Math.max(0, at)).toFixed(4));
    });
  }
  function updateProgress() {
    const height = root.scrollHeight - innerHeight;
    const p = height > 0 ? Math.min(1, Math.max(0, scrollY / height)) : 0;
    const text = Math.round(p * 100) + "%";
    pcts.forEach((el) => { el.textContent = text; });
    if (railFill) railFill.style.setProperty("--p", p.toFixed(4));
    if (pill) pill.style.setProperty("--p", p.toFixed(4));
  }

  /* Projects: each "In depth" panel starts closed, opens as a full-width
     panel under its card's row, and only one is open at a time. */
  const depthToggles = $$("[data-depth-toggle]");
  const panelOf = (toggle) => doc.getElementById(toggle.getAttribute("aria-controls"));
  function setDepth(toggle, open) {
    const panel = panelOf(toggle);
    toggle.setAttribute("aria-expanded", String(open));
    setShown(panel, open);
    toggle.closest(".proj").classList.toggle("is-open", open);
  }
  depthToggles.forEach((toggle) => {
    setDepth(toggle, false);
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") !== "true";
      depthToggles.forEach((other) => { if (other !== toggle) setDepth(other, false); });
      setDepth(toggle, open);
      placeTicks();
      if (!open) return;
      const panel = panelOf(toggle);
      const top = panel.getBoundingClientRect().top;
      if (top > innerHeight * 0.78) {
        scrollTo({ top: scrollY + top - innerHeight * 0.3, behavior: reduced ? "auto" : "smooth" });
      }
    });
  });
  $$("[data-depth-close]").forEach((button) => button.addEventListener("click", () => {
    const toggle = doc.getElementById("toggle-" + button.dataset.depthClose);
    // Focus leaves the panel before it is hidden, so it never rests inside
    // an aria-hidden element.
    toggle.focus({ preventScroll: true });
    setDepth(toggle, false);
    placeTicks();
    const card = toggle.closest(".proj");
    card.scrollIntoView({ block: "start", behavior: reduced ? "auto" : "smooth" });
  }));

  /* Timeline: each entry's detail is a native disclosure. On a wide screen
     it opens as a card under the entry's title; Escape or a click elsewhere
     closes it. The lane filters hide and show lanes. */
  const tl = $("[data-tl]");
  const cards = tl ? $$("[data-tl-card]", tl) : [];
  const entries = tl ? $$(".tl-entry", tl) : [];
  function placePop(card) {
    const summary = $("summary", card);
    const shown = $$(":scope > span", summary).filter((el) => el.offsetParent && el.offsetHeight > 1);
    const last = shown[shown.length - 1];
    if (last) card.style.setProperty("--pop", (last.offsetTop + last.offsetHeight + 8) + "px");
  }
  cards.forEach((card) => {
    card.addEventListener("toggle", () => {
      card.closest(".tl-entry").classList.toggle("is-open", card.open);
      if (card.open && wideQuery.matches) placePop(card);
      if (!card.open) card.style.removeProperty("--pop");
      placeTicks();
    });
  });
  const closeCard = (card, focus) => {
    card.open = false;
    if (focus) $("summary", card).focus({ preventScroll: true });
  };
  $$("[data-tl-close]").forEach((b) => b.addEventListener("click", () => closeCard(b.closest("details"), true)));
  $$("[data-tl-go]").forEach((a) => a.addEventListener("click", () => closeCard(a.closest("details"), false)));
  doc.addEventListener("click", (e) => {
    if (!wideQuery.matches) return;
    cards.forEach((card) => { if (card.open && !card.contains(e.target)) closeCard(card, false); });
  });
  doc.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    const open = cards.find((card) => card.open);
    if (open) closeCard(open, true);
    if (mnav && mnav.open) {
      mnav.open = false;
      $("summary", mnav).focus();
    }
  });

  const filters = tl ? $$("[data-lane]", tl).filter((el) => el.tagName === "BUTTON") : [];
  const empty = $("[data-tl-empty]");
  function applyFilters() {
    const hidden = filters.filter((b) => b.getAttribute("aria-pressed") === "false").map((b) => b.dataset.lane);
    tl.dataset.hide = hidden.join(" ");
    if (empty) setShown(empty, hidden.length === filters.length);
    // The year pill on a phone marks the first shown entry of each year.
    const seen = new Set();
    entries.forEach((entry) => {
      const shown = !hidden.includes(entry.dataset.lane);
      const first = shown && !seen.has(entry.dataset.year);
      if (first) seen.add(entry.dataset.year);
      entry.toggleAttribute("data-year-mark", first);
      if (!shown) $$("details[open]", entry).forEach((d) => { d.open = false; });
    });
    measure();
    placeTicks();
  }
  filters.forEach((b) => b.addEventListener("click", () => {
    b.setAttribute("aria-pressed", String(b.getAttribute("aria-pressed") === "false"));
    applyFilters();
  }));

  /* The design's switches, read now that the styles are in. */
  HEAVY.knot = designSays("--pg-knot");
  HEAVY.tilt = designSays("--pg-tilt");
  HEAVY.strip = designSays("--pg-strip");
  HEAVY.scroll = designSays("--pg-scroll");

  /* Heavy element: card tilt and lift, by pointer and by touch. */
  if (HEAVY.tilt) {
    $$("[data-tilt]").forEach((card) => {
      const glare = $(":scope > .glare", card);
      const tilt = (e) => {
        if (reduced) return;
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width;
        const y = (e.clientY - r.top) / r.height;
        const k = Math.min(1, 380 / r.width);
        const lift = e.pointerType === "touch" ? 2 : 4;
        card.style.transform = "perspective(1000px) rotateX(" + ((0.5 - y) * 7 * k).toFixed(2) +
          "deg) rotateY(" + ((x - 0.5) * 9 * k).toFixed(2) + "deg) translateY(-" + lift + "px)";
        card.style.setProperty("--mx", (x * 100).toFixed(1) + "%");
        card.style.setProperty("--my", (y * 100).toFixed(1) + "%");
        if (glare) glare.style.opacity = "1";
      };
      const untilt = () => {
        card.style.transform = "";
        if (glare) glare.style.opacity = "";
      };
      card.addEventListener("pointermove", tilt);
      card.addEventListener("pointerdown", tilt);
      card.addEventListener("pointerleave", untilt);
      card.addEventListener("pointercancel", untilt);
      card.addEventListener("pointerup", (e) => { if (e.pointerType === "touch") untilt(); });
    });
  }
  const untiltAll = () => $$("[data-tilt]").forEach((card) => {
    card.style.transform = "";
    const glare = $(":scope > .glare", card);
    if (glare) glare.style.opacity = "";
  });

  /* Heavy element: scroll effects. The spine fills as the page passes it,
     a reading line marks the month at 55% of the viewport on a wide
     screen, and the faded section words drift.

     The sections below the Intro skip their layout while off screen
     (content-visibility in base.css). Reading a position inside one would
     force that layout and undo the saving, so positions are read only in
     sections that are on screen, which are laid out already. */
  const spineFill = $("[data-spine-fill]");
  const mspineFill = $("[data-mspine-fill]");
  const readLine = $("[data-tl-read]");
  const chip = $("[data-tl-chip]");
  const list = $("[data-tl-list]");
  const marks = tl ? $$(".tl-mark", tl) : [];
  const fadeWords = $$("[data-fade-word]");
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  let topMonth = 0;
  let months = 1;
  if (tl) {
    const [year, month] = tl.dataset.top.split("-").map(Number);
    topMonth = year * 12 + month - 1;
    months = Number(tl.dataset.months);
  }
  const onScreen = new Set();
  const timelineSection = tl ? tl.closest("[data-section]") : null;
  const timelineShown = () => timelineSection && onScreen.has(timelineSection);
  let spans = [];
  function measure() {
    if (!list || !timelineShown()) return;
    const listTop = list.getBoundingClientRect().top;
    spans = entries.map((entry) => {
      const box = entry.getBoundingClientRect();
      return { card: $(".tl-card", entry), y0: box.top - listTop, y1: box.bottom - listTop };
    });
  }
  new IntersectionObserver((changes) => {
    changes.forEach((c) => { if (c.isIntersecting) onScreen.add(c.target); else onScreen.delete(c.target); });
    if (!ready) return;
    measure();
    onScroll();
  }).observe(timelineSection || doc.body);
  sections.forEach((section) => { if (section !== timelineSection) sectionWatchFx.observe(section); });
  function clearScrollFx() {
    [spineFill, mspineFill].forEach((f) => { if (f) f.style.transform = ""; });
    if (readLine) readLine.style.opacity = "";
    if (chip) chip.style.opacity = "";
    spans.forEach((s) => { if (s.card) s.card.style.outline = ""; });
    marks.forEach((m) => m.classList.remove("lit"));
    fadeWords.forEach((w) => { w.style.transform = ""; });
  }
  function updateScrollFx() {
    if (!HEAVY.scroll || reduced) return;
    const vh = innerHeight;
    const mid = vh * 0.55;
    // Every read before any write, so the browser lays out once.
    const words = fadeWords.filter((w) => onScreen.has(w.closest("[data-section]")))
      .map((w) => [w, w.parentElement.getBoundingClientRect().top]);
    if (list && timelineShown()) {
      const r = list.getBoundingClientRect();
      const wide = wideQuery.matches;
      const axisHeight = wide && readLine ? readLine.parentElement.getBoundingClientRect().height : 0;
      const lit = wide ? [] : marks.map((m) => m.getBoundingClientRect().top < mid);
      const fill = Math.min(1, Math.max(0, (mid - r.top) / r.height)).toFixed(4);
      const activeFill = wide ? spineFill : mspineFill;
      if (activeFill) activeFill.style.transform = "scaleY(" + fill + ")";
      if (wide && readLine && chip) {
        const y = mid - r.top;
        const on = y >= 0 && y < axisHeight;
        readLine.style.opacity = chip.style.opacity = on ? "1" : "0";
        if (on) {
          readLine.style.transform = "translateY(" + y.toFixed(1) + "px)";
          chip.style.transform = "translate(-50%, calc(" + y.toFixed(1) + "px - 50%))";
          const index = topMonth - Math.floor((y / axisHeight) * months);
          chip.textContent = monthNames[((index % 12) + 12) % 12] + " " + Math.floor(index / 12);
        }
        spans.forEach((s) => {
          const hit = on && y >= s.y0 && y <= s.y1;
          if (s.card) {
            s.card.style.outline = hit ? "2px solid var(--acc-ink)" : "";
            s.card.style.outlineOffset = hit ? "2px" : "";
          }
        });
      } else {
        marks.forEach((m, i) => m.classList.toggle("lit", lit[i]));
      }
    }
    words.forEach(([w, top]) => {
      const d = (top - vh / 2) / vh;
      w.style.transform = Math.abs(d) < 1.5 ? "translateX(" + (d * -5).toFixed(2) + "%)" : "";
    });
  }

  let queued = false;
  let ready = false;
  function onScroll() {
    if (!ready || queued) return;
    queued = true;
    nextFrame(() => {
      queued = false;
      updateProgress();
      updateScrollFx();
    });
  }
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", () => {
    if (!ready) return;
    measure();
    placeTicks();
    sizeKnot();
    onScroll();
  });

  /* Heavy element: the availability strip, set moving after load, with a
     pause control (WCAG 2.2.2). The control sits inside a section, so it is
     shown and hidden with setShown. */
  const strip = $("[data-strip]");
  let stripAnim = null;
  function startStrip() {
    if (!HEAVY.strip || reduced || !strip || stripAnim || !strip.animate) return;
    const still = $(".strip-static", strip);
    const button = $("[data-strip-pause]", strip);
    // On a phone the still line wraps; the moving one does not. Keep the
    // height, so nothing below the strip moves when it starts.
    strip.style.minHeight = strip.offsetHeight + "px";
    const track = doc.createElement("div");
    track.className = "strip-track";
    track.setAttribute("aria-hidden", "true");
    for (let g = 0; g < 2; g += 1) {
      const group = doc.createElement("div");
      group.className = "strip-group";
      for (let k = 0; k < 2; k += 1) {
        $$(":scope > *", still).forEach((node) => group.appendChild(node.cloneNode(true)));
        group.appendChild($(".sq", still).cloneNode(true));
      }
      track.appendChild(group);
    }
    strip.insertBefore(track, button);
    still.classList.add("vh");
    stripAnim = track.animate([{ transform: "translateX(0)" }, { transform: "translateX(-50%)" }],
      { duration: 52000, iterations: Infinity });
    setShown(button, true);
    button.classList.remove("paused");
    $("[data-strip-label]", button).textContent = "Pause";
    button.onclick = () => {
      const paused = stripAnim.playState === "paused";
      if (paused) stripAnim.play(); else stripAnim.pause();
      button.classList.toggle("paused", !paused);
      $("[data-strip-label]", button).textContent = paused ? "Pause" : "Play";
    };
  }
  function stopStrip() {
    if (!stripAnim) return;
    stripAnim.cancel();
    stripAnim = null;
    $(".strip-track", strip).remove();
    $(".strip-static", strip).classList.remove("vh");
    setShown($("[data-strip-pause]", strip), false);
    strip.style.minHeight = "";
  }

  /* Heavy element: the torus knot, drawn by knot.js in a worker on a
     canvas this page hands over, so neither its start nor its frames run on
     the main thread. Started after the content is visible, paused off
     screen and in a hidden tab, still under reduced motion. A browser that
     cannot hand a canvas to a worker gets no knot, and so does a design
     that hides the canvas or sets --pg-knot to 0. */
  const knotCanvas = $("[data-knot]");
  const hero = $("#intro");
  const knot = { worker: null, visible: true };
  const knotSize = () => ({ width: knotCanvas.clientWidth, ratio: devicePixelRatio || 1 });
  function tellKnot(message) {
    if (knot.worker) knot.worker.postMessage(message);
  }
  function startKnot() {
    if (!HEAVY.knot || !knotCanvas || knot.worker || !knotCanvas.transferControlToOffscreen || !window.Worker) return;
    if (getComputedStyle(knotCanvas).display === "none" || !knotCanvas.clientWidth) return;
    const offscreen = knotCanvas.transferControlToOffscreen();
    knot.worker = new Worker(new URL("knot.js", here));
    knot.worker.postMessage({
      type: "start", canvas: offscreen, ...knotSize(), reduced, visible: knot.visible && !doc.hidden,
      colour: getComputedStyle(hero).getPropertyValue("--knot").trim(),
    }, [offscreen]);
    knotCanvas.classList.add("on");
    new IntersectionObserver(([entry]) => {
      knot.visible = entry.isIntersecting;
      tellKnot({ type: "visible", value: knot.visible && !doc.hidden });
    }).observe(knotCanvas);
  }
  function sizeKnot() {
    if (knot.worker) tellKnot({ type: "size", ...knotSize() });
  }
  if (hero) {
    hero.addEventListener("pointermove", (e) => {
      if (!knot.worker) return;
      const r = hero.getBoundingClientRect();
      tellKnot({ type: "pointer", x: (e.clientX - r.left) / r.width - 0.5, y: (e.clientY - r.top) / r.height - 0.5 });
    });
  }
  doc.addEventListener("visibilitychange", () => tellKnot({ type: "visible", value: knot.visible && !doc.hidden }));

  /* Reduced motion can change while the page is open. */
  motionQuery.addEventListener("change", (e) => {
    reduced = e.matches;
    tellKnot({ type: "reduced", value: reduced });
    if (reduced) {
      stopStrip();
      untiltAll();
      clearScrollFx();
    } else {
      startStrip();
      onScroll();
    }
  });

  /* Start. Nothing above reads the layout. The first measurement waits
     until the page has loaded and the browser is idle, together with the
     motion, so the content is on screen before anything is measured or
     moves, and the page is laid out once rather than once per reading. */
  const later = () => {
    const idle = window.requestIdleCallback || ((fn) => setTimeout(fn, 300));
    idle(() => {
      ready = true;
      measure();
      placeTicks();
      updateProgress();
      updateScrollFx();
      startKnot();
      startStrip();
      if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(() => { measure(); placeTicks(); });
    }, { timeout: 1500 });
  };
  if (doc.readyState === "complete") later();
  else addEventListener("load", later, { once: true });
})();
