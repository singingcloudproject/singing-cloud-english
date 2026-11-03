// Singing Cloud — small helpers: mobile menu, header shadow, gentle reveal animation, contact form.
document.documentElement.classList.add("js");

// Mobile menu
const toggle = document.querySelector(".nav-toggle");
const nav = document.getElementById("site-nav");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!open));
    nav.classList.toggle("open", !open);
  });
  nav.addEventListener("click", (ev) => {
    if (ev.target.closest("a")) {
      toggle.setAttribute("aria-expanded", "false");
      nav.classList.remove("open");
    }
  });
}

// Header gets a thin line once you scroll
const header = document.querySelector(".site-header");
const onScroll = () => header && header.classList.toggle("scrolled", window.scrollY > 8);
window.addEventListener("scroll", onScroll, { passive: true });
onScroll();

// Fade sections in as they scroll into view
const items = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver(
    (entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
    }),
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );
  items.forEach((el) => io.observe(el));
} else {
  items.forEach((el) => el.classList.add("in"));
}

// Footer year
document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

/* ---------- the singing cloud (hero) ----------
   Same singer as Singing Cloud Studio: the mouth moves between "ah" (wide), "oh" (round) and "mm" (nearly closed)
   following a little melody of long held notes and quick phrases. On big notes the cloud stretches up and leans
   back with a brighter glow; between phrases it squashes down a little; it floats and sways the whole time.
   Instead of music notes, the letters A, B, C, D float out of its mouth one after another.
   Runs only while the hero is on screen; "reduce motion" shows a still pose with no letters. */
