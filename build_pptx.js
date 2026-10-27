// Build LaborForce_CookCountyHealth.pptx — mirrors E:\Claude\laborforce-deck\index.html slide for slide.
const path = require("path");
const pptxgen = require("pptxgenjs");
const SKILL = "C:/Users/Harvey/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/564b9f4b-3748-4da8-a6a7-464f9abeae50/5ec5e425-04f4-4052-959b-a3f31f8af806/skills/pptx";
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));

const OUT = process.argv[2] || "E:/Claude/laborforce-deck/LaborForce_CookCountyHealth.pptx";

// ---- brand tokens (from index.html :root, 2026-10-26 blue palette) ----
const NAVY = "0C3C75", TEAL = "0A8FA6", PAPER = "F4F6F9", SURFACE = "FFFFFF", INK = "15283D", INK2 = "4A5B6E",
  MUTED = "6E7E90", LINE = "D4DCE6", TEALL = "E0F1F6", PANEL = "E8EDF3", PANEL2 = "E8EDF3";
const TITLE_MUTED = "6A7F96";
// navy-slide palette (rgba values flattened over the navy)
const N_TEAL = "7FD3E3", N_TITLE_MUTED = "9FC0DC", N_BODY = "C3D2E3", N_MUTED = "94A9C0", N_LINE = "375F8F", N_SPAN = "C5D6E8", N_CALLOUT = "35B3C9";
const N_CARD = "1B487E", N_CARD_LINE = "2C5687", N_ASK = "1D4A7F", N_NOTE = "8EA4BB";
const LOGO = "E:/Claude/laborforce-deck/brand/logo_full_large.png"; // 1150x757 transparent PNG (aspect 1.519)

const THEME = {
  name: "LaborForce",
  headFontFace: "Segoe UI", bodyFontFace: "Segoe UI",
  colors: { dk1: INK, lt1: SURFACE, dk2: NAVY, lt2: PAPER, accent1: TEAL, accent2: TEALL, accent3: N_TEAL, accent4: INK2, accent5: MUTED, accent6: LINE, hlink: TEAL, folHlink: INK2 },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "LaborForce Medical Management";
pres.company = "LaborForce Medical Management";
pres.title = "LaborForce Medical Management — Cook County Health Executive Briefing";
pres.subject = "90-day TPL/Workers' Comp revenue-recovery pilot";

const W = 13.333, H = 7.5, M = 0.6, CW = W - 2 * M; // 12.133
const FONT = "Segoe UI";
const FOOT_Y = 6.98;

// ---- layouts ----
pres.defineSlideMaster({
  title: "LIGHT", background: { color: PAPER },
  objects: [
    { line: { x: M, y: FOOT_Y, w: CW, h: 0, line: { color: LINE, width: 0.75 } } },
    { text: { text: "LABORFORCE MEDICAL MANAGEMENT", options: { x: M, y: FOOT_Y + 0.08, w: 6, h: 0.25, fontFace: FONT, fontSize: 8, color: MUTED, charSpacing: 1.5, margin: 0, valign: "top" } } },
  ],
});
pres.defineSlideMaster({
  title: "NAVY", background: { color: NAVY },
  objects: [
    { line: { x: M, y: FOOT_Y, w: CW, h: 0, line: { color: N_LINE, width: 0.75 } } },
    { text: { text: "LABORFORCE MEDICAL MANAGEMENT", options: { x: M, y: FOOT_Y + 0.08, w: 6, h: 0.25, fontFace: FONT, fontSize: 8, color: N_MUTED, charSpacing: 1.5, margin: 0, valign: "top" } } },
  ],
});
pres.defineSlideMaster({ title: "COVER", background: { color: PAPER }, objects: [] });
pres.defineSlideMaster({
  title: "CLOSING", background: { color: NAVY },
  objects: [
    { line: { x: M, y: FOOT_Y, w: CW, h: 0, line: { color: N_LINE, width: 0.75 } } },
    { text: { text: "CONFIDENTIAL — FOR DISCUSSION PURPOSES", options: { x: M, y: FOOT_Y + 0.08, w: 6, h: 0.25, fontFace: FONT, fontSize: 8, color: N_MUTED, charSpacing: 1.5, margin: 0, valign: "top" } } },
  ],
});

// ---- helpers ----
function T(slide, text, x, y, w, h, o = {}) {
  const opts = Object.assign({ x, y, w, h, fontFace: FONT, fontSize: 11, color: INK, margin: 0, valign: "top", isTextBox: true, paraSpaceAfter: 0 }, o);
  slide.addText(text, opts);
}
function rect(slide, x, y, w, h, fill, o = {}) {
  slide.addShape(pres.ShapeType.rect, Object.assign({ x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 } }, o));
}
function rrect(slide, x, y, w, h, fill, radius = 0.04) {
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 }, rectRadius: radius });
}
function hline(slide, x, y, w, color = LINE, width = 0.75) {
  slide.addShape(pres.ShapeType.line, { x, y, w, h: 0, line: { color, width } });
}
function vline(slide, x, y, h, color = LINE, width = 0.75) {
  slide.addShape(pres.ShapeType.line, { x, y, w: 0, h, line: { color, width } });
}
function pageNo(slide, n, dark) {
  T(slide, `${String(n).padStart(2, "0")} / 08`, W - M - 2, FOOT_Y + 0.08, 2, 0.25, { fontSize: 8, color: dark ? N_MUTED : MUTED, align: "right", charSpacing: 1.5 });
}
function kicker(slide, n, label, dark) {
  const numColor = dark ? N_MUTED : MUTED, labColor = dark ? N_TEAL : TEAL;
  slide.addText([
    { text: `${n}`, options: { color: numColor, charSpacing: 0.5 } },
    { text: "   |   ", options: { color: dark ? N_LINE : LINE } },
    { text: label.toUpperCase(), options: { color: labColor, bold: true, charSpacing: 2 } },
  ], { x: M, y: 0.45, w: 9, h: 0.3, fontFace: FONT, fontSize: 9, margin: 0, valign: "top", isTextBox: true });
}
function title(slide, runs, y, h, size, dark, w = CW) {
  const mutedColor = dark ? N_TITLE_MUTED : TITLE_MUTED, mainColor = dark ? "FFFFFF" : NAVY;
  const arr = runs.map(r => ({ text: r.text, options: Object.assign({ color: r.muted ? mutedColor : mainColor }, r.breakLine ? { breakLine: true } : {}) }));
  slide.addText(arr, { x: M, y, w, h, fontFace: FONT, fontSize: size, bold: false, margin: 0, valign: "top", isTextBox: true, charSpacing: -1, lineSpacingMultiple: 1.0 });
}
function eyebrow(slide, text, x, y, w, dark, o = {}) {
  T(slide, text.toUpperCase(), x, y, w, 0.22, Object.assign({ fontSize: 8, bold: true, color: dark ? N_TEAL : TEAL, charSpacing: 1.5 }, o));
}
function callout(slide, label, runs, x, y, w, h, dark, size = 12.5) {
  rect(slide, x, y + 0.02, 0.035, h - 0.04, dark ? N_CALLOUT : TEAL);
  eyebrow(slide, label, x + 0.3, y, w - 0.3, dark);
  const arr = typeof runs === "string" ? runs : runs;
  T(slide, arr, x + 0.3, y + 0.3, w - 0.3, h - 0.3, { fontSize: size, color: dark ? N_BODY : INK2, lineSpacingMultiple: 1.15 });
}
function bullets(slide, items, x, y, w, h, o = {}) {
  const size = o.fontSize || 11;
  const arr = items.map((t, i) => ({ text: t, options: { bullet: { indent: 12, code: "25CF" }, breakLine: i < items.length - 1 } }));
  slide.addText(arr, Object.assign({ x, y, w, h, fontFace: FONT, fontSize: size, color: INK2, margin: 0, valign: "top", isTextBox: true, paraSpaceAfter: 5, lineSpacingMultiple: 1.12 }, o));
}

