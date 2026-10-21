/* Enhancement for the gallery page: packs the showcase's cards as on
   Pinterest in a browser without CSS grid-lanes (ADR-0016, Changes,
   2026-10-20). Every word is already in the HTML, and the page works
   without this file: the cards then sit in rows of the same columns
   (scope floor line 3). It stores nothing, sets no cookie and requests
   nothing (scope floor line 2).

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
