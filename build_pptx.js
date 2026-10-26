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
  T(slide, `${String(n).padStart(2, "0")} / 10`, W - M - 2, FOOT_Y + 0.08, 2, 0.25, { fontSize: 8, color: dark ? N_MUTED : MUTED, align: "right", charSpacing: 1.5 });
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

// =====================================================================
// SLIDE 1 — Cover
// =====================================================================
{
  const s = pres.addSlide({ masterName: "COVER" });
  const LW = 7.3; // left column width
  // left column
  s.addImage({ path: LOGO, x: M, y: 0.42, w: 1.44, h: 0.95 });
  T(s, "You deliver care. We recover revenue.", M, 1.75, 6.0, 0.3, { fontSize: 12, color: TEAL, bold: true });
  s.addText([
    { text: "Uncovering revenue.", options: { color: NAVY, breakLine: true } },
    { text: "Strengthening hospital performance.", options: { color: TEAL } },
  ], { x: M, y: 2.1, w: LW, h: 1.95, fontFace: FONT, fontSize: 36, margin: 0, valign: "top", isTextBox: true, charSpacing: -1.5, lineSpacingMultiple: 0.98 });
  T(s, "A strategic revenue identification and recovery partnership — extending Cook County Health's revenue cycle, not replacing it.", M, 4.15, 5.6, 0.95, { fontSize: 13, color: INK2, lineSpacingMultiple: 1.3 });
  // facts
  const fy = 5.45;
  hline(s, M, fy, LW, NAVY, 1.5);
  const fcols = [[M, 3.0, "Prepared for", "Cook County Health\nExecutive Leadership — CEO · CFO · COO"], [M + 3.25, 1.9, "Prepared by", "LaborForce\nMedical Management"], [M + 5.4, 1.9, "Briefing", "Executive proposal\nOctober 2026"]];
  fcols.forEach(([x, w, dt, dd]) => {
    T(s, dt.toUpperCase(), x, fy + 0.2, w, 0.22, { fontSize: 8, bold: true, color: MUTED, charSpacing: 1.5 });
    T(s, dd, x, fy + 0.45, w, 0.65, { fontSize: 10.5, color: NAVY, bold: true, lineSpacingMultiple: 1.2 });
  });
  hline(s, M, FOOT_Y, LW, LINE);
  T(s, "CONFIDENTIAL — FOR DISCUSSION PURPOSES", M, FOOT_Y + 0.08, 5, 0.25, { fontSize: 8, color: MUTED, charSpacing: 1.5 });
  T(s, "01 / 10", M + LW - 2, FOOT_Y + 0.08, 2, 0.25, { fontSize: 8, color: MUTED, align: "right", charSpacing: 1.5 });

  // right: "At a glance" navy panel, full height
  const px = 8.45, pw = W - px;
  rect(s, px, 0, pw, H, NAVY);
  rect(s, px, 0, 0.06, H, TEAL);
  const ix = px + 0.5, iw = pw - 0.95;
  eyebrow(s, "At a glance", ix, 0.6, iw, true, { fontSize: 9 });
  const glance = [["+336%", "Monthly TPL recoveries at Chicago-area partner hospitals, March – July 2026 ($33K → $144K)"], ["90%+", "Payer identification accuracy, up from under 30%"], ["79%", "Of screened July encounters verified (141 of 178)"]];
  glance.forEach(([v, l], i) => {
    const y = 1.0 + i * 1.3;
    if (i > 0) hline(s, ix, y - 0.12, iw, N_LINE);
    T(s, v, ix, y, iw, 0.62, { fontSize: 38, color: "FFFFFF", charSpacing: -2 });
    T(s, l, ix, y + 0.66, iw, 0.5, { fontSize: 10.5, color: N_SPAN, lineSpacingMultiple: 1.2 });
  });
  // the ask
  const ay = 5.05, ah = 1.25;
  rrect(s, ix - 0.1, ay, iw + 0.2, ah, N_ASK, 0.04);
  eyebrow(s, "The ask", ix + 0.1, ay + 0.2, iw, true);
  T(s, "A 90-day pilot at John H. Stroger, Jr. Hospital — transparent, measurable, and jointly reviewed.", ix + 0.1, ay + 0.47, iw - 0.2, 0.7, { fontSize: 12, color: "FFFFFF", lineSpacingMultiple: 1.25 });
  T(s, "Program-reported figures; not independently attributed.", ix, 6.65, iw, 0.25, { fontSize: 9, color: N_NOTE });
  s.addNotes("Cover. Program results are program-reported figures from Chicago-area partner hospitals, March–July 2026; not independently attributed.");
}