// ---- slides (v11: 8-slide index.html, commit ca21850, 2026-10-26) ----
const BRAND = "E:/Claude/laborforce-deck/brand";
const NM_LOGO = BRAND + "/nm_logo.svg", HPH_LOGO = BRAND + "/hph_logo.png";
const N_TOP = "1F4C80", N_TOP_LINE = "2F5A8D", N_BASE = "061F45", N_BASE_LINE = "2A4A72", N_MID = "0677AE", N_BASE_SPAN = "AEBFD6";

// =====================================================================
// SLIDE 1 — Cover
// =====================================================================
{
  const s = pres.addSlide({ masterName: "COVER" });
  const LW = 7.3;
  // hospital photo (62% x 84% of the slide, bottom-right), pre-faded toward the left / top / bottom (make_cover_photo.py)
  s.addImage({ path: BRAND + "/hospital_cover_faded.png", x: W - 8.27, y: H - 6.3, w: 8.27, h: 6.3 });
  // cover body, vertically centred in the left column (no facts row, no logo)
  T(s, "You Deliver Care, We Optimize Revenue.", M, 1.8, 6.0, 0.3, { fontSize: 12, color: TEAL, bold: true });
  s.addText([
    { text: "Uncovering revenue.", options: { color: NAVY, breakLine: true } },
    { text: "Strengthening hospital performance.", options: { color: TEAL } },
  ], { x: M, y: 2.15, w: LW, h: 1.95, fontFace: FONT, fontSize: 36, margin: 0, valign: "top", isTextBox: true, charSpacing: -1.5, lineSpacingMultiple: 0.98 });
  T(s, "A revenue identification and recovery partnership for Cook County Health's emergency and trauma care.", M, 4.2, 4.9, 0.95, { fontSize: 13, color: INK2, lineSpacingMultiple: 1.3 });
  // hospital partners: Northwestern Medicine | Humboldt Park Health
  const py = 5.05;
  T(s, "HOSPITAL PARTNERS", M, py, 4, 0.22, { fontSize: 8, bold: true, color: MUTED, charSpacing: 1.5 });
  const nmH = 0.31, nmW = nmH * 730 / 137, hpH = 0.44, hpW = hpH * 782 / 227, lcy = py + 0.3 + hpH / 2;
  s.addImage({ path: NM_LOGO, x: M, y: lcy - nmH / 2, w: nmW, h: nmH });
  vline(s, M + nmW + 0.28, lcy - 0.26, 0.52, LINE);
  s.addImage({ path: HPH_LOGO, x: M + nmW + 0.56, y: lcy - hpH / 2, w: hpW, h: hpH });
  hline(s, M, FOOT_Y, LW, LINE);
  T(s, "CONFIDENTIAL — FOR DISCUSSION PURPOSES", M, FOOT_Y + 0.08, 5, 0.25, { fontSize: 8, color: MUTED, charSpacing: 1.5 });
  T(s, "01 / 08", M + LW - 2, FOOT_Y + 0.08, 2, 0.25, { fontSize: 8, color: MUTED, align: "right", charSpacing: 1.5 });

  s.addNotes("Cover: one column, hospital photo on the right. The right-hand stats panel was removed on 2026-10-26 to match the web deck.");
}

