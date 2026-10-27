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
  T(slide, `${String(n).padStart(2, "0")} / 04`, W - M - 2, FOOT_Y + 0.08, 2, 0.25, { fontSize: 8, color: dark ? N_MUTED : MUTED, align: "right", charSpacing: 1.5 });
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

// ---- slides (v13: 4-slide index.html, commit 2ed2890, + clickable financial scenarios, 2026-10-26) ----
const BRAND = "E:/Claude/laborforce-deck/brand";
const NM_LOGO = BRAND + "/nm_logo.svg", HPH_LOGO = BRAND + "/hph_logo.png";
const N_TOP = "1F4C80", N_TOP_LINE = "2F5A8D", N_BASE = "061F45", N_BASE_LINE = "2A4A72", N_MID = "0677AE", N_BASE_SPAN = "AEBFD6";

// =====================================================================
// SLIDE 1 — Cover (headline top-left, photo top-right, partner cards along the bottom)
// =====================================================================
{
  const s = pres.addSlide({ masterName: "COVER" });
  const LW = 7.3;
  // hospital photo: top-right corner, 64% x 68% of the slide, pre-faded toward the left and the bottom (make_cover_photo.py)
  const phW = W * 0.64, phH = H * 0.68;
  s.addImage({ path: BRAND + "/hospital_cover_faded.png", x: W - phW, y: 0, w: phW, h: phH });
  // headline + two-line deck
  s.addText([
    { text: "You Deliver Care,", options: { color: NAVY, breakLine: true } },
    { text: "We Optimize Revenue.", options: { color: TEAL } },
  ], { x: M, y: 1.05, w: 8.0, h: 1.45, fontFace: FONT, fontSize: 45, margin: 0, valign: "top", isTextBox: true, charSpacing: -2, lineSpacingMultiple: 0.98 });
  s.addText([
    { text: "Technology identifies opportunities.", options: { breakLine: true } },
    { text: "We bring them to resolution." },
  ], { x: M, y: 2.72, w: 6.5, h: 0.75, fontFace: FONT, fontSize: 15, color: INK2, margin: 0, valign: "top", isTextBox: true, lineSpacingMultiple: 1.25 });
  // hospital partners: two large cards across the content width
  const cardH = 1.39, cardY = FOOT_Y - 0.2 - cardH, cgap = 0.22, cardW = (CW - cgap) / 2;
  T(s, "HOSPITAL PARTNERS", M, cardY - 0.36, 4, 0.22, { fontSize: 8, bold: true, color: MUTED, charSpacing: 1.5 });
  [[NM_LOGO, 0.67, 730 / 137], [HPH_LOGO, 0.96, 782 / 227]].forEach(([logo, lh, ratio], i) => {
    const x = M + i * (cardW + cgap), lw = lh * ratio;
    s.addShape(pres.ShapeType.roundRect, { x, y: cardY, w: cardW, h: cardH, fill: { color: "FFFFFF" }, line: { color: LINE, width: 0.75 }, rectRadius: 0.07 });
    s.addImage({ path: logo, x: x + (cardW - lw) / 2, y: cardY + (cardH - lh) / 2, w: lw, h: lh });
  });
  // footer (unchanged)
  hline(s, M, FOOT_Y, LW, LINE);
  T(s, "CONFIDENTIAL — FOR DISCUSSION PURPOSES", M, FOOT_Y + 0.08, 5, 0.25, { fontSize: 8, color: MUTED, charSpacing: 1.5 });
  T(s, "01 / 04", M + LW - 2, FOOT_Y + 0.08, 2, 0.25, { fontSize: 8, color: MUTED, align: "right", charSpacing: 1.5 });
  s.addNotes("Cover: headline top-left, hospital photo top-right, hospital partner cards along the bottom.");
}

