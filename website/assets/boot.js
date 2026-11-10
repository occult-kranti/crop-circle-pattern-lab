/* boot.js — static-host resource assembler for the Crop Circles site.
   The repo ships large files as <path>.parts/part_NNN chunks and binaries as base64
   sidecars (a transport constraint, not a content choice). This loader makes the site
   work identically on GitHub Pages and on any static server:
   - tries the whole file first (fast path when present),
   - falls back to sequential .parts chunks,
   - bootEval()s JS, converts .b64 images to blob URLs.
   No dependencies. */
(function (g) {
  const pending = [];
  const readyFns = [];
  let armed = false;

  async function bootText(path) {
    try {
      const r = await fetch(path);
      if (r.ok) return await r.text();
    } catch (e) { /* fall through to parts */ }
    const out = [];
    for (let i = 0; ; i++) {
      const p = await fetch(`${path}.parts/part_${String(i).padStart(3, "0")}`);
      if (!p.ok) break;
      out.push(await p.text());
      if (i > 500) throw new Error("runaway parts loop: " + path);
    }
    if (!out.length) throw new Error("boot: cannot load " + path);
    return out.join("");
  }

  async function bootEval(path) {
    let src = await bootText(path);
    // indirect eval runs in global scope, but top-level const/let do NOT bind globals.
    // Our data files are generated with top-level const — demote to var for global binding.
    src = src.replace(/^(const|let)\s+/gm, "var ");
    (0, eval)(src + "\n//# sourceURL=" + path); // indirect eval → global scope
  }

  async function bootImageURL(path) {
    // path like assets/cymatics/x.jpg — try real file, else .b64 (possibly chunked)
    try {
      const r = await fetch(path, { method: "HEAD" });
      if (r.ok) return path;
    } catch (e) {}
    const b64 = (await bootText(path + ".b64")).trim();
    const bin = atob(b64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return URL.createObjectURL(new Blob([bytes], { type: "image/jpeg" }));
  }

  function load(paths) {
    for (const p of paths) pending.push(bootEval(p));
    arm();
  }
  function loadImages(selector) {
    pending.push((async () => {
      for (const el of document.querySelectorAll(selector || "img[data-boot-img]")) {
        el.src = await bootImageURL(el.dataset.bootImg);
      }
    })());
    arm();
  }
  function ready(fn) { readyFns.push(fn); arm(); }
  function arm() {
    if (armed) return;
    armed = true;
    Promise.all(pending).then(() => readyFns.forEach(f => f()))
      .catch(e => { console.error("boot failed:", e); readyFns.forEach(f => f()); });
  }
  // If nothing is registered, fire ready immediately on next tick.
  setTimeout(() => { if (!armed) arm(); }, 0);

  g.BOOT = { load, loadImages, ready, bootText, bootImageURL };
})(window);