// =====================================================================
// SLIDE 2 — Executive summary
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "02", "Executive summary", false);
  title(s, [{ text: "We work inside the revenue cycle" }, { text: " you already run.", muted: true }], 0.85, 0.7, 30, false);
  const items = [
    ["01 / Context", "The pressure", "Hospitals face reimbursement challenges, rising operational costs, complex payer requirements, and growing uncompensated care obligations.", false],
    ["02 / Opportunity", "The gap", "In ED, trauma and other encounters, Workers' Compensation, Third-Party Liability, auto and other responsible-party coverage can go unidentified or unpursued by traditional workflows.", false],
    ["03 / Support", "What LaborForce adds", "Specialized payer identification, patient engagement, revenue auditing, payer verification, and lien administration support.", false],
    ["04 / Outcome", "The goal", "Identify additional reimbursement, improve revenue realization, and reduce avoidable administrative work — without replacing current systems or teams.", true],
  ];
  const gy = 1.9, gap = 0.3, cw = (CW - 3 * gap) / 4;
  items.forEach(([eb, h3, p, goal], i) => {
    const x = M + i * (cw + gap);
    hline(s, x, gy, cw, LINE);
    eyebrow(s, eb, x, gy + 0.2, cw, false);
    T(s, h3, x, gy + 0.5, cw, 0.4, { fontSize: 17, bold: true, color: goal ? TEAL : NAVY, charSpacing: -0.5 });
    T(s, p, x, gy + 0.98, cw, 1.7, { fontSize: 12, color: INK2, lineSpacingMultiple: 1.3 });
  });
  const sy = 5.2;
  hline(s, M, sy, CW, LINE);
  eyebrow(s, "How it works", M, sy + 0.17, 3, false);
  const steps = [
    ["01", "Technology screening", "Injury-related encounters are flagged from existing registration and billing data."],
    ["02", "Specialist review", "Analysts determine the likely responsible payer and what information is missing."],
    ["03", "Direct patient contact", "Dedicated staff confirm the facts and close gaps, respecting each patient's choices."],
    ["04", "Follow-through", "Billing corrections, lien support, and payer follow-up until the account resolves."],
  ];
  steps.forEach(([n, h, p], i) => {
    const x = M + i * (cw + gap);
    T(s, n, x, sy + 0.5, 0.4, 0.22, { fontSize: 9, color: TEAL });
    T(s, h, x + 0.35, sy + 0.47, cw - 0.35, 0.28, { fontSize: 12, bold: true, color: NAVY });
    T(s, p, x + 0.35, sy + 0.77, cw - 0.35, 0.9, { fontSize: 10, color: INK2, lineSpacingMultiple: 1.2 });
  });
  pageNo(s, 2, false);
}

// =====================================================================
// SLIDE 3 — The challenge
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "03", "Where revenue slips", false);
  title(s, [{ text: "Revenue that traditional workflows may overlook." }], 0.85, 0.6, 30, false);
  T(s, "Patients often arrive after workplace incidents, motor vehicle accidents, or injuries involving another liable party. Registration and billing workflows may not consistently capture or resolve:", M, 1.5, 10.5, 0.6, { fontSize: 12, color: INK2, lineSpacingMultiple: 1.25 });
  const qs = [
    "Whether the injury occurred while the patient was working",
    "Whether a motor vehicle or other third party may be responsible",
    "Whether another insurer or payer should be investigated",
    "Whether the hospital has the right claim, attorney, or payer information",
    "Whether a hospital lien is available, documented, and followed up",
    "Whether unresolved cases need investigation after discharge",
  ];
  const qy = 2.25, flowW = 3.9, leftW = CW - flowW - 0.4, cgap = 0.12, cardW = (leftW - cgap) / 2, cardH = 0.92;
  qs.forEach((q, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = M + col * (cardW + cgap), y = qy + row * (cardH + cgap);
    rrect(s, x, y, cardW, cardH, PANEL, 0.04);
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.22, y: y + (cardH - 0.28) / 2, w: 0.28, h: 0.28, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
    T(s, String(i + 1).padStart(2, "0"), x + 0.22, y + (cardH - 0.28) / 2, 0.28, 0.28, { fontSize: 7.5, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T(s, q, x + 0.65, y, cardW - 0.85, cardH, { fontSize: 12.5, color: NAVY, lineSpacingMultiple: 1.2, valign: "middle" });
  });
  const gridH = 3 * cardH + 2 * cgap;
  const fx = M + leftW + 0.4;
  s.addShape(pres.ShapeType.roundRect, { x: fx, y: qy, w: flowW, h: gridH, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 }, rectRadius: 0.05 });
  eyebrow(s, "Where the revenue goes", fx + 0.22, qy + 0.22, flowW - 0.4, false);
  const flow = [
    ["Injury-related encounter", "Workplace injury, motor vehicle accident, or incident involving a third party", PANEL, NAVY, INK2],
    ["Responsible payer missed", "Not identified at registration, or identified but not followed through", PANEL, NAVY, INK2],
    ["Absorbed by the hospital", "Written off as bad debt or uncompensated care", NAVY, "FFFFFF", N_SPAN],
  ];
  const farrow = 0.22, fb0 = qy + 0.5, fbw = flowW - 0.44, fbH = (gridH - 0.5 - 0.16 - 2 * farrow) / 3;
  flow.forEach(([h, p, fill, hc, pc], i) => {
    const y = fb0 + i * (fbH + farrow);
    rrect(s, fx + 0.22, y, fbw, fbH, fill, 0.03);
    T(s, h, fx + 0.37, y + 0.07, fbw - 0.3, 0.24, { fontSize: 11.5, bold: true, color: hc, charSpacing: -0.2 });
    T(s, p, fx + 0.37, y + 0.3, fbw - 0.3, fbH - 0.32, { fontSize: 8.5, color: pc, lineSpacingMultiple: 1.05 });
    if (i < 2) s.addShape(pres.ShapeType.line, { x: fx + flowW / 2, y: y + fbH + 0.05, w: 0, h: farrow - 0.1, line: { color: TEAL, width: 1.25, endArrowType: "triangle" } });
  });
  const cy = qy + gridH + 0.24, chh = 0.66;
  rect(s, M, cy, CW, chh, TEALL);
  rect(s, M, cy, 0.05, chh, TEAL);
  eyebrow(s, "The consequence", M + 0.3, cy + 0.26, 1.8, false);
  T(s, "Valid reimbursement opportunities may remain unidentified, incorrectly routed, delayed, or insufficiently pursued.", M + 2.2, cy, CW - 2.5, chh, { fontSize: 13, color: NAVY, valign: "middle" });
  pageNo(s, 3, false);
}