// =====================================================================
// SLIDE 2 — Executive summary
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "02", "Executive summary", false);
  title(s, [{ text: "Extending your revenue cycle" }, { text: " — not replacing it.", muted: true }], 0.85, 0.7, 30, false);

  const items = [
    ["01 / Context", "The pressure", "Hospitals face reimbursement challenges, rising operational costs, complex payer requirements, and growing uncompensated care obligations.", false],
    ["02 / Opportunity", "The gap", "In ED, trauma and other encounters, Workers' Compensation, Third-Party Liability, auto and other responsible-party coverage can go unidentified or unpursued by traditional workflows.", false],
    ["03 / Support", "What LaborForce adds", "Specialized payer identification, patient engagement, revenue auditing, payer verification, and lien administration support.", false],
    ["04 / Outcome", "The goal", "Identify additional reimbursement, improve revenue realization, and reduce avoidable administrative work — without replacing current systems or teams.", true],
  ];
  const gy = 1.85, gap = 0.3, cw = (CW - 3 * gap) / 4;
  items.forEach(([eb, h3, p, goal], i) => {
    const x = M + i * (cw + gap);
    hline(s, x, gy, cw, LINE);
    eyebrow(s, eb, x, gy + 0.18, cw, false);
    T(s, h3, x, gy + 0.46, cw, 0.4, { fontSize: 16, bold: true, color: goal ? TEAL : NAVY, charSpacing: -0.5 });
    T(s, p, x, gy + 0.9, cw, 1.5, { fontSize: 11.5, color: INK2, lineSpacingMultiple: 1.25 });
  });

  // How it works strip
  const sy = 4.55;
  hline(s, M, sy, CW, LINE);
  eyebrow(s, "How it works", M, sy + 0.2, 3, false);
  const steps = [
    ["01", "Technology screening", "Injury-related encounters are flagged from existing registration and billing data."],
    ["02", "Specialist review", "Analysts determine the likely responsible payer and what information is missing."],
    ["03", "Direct patient contact", "Dedicated staff confirm the facts and close gaps, respecting each patient's choices."],
    ["04", "Follow-through", "Billing corrections, lien support, and payer follow-up until the account resolves."],
  ];
  steps.forEach(([n, h, p], i) => {
    const x = M + i * (cw + gap);
    T(s, n, x, sy + 0.55, 0.5, 0.25, { fontSize: 10, color: MUTED });
    T(s, h, x + 0.45, sy + 0.52, cw - 0.45, 0.3, { fontSize: 13, bold: true, color: NAVY });
    T(s, p, x + 0.45, sy + 0.88, cw - 0.45, 1.1, { fontSize: 10.5, color: INK2, lineSpacingMultiple: 1.25 });
  });
  pageNo(s, 2, false);
}