// =====================================================================
// SLIDE 2 — The hidden revenue challenge (essential-hospitals band + "Whether" cards)
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "02", "The hidden revenue challenge", false);
  title(s, [{ text: "Revenue that traditional workflows overlooked." }], 0.85, 0.6, 30, false);

  // navy band: three columns
  const by = 1.5, bh = 1.18, pad = 0.26, bgap = 0.28;
  rrect(s, M, by, CW, bh, NAVY, 0.06);
  const inner = CW - 2 * pad - 2 * bgap, fr = inner / 3.4, c1 = 1.15 * fr, c2 = 1.25 * fr, c3 = 1.0 * fr;
  const x1 = M + pad, x2 = x1 + c1 + bgap, x3 = x2 + c2 + bgap;
  T(s, "THE REVENUE CHALLENGE FACING ESSENTIAL HOSPITALS", x1, by + 0.2, c1, 0.2, { fontSize: 7.5, bold: true, color: N_TEAL, charSpacing: 1 });
  T(s, "Essential hospitals face growing financial pressure from uncompensated care, Medicaid underpayments, and limited resources.", x1, by + 0.44, c1, 0.6, { fontSize: 10, color: "DBE6F2", lineSpacingMultiple: 1.2 });
  vline(s, x2 - bgap / 2, by + 0.18, bh - 0.36, N_LINE);
  vline(s, x3 - bgap / 2, by + 0.18, bh - 0.36, N_LINE);
  T(s, "IN 2023, ESSENTIAL HOSPITALS REPORTED", x2, by + 0.16, c2, 0.2, { fontSize: 7.5, bold: true, color: N_TITLE_MUTED, charSpacing: 1 });
  const sw = (c2 - 0.26) / 2;
  [["$11B", "in uncompensated care"], ["$11.4B", "in additional under-reimbursed care"]].forEach(([v, l], i) => {
    const x = x2 + i * (sw + 0.26);
    T(s, v, x, by + 0.36, sw, 0.46, { fontSize: 27, bold: true, color: "FFFFFF", charSpacing: -1.5 });
    T(s, l, x, by + 0.8, sw, 0.3, { fontSize: 9, color: N_SPAN, lineSpacingMultiple: 1.1 });
  });
  s.addText([
    { text: "H.R. 1", options: { bold: true, color: N_TEAL } },
    { text: " adds further financial pressure, making revenue optimization increasingly critical.", options: { color: "FFFFFF" } },
  ], { x: x3, y: by + 0.2, w: c3, h: 0.6, fontFace: FONT, fontSize: 10, margin: 0, valign: "top", isTextBox: true, lineSpacingMultiple: 1.2 });
  T(s, "Source: America's Essential Hospitals, Essential Data (2025)", x3, by + 0.84, c3, 0.2, { fontSize: 7, color: N_NOTE });

  // intro
  T(s, "Patients often arrive after workplace incidents, motor vehicle accidents, or injuries involving another liable party. Registration and billing workflows may not consistently capture or resolve:", M, by + bh + 0.14, 11.2, 0.5, { fontSize: 11.5, color: INK2, lineSpacingMultiple: 1.2 });

  // six question cards + flow card
  const qs = [
    "Whether the injury occurred while the patient was working",
    "Whether a motor vehicle or other third party may be responsible",
    "Whether another insurer or payer should be investigated",
    "Whether the hospital has the right claim, attorney, or payer information",
    "Whether a hospital lien is available, documented, and followed up",
    "Whether unresolved cases need investigation after discharge",
  ];
  const qy = by + bh + 0.78, flowW = 3.9, leftW = CW - flowW - 0.4, cgap = 0.1, cardW = (leftW - cgap) / 2, cardH = 0.66;
  qs.forEach((q, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = M + col * (cardW + cgap), y = qy + row * (cardH + cgap);
    rrect(s, x, y, cardW, cardH, PANEL, 0.04);
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.18, y: y + (cardH - 0.26) / 2, w: 0.26, h: 0.26, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
    T(s, String(i + 1).padStart(2, "0"), x + 0.18, y + (cardH - 0.26) / 2, 0.26, 0.26, { fontSize: 7, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T(s, q, x + 0.58, y, cardW - 0.75, cardH, { fontSize: 10.5, color: NAVY, lineSpacingMultiple: 1.15, valign: "middle" });
  });
  const gridH = 3 * cardH + 2 * cgap;
  const fx = M + leftW + 0.4;
  const farrow = 0.2, fb0 = qy + 0.42, fbw = flowW - 0.32, fbH = 0.52;
  const flowH = 0.42 + 3 * fbH + 2 * farrow + 0.12;
  s.addShape(pres.ShapeType.roundRect, { x: fx, y: qy, w: flowW, h: flowH, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 }, rectRadius: 0.05 });
  eyebrow(s, "Where the revenue goes", fx + 0.16, qy + 0.14, flowW - 0.3, false);
  const flow = [
    ["Injury-related encounter", "Workplace injury, motor vehicle accident, or incident involving a third party", PANEL, NAVY, INK2],
    ["Responsible payer missed", "Not identified at registration, or identified but not followed through", PANEL, NAVY, INK2],
    ["Absorbed by the hospital", "Written off as bad debt or uncompensated care", NAVY, "FFFFFF", N_SPAN],
  ];
  flow.forEach(([h, p, fill, hc, pc], i) => {
    const y = fb0 + i * (fbH + farrow);
    rrect(s, fx + 0.16, y, fbw, fbH, fill, 0.03);
    T(s, h, fx + 0.28, y + 0.05, fbw - 0.24, 0.22, { fontSize: 10, bold: true, color: hc, charSpacing: -0.2 });
    T(s, p, fx + 0.28, y + 0.24, fbw - 0.24, fbH - 0.26, { fontSize: 8, color: pc, lineSpacingMultiple: 1.05 });
    if (i < 2) s.addShape(pres.ShapeType.line, { x: fx + flowW / 2, y: y + fbH + 0.04, w: 0, h: farrow - 0.08, line: { color: TEAL, width: 1.25, endArrowType: "triangle" } });
  });
  const cy = qy + Math.max(gridH, flowH) + 0.15, chh = 0.56;
  rect(s, M, cy, CW, chh, TEALL);
  rect(s, M, cy, 0.05, chh, TEAL);
  eyebrow(s, "The consequence", M + 0.28, cy + 0.19, 1.8, false);
  T(s, "Valid reimbursement opportunities may remain unidentified, incorrectly routed, delayed, or insufficiently pursued.", M + 2.1, cy, CW - 2.4, chh, { fontSize: 11.5, color: NAVY, valign: "middle" });
  pageNo(s, 2, false);
}