// =====================================================================
// SLIDE 4 — The LaborForce solution (navy, isometric five-layer waterfall)
// =====================================================================
{
  const s = pres.addSlide({ masterName: "NAVY" });
  kicker(s, "04", "Five critical functions", true);
  title(s, [{ text: "The LaborForce solution.", breakLine: true }, { text: "A specialized operational layer.", muted: true }], 0.85, 1.1, 28, true);

  // --- left: slabs, geometry taken from the HTML's SVG (viewBox 520 x 610) ---
  const SX = M, SY = 1.98, K = 4.82 / 610; // scale: px -> inches
  const P = (x, y) => ({ x: SX + x * K, y: SY + y * K });
  const poly = (pts, fill, name) => {
    const xs = pts.map(p => p.x), ys = pts.map(p => p.y);
    const x0 = Math.min(...xs), y0 = Math.min(...ys), w = Math.max(...xs) - x0, h = Math.max(...ys) - y0;
    s.addShape(pres.ShapeType.custGeom, { x: x0, y: y0, w, h, fill: { color: fill }, line: { color: fill, width: 0.5 }, objectName: name,
      points: pts.map(p => ({ x: p.x - x0, y: p.y - y0 })).concat([{ close: true }]) });
  };
  const slabColors = [["BFEFE0", "7ADBC0", "3DB48F"], ["8FE0C9", "4CC9A6", "1D9E75"], ["9CC8F0", "5AA2E6", "2F7FCB"], ["6FB0EE", "3A8FDB", "1F67AE"], ["4A97E2", "2B74BE", "1A5590"]];
  slabColors.forEach(([top, left, right], i) => {
    const o = 118 * i, n = i + 1;
    poly([P(60, 52 + o), P(260, 90 + o), P(260, 108 + o), P(60, 70 + o)], left, `slab-${n}-left`);
    poly([P(460, 52 + o), P(260, 90 + o), P(260, 108 + o), P(460, 70 + o)], right, `slab-${n}-right`);
    poly([P(60, 52 + o), P(260, 14 + o), P(460, 52 + o), P(260, 90 + o)], top, `slab-${n}-top`);
    const c = P(260, 52 + o);
    T(s, String(n).padStart(2, "0"), c.x - 0.5, c.y - 0.15, 1.0, 0.3, { fontSize: 11, bold: true, color: NAVY, align: "center", valign: "middle", objectName: `slab-${n}-num` });
    if (i < 4) {
      const a = P(260, 108 + o), b = P(260, 138 + o);
      s.addShape(pres.ShapeType.line, { x: a.x, y: a.y, w: 0, h: b.y - a.y, line: { color: N_TEAL, width: 1.25, dashType: "sysDash" }, objectName: `slab-${n}-link` });
      s.addShape(pres.ShapeType.ellipse, { x: a.x - 0.03, y: a.y - 0.03, w: 0.06, h: 0.06, fill: { color: N_TEAL }, line: { color: N_TEAL, width: 0 }, objectName: `slab-${n}-drop` });
    }
  });

  // --- right: five function rows ---
  const fns = [
    ["Proactive Revenue Identification", "Review injury-related encounters, identify potentially responsible payers, and prioritize accounts for investigation."],
    ["Dedicated Patient Engagement", "Outreach to verify injury circumstances and collect missing claim, employer, insurer, or attorney information."],
    ["Payer Verification & RCM Coordination", "Coordinate findings with registration, billing, and revenue cycle teams for payer determination and follow-up."],
    ["Revenue Auditing & Reconciliation", "Monitor unresolved cases, flag missing or inconsistent information, and track case status and reimbursement."],
    ["Lien Administration & Recovery", "Support approved lien documentation, follow-up, and reimbursement tracking within the legal and contractual framework."],
  ];
  const rx = SX + 520 * K + 0.45, rw = W - M - rx, ry0 = 1.98, rh = 0.82, rgap = 0.1;
  fns.forEach(([h, p], i) => {
    const y = ry0 + i * (rh + rgap), n = i + 1;
    s.addShape(pres.ShapeType.roundRect, { x: rx, y, w: rw, h: rh, fill: { color: "174579" }, line: { color: N_CARD_LINE, width: 0.75 }, rectRadius: 0.05, objectName: `fn-${n}-card` });
    s.addShape(pres.ShapeType.ellipse, { x: rx + 0.2, y: y + 0.24, w: 0.34, h: 0.34, fill: { color: N_CARD_LINE }, line: { color: N_CARD_LINE, width: 0 }, objectName: `fn-${n}-badge` });
    T(s, String(n).padStart(2, "0"), rx + 0.2, y + 0.24, 0.34, 0.34, { fontSize: 8.5, bold: true, color: "FFFFFF", align: "center", valign: "middle", objectName: `fn-${n}-badgenum` });
    T(s, h, rx + 0.72, y + 0.12, rw - 0.9, 0.28, { fontSize: 13, bold: true, color: "FFFFFF", charSpacing: -0.2, objectName: `fn-${n}-title` });
    T(s, p, rx + 0.72, y + 0.42, rw - 0.9, 0.38, { fontSize: 9.5, color: N_SPAN, lineSpacingMultiple: 1.15, objectName: `fn-${n}-desc` });
  });
  T(s, "LaborForce works alongside your billing and collections teams.", rx, ry0 + 5 * rh + 4 * rgap + 0.12, rw, 0.25, { fontSize: 9.5, color: N_BODY, italic: true });
  pageNo(s, 4, true);
  s.addNotes("Five-layer waterfall: findings flow from identification (01) down to lien administration and recovery (05). LaborForce works alongside the hospital's billing and collections teams.");
}