// =====================================================================
// SLIDE 3 — The challenge
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "03", "The challenge", false);
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
  // question cards (2 x 3) on the left
  const qy = 2.3, flowW = 3.9, leftW = CW - flowW - 0.4, cgap = 0.12, cardW = (leftW - cgap) / 2, cardH = 0.9;
  qs.forEach((q, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = M + col * (cardW + cgap), y = qy + row * (cardH + cgap);
    rrect(s, x, y, cardW, cardH, PANEL, 0.04);
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.2, y: y + 0.2, w: 0.27, h: 0.27, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
    T(s, String(i + 1).padStart(2, "0"), x + 0.2, y + 0.2, 0.27, 0.27, { fontSize: 7.5, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T(s, q, x + 0.6, y + 0.17, cardW - 0.8, cardH - 0.3, { fontSize: 12, color: NAVY, lineSpacingMultiple: 1.2 });
  });
  const gridH = 3 * cardH + 2 * cgap;

  // flow card on the right: where the revenue goes
  const fx = M + leftW + 0.4;
  s.addShape(pres.ShapeType.roundRect, { x: fx, y: qy, w: flowW, h: gridH, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 }, rectRadius: 0.05 });
  eyebrow(s, "Where the revenue goes", fx + 0.22, qy + 0.2, flowW - 0.4, false);
  const flow = [
    ["Injury-related encounter", "Workplace injury, motor vehicle accident, or incident involving a third party", PANEL, NAVY, INK2],
    ["Responsible payer missed", "Not identified at registration, or identified but not followed through", PANEL, NAVY, INK2],
    ["Absorbed by the hospital", "Written off as bad debt or uncompensated care", NAVY, "FFFFFF", N_SPAN],
  ];
  const fbH = 0.64, farrow = 0.22, fb0 = qy + 0.52, fbw = flowW - 0.44;
  flow.forEach(([h, p, fill, hc, pc], i) => {
    const y = fb0 + i * (fbH + farrow);
    rrect(s, fx + 0.22, y, fbw, fbH, fill, 0.03);
    T(s, h, fx + 0.37, y + 0.08, fbw - 0.3, 0.25, { fontSize: 11.5, bold: true, color: hc, charSpacing: -0.2 });
    T(s, p, fx + 0.37, y + 0.32, fbw - 0.3, 0.3, { fontSize: 8.5, color: pc, lineSpacingMultiple: 1.1 });
    if (i < 2) s.addShape(pres.ShapeType.line, { x: fx + flowW / 2, y: y + fbH + 0.04, w: 0, h: farrow - 0.08, line: { color: TEAL, width: 1.25, endArrowType: "triangle" } });
  });

  // consequence bar
  const cy = qy + gridH + 0.3, chh = 0.72;
  rect(s, M, cy, CW, chh, TEALL);
  rect(s, M, cy, 0.05, chh, TEAL);
  eyebrow(s, "The consequence", M + 0.3, cy + 0.26, 1.8, false);
  T(s, "Valid reimbursement opportunities may remain unidentified, incorrectly routed, delayed, or insufficiently pursued.", M + 2.2, cy, CW - 2.5, chh, { fontSize: 13, color: NAVY, valign: "middle" });
  pageNo(s, 3, false);
}

// =====================================================================
// SLIDE 4 — The LaborForce solution (navy)
// =====================================================================
{
  const s = pres.addSlide({ masterName: "NAVY" });
  kicker(s, "04", "The LaborForce solution", true);
  title(s, [{ text: "A specialized operational layer.", breakLine: true }, { text: "Five critical functions.", muted: true }], 0.85, 1.2, 30, true);

  const fns = [
    ["Proactive Revenue Identification", "Review injury-related encounters, identify potentially responsible payers, and prioritize accounts for investigation."],
    ["Dedicated Patient Engagement", "Outreach to verify injury circumstances and collect missing claim, employer, insurer, or attorney information."],
    ["Payer Verification & RCM Coordination", "Coordinate findings with registration, billing, and revenue cycle teams for payer determination and follow-up."],
    ["Revenue Auditing & Reconciliation", "Monitor unresolved cases, flag missing or inconsistent information, and track case status and reimbursement."],
    ["Lien Administration & Recovery", "Support approved lien documentation, follow-up, and reimbursement tracking within the legal and contractual framework."],
  ];
  const gy = 2.4, gap = 0.28, cw = (CW - 4 * gap) / 5;
  fns.forEach(([h, p], i) => {
    const x = M + i * (cw + gap);
    hline(s, x, gy, cw, N_LINE);
    T(s, String(i + 1).padStart(2, "0"), x, gy + 0.2, 0.6, 0.25, { fontSize: 10, color: N_TEAL });
    T(s, h, x, gy + 0.5, cw, 0.75, { fontSize: 14, bold: true, color: "FFFFFF", charSpacing: -0.3, lineSpacingMultiple: 1.1 });
    T(s, p, x, gy + 1.3, cw, 1.4, { fontSize: 10.5, color: N_BODY, lineSpacingMultiple: 1.25 });
  });

  callout(s, "Working alongside your team", "LaborForce does not replace hospital billing or collection operations. We uncover and advance opportunities that existing workflows may not have the specialized resources to fully investigate.", M, 5.35, 11.2, 1.1, true, 14);
  pageNo(s, 4, true);
}