// =====================================================================
// SLIDE 3 — The LaborForce solution (navy, isometric five-layer waterfall)
// =====================================================================
{
  const s = pres.addSlide({ masterName: "NAVY" });
  kicker(s, "03", "Five critical functions", true);
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
  pageNo(s, 3, true);
  s.addNotes("Five-layer waterfall: findings flow from identification (01) down to lien administration and recovery (05). LaborForce works alongside the hospital's billing and collections teams.");
}

// =====================================================================
// SLIDE 4 — Financial opportunity (four clickable levels per input; 255 hidden state pages follow)
// =====================================================================
// Each input has four levels. In slideshow, clicking a level jumps to the hidden page that shows
// that scenario, so the whole slide (headline, results, people grid, sensitivity chart, chain)
// updates. The default scenario is the visible slide 4; the other 255 pages are hidden, so they
// are skipped when advancing and left out of print and PDF.
const LEVELS = [
  ["volume", "Annual ED encounters", [50000, 100000, 150000, 200000], v => v.toLocaleString("en-US")],
  ["coverage", "Additional coverage identified", [2, 4, 6, 8], v => v + "%"],
  ["collection", "Average incremental net collection", [2000, 3000, 4000, 5000], v => money(v)],
  ["charge", "Average ED charge", [5000, 7500, 10000, 15000], v => money(v)],
];
const DEFAULT_STATE = [2, 2, 2, 2];
function money(v) { return "$" + Math.round(v).toLocaleString("en-US"); }
function headline(v) { return v >= 999500 ? "$" + (v / 1e6).toFixed(1).replace(/\.0$/, "") + "M" : v >= 1e3 ? "$" + Math.round(v / 1e3) + "K" : money(v); }
function compactMoney(v) { return v >= 1e6 ? "$" + (v / 1e6).toLocaleString("en-US", { maximumFractionDigits: 2 }) + "M" : v >= 1e3 ? "$" + (v / 1e3).toLocaleString("en-US", { maximumFractionDigits: 2 }) + "K" : "$" + v.toLocaleString("en-US"); }
const stateKey = st => st.join("");
const ALL_STATES = [];
for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++) for (let c = 0; c < 4; c++) for (let d = 0; d < 4; d++) ALL_STATES.push([a, b, c, d]);
const FIN_SLIDE = 4;
const slideOf = { [stateKey(DEFAULT_STATE)]: FIN_SLIDE };
{ let n = FIN_SLIDE + 1; ALL_STATES.forEach(st => { if (stateKey(st) !== stateKey(DEFAULT_STATE)) slideOf[stateKey(st)] = n++; }); }