// =====================================================================
// SLIDE 5 — Financial opportunity (static model, default scenario)
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "05", "Financial opportunity", false);
  title(s, [{ text: "Turn hidden revenue opportunities into visible results." }], 0.85, 0.55, 28, false);

  // left: assumptions with static slider tracks
  const lx = M, lw = 4.3, ay = 1.55;
  s.addShape(pres.ShapeType.ellipse, { x: lx, y: ay + 0.06, w: 0.1, h: 0.1, fill: { color: TEAL }, line: { color: TEAL, width: 0 } });
  T(s, "PLANNING INPUTS", lx + 0.18, ay, lw, 0.22, { fontSize: 8, bold: true, color: MUTED, charSpacing: 1.5 });
  const assumptions = [
    ["01", "Annual ED encounters", "150,000", "25,000", "200,000", (150000 - 25000) / 175000],
    ["02", "Additional coverage identified", "6%", "2%", "10%", 0.5],
    ["03", "Average incremental net collection", "$4,000", "$500", "$5,000", (4000 - 500) / (5000 - 500)],
    ["04", "Average ED charge", "$10,000", "$3,000", "$15,000", (10000 - 3000) / (15000 - 3000)],
  ];
  const arH = 1.0;
  assumptions.forEach(([n, lab, val, lo, hi, f], i) => {
    const y = ay + 0.38 + i * arH;
    hline(s, lx, y, lw, LINE);
    T(s, [{ text: n + "  ", options: { color: TEAL, fontSize: 9 } }, { text: lab, options: { color: NAVY, bold: true } }], lx, y + 0.18, lw - 1.05, 0.3, { fontSize: 11.5 });
    T(s, val, lx + lw - 1.05, y + 0.1, 1.05, 0.4, { fontSize: 17, bold: true, color: NAVY, align: "right", charSpacing: -0.5 });
    const ty = y + 0.6;
    rrect(s, lx, ty, lw, 0.06, PANEL, 0.03);
    rrect(s, lx, ty, lw * f, 0.06, TEAL, 0.03);
    s.addShape(pres.ShapeType.ellipse, { x: lx + lw * f - 0.08, y: ty - 0.05, w: 0.16, h: 0.16, fill: { color: "FFFFFF" }, line: { color: TEAL, width: 1.5 } });
    T(s, lo, lx, ty + 0.14, 2, 0.2, { fontSize: 8.5, color: MUTED });
    T(s, hi, lx + lw - 2, ty + 0.14, 2, 0.2, { fontSize: 8.5, color: MUTED, align: "right" });
  });
  hline(s, lx, ay + 0.38 + 4 * arH, lw, LINE);
  vline(s, lx + lw + 0.4, 1.55, 4.5, LINE);

  // right: result strip — headline on the left, two supporting results stacked on the right
  const rx = M + 5.1, rw = CW - 5.1, ry = 1.55, rh = 1.45;
  rrect(s, rx, ry, rw, rh, NAVY, 0.04);
  const c1 = rw * 0.5;
  const labO = { fontSize: 7.5, bold: true, color: N_TEAL, charSpacing: 0.5 };
  T(s, "ANNUAL INCREMENTAL NET COLLECTIONS", rx + 0.28, ry + 0.2, c1 - 0.4, 0.2, labO);
  T(s, "$36M", rx + 0.26, ry + 0.38, c1 - 0.4, 0.7, { fontSize: 46, color: "FFFFFF", charSpacing: -2.5 });
  T(s, "≈ $3M a month · ≈ $99K a day · $108M over three years", rx + 0.28, ry + 1.06, c1 - 0.35, 0.24, { fontSize: 8, bold: true, color: N_TEAL });
  vline(s, rx + c1, ry + 0.22, rh - 0.44, N_LINE);
  const x2 = rx + c1 + 0.3, w2 = rw - c1 - 0.55;
  T(s, "IDENTIFIED ENCOUNTERS / YEAR", x2, ry + 0.2, w2, 0.2, labO);
  T(s, "9,000", x2, ry + 0.36, w2, 0.4, { fontSize: 22, color: "FFFFFF", charSpacing: -1 });
  hline(s, x2, ry + 0.78, w2, N_LINE);
  T(s, "ASSOCIATED GROSS CHARGES / YEAR", x2, ry + 0.86, w2, 0.2, labO);
  T(s, "$90M", x2, ry + 1.02, w2, 0.4, { fontSize: 22, color: "FFFFFF", charSpacing: -1 });

  // viz grid: people chart (left) + sensitivity chart (right)
  const vy = ry + rh + 0.25, vgap = 0.4, vw = (rw - vgap) / 2;
  eyebrow(s, "Volume & coverage", rx, vy, vw, false);
  T(s, "A visible share of every visit.", rx, vy + 0.24, vw, 0.3, { fontSize: 13, bold: true, color: NAVY, charSpacing: -0.3 });
  const cols = 20, rows = 10, total = 150, covered = 9; // 1 figure = 1,000 visits; 9,000 identified
  const cellW = (vw - (cols - 1) * 0.03) / cols, cellH = 0.15, gy0 = vy + 0.65;
  for (let k = 0; k < total; k++) {
    const r = Math.floor(k / cols), c = k % cols;
    s.addShape(pres.ShapeType.roundRect, { x: rx + c * (cellW + 0.03), y: gy0 + r * (cellH + 0.04), w: cellW, h: cellH, fill: { color: k < covered ? TEAL : "CCD6E0" }, line: { color: k < covered ? TEAL : "CCD6E0", width: 0 }, rectRadius: 0.02 });
  }
  const ky = gy0 + Math.ceil(total / cols) * (cellH + 0.04) + 0.1;
  rrect(s, rx, ky + 0.06, 0.1, 0.1, TEAL, 0.01);
  T(s, "Additional coverage identified", rx + 0.16, ky, 2.3, 0.22, { fontSize: 8.5, color: MUTED });
  rrect(s, rx + 2.4, ky + 0.06, 0.1, 0.1, "CCD6E0", 0.01);
  T(s, "Other encounters", rx + 2.56, ky, 1.6, 0.22, { fontSize: 8.5, color: MUTED });

  const cx = rx + vw + vgap;
  eyebrow(s, "Coverage sensitivity", cx, vy, vw, false);
  T(s, "What changes as coverage improves?", cx, vy + 0.24, vw, 0.3, { fontSize: 13, bold: true, color: NAVY, charSpacing: -0.3 });
  T(s, [{ text: "$36M", options: { bold: true, color: TEAL, fontSize: 14 } }, { text: "  at 6% identified coverage", options: { color: MUTED } }], cx, vy + 0.6, vw, 0.3, { fontSize: 9 });
  const rates = [2, 3, 4, 5, 6, 7, 8, 9, 10];
  const vals = rates.map(r => 150000 * r / 100 * 4000 / 1e6);
  s.addChart(pres.ChartType.line, [{ name: "Annual net collections ($M)", labels: rates.map(r => r + "%"), values: vals }], {
    x: cx - 0.1, y: vy + 0.85, w: vw + 0.1, h: 1.95,
    chartColors: [TEAL], lineSize: 2.25, lineDataSymbol: "circle", lineDataSymbolSize: 6, lineDataSymbolLineColor: TEAL,
    showLegend: false, showTitle: false,
    showValue: true, dataLabelPosition: "t", dataLabelFormatCode: '"$"0"M"', dataLabelFontSize: 7.5, dataLabelColor: INK2, dataLabelFontFace: FONT,
    valAxisMinVal: 0, valAxisMaxVal: 70, valAxisMajorUnit: 10, valAxisLabelFormatCode: '"$"0"M"', valAxisLabelFontSize: 7.5, valAxisLabelColor: MUTED, valAxisLabelFontFace: FONT,
    valGridLine: { color: "DDE3EA", size: 0.5 }, catGridLine: { style: "none" },
    catAxisLabelFontSize: 7.5, catAxisLabelColor: MUTED, catAxisLabelFontFace: FONT,
    catAxisTitle: "Additional coverage identified (%)", showCatAxisTitle: true, catAxisTitleFontSize: 7.5, catAxisTitleColor: MUTED, catAxisTitleFontFace: FONT,
    valAxisLineShow: false, catAxisLineShow: false, plotArea: { fill: { color: PAPER } }, chartArea: { fill: { color: PAPER } },
  });

  // calculation chain
  const chy = 6.15, chh = 0.6;
  const chain = [["Annual encounters", "150,000"], ["Additional coverage", "6%"], ["Net collection / encounter", "$4,000"], ["Annual net collections", "$36,000,000"]];
  const syms = ["×", "×", "="], symW = 0.4, boxW = (CW - 3 * symW) / 4;
  chain.forEach(([lab, val], i) => {
    const x = M + i * (boxW + symW), last = i === 3;
    if (last) rrect(s, x, chy, boxW, chh, TEALL, 0.03);
    else s.addShape(pres.ShapeType.roundRect, { x, y: chy, w: boxW, h: chh, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 }, rectRadius: 0.03 });
    T(s, lab.toUpperCase(), x + 0.2, chy + 0.1, boxW - 0.4, 0.2, { fontSize: 7.5, color: MUTED, charSpacing: 1 });
    T(s, val, x + 0.2, chy + 0.29, boxW - 0.4, 0.3, { fontSize: 15, bold: true, color: last ? TEAL : NAVY, charSpacing: -0.5 });
    if (i < 3) T(s, syms[i], x + boxW, chy, symW, chh, { fontSize: 16, color: MUTED, align: "center", valign: "middle" });
  });
  pageNo(s, 5, false);
  s.addNotes("Static version of the interactive planning model at its starting scenario: 150,000 ED encounters × 6% additional coverage × $4,000 net per encounter = $36M per year; 9,000 identified encounters; $90M associated gross charges at a $10,000 average ED charge. Each figure in the grid = 1,000 ED encounters. Illustrative planning model, not a forecast.");
}