// =====================================================================
// SLIDE 5 — Operating experience
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "05", "Experience with healthcare partners", false);
  title(s, [{ text: "Proven operating experience", breakLine: true }, { text: "in Chicago-area hospitals.", muted: true }], 0.85, 1.2, 30, false);

  // left: partners
  const lx = M, lw = 3.5, ty = 2.25;
  eyebrow(s, "Current program partners", lx, ty, lw, false);
  hline(s, lx, ty + 0.35, lw, LINE);
  T(s, "Northwestern\nMedicine", lx, ty + 0.5, lw, 0.9, { fontSize: 22, color: NAVY, charSpacing: -1, lineSpacingMultiple: 1.05 });
  hline(s, lx, ty + 1.45, lw, LINE);
  T(s, "Humboldt\nPark Health", lx, ty + 1.6, lw, 0.9, { fontSize: 22, color: NAVY, charSpacing: -1, lineSpacingMultiple: 1.05 });

  // right: list
  const rx = M + 4.2, rw = CW - 4.2;
  T(s, "These partnerships have built operational experience in:", rx, ty, rw, 0.3, { fontSize: 12.5, color: INK, bold: true });
  const checks = [
    "Screening emergency department encounters for potential TPL/WC opportunities",
    "Implementing dedicated patient engagement and case investigation workflows",
    "Coordinating across hospital departments and revenue cycle teams",
    "Tracking potentially recoverable cases and resolving missing information",
    "Building reporting and audit processes that support hospital financial visibility",
  ];
  const runs = [];
  checks.forEach((c, i) => {
    runs.push({ text: "✓   ", options: { color: TEAL, bold: true } });
    runs.push({ text: c, options: { color: INK2, breakLine: i < checks.length - 1 } });
  });
  s.addText(runs, { x: rx, y: ty + 0.42, w: rw, h: 2.0, fontFace: FONT, fontSize: 11.5, margin: 0, valign: "top", isTextBox: true, paraSpaceAfter: 6, lineSpacingMultiple: 1.15 });

  // results band
  const by = 4.9, bh = 1.9;
  rrect(s, M, by, CW, bh, NAVY, 0.04);
  T(s, "PROGRAM RESULTS · MARCH – JULY 2026", M + 0.3, by + 0.25, 5, 0.22, { fontSize: 8, bold: true, color: N_TEAL, charSpacing: 1.5 });
  T(s, "Program-reported; not independently attributed", M + CW - 5.3, by + 0.25, 5, 0.22, { fontSize: 9, color: N_SPAN, align: "right", italic: true });
  const stats = [
    ["+336%", "Monthly TPL recoveries\n$33K → $144K"],
    ["90%+", "Payer identification accuracy\nup from under 30%"],
    ["141 / 178", "July encounters verified\n79% of those screened"],
    ["$198,940", "Charges on 32 Workers' Comp\ncases identified in July"],
  ];
  const sw = (CW - 0.6) / 4;
  stats.forEach(([v, l], i) => {
    const x = M + 0.3 + i * sw;
    if (i > 0) vline(s, x - 0.15, by + 0.7, 0.95, N_LINE);
    T(s, v, x, by + 0.65, sw - 0.3, 0.5, { fontSize: 26, color: "FFFFFF", charSpacing: -1 });
    T(s, l, x, by + 1.2, sw - 0.3, 0.55, { fontSize: 10, color: N_SPAN, lineSpacingMultiple: 1.15 });
  });
  pageNo(s, 5, false);
}

// =====================================================================
// SLIDE 6 — Opportunity at CCH
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "06", "Opportunity at Cook County Health", false);
  title(s, [{ text: "A focused TPL/WC program for a high-volume safety-net system." }], 0.85, 0.6, 28, false);
  T(s, "Cook County Health serves a high volume of patients through its emergency departments, trauma services, and broader network. A focused revenue identification program could help CCH:", M, 1.5, 11, 0.6, { fontSize: 12, color: INK2, lineSpacingMultiple: 1.25 });

  const outs = [
    ["Find coverage", "Evaluate whether additional responsible-party coverage exists for selected encounters."],
    ["Document claims", "Improve identification and documentation of injury-related claims."],
    ["Bill accurately", "Strengthen billing accuracy and reimbursement follow-up."],
    ["Stop leakage", "Reduce avoidable revenue leakage."],
    ["Gain visibility", "Establish clearer visibility into potentially recoverable accounts."],
    ["Protect the mission", "Support financial sustainability without compromising access to care."],
  ];
  const gy = 2.4, gap = 0.35, cw = (CW - 2 * gap) / 3, rh = 1.2;
  outs.forEach(([h, p], i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = M + col * (cw + gap), y = gy + row * rh;
    hline(s, x, y, cw, LINE);
    T(s, String(i + 1).padStart(2, "0"), x, y + 0.15, 0.5, 0.25, { fontSize: 9, color: TEAL });
    T(s, h, x + 0.45, y + 0.12, cw - 0.45, 0.3, { fontSize: 14, bold: true, color: NAVY, charSpacing: -0.3 });
    T(s, p, x + 0.45, y + 0.45, cw - 0.45, 0.65, { fontSize: 10.5, color: INK2, lineSpacingMultiple: 1.2 });
  });

  // context strip
  const cy = 5.0;
  hline(s, M, cy, CW, "C8D3C9");
  const half = (CW - 0.6) / 2;
  eyebrow(s, "Why Cook County Health", M, cy + 0.2, half, false);
  T(s, "A safety-net system with high-volume emergency and trauma services, where injury-related encounters are frequent and every recovered dollar protects access to community care.", M, cy + 0.5, half, 1.2, { fontSize: 11.5, color: INK2, lineSpacingMultiple: 1.25 });
  const x2 = M + half + 0.6;
  eyebrow(s, "Illustrative sizing", x2, cy + 0.2, half, false);
  s.addText([
    { text: "150,000", options: { bold: true, color: NAVY } }, { text: " ED encounters × " },
    { text: "6%", options: { bold: true, color: NAVY } }, { text: " with additional coverage × " },
    { text: "$4,000", options: { bold: true, color: NAVY } }, { text: " net per encounter ≈ " },
    { text: "$36M", options: { bold: true, color: NAVY } }, { text: " per year. A planning model, not a forecast — adjustable on the next page." },
  ], { x: x2, y: cy + 0.5, w: half, h: 1.2, fontFace: FONT, fontSize: 11.5, color: INK2, margin: 0, valign: "top", isTextBox: true, lineSpacingMultiple: 1.25 });
  pageNo(s, 6, false);
}