function financialSlide(st, hidden) {
  const s = pres.addSlide({ masterName: "LIGHT" });
  if (hidden) s.hidden = true;
  const [vol, cov, coll, charge] = LEVELS.map((L, i) => L[2][st[i]]);
  const encounters = vol * cov / 100, annual = encounters * coll, charges = encounters * charge;
  kicker(s, "04", "Financial opportunity", false);
  title(s, [{ text: "Turn hidden revenue opportunities into visible results." }], 0.85, 0.55, 28, false);

  // left: inputs, each with four clickable levels
  const lx = M, lw = 4.3, ay = 1.55;
  s.addShape(pres.ShapeType.ellipse, { x: lx, y: ay + 0.06, w: 0.1, h: 0.1, fill: { color: TEAL }, line: { color: TEAL, width: 0 } });
  T(s, "PLANNING INPUTS", lx + 0.18, ay, lw - 1.2, 0.22, { fontSize: 8, bold: true, color: MUTED, charSpacing: 1.5 });
  T(s, "Reset ↺", lx + lw - 1.0, ay - 0.02, 1.0, 0.24, { fontSize: 8.5, bold: true, color: TEAL, align: "right", underline: true, hyperlink: { slide: FIN_SLIDE, tooltip: "Back to the starting scenario" } });
  const arH = 1.0;
  LEVELS.forEach(([key, lab, vals, fmt], i) => {
    const y = ay + 0.38 + i * arH, active = st[i];
    hline(s, lx, y, lw, LINE);
    T(s, [{ text: String(i + 1).padStart(2, "0") + "  ", options: { color: TEAL, fontSize: 9 } }, { text: lab, options: { color: NAVY, bold: true } }], lx, y + 0.18, lw - 1.05, 0.3, { fontSize: 11.5 });
    T(s, fmt(vals[active]), lx + lw - 1.3, y + 0.1, 1.3, 0.4, { fontSize: 17, bold: true, color: NAVY, align: "right", charSpacing: -0.5 });
    const ty = y + 0.6, f = active / 3;
    rrect(s, lx, ty, lw, 0.06, PANEL, 0.03);
    if (f > 0) rrect(s, lx, ty, lw * f, 0.06, TEAL, 0.03);
    vals.forEach((v, k) => {
      const cx = lx + lw * k / 3, isActive = k === active;
      if (isActive) s.addShape(pres.ShapeType.ellipse, { x: cx - 0.09, y: ty - 0.06, w: 0.18, h: 0.18, fill: { color: "FFFFFF" }, line: { color: TEAL, width: 1.5 } });
      else s.addShape(pres.ShapeType.ellipse, { x: cx - 0.06, y: ty - 0.03, w: 0.12, h: 0.12, fill: { color: k < active ? TEAL : "FFFFFF" }, line: { color: TEAL, width: 1 } });
      const lo = { fontSize: 8.5, color: isActive ? NAVY : MUTED, bold: isActive };
      if (k === 0) T(s, fmt(v), lx, ty + 0.14, 1.2, 0.2, lo);
      else if (k === 3) T(s, fmt(v), lx + lw - 1.2, ty + 0.14, 1.2, 0.2, { ...lo, align: "right" });
      else T(s, fmt(v), cx - 0.6, ty + 0.14, 1.2, 0.2, { ...lo, align: "center" });
      if (!isActive) {
        const target = st.slice(); target[i] = k;
        // transparent click target over the level dot and its label
        s.addShape(pres.ShapeType.rect, { x: Math.max(lx - 0.1, cx - 0.4), y: ty - 0.16, w: 0.8, h: 0.52, fill: { color: "FFFFFF", transparency: 100 }, line: { color: "FFFFFF", width: 0, transparency: 100 }, hyperlink: { slide: slideOf[stateKey(target)], tooltip: lab + ": " + fmt(v) } });
      }
    });
  });
  hline(s, lx, ay + 0.38 + 4 * arH, lw, LINE);
  T(s, "Click a value to change the scenario; every figure on the slide updates.", lx, ay + 0.38 + 4 * arH + 0.08, lw, 0.22, { fontSize: 8, italic: true, color: MUTED });
  vline(s, lx + lw + 0.4, 1.55, 4.5, LINE);

  // right: result strip — headline on the left, two supporting results stacked on the right
  const rx = M + 5.1, rw = CW - 5.1, ry = 1.55, rh = 1.45;
  rrect(s, rx, ry, rw, rh, NAVY, 0.04);
  const c1 = rw * 0.5;
  const labO = { fontSize: 7.5, bold: true, color: N_TEAL, charSpacing: 0.5 };
  T(s, "ANNUAL INCREMENTAL NET COLLECTIONS", rx + 0.28, ry + 0.2, c1 - 0.4, 0.2, labO);
  T(s, headline(annual), rx + 0.26, ry + 0.38, c1 - 0.4, 0.7, { fontSize: 46, color: "FFFFFF", charSpacing: -2.5 });
  T(s, "≈ " + headline(annual / 12) + " a month · ≈ " + headline(annual / 365) + " a day · " + headline(annual * 3) + " over three years", rx + 0.28, ry + 1.06, c1 - 0.35, 0.24, { fontSize: 8, bold: true, color: N_TEAL });
  vline(s, rx + c1, ry + 0.22, rh - 0.44, N_LINE);
  const x2 = rx + c1 + 0.3, w2 = rw - c1 - 0.55;
  T(s, "IDENTIFIED ENCOUNTERS / YEAR", x2, ry + 0.2, w2, 0.2, labO);
  T(s, encounters.toLocaleString("en-US"), x2, ry + 0.36, w2, 0.4, { fontSize: 22, color: "FFFFFF", charSpacing: -1 });
  hline(s, x2, ry + 0.78, w2, N_LINE);
  T(s, "ASSOCIATED GROSS CHARGES / YEAR", x2, ry + 0.86, w2, 0.2, labO);
  T(s, compactMoney(charges), x2, ry + 1.02, w2, 0.4, { fontSize: 22, color: "FFFFFF", charSpacing: -1 });

  // viz grid: people chart (left) + sensitivity chart (right)
  const vy = ry + rh + 0.25, vgap = 0.4, vw = (rw - vgap) / 2;
  eyebrow(s, "Volume & coverage", rx, vy, vw, false);
  T(s, "A visible share of every visit.", rx, vy + 0.24, vw, 0.3, { fontSize: 13, bold: true, color: NAVY, charSpacing: -0.3 });
  const cols = 25, total = vol / 1000, covered = Math.round(total * cov / 100); // 1 figure = 1,000 visits
  const cellW = (vw - (cols - 1) * 0.03) / cols, cellH = 0.15, pitch = 0.19, gy0 = vy + 0.65;
  for (let k = 0; k < total; k++) {
    const r = Math.floor(k / cols), c = k % cols;
    s.addShape(pres.ShapeType.roundRect, { x: rx + c * (cellW + 0.03), y: gy0 + r * pitch, w: cellW, h: cellH, fill: { color: k < covered ? TEAL : "CCD6E0" }, line: { color: k < covered ? TEAL : "CCD6E0", width: 0 }, rectRadius: 0.02 });
  }
  const ky = gy0 + 8 * pitch + 0.1;
  rrect(s, rx, ky + 0.06, 0.1, 0.1, TEAL, 0.01);
  T(s, "Additional coverage identified", rx + 0.16, ky, 2.3, 0.22, { fontSize: 8.5, color: MUTED });
  rrect(s, rx + 2.4, ky + 0.06, 0.1, 0.1, "CCD6E0", 0.01);
  T(s, "Other encounters", rx + 2.56, ky, 1.6, 0.22, { fontSize: 8.5, color: MUTED });

  const cx = rx + vw + vgap;
  eyebrow(s, "Coverage sensitivity", cx, vy, vw, false);
  T(s, "What changes as coverage improves?", cx, vy + 0.24, vw, 0.3, { fontSize: 13, bold: true, color: NAVY, charSpacing: -0.3 });
  T(s, [{ text: headline(annual), options: { bold: true, color: TEAL, fontSize: 14 } }, { text: "  at " + cov + "% identified coverage", options: { color: MUTED } }], cx, vy + 0.6, vw, 0.3, { fontSize: 9 });
  const rates = [2, 3, 4, 5, 6, 7, 8, 9, 10];
  const vals = rates.map(r => vol * r / 100 * coll / 1e6);
  const vmax = Math.ceil(Math.max(...vals) * 1.15 / 10) * 10, unit = vmax > 70 ? 20 : 10;
  s.addChart(pres.ChartType.line, [{ name: "Annual net collections ($M)", labels: rates.map(r => r + "%"), values: vals }], {
    x: cx - 0.1, y: vy + 0.85, w: vw + 0.1, h: 1.95,
    chartColors: [TEAL], lineSize: 2.25, lineDataSymbol: "circle", lineDataSymbolSize: 6, lineDataSymbolLineColor: TEAL,
    showLegend: false, showTitle: false,
    showValue: true, dataLabelPosition: "t", dataLabelFormatCode: '"$"0"M"', dataLabelFontSize: 7.5, dataLabelColor: INK2, dataLabelFontFace: FONT,
    valAxisMinVal: 0, valAxisMaxVal: vmax, valAxisMajorUnit: unit, valAxisLabelFormatCode: '"$"0"M"', valAxisLabelFontSize: 7.5, valAxisLabelColor: MUTED, valAxisLabelFontFace: FONT,
    valGridLine: { color: "DDE3EA", size: 0.5 }, catGridLine: { style: "none" },
    catAxisLabelFontSize: 7.5, catAxisLabelColor: MUTED, catAxisLabelFontFace: FONT,
    catAxisTitle: "Additional coverage identified (%)", showCatAxisTitle: true, catAxisTitleFontSize: 7.5, catAxisTitleColor: MUTED, catAxisTitleFontFace: FONT,
    valAxisLineShow: false, catAxisLineShow: false, plotArea: { fill: { color: PAPER } }, chartArea: { fill: { color: PAPER } },
  });

  // calculation chain
  const chy = 6.15, chh = 0.6;
  const chain = [["Annual encounters", vol.toLocaleString("en-US")], ["Additional coverage", cov + "%"], ["Net collection / encounter", money(coll)], ["Annual net collections", money(annual)]];
  const syms = ["×", "×", "="], symW = 0.4, boxW = (CW - 3 * symW) / 4;
  chain.forEach(([lab, val], i) => {
    const x = M + i * (boxW + symW), last = i === 3;
    if (last) rrect(s, x, chy, boxW, chh, TEALL, 0.03);
    else s.addShape(pres.ShapeType.roundRect, { x, y: chy, w: boxW, h: chh, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 }, rectRadius: 0.03 });
    T(s, lab.toUpperCase(), x + 0.2, chy + 0.1, boxW - 0.4, 0.2, { fontSize: 7.5, color: MUTED, charSpacing: 1 });
    T(s, val, x + 0.2, chy + 0.29, boxW - 0.4, 0.3, { fontSize: 15, bold: true, color: last ? TEAL : NAVY, charSpacing: -0.5 });
    if (i < 3) T(s, syms[i], x + boxW, chy, symW, chh, { fontSize: 16, color: MUTED, align: "center", valign: "middle" });
  });
  pageNo(s, 4, false);
  if (!hidden) s.addNotes("Planning model with four clickable levels per input. In slideshow, click a value under a slider to switch scenario; Reset returns to the starting scenario (150,000 ED encounters × 6% additional coverage × $4,000 net per encounter = $36M per year; 9,000 identified encounters; $90M associated gross charges at a $10,000 average ED charge). Each figure in the grid = 1,000 ED encounters. Illustrative planning model, not a forecast. The 255 hidden pages after this slide are the other scenarios.");
  return s;
}
financialSlide(DEFAULT_STATE, false);
ALL_STATES.forEach(st => { if (stateKey(st) !== stateKey(DEFAULT_STATE)) financialSlide(st, true); });

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("Wrote", OUT);
})().catch(e => { console.error(e); process.exit(1); });