// =====================================================================
// SLIDE 6 — 90-day pilot
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "06", "Proposed partnership", false);
  title(s, [{ text: "90-day pilot.", breakLine: true }, { text: "John H. Stroger, Jr. Hospital.", muted: true }], 0.85, 1.2, 30, false);
  const phases = [
    ["Phase 01", "Days 1 – 15", 15, "Discovery & Baseline", "Review current injury-related registration, payer identification, billing, and follow-up. Agree on pilot scope, eligibility criteria, compliance requirements, and baseline measures.", "DBE8F7", NAVY, "5B8FD6"],
    ["Phase 02", "Days 16 – 60", 45, "Identification & Investigation", "Evaluate designated encounters, conduct authorized patient outreach, identify alternative payer sources, and coordinate verified findings with existing hospital teams.", TEAL, "FFFFFF", TEAL],
    ["Phase 03", "Days 61 – 90", 30, "Validation & Review", "Reconcile outcomes, review billing corrections and collections, assess operational impact, and recommend continued monitoring and potential expansion.", NAVY, "FFFFFF", NAVY],
  ];
  const py = 2.15, gap = 0.3, cw = (CW - 2 * gap) / 3, ch = 2.45, hh = 0.4;
  phases.forEach(([ph, days, d, h, p, hfill, hcol, mfill], i) => {
    const x = M + i * (cw + gap);
    s.addShape(pres.ShapeType.roundRect, { x, y: py, w: cw, h: ch, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 }, rectRadius: 0.05 });
    rect(s, x + 0.01, py + 0.01, cw - 0.02, hh, hfill);
    T(s, ph.toUpperCase(), x + 0.25, py, cw / 2, hh, { fontSize: 9, bold: true, color: hcol, charSpacing: 1, valign: "middle" });
    T(s, days.toUpperCase(), x + cw / 2, py, cw / 2 - 0.25, hh, { fontSize: 9, bold: true, color: hcol, charSpacing: 1, valign: "middle", align: "right" });
    const my = py + hh + 0.22, mw = cw - 0.5 - 1.1;
    rrect(s, x + 0.25, my, mw, 0.08, PANEL, 0.03);
    rrect(s, x + 0.25, my, mw * d / 90, 0.08, mfill, 0.03);
    T(s, `${d} of 90 days`, x + 0.25 + mw + 0.12, my - 0.08, 1.0, 0.24, { fontSize: 8.5, color: MUTED });
    T(s, h, x + 0.25, py + hh + 0.45, cw - 0.5, 0.35, { fontSize: 15, bold: true, color: NAVY, charSpacing: -0.3 });
    T(s, p, x + 0.25, py + hh + 0.85, cw - 0.5, 1.15, { fontSize: 10.5, color: INK2, lineSpacingMultiple: 1.25 });
  });
  const iy = py + ch + 0.3, ih = 6.78 - iy;
  const info = [
    ["How to read the pilot", [{ text: "Many claims take longer than 90 days to resolve. The pilot measures " }, { text: "leading indicators", options: { bold: true, color: NAVY } }, { text: " and any collections realized; final financial performance is reviewed as the identified account cohort matures." }], null],
    ["Cook County Health provides", null, ["Executive sponsor and agreed pilot scope", "ED volume, payer mix, and current TPL/WC workflow data", "Compliance requirements and data-access terms"]],
    ["LaborForce provides", null, ["Screening, specialist review, and case investigation", "Dedicated patient outreach and lien administration support", "Joint reporting at days 30, 60, and 90"]],
  ];
  info.forEach(([eb, runs, items], i) => {
    const x = M + i * (cw + gap);
    rrect(s, x, iy, cw, ih, PANEL, 0.04);
    rect(s, x, iy, cw, 0.05, TEAL);
    eyebrow(s, eb, x + 0.25, iy + 0.25, cw - 0.5, false);
    if (runs) T(s, runs, x + 0.25, iy + 0.55, cw - 0.5, ih - 0.65, { fontSize: 10.5, color: INK2, lineSpacingMultiple: 1.25 });
    else bullets(s, items, x + 0.25, iy + 0.55, cw - 0.5, ih - 0.65, { fontSize: 10.5, paraSpaceAfter: 3 });
  });
  pageNo(s, 6, false);
}