// =====================================================================
// SLIDE 7 — Financial opportunity (static model, default scenario)
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "07", "Financial opportunity", false);
  title(s, [{ text: "Turn assumptions into a visible opportunity." }], 0.85, 0.55, 28, false);
  T(s, "Four planning assumptions at the starting scenario, with the coverage and collection results shown together.", M, 1.42, 10, 0.3, { fontSize: 12, color: INK2 });

  // left: assumptions
  const lx = M, lw = 4.2, ay = 1.95;
  s.addShape(pres.ShapeType.ellipse, { x: lx, y: ay + 0.06, w: 0.1, h: 0.1, fill: { color: TEAL }, line: { color: TEAL, width: 0 } });
  T(s, "PLANNING ASSUMPTIONS", lx + 0.18, ay, lw, 0.22, { fontSize: 8, bold: true, color: MUTED, charSpacing: 1.5 });
  const assumptions = [
    ["01", "Annual ED encounters", "150,000", "Annual emergency department visits, including repeat visits."],
    ["02", "Additional coverage identified", "6%", "Share of encounters with an additional collectible coverage opportunity."],
    ["03", "Average incremental net collection", "$4,000", "Average additional net collection per identified encounter."],
    ["04", "Average ED charge", "$17,000", "Gross charge per identified encounter, before collection adjustments."],
  ];
  const arH = 0.92;
  assumptions.forEach(([n, lab, val, desc], i) => {
    const y = ay + 0.4 + i * arH;
    hline(s, lx, y, lw, LINE);
    T(s, [{ text: n + "  ", options: { color: TEAL, fontSize: 9 } }, { text: lab, options: { color: INK, bold: true } }], lx, y + 0.14, lw - 1.3, 0.3, { fontSize: 11.5 });
    T(s, val, lx + lw - 1.3, y + 0.1, 1.3, 0.35, { fontSize: 15, bold: true, color: NAVY, align: "right", charSpacing: -0.5 });
    T(s, desc, lx, y + 0.47, lw, 0.4, { fontSize: 9.5, color: MUTED, lineSpacingMultiple: 1.15 });
  });
  hline(s, lx, ay + 0.4 + 4 * arH, lw, LINE);

  // right: result strip
  const rx = M + 4.8, rw = CW - 4.8, ry = 1.95, rh = 1.5;
  rrect(s, rx, ry, rw, rh, NAVY, 0.04);
  const c1 = rw * 0.36, c2 = rw * 0.31, c3 = rw - c1 - c2;
  const labO = { fontSize: 7.5, bold: true, color: N_TEAL, charSpacing: 0.5, lineSpacingMultiple: 1.1 };
  T(s, "ANNUAL INCREMENTAL NET COLLECTIONS", rx + 0.28, ry + 0.24, c1 - 0.45, 0.38, labO);
  T(s, "$36M", rx + 0.28, ry + 0.58, c1 - 0.4, 0.6, { fontSize: 36, color: "FFFFFF", charSpacing: -2 });
  T(s, "Starting scenario", rx + 0.28, ry + 1.18, c1 - 0.4, 0.22, { fontSize: 9, color: N_SPAN });
  vline(s, rx + c1, ry + 0.3, rh - 0.6, N_LINE);
  T(s, "IDENTIFIED ENCOUNTERS / YEAR", rx + c1 + 0.25, ry + 0.24, c2 - 0.4, 0.38, labO);
  T(s, "9,000", rx + c1 + 0.25, ry + 0.62, c2 - 0.4, 0.5, { fontSize: 26, color: "FFFFFF", charSpacing: -1 });
  T(s, "6% of 150,000 encounters", rx + c1 + 0.25, ry + 1.18, c2 - 0.4, 0.22, { fontSize: 9, color: N_SPAN });
  vline(s, rx + c1 + c2, ry + 0.3, rh - 0.6, N_LINE);
  T(s, "ASSOCIATED GROSS CHARGES / YEAR", rx + c1 + c2 + 0.25, ry + 0.24, c3 - 0.45, 0.38, labO);
  T(s, "$153M", rx + c1 + c2 + 0.25, ry + 0.62, c3 - 0.45, 0.5, { fontSize: 26, color: "FFFFFF", charSpacing: -1 });
  T(s, "23.5% assumed net-to-gross collection", rx + c1 + c2 + 0.25, ry + 1.18, c3 - 0.4, 0.22, { fontSize: 9, color: N_SPAN });

  // right: sensitivity chart
  const chy = ry + rh + 0.15;
  eyebrow(s, "Coverage sensitivity", rx, chy, 4, false);
  T(s, "What changes as coverage improves?", rx, chy + 0.24, 4.6, 0.3, { fontSize: 13, bold: true, color: NAVY, charSpacing: -0.3 });
  T(s, [{ text: "$36M", options: { bold: true, color: NAVY } }, { text: " at 6% identified coverage", options: { color: INK2 } }], rx + 4.6, chy + 0.26, rw - 4.6, 0.3, { fontSize: 11, align: "right" });
  const rates = [2, 3, 4, 5, 6, 7, 8, 9, 10];
  const vals = rates.map(r => 150000 * r / 100 * 4000 / 1e6); // $M
  s.addChart(pres.ChartType.line, [{ name: "Annual net collections ($M)", labels: rates.map(r => r + "%"), values: vals }], {
    x: rx - 0.1, y: chy + 0.52, w: rw + 0.1, h: 1.5,
    chartColors: [TEAL], lineSize: 2.25, lineDataSymbol: "circle", lineDataSymbolSize: 6, lineDataSymbolLineColor: TEAL,
    showLegend: false, showTitle: false,
    showValue: true, dataLabelPosition: "t", dataLabelFormatCode: '"$"0"M"', dataLabelFontSize: 8, dataLabelColor: INK2, dataLabelFontFace: FONT,
    valAxisMinVal: 0, valAxisMaxVal: 70, valAxisMajorUnit: 10, valAxisLabelFormatCode: '"$"0"M"', valAxisLabelFontSize: 8, valAxisLabelColor: MUTED, valAxisLabelFontFace: FONT,
    valGridLine: { color: "DDE3DE", size: 0.5 }, catGridLine: { style: "none" },
    catAxisLabelFontSize: 8, catAxisLabelColor: MUTED, catAxisLabelFontFace: FONT,
    catAxisTitle: "Additional coverage identified (%)", showCatAxisTitle: true, catAxisTitleFontSize: 8, catAxisTitleColor: MUTED, catAxisTitleFontFace: FONT,
    valAxisLineShow: false, catAxisLineShow: false, plotArea: { fill: { color: PAPER } }, chartArea: { fill: { color: PAPER } },
  });
  T(s, "The line compares 2% to 10% identified coverage at 150,000 encounters and $4,000 net collection per encounter.", rx, chy + 2.05, rw, 0.22, { fontSize: 8.5, color: MUTED, italic: true });

  // calculation chain
  const cy = 5.98, ch = 0.6;
  const chain = [["Annual encounters", "150,000"], ["Additional coverage", "6%"], ["Net collection / encounter", "$4,000"], ["Annual net collections", "$36,000,000"]];
  const syms = ["×", "×", "="];
  const symW = 0.4, boxW = (CW - 3 * symW) / 4;
  chain.forEach(([lab, val], i) => {
    const x = M + i * (boxW + symW);
    const last = i === 3;
    if (last) rrect(s, x, cy, boxW, ch, TEALL, 0.03);
    else s.addShape(pres.ShapeType.roundRect, { x, y: cy, w: boxW, h: ch, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 }, rectRadius: 0.03 });
    T(s, lab.toUpperCase(), x + 0.2, cy + 0.1, boxW - 0.4, 0.2, { fontSize: 7.5, color: MUTED, charSpacing: 1 });
    T(s, val, x + 0.2, cy + 0.28, boxW - 0.4, 0.3, { fontSize: 15, bold: true, color: last ? TEAL : NAVY, charSpacing: -0.5 });
    if (i < 3) T(s, syms[i], x + boxW, cy, symW, ch, { fontSize: 16, color: MUTED, align: "center", valign: "middle" });
  });

  T(s, [{ text: "Illustrative, not a forecast. ", options: { bold: true, color: NAVY } }, { text: "Replace planning assumptions with Cook County Health encounter, payer and collection data during discovery. No program costs are deducted in this model.", options: { color: INK2 } }], M, 6.65, CW, 0.28, { fontSize: 10 });
  pageNo(s, 7, false);
  s.addNotes("Static version of the interactive planning model at its starting scenario: 150,000 ED encounters × 6% additional coverage × $4,000 net per encounter = $36M per year; 9,000 identified encounters; $153M associated gross charges at a $17,000 average ED charge; 23.5% assumed net-to-gross collection. Illustrative, not a forecast.");
}

