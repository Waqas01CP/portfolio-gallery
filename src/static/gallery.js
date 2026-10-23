/* Enhancements for the gallery page. Every word is already in the HTML,
   and the page works without this file (scope floor line 3). It stores
   nothing, sets no cookie and requests nothing from another site (scope
   floor line 2).

   First, packing: the showcase's cards as on Pinterest in a browser
   without CSS grid-lanes (ADR-0016, Changes, 2026-10-20); without this
   file the cards sit in rows of the same columns.

   Each card, in folder order, goes to the column whose bottom is highest,
   the leftmost of equals, as grid-lanes places them: so no card sits above
   the one before it, and the eye meets the cards in the order a keyboard
   and a screen reader do. The columns are the ones gallery.css lays out,
   read from the list's own grid, so the two never disagree. Every picture
   has its size in the HTML, so a card's height is known before its
   picture loads. No animation frame is requested, under any setting. */
(() => {
  "use strict";

  const list = document.querySelector("[data-pack]");
  if (!list || !window.CSS || CSS.supports("display", "grid-lanes") || !window.ResizeObserver) return;
  const cards = Array.from(list.children);

  const unpack = () => {
    list.classList.remove("is-packed");
    list.style.height = "";
    for (const card of cards) {
      card.style.left = card.style.top = card.style.width = "";
    }
  };

  const pack = () => {
    const style = getComputedStyle(list);
    // The grid's columns as laid out, in pixels: "345.333px 345.333px ...".
    const columns = style.gridTemplateColumns.split(" ").map(parseFloat).filter((w) => w > 0);
    if (columns.length < 2) {
      unpack();
      return;
    }
    const columnGap = parseFloat(style.columnGap) || 0;
    const rowGap = parseFloat(style.rowGap) || 0;
    const lefts = [];
    columns.reduce((left, width) => (lefts.push(left), left + width + columnGap), 0);
    list.classList.add("is-packed");
    // Widths first, then every height in one read, then the places.
    cards.forEach((card) => { card.style.width = `${columns[0]}px`; });
    const heights = cards.map((card) => card.getBoundingClientRect().height);
    const bottoms = columns.map(() => 0);
    cards.forEach((card, i) => {
      let column = 0;
      for (let c = 1; c < bottoms.length; c += 1) {
        if (bottoms[c] < bottoms[column]) column = c;
      }
      card.style.left = `${lefts[column]}px`;
      card.style.top = `${bottoms[column]}px`;
      bottoms[column] += heights[i] + rowGap;
    });
    list.style.height = `${Math.max(...bottoms) - rowGap}px`;
  };

  pack();
  // Again when the list's width or a card's height changes, as with the
  // window's size or the text's. Later, not inside the observer's own
  // callback, so a change it makes is never reported as a loop.
  // A pass that changes nothing changes no size, so the observer settles.
  let pending = false;
  const observer = new ResizeObserver(() => {
    if (pending) return;
    pending = true;
    setTimeout(() => {
      pending = false;
      pack();
    }, 0);
  });
  observer.observe(list);
  cards.forEach((card) => observer.observe(card));
})();

/* Second, the showcase's larger copy in an overlay on the gallery (Brief
   13, Addendum 1; ADR-0016, Changes, 2026-10-23). A click on a card's
   picture, or Enter on it, opens the page's own <dialog> with showModal():
   the browser makes the rest of the page inert, keeps focus inside, and
   closes it on Escape. Its Close button, and a click outside the picture,
   close it too; focus then returns to the card's link. The picture is the
   same file the link opens, shown whole at its own size within the window,
   with its size set before it loads; nothing moves. A click that asks for
   a new tab or window, and a browser without showModal, keep the plain
   link. */
(() => {
  "use strict";

  const view = document.querySelector("[data-view]");
  if (!view || typeof view.showModal !== "function") return;
  const name = view.querySelector("[data-view-name]");
  const close = view.querySelector("[data-view-close]");
  let opener = null;
  let picture = null;

  document.querySelectorAll(".g-site .g-frame").forEach((link) => {
    link.addEventListener("click", (event) => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const [width, height] = (link.dataset.full || "").split("x").map(Number);
      picture = document.createElement("img");
      picture.className = "g-view-pic";
      if (width && height) {
        picture.width = width;
        picture.height = height;
      }
      picture.alt = link.querySelector("img").alt;
      picture.src = link.getAttribute("href");
      view.append(picture);
      name.textContent = link.closest(".g-site").querySelector(".g-name").textContent.trim();
      opener = link;
      view.showModal();
      if (close) close.focus();
    });
  });

  if (close) close.addEventListener("click", () => view.close());
  // A click outside the picture lands on the dialog itself, or on its
  // backdrop, which reports the dialog as its target.
  view.addEventListener("click", (event) => {
    if (event.target === view) view.close();
  });
  view.addEventListener("close", () => {
    if (picture) picture.remove();
    picture = null;
    if (opener) opener.focus();
    opener = null;
  });
})();