// =====================================================================
// SLIDE 7 — Success metrics
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "07", "Proposed success metrics", false);
  title(s, [{ text: "Transparent. Measurable.", breakLine: true }, { text: "Jointly reviewed.", muted: true }], 0.85, 1.2, 30, false);
  const groups = [
    ["Leading", "0A8FA6", "Early signals that cases are being found and verified", ["Encounters screened and flagged", "Number and % with verified additional responsible-party coverage", "Accounts accepted for billing correction or recovery action"]],
    ["Financial", "0C3C75", "What the program returns, net of adjustments", ["Additional collections attributable to the program, net of reversals and adjustments", "Incremental net revenue after program costs"]],
    ["Operational", "2F6FB5", "Effect on hospital teams and account flow", ["Staff workload", "Turnaround time", "Unresolved account aging"]],
    ["Quality", "7A95AD", "Safeguards that stay in place throughout", ["Compliance", "Patient experience", "Documentation quality"]],
  ];
  const gy = 2.2, gap = 0.25, w = (CW - 3 * gap) / 4, gh = 2.45;
  groups.forEach(([h, accent, desc, items], i) => {
    const x = M + i * (w + gap);
    rrect(s, x, gy, w, gh, PANEL, 0.04);
    rect(s, x, gy, w, 0.06, accent);
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.25, y: gy + 0.33, w: 0.14, h: 0.14, fill: { color: accent }, line: { color: accent, width: 0 } });
    T(s, h, x + 0.5, gy + 0.22, w - 0.7, 0.35, { fontSize: 15, bold: true, color: NAVY });
    T(s, desc, x + 0.25, gy + 0.62, w - 0.5, 0.45, { fontSize: 9.5, color: MUTED, lineSpacingMultiple: 1.2 });
    bullets(s, items, x + 0.25, gy + 1.1, w - 0.5, 1.3, { fontSize: 10.5, paraSpaceAfter: 4 });
  });
  const cy = gy + gh + 0.3;
  hline(s, M, cy, CW, LINE);
  eyebrow(s, "Joint review cadence", M, cy + 0.2, 4, false);
  const cad = [["Launch", "Scope, eligibility criteria, and baseline agreed", true], ["Day 30", "Baseline confirmed; screening volumes and first flagged cohort", false], ["Day 60", "Verification rate, accounts accepted for correction, staff workload impact", false], ["Day 90", "Collections to date, cohort maturity, and a joint decision on continuation", false]];
  const ty = cy + 0.62, cw4 = CW / 4, dot = 0.2;
  hline(s, M + 0.1, ty + dot / 2, CW - 0.2, LINE, 1.5);
  cad.forEach(([d, p, filled], i) => {
    const x = M + i * cw4;
    s.addShape(pres.ShapeType.ellipse, { x, y: ty, w: dot, h: dot, fill: { color: filled ? TEAL : SURFACE }, line: { color: TEAL, width: 2 } });
    T(s, d.toUpperCase(), x, ty + 0.35, cw4 - 0.3, 0.22, { fontSize: 9, bold: true, color: NAVY, charSpacing: 1 });
    T(s, p, x, ty + 0.6, cw4 - 0.4, 0.6, { fontSize: 10.5, color: INK2, lineSpacingMultiple: 1.2 });
  });
  pageNo(s, 7, false);
}