// =====================================================================
// SLIDE 8 — 90-day pilot
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "08", "Proposed partnership", false);
  title(s, [{ text: "90-day pilot.", breakLine: true }, { text: "John H. Stroger, Jr. Hospital.", muted: true }], 0.85, 1.2, 30, false);

  // phase cards
  const phases = [
    ["Phase 01", "Days 1 – 15", 15, "Discovery & Baseline", "Review current injury-related registration, payer identification, billing, and follow-up. Agree on pilot scope, eligibility criteria, compliance requirements, and baseline measures.", "DBE8F7", NAVY, "5B8FD6"],
    ["Phase 02", "Days 16 – 60", 45, "Identification & Investigation", "Evaluate designated encounters, conduct authorized patient outreach, identify alternative payer sources, and coordinate verified findings with existing hospital teams.", TEAL, "FFFFFF", TEAL],
    ["Phase 03", "Days 61 – 90", 30, "Validation & Review", "Reconcile outcomes, review billing corrections and collections, assess operational impact, and recommend continued monitoring and potential expansion.", NAVY, "FFFFFF", NAVY],
  ];
  const py = 2.2, gap = 0.3, cw = (CW - 2 * gap) / 3, ch = 2.5, hh = 0.4;
  phases.forEach(([ph, days, d, h, p, hfill, hcol, mfill], i) => {
    const x = M + i * (cw + gap);
    s.addShape(pres.ShapeType.roundRect, { x, y: py, w: cw, h: ch, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 }, rectRadius: 0.05 });
    rect(s, x + 0.01, py + 0.01, cw - 0.02, hh, hfill);
    T(s, ph.toUpperCase(), x + 0.25, py, cw / 2, hh, { fontSize: 9, bold: true, color: hcol, charSpacing: 1, valign: "middle" });
    T(s, days.toUpperCase(), x + cw / 2, py, cw / 2 - 0.25, hh, { fontSize: 9, bold: true, color: hcol, charSpacing: 1, valign: "middle", align: "right" });
    // meter
    const my = py + hh + 0.22, mw = cw - 0.5 - 1.1;
    rrect(s, x + 0.25, my, mw, 0.08, PANEL, 0.03);
    rrect(s, x + 0.25, my, mw * d / 90, 0.08, mfill, 0.03);
    T(s, `${d} of 90 days`, x + 0.25 + mw + 0.12, my - 0.08, 1.0, 0.24, { fontSize: 8.5, color: MUTED });
    T(s, h, x + 0.25, py + hh + 0.45, cw - 0.5, 0.35, { fontSize: 15, bold: true, color: NAVY, charSpacing: -0.3 });
    T(s, p, x + 0.25, py + hh + 0.85, cw - 0.5, 1.2, { fontSize: 10.5, color: INK2, lineSpacingMultiple: 1.25 });
  });

  // lower: callout + roles
  const ly = py + ch + 0.3;
  hline(s, M, ly, CW, LINE);
  const callW = 4.8;
  callout(s, "How to read the pilot", [
    { text: "Many claims take longer than 90 days to resolve. The pilot measures " },
    { text: "leading indicators", options: { bold: true, color: NAVY } },
    { text: " and any collections realized; final financial performance is reviewed as the identified account cohort matures." },
  ], M, ly + 0.25, callW, 1.5, false, 11);
  const rx0 = M + callW + 0.5, rw0 = CW - callW - 0.5, half = (rw0 - 0.3) / 2;
  eyebrow(s, "Cook County Health provides", rx0, ly + 0.25, half, false);
  bullets(s, ["Executive sponsor and agreed pilot scope", "ED volume, payer mix, and current TPL/WC workflow data", "Compliance requirements and data-access terms"], rx0, ly + 0.52, half, 1.3, { fontSize: 10.5, paraSpaceAfter: 3 });
  eyebrow(s, "LaborForce provides", rx0 + half + 0.3, ly + 0.25, half, false);
  bullets(s, ["Screening, specialist review, and case investigation", "Dedicated patient outreach and lien administration support", "Joint reporting at days 30, 60, and 90"], rx0 + half + 0.3, ly + 0.52, half, 1.3, { fontSize: 10.5, paraSpaceAfter: 3 });
  pageNo(s, 8, false);
}