(() => {
  const stage = document.querySelector(".logo-stage");
  if (!stage) return;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const svg = stage.querySelector(".mascot");
  const body = svg.querySelector(".sc-body");
  const shadow = svg.querySelector(".sc-shadow");
  const mouthEls = [...svg.querySelectorAll(".sc-m")];
  const tongue = svg.querySelector(".sc-tongue");
  const glow = stage.querySelector(".art-glow");
  const lettersBox = stage.querySelector(".letters");

  // must match mascot.py
  const CX = 208, CY = 104, PX = 200, PY = 282, VB_X = -30, VB_Y = -40, VB_W = 460;
  const SHAPES = { rest: [118, 108, 20], ah: [124, 122, 22], oh: [74, 106, -58], oo: [52, 60, -40], eh: [110, 62, 16], mm: [86, 7, 8] };
  // the melody: [mouth shape, seconds, how big the note is 0–1]
  const MELODY = [
    ["mm", 0.8, 0], ["ah", 2.1, 1],
    ["mm", 0.2, 0], ["oh", 0.34, 0.25], ["eh", 0.26, 0.2], ["ah", 0.32, 0.3], ["oo", 0.38, 0.25],
    ["mm", 0.6, 0], ["oh", 1.7, 0.8],
    ["eh", 0.24, 0.2], ["ah", 0.3, 0.35], ["mm", 0.18, 0], ["ah", 0.34, 0.3], ["oo", 0.32, 0.2],
    ["mm", 0.9, 0], ["ah", 2.5, 1], ["oh", 0.55, 0.5], ["mm", 1.3, 0],
  ];
  // the letters and their soft, friendly colours (sky blue, warm gold, coral, mint)
  const LETTERS = [["A", "#4a9ee0"], ["B", "#e2a942"], ["C", "#ee8a6a"], ["D", "#4fb58a"]];

  const mouthPath = (w, h, t) =>
    `M${(CX - w).toFixed(1)} ${CY}C${(CX - w * 0.55).toFixed(1)} ${(CY + t).toFixed(1)} ${(CX + w * 0.55).toFixed(1)} ${(CY + t).toFixed(1)} ${(CX + w).toFixed(1)} ${CY}` +
    `C${(CX + w).toFixed(1)} ${(CY + h * 1.33).toFixed(1)} ${(CX - w).toFixed(1)} ${(CY + h * 1.33).toFixed(1)} ${(CX - w).toFixed(1)} ${CY}Z`;
  const approach = (cur, target, speed, dt) => cur + (target - cur) * (1 - Math.exp(-speed * dt));

  const mouth = [...SHAPES.rest];
  const s = { stretch: 0, lean: 0, lift: 0, power: 0 };
  let note = 0, noteTime = 0, time = 0, leanDir = 1, letterIndex = 0, lastLetter = -9;
  let pose = { w: SHAPES.rest[0], h: SHAPES.rest[1], float: 0, drift: 0 };

  const render = (w, h, t, float, drift, sway) => {
    const sy = 1 + s.stretch, sx = 1 - s.stretch * 0.55;
    body.setAttribute("transform",
      `translate(${(PX + drift).toFixed(2)} ${(PY + float + s.lift).toFixed(2)}) rotate(${(s.lean + sway).toFixed(2)}) scale(${sx.toFixed(4)} ${sy.toFixed(4)}) translate(${-PX} ${-PY})`);
    const d = mouthPath(w, h, t);
    mouthEls.forEach((el) => el.setAttribute("d", d));
    tongue.setAttribute("transform", `translate(${CX} ${(CY + h * 0.8).toFixed(1)}) scale(${(w * 0.46).toFixed(2)} ${(Math.max(h, 1) * 0.4).toFixed(2)})`);
    const up = Math.max(0, -(float + s.lift)) / 30;
    shadow.setAttribute("transform", `translate(${(drift * 0.5).toFixed(2)} 0) translate(200 312) scale(${(1 - up * 0.35).toFixed(3)} 1) translate(-200 -312)`);
    shadow.setAttribute("opacity", (1 - up * 0.5).toFixed(3));
    glow.style.opacity = (0.55 + 0.45 * s.power).toFixed(3);
    glow.style.transform = `translate3d(${(drift * 0.4).toFixed(1)}px, ${((float + s.lift) * 0.5).toFixed(1)}px, 0) scale(${(0.92 + 0.16 * s.power).toFixed(3)})`;
    pose = { w, h, float: float + s.lift, drift };
  };

  // a letter pops out of the mouth, drifts up in a soft colour and fades away
  const sendLetter = () => {
    if (lettersBox.childElementCount > 5) return;
    const st = stage.getBoundingClientRect(), r = svg.getBoundingClientRect();
    const k = r.width / VB_W;
    const x0 = r.left - st.left + (CX - VB_X + pose.drift) * k;
    const y0 = r.top - st.top + (CY - VB_Y + pose.h * 0.45 + pose.float) * k;
    const [ch, colour] = LETTERS[letterIndex++ % LETTERS.length];
    const el = document.createElement("span");
    el.className = "letter";
    el.textContent = ch;
    const side = letterIndex % 2 ? 1 : -1;                          // alternate left / right
    el.style.cssText =
      `--c:${colour};--x0:${x0.toFixed(1)}px;--y0:${y0.toFixed(1)}px;` +
      `--dx:${(side * (40 + Math.random() * 60) * k * 2.2).toFixed(1)}px;--rise:${((150 + Math.random() * 60) * k * 2.2).toFixed(1)}px;` +
      `--r:${(side * (6 + Math.random() * 10)).toFixed(1)}deg;--dur:${(3.1 + Math.random() * 0.8).toFixed(2)}s`;
    el.addEventListener("animationend", () => el.remove());
    lettersBox.appendChild(el);
  };

  const frame = (dt) => {
    time += dt;
    noteTime += dt;
    let [shape, dur, power] = MELODY[note];
    if (noteTime >= dur) {
      noteTime -= dur;
      note = (note + 1) % MELODY.length;
      [shape, dur, power] = MELODY[note];
      if (dur >= 1 && power > 0.5) leanDir = -leanDir;
      if (shape !== "mm" && time - lastLetter > 0.6) { lastLetter = time; setTimeout(sendLetter, 120); } // once the mouth has opened
    }
    const long = dur >= 1;
    const target = SHAPES[shape];
    const speed = shape === "mm" ? 14 : long ? 6 : 18;
    for (let i = 0; i < 3; i++) mouth[i] = approach(mouth[i], target[i], speed, dt);
    let vib = 0;
    if (long && power > 0) vib = Math.sin(time * 2 * Math.PI * 5.4) * Math.min(1, Math.max(0, (noteTime - 0.5) / 0.6)) * power;
    const held = long ? Math.min(1, noteTime / (dur * 0.6)) : 1;
    let tStretch, tLean, tLift;
    if (shape === "mm") { tStretch = -0.045; tLean = 0; tLift = 5; }
    else { tStretch = 0.015 + 0.075 * power * held; tLean = -5.5 * power * held * leanDir; tLift = -14 * power * held; }
    s.stretch = approach(s.stretch, tStretch, long ? 2.4 : 5, dt);
    s.lean = approach(s.lean, tLean, 2.2, dt);
    s.lift = approach(s.lift, tLift, 2.8, dt);
    s.power = approach(s.power, shape === "mm" ? 0 : power, 3, dt);
    render(mouth[0] + vib * 2, Math.max(2, mouth[1] + vib * 5), mouth[2], Math.sin(time * 1.05) * 7, Math.sin(time * 0.62) * 6, Math.sin(time * 1.3) * 1.8);
  };

  render(...SHAPES.rest, 0, 0, 0); // still pose (also what "reduce motion" users see)
  if (reduce) return;

  let raf = 0, last = 0, running = false, visible = true;
  const loop = (now) => {
    frame(Math.min(0.05, (now - last) / 1000));
    last = now;
    raf = requestAnimationFrame(loop);
  };
  const start = () => { if (!running) { running = true; last = performance.now(); raf = requestAnimationFrame(loop); } };
  const stop = () => { running = false; cancelAnimationFrame(raf); };
  // pause while the hero is off screen or the tab is hidden — saves battery on phones
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(([en]) => { visible = en.isIntersecting; visible && !document.hidden ? start() : stop(); })
      .observe(stage.closest(".hero") || stage);
  } else start();
  document.addEventListener("visibilitychange", () => (document.hidden || !visible ? stop() : start()));
})();

// "Teach with us" form: the ticked lessons are sent together as one field ("Conversation, IELTS, …")
document.querySelectorAll("form.form").forEach((form) => {
  const hidden = form.querySelector('input[name="lessons"]');
  if (!hidden) return;
  const sync = () => (hidden.value = [...form.querySelectorAll('[data-join="lessons"]:checked')].map((c) => c.value).join(", "));
  form.addEventListener("change", sync);
  form.addEventListener("reset", () => setTimeout(sync));
});

// Contact form → Formspree (sends without leaving the page)
document.querySelectorAll("form.form").forEach((form) => {
  const status = form.querySelector(".form-status");
  const button = form.querySelector("button[type=submit]");
  const label = button.textContent;
  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    status.className = "form-status";
    if (form.dataset.connected !== "true") {
      status.textContent = form.dataset.notConnected;
      status.classList.add("err");
      return;
    }
    button.disabled = true;
    button.textContent = form.dataset.sending;
    try {
      const res = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" },
      });
      if (!res.ok) throw new Error(res.status);
      form.reset();
      status.textContent = form.dataset.success;
      status.classList.add("ok");
    } catch (err) {
      status.textContent = form.dataset.error;
      status.classList.add("err");
    } finally {
      button.disabled = false;
      button.textContent = label;
    }
  });
});