// =====================================================================
// SLIDE 8 — Our ask (navy)
// =====================================================================
{
  const s = pres.addSlide({ masterName: "CLOSING" });
  kicker(s, "08", "Our ask", true);
  s.addText([
    { text: "Our ask: a 90-day pilot at ", options: { color: "FFFFFF" } },
    { text: "John H. Stroger, Jr. Hospital.", options: { color: N_TEAL } },
  ], { x: M, y: 0.85, w: CW, h: 0.75, fontFace: FONT, fontSize: 30, margin: 0, valign: "top", isTextBox: true, charSpacing: -1, lineSpacingMultiple: 1.05 });
  T(s, "Strengthen Cook County Health's fiscal resilience while supporting accessible, high-quality care for the community — through a focused, transparent, and measurable pilot, reviewed jointly at days 30, 60, and 90.", M, 1.7, 10.4, 0.75, { fontSize: 12.5, color: N_BODY, lineSpacingMultiple: 1.3 });
  const steps = [["Confirm sponsor & scope", "Executive sponsor and pilot scope at Stroger Hospital"], ["Share baseline data", "ED volume, payer mix, and the current TPL/WC workflow"], ["Agree & launch", "Compliance requirements and success metrics; launch Phase 1"]];
  const sy = 2.85, sgap = 0.3, sw = (CW - 2 * sgap) / 3, sh = 1.9;
  steps.forEach(([h, p], i) => {
    const x = M + i * (sw + sgap);
    s.addShape(pres.ShapeType.roundRect, { x, y: sy, w: sw, h: sh, fill: { color: N_CARD }, line: { color: N_CARD_LINE, width: 0.75 }, rectRadius: 0.05 });
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.3, y: sy + 0.3, w: 0.32, h: 0.32, fill: { color: TEAL }, line: { color: TEAL, width: 0 } });
    T(s, String(i + 1).padStart(2, "0"), x + 0.3, sy + 0.3, 0.32, 0.32, { fontSize: 8.5, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T(s, h, x + 0.3, sy + 0.76, sw - 0.6, 0.35, { fontSize: 16, bold: true, color: "FFFFFF", charSpacing: -0.3 });
    T(s, p, x + 0.3, sy + 1.14, sw - 0.6, 0.6, { fontSize: 11, color: N_BODY, lineSpacingMultiple: 1.25 });
  });
  // small logo tile bottom-left (HTML: 58 px tall tile, 8x14 px padding, on a 1440 px canvas), thank-you bottom-right
  const lh = 0.54, lw = 0.85, ly = FOOT_Y - 0.12 - lh, imgH = lh - 0.15, imgW = imgH * 1150 / 757;
  rrect(s, M, ly, lw, lh, "FFFFFF", 0.04);
  s.addImage({ path: LOGO, x: M + (lw - imgW) / 2, y: ly + 0.075, w: imgW, h: imgH });
  T(s, "Thank you", W - M - 4.4, ly - 0.05, 4.4, 0.28, { fontSize: 14, bold: true, color: "FFFFFF", align: "right" });
  T(s, "We look forward to discussing the pilot with your leadership team.", W - M - 4.4, ly + 0.25, 4.4, 0.3, { fontSize: 10.5, color: N_BODY, align: "right" });
  pageNo(s, 8, true);
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("Wrote", OUT);
})().catch(e => { console.error(e); process.exit(1); });
