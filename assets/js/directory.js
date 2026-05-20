// TribalGaming.com — Directory page logic
// Filters, sort, search, interactive map pins.

(function () {
  const tribes = window.TRIBES || [];
  const pins = window.TRIBE_PINS || {};

  const $grid = document.getElementById("tribeGrid");
  const $count = document.getElementById("shownCount");
  const $total = document.getElementById("totalCount");
  const $totalProps = document.getElementById("totalProps");
  const $q = document.getElementById("q");
  const $sort = document.getElementById("sort");
  const $fsb = document.getElementById("fsb");
  const $mapPins = document.getElementById("pins");

  $total.textContent = tribes.length;
  $totalProps.textContent = tribes.reduce((s, t) => s + (t.properties || 0), 0);

  // Mark states that have operators
  const occupiedStates = new Set();
  tribes.forEach((t) => {
    (t.state || "").split("/").forEach((s) => occupiedStates.add(s.trim()));
  });
  document.querySelectorAll(".state").forEach((el) => {
    if (occupiedStates.has(el.dataset.state)) el.classList.add("has-casino");
    el.addEventListener("click", () => {
      $q.value = el.dataset.state;
      render();
      window.scrollTo({ top: $grid.offsetTop - 80, behavior: "smooth" });
    });
    el.addEventListener("mouseenter", () => {
      const s = el.dataset.state;
      el.setAttribute(
        "data-title",
        (tribes.filter((t) => (t.state || "").includes(s)).length || 0) + " operator(s) in " + s
      );
    });
  });

  // Render pins
  function renderPins(data) {
    $mapPins.innerHTML = "";
    const grouped = {};
    data.forEach((t) => {
      const key = (t.state || "").split("/")[0];
      if (!grouped[key]) grouped[key] = [];
      grouped[key].push(t);
    });
    Object.keys(grouped).forEach((k) => {
      // Translate our geographic pins (which were roughly laid out) into the map viewBox
      const p = getStateCenter(k);
      if (!p) return;
      const g = grouped[k];
      const r = Math.min(4 + Math.sqrt(g.length) * 2, 12);
      const pin = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      pin.setAttribute("cx", p.x);
      pin.setAttribute("cy", p.y);
      pin.setAttribute("r", r);
      pin.setAttribute("class", "pin");
      pin.setAttribute("data-state", k);
      const title = document.createElementNS("http://www.w3.org/2000/svg", "title");
      title.textContent = `${k}: ${g.length} operator${g.length > 1 ? "s" : ""}`;
      pin.appendChild(title);
      pin.addEventListener("click", () => {
        $q.value = k;
        render();
        window.scrollTo({ top: $grid.offsetTop - 80, behavior: "smooth" });
      });
      $mapPins.appendChild(pin);
    });
  }

  // Find center of a state path in the current SVG
  function getStateCenter(code) {
    const el = document.querySelector(`.state[data-state="${code}"]`);
    if (!el) return null;
    const b = el.getBBox();
    return { x: b.x + b.width / 2, y: b.y + b.height / 2 };
  }

  // Card
  function card(t) {
    const flag = t.country === "CA" ? "🇨🇦" : "🇺🇸";
    const cls =
      t.class === "FN"
        ? `<span class="pill blue">First Nations</span>`
        : `<span class="pill red">Class ${t.class}</span>`;
    const sb = t.sportsBetting && !/Not/i.test(t.sportsBetting)
      ? `<span class="pill green">Sports betting</span>`
      : "";
    return `
      <article class="tribe-card">
        <h3><a href="/directory/${t.slug}/">${t.name}</a></h3>
        <div class="loc">${flag} ${t.state} · ${t.region}${t.est ? " · Est. " + t.est : ""}</div>
        <div class="props">${t.headline}</div>
        <div class="tags">${cls}${sb}<span class="pill">${t.properties} ${t.properties === 1 ? "property" : "properties"}</span></div>
        <div class="small muted" style="margin-bottom:10px;">${t.highlight || ""}</div>
        <div class="actions">
          <a class="btn sm" href="/directory/${t.slug}/">View profile</a>
          <a class="btn sm ghost" href="/compare/?a=${t.slug}">Compare</a>
        </div>
      </article>`;
  }

  function getFilters() {
    const countries = [...document.querySelectorAll(".fctry")].filter((c) => c.checked).map((c) => c.value);
    const classes = [...document.querySelectorAll(".fcls")].filter((c) => c.checked).map((c) => c.value);
    return { countries, classes, sportsBetting: $fsb.checked, q: ($q.value || "").trim().toLowerCase(), sort: $sort.value };
  }

  function render() {
    const f = getFilters();
    let rows = tribes.filter((t) => {
      if (!f.countries.includes(t.country)) return false;
      if (!f.classes.some((c) => (t.class || "").includes(c))) return false;
      if (f.sportsBetting && (!t.sportsBetting || /Not/i.test(t.sportsBetting))) return false;
      if (f.q) {
        const hay = [t.name, t.state, t.region, t.headline, t.highlight, t.country].join(" ").toLowerCase();
        if (!hay.includes(f.q)) return false;
      }
      return true;
    });
    if (f.sort === "properties") rows.sort((a, b) => (b.properties || 0) - (a.properties || 0));
    else if (f.sort === "state") rows.sort((a, b) => (a.state || "").localeCompare(b.state || ""));
    else rows.sort((a, b) => a.name.localeCompare(b.name));

    $grid.innerHTML = rows.length
      ? rows.map(card).join("")
      : `<div style="grid-column:1/-1; padding:40px; text-align:center; color:var(--muted);">No operators match those filters. <a href="#" onclick="event.preventDefault(); resetFilters();">Reset</a></div>`;
    $count.textContent = rows.length;
    renderPins(rows);
  }

  window.resetFilters = function () {
    $q.value = "";
    $fsb.checked = false;
    document.querySelectorAll(".fctry, .fcls").forEach((c) => (c.checked = true));
    $sort.value = "name";
    render();
  };

  // Wire up
  document.querySelectorAll(".fctry, .fcls").forEach((el) => el.addEventListener("change", render));
  $fsb.addEventListener("change", render);
  $q.addEventListener("input", render);
  $sort.addEventListener("change", render);

  render();
})();