// =====================================================================
// SLIDE 9 — Success metrics
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kicker(s, "09", "Proposed success metrics", false);
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

  // cadence track
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
  pageNo(s, 9, false);
}

// =====================================================================
// SLIDE 10 — Partnership objective (navy)
// =====================================================================
{
  const s = pres.addSlide({ masterName: "CLOSING" });
  kicker(s, "10", "Partnership objective", true);
  s.addText([
    { text: "Strengthen Cook County Health's fiscal resilience — ", options: { color: "FFFFFF" } },
    { text: "while supporting accessible, high-quality care for the community.", options: { color: N_TITLE_MUTED } },
  ], { x: M, y: 0.85, w: CW, h: 1.25, fontFace: FONT, fontSize: 28, margin: 0, valign: "top", isTextBox: true, charSpacing: -1, lineSpacingMultiple: 1.05 });
  T(s, "We uncover reimbursement opportunities that traditional workflows may overlook, and we welcome the chance to evaluate the impact together through a focused, transparent, and measurable pilot.", M, 2.2, 10.2, 0.7, { fontSize: 12.5, color: N_BODY, lineSpacingMultiple: 1.3 });

  // step cards
  const steps = [["Confirm sponsor & scope", "Executive sponsor and pilot scope at Stroger Hospital"], ["Share baseline data", "ED volume, payer mix, and the current TPL/WC workflow"], ["Agree & launch", "Compliance requirements and success metrics; launch Phase 1"]];
  const sy = 3.15, sgap = 0.3, sw = (CW - 2 * sgap) / 3, sh = 1.85;
  steps.forEach(([h, p], i) => {
    const x = M + i * (sw + sgap);
    s.addShape(pres.ShapeType.roundRect, { x, y: sy, w: sw, h: sh, fill: { color: N_CARD }, line: { color: N_CARD_LINE, width: 0.75 }, rectRadius: 0.05 });
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.3, y: sy + 0.3, w: 0.32, h: 0.32, fill: { color: TEAL }, line: { color: TEAL, width: 0 } });
    T(s, String(i + 1).padStart(2, "0"), x + 0.3, sy + 0.3, 0.32, 0.32, { fontSize: 8.5, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T(s, h, x + 0.3, sy + 0.78, sw - 0.6, 0.35, { fontSize: 16, bold: true, color: "FFFFFF", charSpacing: -0.3 });
    T(s, p, x + 0.3, sy + 1.17, sw - 0.6, 0.6, { fontSize: 11, color: N_BODY, lineSpacingMultiple: 1.25 });
  });

  // bottom: logo + thank-you
  const ly = 5.55;
  rrect(s, M, ly, 1.75, 1.1, "FFFFFF", 0.05);
  s.addImage({ path: LOGO, x: M + 0.2, y: ly + 0.1, w: 1.35, h: 0.89 });
  T(s, "Thank you", W - M - 4.4, ly + 0.3, 4.4, 0.3, { fontSize: 14, bold: true, color: "FFFFFF", align: "right" });
  T(s, "We look forward to discussing a pilot at Stroger with your leadership team.", W - M - 4.4, ly + 0.62, 4.4, 0.5, { fontSize: 10.5, color: N_BODY, align: "right", lineSpacingMultiple: 1.25 });
  pageNo(s, 10, true);
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("Wrote", OUT);
})().catch(e => { console.error(e); process.exit(1); });
