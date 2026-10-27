# -*- coding: utf-8 -*-
"""Transform the original LaborForce deck into the refined version.

Usage: python -I build_refined.py <original.html> <output.html>
Needs brand/logo_mark.png, brand/logo_full.png (made by prepare_logo.py),
brand/nm_logo.svg and brand/hph_logo.png (partner logos).
"""
import base64
import os
import re
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
with open(src_path, encoding='utf-8') as f:
    lines = f.read().split('\n')

# ---------------------------------------------------------------------------
# 1. Drop the three.js bundle + lfm-blender-scene component (lines 460..4439).
# ---------------------------------------------------------------------------
assert lines[459].startswith('(()=>{var $l=0,Zo=1'), lines[459][:40]
assert lines[4438] == '*/', repr(lines[4438])
lines = lines[:459] + lines[4439:]
html = '\n'.join(lines)


def replace_once(old, new, label):
    count = html.count(old)
    assert count == 1, f'{label}: expected 1 match, found {count}'
    return html.replace(old, new)


def replace_section(section_id, new_markup):
    """Swap a whole <section id="..."> ... </section> block."""
    global html
    pattern = re.compile(r'<section class="report-section[^"]*" id="' + section_id + r'".*?</section>', re.S)
    assert len(pattern.findall(html)) == 1, section_id
    html = pattern.sub(lambda m: new_markup, html)


def data_uri(name, mime):
    with open(os.path.join(here, 'brand', name), 'rb') as fh:
        return 'data:' + mime + ';base64,' + base64.b64encode(fh.read()).decode('ascii')


mark_uri = data_uri('logo_mark.png', 'image/png')
full_uri = data_uri('logo_full.png', 'image/png')
nm_uri = data_uri('nm_logo.svg', 'image/svg+xml')
hph_uri = data_uri('hph_logo.png', 'image/png')
hospital_uri = data_uri('hospital_cover.jpg', 'image/jpeg')  # Unsplash photo 1586773860418, Unsplash License
LOGO_FULL = '<img class="%s" src="' + full_uri + '" alt="LaborForce Medical Management" width="640" height="421" decoding="async">'
ARROW_DOWN = '<div class="flow-arrow" aria-hidden="true"><svg viewBox="0 0 16 16"><path d="M8 2v11M3.5 8.5 8 13l4.5-4.5"/></svg></div>'

# ---------------------------------------------------------------------------
# 2. Header: logo mark replaces the typed "LF"; drop "Prepared for Cook County Health".
# ---------------------------------------------------------------------------
html = replace_once('<span class="brand-symbol" aria-hidden="true">L<span>F</span></span>',
                    '<img class="brand-mark" src="' + mark_uri + '" alt="" width="177" height="160" decoding="async">', 'header mark')
html = replace_once('    <div class="header-context"><span>Prepared for</span><strong>Cook County Health</strong></div>\n', '', 'header context')

# ---------------------------------------------------------------------------
# 3. Cover: tagline + title at top-left, facts row with the logo in "Prepared by",
#    navy "at a glance" panel with a one-line ask.
# ---------------------------------------------------------------------------
replace_section('cover', '''<section class="report-section report-cover is-active" id="cover" data-label="Introduction" aria-labelledby="cover-title">
        <div class="cover-left">
          <img class="cover-photo" src="''' + hospital_uri + '''" alt="" aria-hidden="true" decoding="async">
          <div class="cover-body">
            <p class="cover-pretitle">You deliver care. We recover revenue.</p>
            <h1 id="cover-title">Uncovering revenue.<br><span>Strengthening hospital performance.</span></h1>
            <p class="cover-deck">A revenue identification and recovery partnership for Cook County Health's emergency and trauma care.</p>
            <div class="cover-partners"><span class="eyebrow">Hospital partners</span><div class="cover-partner-logos"><img src="''' + nm_uri + '''" alt="Northwestern Medicine" width="730" height="137" decoding="async"><img src="''' + hph_uri + '''" alt="Humboldt Park Health" width="782" height="227" decoding="async"></div></div>
          </div>
          <div class="section-foot"><span>Confidential — for discussion purposes</span><span>01 / 10</span></div>
        </div>
        <aside class="cover-panel" aria-label="At a glance">
          <span class="eyebrow">At a glance</span>
          <div class="glance-stat"><strong>+336%</strong><span>Monthly TPL recoveries at Chicago-area partner hospitals, March – July 2026 ($33K → $144K)</span></div>
          <div class="glance-stat"><strong>90%+</strong><span>Payer identification accuracy, up from under 30%</span></div>
          <div class="glance-stat"><strong>79%</strong><span>Of screened July encounters verified (141 of 178)</span></div>
          <p class="glance-ask"><span class="eyebrow">The ask</span>A 90-day pilot at John H. Stroger, Jr. Hospital</p>
          <p class="glance-note">Program-reported figures; not independently attributed.</p>
        </aside>
      </section>''')

# ---------------------------------------------------------------------------
# 4. Slide 2: card styling is CSS-only; add the "How it works" strip.
# ---------------------------------------------------------------------------
html = replace_once('''        <div class="section-foot"><span>LaborForce Medical Management</span><span>02 / 10</span></div>''',
'''        <div class="method-strip" aria-label="How the program works">
          <span class="callout-label">How it works</span>
          <ol class="method-steps">
            <li><span>01</span><strong>Technology screening</strong><p>Injury-related encounters are flagged from existing registration and billing data.</p></li>
            <li><span>02</span><strong>Specialist review</strong><p>Analysts determine the likely responsible payer and what information is missing.</p></li>
            <li><span>03</span><strong>Direct patient contact</strong><p>Dedicated staff confirm the facts and close gaps, respecting each patient's choices.</p></li>
            <li><span>04</span><strong>Follow-through</strong><p>Billing corrections, lien support, and payer follow-up until the account resolves.</p></li>
          </ol>
        </div>
        <div class="section-foot"><span>LaborForce Medical Management</span><span>02 / 10</span></div>''', 'slide 2 strip')

html = replace_once('<h2 id="summary-title">Extending your revenue cycle<span class="title-muted"> — not replacing it.</span></h2>',
                    '<h2 id="summary-title">We work inside the revenue cycle<span class="title-muted"> you already run.</span></h2>', 'slide 2 title')

# ---------------------------------------------------------------------------
# 5. Slide 3: equal-height question cards, matched flow card, consequence at the bottom.
# ---------------------------------------------------------------------------
replace_section('challenge', '''<section class="report-section" id="challenge" data-label="The challenge" aria-labelledby="challenge-title">
        <div class="section-kicker"><span>03</span> The challenge</div>
        <div class="section-heading"><h2 id="challenge-title">Revenue that traditional workflows may overlook.</h2><p class="section-intro">Patients often arrive after workplace incidents, motor vehicle accidents, or injuries involving another liable party. Registration and billing workflows may not consistently capture or resolve:</p></div>
        <div class="challenge-grid">
          <ol class="question-cards">
            <li><span>01</span><p>Whether the injury occurred while the patient was working</p></li>
            <li><span>02</span><p>Whether a motor vehicle or other third party may be responsible</p></li>
            <li><span>03</span><p>Whether another insurer or payer should be investigated</p></li>
            <li><span>04</span><p>Whether the hospital has the right claim, attorney, or payer information</p></li>
            <li><span>05</span><p>Whether a hospital lien is available, documented, and followed up</p></li>
            <li><span>06</span><p>Whether unresolved cases need investigation after discharge</p></li>
          </ol>
          <div class="flow-card" aria-label="Where overlooked revenue goes">
            <span class="callout-label">Where the revenue goes</span>
            <ol class="flow-steps">
              <li><strong>Injury-related encounter</strong><span>Workplace injury, motor vehicle accident, or incident involving a third party</span></li>
              ''' + ARROW_DOWN + '''
              <li><strong>Responsible payer missed</strong><span>Not identified at registration, or identified but not followed through</span></li>
              ''' + ARROW_DOWN + '''
              <li class="flow-end"><strong>Absorbed by the hospital</strong><span>Written off as bad debt or uncompensated care</span></li>
            </ol>
          </div>
        </div>
        <div class="consequence-bar"><span class="callout-label">The consequence</span><p>Valid reimbursement opportunities may remain unidentified, incorrectly routed, delayed, or insufficiently pursued.</p></div>
        <div class="section-foot"><span>LaborForce Medical Management</span><span>03 / 10</span></div>
      </section>''')

# ---------------------------------------------------------------------------
# 6. Slide 4: LaborForce drawn as a layer between the existing revenue cycle
#    and the recovered outcome.
# ---------------------------------------------------------------------------
def build_cake():
    """Five isometric slabs stacked top-to-bottom, with flow lines in the gaps."""
    cx, w, h, t = 260, 200, 38, 18
    ys = [52, 170, 288, 406, 524]
    colors = [  # top, left face, right face
        ('#BFEFE0', '#7ADBC0', '#3DB48F'),
        ('#8FE0C9', '#4CC9A6', '#1D9E75'),
        ('#9CC8F0', '#5AA2E6', '#2F7FCB'),
        ('#6FB0EE', '#3A8FDB', '#1F67AE'),
        ('#4A97E2', '#2B74BE', '#1A5590'),
    ]
    out = []
    for i, y in enumerate(ys, start=1):
        top_c, left_c, right_c = colors[i - 1]
        out.append(
            f'<g class="slab" data-i="{i}" tabindex="0" role="button" aria-label="Layer {i}">'
            f'<polygon class="face-l" points="{cx-w},{y} {cx},{y+h} {cx},{y+h+t} {cx-w},{y+t}" fill="{left_c}"/>'
            f'<polygon class="face-r" points="{cx+w},{y} {cx},{y+h} {cx},{y+h+t} {cx+w},{y+t}" fill="{right_c}"/>'
            f'<polygon class="face-t" points="{cx-w},{y} {cx},{y-h} {cx+w},{y} {cx},{y+h}" fill="{top_c}"/>'
            f'<text class="slab-num" x="{cx}" y="{y+5}" text-anchor="middle">{i:02d}</text></g>')
        if i < 5:
            y1, y2 = y + h + t, ys[i] - h + 6
            out.append(
                f'<g class="gap" data-gap="{i}" aria-hidden="true">'
                f'<line class="flow-line" x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}"/>'
                f'<circle class="drop" cx="{cx}" cy="{y1}" r="3.2"/><circle class="drop d2" cx="{cx}" cy="{y1}" r="3.2"/></g>')
    return ('<svg class="cake" viewBox="0 0 520 610" role="img" aria-label="Five layers, from identification at the top to recovery at the bottom">'
            '<title>Five-layer waterfall</title>' + ''.join(out) + '</svg>')


FUNCTIONS = [
    ('Proactive Revenue Identification', 'Review injury-related encounters, identify potentially responsible payers, and prioritize accounts for investigation.'),
    ('Dedicated Patient Engagement', 'Outreach to verify injury circumstances and collect missing claim, employer, insurer, or attorney information.'),
    ('Payer Verification &amp; RCM Coordination', 'Coordinate findings with registration, billing, and revenue cycle teams for payer determination and follow-up.'),
    ('Revenue Auditing &amp; Reconciliation', 'Monitor unresolved cases, flag missing or inconsistent information, and track case status and reimbursement.'),
    ('Lien Administration &amp; Recovery', 'Support approved lien documentation, follow-up, and reimbursement tracking within the legal and contractual framework.'),
]
rows = ''.join(
    f'<li class="fn-row" data-i="{i}" tabindex="0"><span class="fn-num">{i:02d}</span><div><strong>{name}</strong><p>{desc}</p></div><i class="fn-bar" aria-hidden="true"></i></li>'
    for i, (name, desc) in enumerate(FUNCTIONS, start=1))

replace_section('solution', '''<section class="report-section solution-section" id="solution" data-label="Our approach" aria-labelledby="solution-title">
        <div class="section-kicker"><span>04</span> Five critical functions</div>
        <div class="section-heading"><h2 id="solution-title">The LaborForce solution.<br><span class="title-muted">A specialized operational layer.</span></h2></div>
        <div class="layer-demo" id="layer-demo">
          ''' + build_cake() + '''
          <div class="fn-col">
            <ol class="fn-list">''' + rows + '''</ol>
            <p class="layer-note">LaborForce works alongside your billing and collections teams.</p>
          </div>
        </div>
        <div class="section-foot"><span>LaborForce Medical Management</span><span>04 / 10</span></div>
      </section>''')

# ---------------------------------------------------------------------------
# 7-8. Slides 5 and 6 removed (user, 2026-10-26). The partner logos moved to the
#      cover; the cover panel keeps the headline results.
# ---------------------------------------------------------------------------
for sid in ('experience', 'opportunity'):
    pattern = re.compile(r'\s*<section class="report-section[^"]*" id="' + sid + r'".*?</section>', re.S)
    assert len(pattern.findall(html)) == 1, sid
    html = pattern.sub('', html)
html = replace_once('          <li><a href="#experience"><span>05</span>Operating experience</a></li>\n', '', 'toc experience')
html = replace_once('          <li><a href="#opportunity"><span>06</span>The CCH opportunity</a></li>\n', '', 'toc opportunity')

# ---------------------------------------------------------------------------
# 9. Slide 7: strip the explanatory text, keep sliders, results, charts, formula.
# ---------------------------------------------------------------------------
html = replace_once('<p class="section-intro">Adjust the four inputs. See the coverage and collection results together.</p>', '', 'fin intro')
html = replace_once('<p>Annual emergency department visits, including repeat visits.</p>', '', 'desc 1')
html = replace_once('<p>Share of encounters with an additional collectible coverage opportunity.</p>', '', 'desc 2')
html = replace_once('<p id="collection-rule">Collection limits adjust with the ED charge assumption.</p>', '', 'desc 3')
html = replace_once('<p>Gross charge per identified encounter, before collection adjustments.</p>', '', 'desc 4')
html = replace_once('''      <p class="constraint-notice" id="constraint-notice" aria-live="polite"></p>\n''', '', 'constraint notice')
html = replace_once('<span class="baseline-change" id="baseline-change">Starting scenario</span>', '', 'baseline change')
html = replace_once('<span id="encounters-detail">6% of 150,000 encounters</span>', '', 'encounters detail')
html = replace_once('<span id="collection-share">23.5% assumed net-to-gross collection</span>', '', 'collection share')
html = replace_once('<span class="unit-pill">1 figure = 1,000 visits</span>', '', 'unit pill')
html = replace_once('<p class="chart-note">Each figure represents 1,000 encounters, not 1,000 unique patients. Partial fill represents part of that unit. Figure styles are illustrative.</p>', '', 'people note')
html = replace_once('<div class="chart-toolbar"><span><i class="key-line"></i> Current volume &amp; collection</span><button class="text-button" type="button" id="fit-chart">Fit scale</button></div><p class="chart-note" id="chart-scale-note">The vertical scale stays fixed while you drag. It expands only when needed.</p>', '', 'chart toolbar')
html = replace_once('''  <div class="financial-slide-bottom"><p><b>Illustrative, not a forecast.</b> 1 figure = 1,000 ED encounters, not unique patients. Replace assumptions with CCH data during discovery.</p><button type="button" class="text-button" id="open-model-notes">Assumptions &amp; details ↗</button></div>\n''', '', 'slide bottom')
dialog = re.compile(r'  <dialog id="model-notes".*?</dialog>\n', re.S)
assert len(dialog.findall(html)) == 1, 'dialog'
html = dialog.sub('', html)
# JS: tolerate the removed elements.
html = replace_once("  const put = (id, value) => { document.getElementById(id).textContent = value; };",
                    "  const put = (id, value) => { const node = document.getElementById(id); if (node) node.textContent = value; };", 'null-safe put')
html = replace_once("  document.getElementById('fit-chart').addEventListener('click', () => revenue.fit());\n", '', 'fit listener')
html = replace_once("  document.getElementById('open-model-notes').addEventListener('click', () => notes.showModal());\n  document.getElementById('close-model-notes').addEventListener('click', () => notes.close());\n", '', 'dialog listeners')
html = replace_once("    if (notes.open) notes.close();", "    if (notes && notes.open) notes.close();", 'notes guard 1')
html = replace_once("    if (notes.open || event.altKey", "    if ((notes && notes.open) || event.altKey", 'notes guard 2')
# Chart geometry: wider aspect so it fits the slide.
html = replace_once('viewBox="0 0 520 310" role="img"', 'viewBox="0 0 520 272" role="img"', 'chart viewBox')
html = replace_once('<text class="axis-title" x="282" y="304" text-anchor="middle">', '<text class="axis-title" x="274" y="266" text-anchor="middle">', 'axis title y')
html = replace_once('const left = 54, right = 495, top = 24, bottom = 260;', 'const left = 54, right = 495, top = 22, bottom = 222;', 'chart bounds')
html = replace_once("""for (let rate = 2; rate <= 10; rate += 2) grid += '<text x="' + x(rate) + '" y="283" text-anchor="middle">'""",
                    """for (let rate = 2; rate <= 10; rate += 2) grid += '<text x="' + x(rate) + '" y="244" text-anchor="middle">'""", 'x labels y')

# ---------------------------------------------------------------------------
# 9b. Model ranges (user, 2026-10-26): ED charge $3,000–$15,000 (default $10,000),
#     net collection fixed $500–$5,000 in $500 steps (no longer tied to the charge).
#     Tagline: "You Deliver Care, We Optimize Revenue."
# ---------------------------------------------------------------------------
html = replace_once('<input id="collection" type="range" min="1063" max="8062" step="1" value="4000"><div class="range-ends"><span id="collection-min">$1,063</span><span id="collection-max">$8,062</span></div>',
                    '<input id="collection" type="range" min="500" max="5000" step="500" value="4000"><div class="range-ends"><span id="collection-min">$500</span><span id="collection-max">$5,000</span></div>', 'collection range')
html = replace_once('<output for="charge" id="charge-output">$17,000</output></div><input id="charge" type="range" min="4000" max="20000" step="250" value="17000"><div class="range-ends"><span>$4,000</span><span>$20,000</span></div>',
                    '<output for="charge" id="charge-output">$10,000</output></div><input id="charge" type="range" min="3000" max="15000" step="250" value="10000"><div class="range-ends"><span>$3,000</span><span>$15,000</span></div>', 'charge range')
html = replace_once('<strong id="charges-result">$153M</strong>', '<strong id="charges-result">$90M</strong>', 'charges default')
html = replace_once('  const defaults = {volume:150000, coverage:6, collection:4000, charge:17000};', '  const defaults = {volume:150000, coverage:6, collection:4000, charge:10000};', 'js defaults')
html = replace_once('  const config = {minimumCollectionRate:0.0625, minimumCollectionFixed:null, lowCharge:4000, highCharge:20000, lowCollectionCap:4000, highCollectionCap:9000};',
                    '  const config = {collectionMin:500, collectionMax:5000};', 'js config')
bounds = re.compile(r'  function collectionBounds\(charge\) \{.*?\n  \}\n', re.S)
assert len(bounds.findall(html)) == 1, 'collectionBounds'
html = bounds.sub('  function collectionBounds(charge) {\n    return {min:config.collectionMin, max:Math.min(config.collectionMax, Math.floor(charge / 500) * 500)};\n  }\n', html)
html = replace_once('You deliver care. We recover revenue.', 'You Deliver Care, We Optimize Revenue.', 'tagline')

# 9c. Slide 7 (user, 2026-10-26): no "assumption" wording; net collection per
#     encounter can never exceed the average ED charge; a livelier headline.
html = replace_once('<h2 id="financial-title">Turn assumptions into a visible opportunity.</h2>', '<h2 id="financial-title">Turn hidden revenue opportunities into visible results.</h2>', 'fin title')
html = replace_once('<button class="text-button" id="reset-scenario" type="button">Reset assumptions ↺</button>', '<button class="text-button" id="reset-scenario" type="button">Reset ↺</button>', 'reset label')
html = replace_once('<span class="scenario-tag"><i></i> Planning assumptions</span>', '<span class="scenario-tag"><i></i> Planning inputs</span>', 'inputs tag')
html = replace_once('aria-label="Financial model assumptions"', 'aria-label="Financial model inputs"', 'inputs aria')
html = replace_once('<strong id="annual-result">$36M</strong></div>', '<strong id="annual-result">$36M</strong><span class="result-sub" id="annual-sub">≈ $3M a month · ≈ $99K a day · $108M over three years</span></div>', 'annual sub')
html = replace_once("    put('annual-result', compactMoney(annual));\n", "    showAnnual(annual);\n", 'annual tween call')
html = replace_once('''  let noticeTimer;\n''', '''  let noticeTimer;
  const headline = value => value >= 999500 ? '$' + (value / 1e6).toFixed(1).replace(/\\.0$/, '') + 'M' : value >= 1e3 ? '$' + Math.round(value / 1e3) + 'K' : money(Math.round(value));
  let shownAnnual = null, annualFrame = 0;
  function showAnnual(target) {
    put('annual-sub', '≈ ' + headline(target / 12) + ' a month · ≈ ' + headline(target / 365) + ' a day · ' + headline(target * 3) + ' over three years');
    const still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (shownAnnual === null || still) { shownAnnual = target; put('annual-result', headline(target)); return; }
    const from = shownAnnual, began = performance.now();
    cancelAnimationFrame(annualFrame);
    const step = now => {
      const t = Math.min(1, (now - began) / 450), k = 1 - Math.pow(1 - t, 3);
      shownAnnual = from + (target - from) * k;
      put('annual-result', headline(shownAnnual));
      if (t < 1) annualFrame = requestAnimationFrame(step);
    };
    annualFrame = requestAnimationFrame(step);
  }
''', 'annual tween fn')

# ---------------------------------------------------------------------------
# 10. Slide 8: phase cards + a matching row of three info cards.
# ---------------------------------------------------------------------------
replace_section('pilot', '''<section class="report-section" id="pilot" data-label="The 90-day pilot" aria-labelledby="pilot-title">
        <div class="section-kicker"><span>08</span> Proposed partnership</div>
        <div class="section-heading"><h2 id="pilot-title">90-day pilot.<br><span class="title-muted">John H. Stroger, Jr. Hospital.</span></h2></div>
        <ol class="phase-cards" aria-label="Pilot phases: 15 days discovery, 45 days investigation, 30 days review">
          <li class="phase-card phase-a"><header><span>Phase 01</span><span>Days 1 – 15</span></header><div class="phase-meter"><i style="--share:16.7%"></i><span>15 of 90 days</span></div><h3>Discovery &amp; Baseline</h3><p>Review current injury-related registration, payer identification, billing, and follow-up. Agree on pilot scope, eligibility criteria, compliance requirements, and baseline measures.</p></li>
          <li class="phase-card phase-b"><header><span>Phase 02</span><span>Days 16 – 60</span></header><div class="phase-meter"><i style="--share:50%"></i><span>45 of 90 days</span></div><h3>Identification &amp; Investigation</h3><p>Evaluate designated encounters, conduct authorized patient outreach, identify alternative payer sources, and coordinate verified findings with existing hospital teams.</p></li>
          <li class="phase-card phase-c"><header><span>Phase 03</span><span>Days 61 – 90</span></header><div class="phase-meter"><i style="--share:33.3%"></i><span>30 of 90 days</span></div><h3>Validation &amp; Review</h3><p>Reconcile outcomes, review billing corrections and collections, assess operational impact, and recommend continued monitoring and potential expansion.</p></li>
        </ol>
        <div class="info-cards">
          <div class="info-card"><span class="eyebrow">How to read the pilot</span><p>Many claims take longer than 90 days to resolve. The pilot measures <strong>leading indicators</strong> and any collections realized; final financial performance is reviewed as the identified account cohort matures.</p></div>
          <div class="info-card"><span class="eyebrow">Cook County Health provides</span><ul><li>Executive sponsor and agreed pilot scope</li><li>ED volume, payer mix, and current TPL/WC workflow data</li><li>Compliance requirements and data-access terms</li></ul></div>
          <div class="info-card"><span class="eyebrow">LaborForce provides</span><ul><li>Screening, specialist review, and case investigation</li><li>Dedicated patient outreach and lien administration support</li><li>Joint reporting at days 30, 60, and 90</li></ul></div>
        </div>
        <div class="section-foot"><span>LaborForce Medical Management</span><span>08 / 10</span></div>
      </section>''')

# ---------------------------------------------------------------------------
# 11. Slide 9: four metric cards + review timeline.
# ---------------------------------------------------------------------------
replace_section('metrics', '''<section class="report-section" id="metrics" data-label="Success metrics" aria-labelledby="metrics-title">
        <div class="section-kicker"><span>09</span> Proposed success metrics</div>
        <div class="section-heading"><h2 id="metrics-title">Transparent. Measurable.<br><span class="title-muted">Jointly reviewed.</span></h2></div>
        <div class="metric-cards">
          <article class="metric-card" style="--accent:#0a8fa6"><h3>Leading</h3><p class="metric-desc">Early signals that cases are being found and verified</p><ul><li>Encounters screened and flagged</li><li>Number and % with verified additional responsible-party coverage</li><li>Accounts accepted for billing correction or recovery action</li></ul></article>
          <article class="metric-card" style="--accent:#0c3c75"><h3>Financial</h3><p class="metric-desc">What the program returns, net of adjustments</p><ul><li>Additional collections attributable to the program, net of reversals and adjustments</li><li>Incremental net revenue after program costs</li></ul></article>
          <article class="metric-card" style="--accent:#2f6fb5"><h3>Operational</h3><p class="metric-desc">Effect on hospital teams and account flow</p><ul><li>Staff workload</li><li>Turnaround time</li><li>Unresolved account aging</li></ul></article>
          <article class="metric-card" style="--accent:#7a95ad"><h3>Quality</h3><p class="metric-desc">Safeguards that stay in place throughout</p><ul><li>Compliance</li><li>Patient experience</li><li>Documentation quality</li></ul></article>
        </div>
        <div class="cadence" aria-label="Joint review cadence">
          <span class="callout-label">Joint review cadence</span>
          <div class="cadence-track">
            <div class="cadence-stop launch"><i></i><strong>Launch</strong><p>Scope, eligibility criteria, and baseline agreed</p></div>
            <div class="cadence-stop"><i></i><strong>Day 30</strong><p>Baseline confirmed; screening volumes and first flagged cohort</p></div>
            <div class="cadence-stop"><i></i><strong>Day 60</strong><p>Verification rate, accounts accepted for correction, staff workload impact</p></div>
            <div class="cadence-stop"><i></i><strong>Day 90</strong><p>Collections to date, cohort maturity, and a joint decision on continuation</p></div>
          </div>
        </div>
        <div class="section-foot"><span>LaborForce Medical Management</span><span>09 / 10</span></div>
      </section>''')

# ---------------------------------------------------------------------------
# 12. Slide 10: the formal ask, next-step cards, logo.
# ---------------------------------------------------------------------------
replace_section('next-steps', '''<section class="report-section closing-section" id="next-steps" data-label="Our ask" aria-labelledby="next-steps-title">
        <div class="section-kicker"><span>10</span> Our ask</div>
        <h2 class="closing-title" id="next-steps-title">Our ask: a 90-day pilot at <span>John H. Stroger, Jr. Hospital.</span></h2>
        <p class="closing-intro">Strengthen Cook County Health's fiscal resilience while supporting accessible, high-quality care for the community — through a focused, transparent, and measurable pilot, reviewed jointly at days 30, 60, and 90.</p>
        <ol class="step-cards" aria-label="Proposed next steps">
          <li><span>01</span><h3>Confirm sponsor &amp; scope</h3><p>Executive sponsor and pilot scope at Stroger Hospital</p></li>
          <li><span>02</span><h3>Share baseline data</h3><p>ED volume, payer mix, and the current TPL/WC workflow</p></li>
          <li><span>03</span><h3>Agree &amp; launch</h3><p>Compliance requirements and success metrics; launch Phase 1</p></li>
        </ol>
        <div class="closing-bottom">
          <div class="closing-signature">''' + (LOGO_FULL % 'closing-logo') + '''</div>
          <div class="closing-tag"><strong>Thank you</strong>We look forward to discussing the pilot with your leadership team.</div>
        </div>
        <div class="section-foot"><span>Confidential — for discussion purposes</span><span>10 / 10</span></div>
      </section>''')
html = replace_once('<li><a href="#next-steps"><span>10</span>Next steps</a></li>', '<li><a href="#next-steps"><span>10</span>Our ask</a></li>', 'toc label')

# ---------------------------------------------------------------------------
# 13. Financial slide: the first time it opens, the sliders glide from their
#     minimums to the default scenario so the audience sees the model respond.
# ---------------------------------------------------------------------------
html = replace_once('''  update();

  const toggle = document.getElementById('toc-toggle');''', '''  update();

  let modelIntroDone = false;
  function animateModel() {
    if (modelIntroDone) return;
    modelIntroDone = true;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const starts = {volume:25000, coverage:2, collection:500, charge:3000};
    const steps = {volume:5000, coverage:0.5, collection:500, charge:250};
    const duration = 1800, started = performance.now();
    const ease = t => 1 - Math.pow(1 - t, 3);
    Object.entries(starts).forEach(([id, value]) => { inputs[id].value = value; });
    update();
    function frame(now) {
      const t = Math.min(1, (now - started) / duration), k = ease(t);
      Object.keys(defaults).forEach(id => {
        const value = starts[id] + (defaults[id] - starts[id]) * k;
        inputs[id].value = t >= 1 ? defaults[id] : Math.round(value / steps[id]) * steps[id];
      });
      update();
      if (t < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  const demo = document.getElementById('layer-demo');
  const slabs = demo ? [...demo.querySelectorAll('.slab')] : [];
  const gaps = demo ? [...demo.querySelectorAll('.gap')] : [];
  const fnRows = demo ? [...demo.querySelectorAll('.fn-row')] : [];
  const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let demoStep = 0, demoTimer = null, demoHeld = false;
  function setLayer(k) {
    slabs.forEach((el, i) => { const n = i + 1; el.classList.toggle('active', n === k); el.classList.toggle('passed', k > 0 && n < k); el.classList.toggle('dim', k > 0 && n > k); });
    gaps.forEach((el, i) => el.classList.toggle('on', k > 0 && i + 1 < k));
    fnRows.forEach((el, i) => { const n = i + 1; el.classList.toggle('active', n === k); el.classList.toggle('dim', k > 0 && n > k); });
  }
  function stopLayerDemo() { clearInterval(demoTimer); demoTimer = null; if (demo) demo.classList.remove('autoplay'); }
  function startLayerDemo() {
    if (!demo || reduceMotion || demoHeld || demoTimer) return;
    demo.classList.add('autoplay');
    setLayer(demoStep = 1);
    demoTimer = setInterval(() => { demoStep = demoStep % 5 + 1; setLayer(demoStep); }, 1600);
  }
  if (demo) {
    const hold = el => { const k = Number(el.dataset.i); demoHeld = true; stopLayerDemo(); setLayer(demoStep = k); };
    [...slabs, ...fnRows].forEach(el => {
      el.addEventListener('mouseenter', () => hold(el));
      el.addEventListener('focus', () => hold(el));
      el.addEventListener('click', () => hold(el));
    });
    demo.addEventListener('mouseleave', () => { demoHeld = false; if (document.getElementById('solution').classList.contains('is-active')) startLayerDemo(); });
    demo.addEventListener('focusout', event => { if (!demo.contains(event.relatedTarget)) { demoHeld = false; if (document.getElementById('solution').classList.contains('is-active')) startLayerDemo(); } });
  }

  const toggle = document.getElementById('toc-toggle');''', 'model intro')
html = replace_once('''    closeContents();
    fitDeck();
  }''', '''    closeContents();
    fitDeck();
    if (sections[current].id === 'financial') animateModel();
    if (sections[current].id === 'solution') startLayerDemo(); else { stopLayerDemo(); if (!demoHeld) setLayer(0); }
  }''', 'hook intro into showSlide')

# ---------------------------------------------------------------------------
# 14. Remove the unused BlenderFigure element and the print hook for the scene.
# ---------------------------------------------------------------------------
html = replace_once('''  class BlenderFigure extends HTMLElement {
    connectedCallback() {
      if (this.querySelector('img')) return;
      const img = document.createElement('img');
      img.src = this.getAttribute('src') || '';
      img.alt = this.getAttribute('alt') || '';
      img.width = 1400; img.height = 1120; img.decoding = 'async';
      this.append(img);
    }
  }

''', '', 'BlenderFigure class')
html = replace_once("  customElements.define('lfm-blender-figure', BlenderFigure);\n", '', 'BlenderFigure define')
html = replace_once('''        slide.querySelectorAll('lfm-blender-scene').forEach(node => {
          const poster = doc.createElement('img');
          poster.src = node.getAttribute('poster');
          poster.alt = 'Decorative healthcare illustration';
          poster.className = 'print-poster';
          node.replaceWith(poster);
        });
''', '', 'print scene hook')
html = replace_once('    body.deck-mode .print-sheet .chart-toolbar { min-height:20px; }',
                    """    body.deck-mode .print-sheet .chart-toolbar { min-height:20px; }
    .print-sheet .slab { opacity:1!important; transform:none!important; }
    .print-sheet .gap .drop { display:none!important; }
    .print-sheet .gap .flow-line { opacity:.9!important; }
    .print-sheet .fn-row { opacity:1!important; }""", 'print slab reset')
html = replace_once('lfm-people-chart,lfm-revenue-chart,lfm-blender-figure{display:block}', 'lfm-people-chart,lfm-revenue-chart{display:block}', 'css display')
html = replace_once('.hero-art lfm-blender-figure{width:100%;height:100%}lfm-blender-figure img{display:block;object-fit:contain;width:100%;height:auto}.hero-art lfm-blender-figure img{height:100%;max-height:550px}', '', 'css blender figure')
html = replace_once('.deck-mode .hero-art lfm-blender-scene{height:100%;width:100%}', '', 'css blender scene')

# ---------------------------------------------------------------------------
# 15. Refinement stylesheet, appended inside the main <style> block.
#     All rules are top-level so the print document picks them up too.
# ---------------------------------------------------------------------------
refinement_css = r'''
/* ===================== Refinement layer (October 2026) ===================== */
body{font-family:"Segoe UI",-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif}
body.deck-mode .report-section{padding:40px 60px 24px}
body.deck-mode .section-kicker{margin-bottom:16px}
body.deck-mode .section-heading{margin-bottom:24px}
.deck-mode .section-foot{letter-spacing:.04em;text-transform:uppercase;font-size:9px}
.deck-mode .deck-navigation button{font-weight:600}
.brand-mark{display:block;height:38px;width:auto}
.deck-mode .brand-mark{height:34px}
.deck-mode[data-orientation="portrait"] .brand-mark{height:28px}
/* Slide 1 — cover */
body.deck-mode .report-cover{display:grid;grid-template-columns:minmax(0,1fr) 420px;padding:0;background:#ffffff}
body.deck-mode .report-cover.is-active{display:grid}
.cover-left{display:flex;flex-direction:column;min-width:0;padding:48px 56px 22px 60px}
.cover-body{margin:auto 0;padding:0 0 20px}
.cover-pretitle{font-size:16px;font-weight:600;letter-spacing:.01em;color:var(--teal);margin-bottom:18px}
.cover-body h1{font-size:64px;line-height:1.04;letter-spacing:-.045em;max-width:800px;color:var(--navy);font-weight:500}
.cover-body h1>span{color:var(--teal)}
.cover-deck{font-size:20px;line-height:1.5;color:var(--ink-2);max-width:660px;margin-top:24px}
.cover-facts{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:28px;margin:0;padding:22px 0 0;border-top:2px solid var(--navy);align-items:start}
.cover-facts dt{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:650;margin-bottom:7px}
.cover-facts dd{margin:0;font-size:15px;line-height:1.45;font-weight:600;color:var(--navy)}
.cover-logo{display:block;height:84px;width:auto;margin-top:-6px}
.cover-left .section-foot{margin-top:auto;padding-top:12px}
.cover-panel{position:relative;background:var(--navy);color:#f5f7fa;padding:50px 42px 34px 46px;display:flex;flex-direction:column;gap:26px}
.cover-panel:before{content:"";position:absolute;left:0;top:0;bottom:0;width:6px;background:linear-gradient(#0a8fa6,#025fb6)}
.cover-panel .eyebrow{color:#7fd3e3;font-size:11px}
.glance-stat strong{display:block;font-size:56px;line-height:1;letter-spacing:-.05em;font-weight:550;color:#ffffff;font-variant-numeric:tabular-nums}
.glance-stat span{display:block;font-size:13px;line-height:1.5;color:#c5d6e8;margin-top:8px;max-width:320px}
.glance-stat+.glance-stat{padding-top:20px;border-top:1px solid #ffffff22}
.glance-ask{margin-top:auto;padding:14px 18px;background:#ffffff12;border-radius:5px;font-size:15px;line-height:1.5;color:#ffffff;font-weight:600}
.glance-ask .eyebrow{display:block;margin-bottom:5px;font-weight:650}
.glance-note{font-size:10px;line-height:1.5;color:#8ea4bb;margin:0}
/* Slide 2 */
body.deck-mode .summary-grid{flex:none;gap:16px}
.deck-mode .summary-item{background:var(--panel);border-top:0;border-left:4px solid var(--teal);border-radius:6px;padding:22px 26px 24px}
.deck-mode .summary-item.summary-goal{border-left-color:var(--navy)}
.deck-mode .summary-item h3{font-size:27px;margin:8px 0 10px}
.deck-mode .summary-item p{font-size:19px;line-height:1.5}
.method-strip{margin-top:auto;border-top:1px solid var(--line);padding-top:14px}
.method-strip .callout-label{font-size:10px;margin-bottom:0}
.method-steps{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-top:10px}
.method-steps li{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;align-items:baseline}
.method-steps li>span{font-size:10px;color:var(--teal);font-variant-numeric:tabular-nums;grid-row:1}
.method-steps li>strong{font-size:15px;font-weight:600;letter-spacing:-.01em;color:var(--navy)}
.method-steps li>p{grid-column:2;font-size:13px;line-height:1.45;color:var(--ink-2)}
#summary .section-foot{margin-top:14px}
/* Slide 3 */
.challenge-grid{display:grid;grid-template-columns:minmax(0,1fr) 400px;gap:36px;align-items:stretch;flex:1;min-height:0}
.question-cards{list-style:none;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr);gap:14px}
.question-cards li{display:flex;gap:14px;align-items:center;background:var(--panel);border-radius:5px;padding:18px 22px;font-size:19px;line-height:1.4;color:var(--navy)}
.question-cards li>span{flex:none;width:28px;height:28px;border-radius:50%;background:var(--navy);color:#ffffff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center}
.question-cards li>p{margin:0}
.flow-card{border:1px solid var(--line);border-radius:6px;padding:18px 20px;background:#ffffff;display:flex;flex-direction:column}
.flow-card .callout-label{margin-bottom:12px}
.flow-steps{list-style:none;display:flex;flex-direction:column;flex:1}
.flow-steps li{flex:1;display:flex;flex-direction:column;justify-content:center;padding:12px 16px;border-radius:4px;background:var(--panel)}
.flow-steps li strong{display:block;font-size:17px;font-weight:600;color:var(--navy);letter-spacing:-.01em}
.flow-steps li span{display:block;font-size:13px;line-height:1.45;color:var(--ink-2);margin-top:4px}
.flow-steps li.flow-end{background:var(--navy)}
.flow-steps li.flow-end strong{color:#ffffff}
.flow-steps li.flow-end span{color:#c5d6e8}
.flow-arrow{flex:none;display:flex;justify-content:center;align-items:center;height:30px}
.flow-arrow svg{width:18px;height:18px;stroke:var(--teal);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.consequence-bar{margin-top:24px;display:grid;grid-template-columns:auto 1fr;gap:22px;align-items:center;background:var(--teal-l);border-left:4px solid var(--teal);padding:15px 20px;border-radius:0 5px 5px 0}
.consequence-bar .callout-label{margin:0;white-space:nowrap}
.consequence-bar p{font-size:17px;line-height:1.5;color:var(--navy)}
#challenge .section-foot{margin-top:14px}
/* Slide 4 — layers */
.layer-stack{display:flex;flex-direction:column;flex:1;min-height:0}
.layer{position:relative;border-radius:6px;padding:18px 24px}
.layer-tag{display:block;font-size:10px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;margin-bottom:8px}
.layer-body strong{display:block;font-size:20px;font-weight:600;letter-spacing:-.01em}
.layer-body span{display:block;font-size:15px;line-height:1.45;margin-top:4px}
.layer-top{background:#ffffff14;border:1px solid #ffffff26;color:#ffffff}
.layer-top .layer-tag{color:#7fd3e3}
.layer-top .layer-body span{color:#c3d2e3}
.layer-base{background:#061f45;border:1px solid #ffffff1a;color:#ffffff}
.layer-base .layer-tag{color:#9fc0dc}
.layer-base .layer-body span{color:#aebfd6}
.layer-mid{background:linear-gradient(135deg,#0a8fa6,#025fb6);color:#ffffff;padding:16px 22px 20px;box-shadow:0 14px 40px #00000040}
.layer-mid .layer-tag{color:#ffffff}
.layer-join{height:22px;width:60px;margin:0 auto;background:linear-gradient(#0a8fa6,#025fb6);clip-path:polygon(0 0,100% 0,50% 100%);opacity:.9}
.layer-functions{list-style:none;display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
.layer-functions li{background:#ffffff;color:var(--navy);border-radius:5px;padding:16px 18px 18px}
.layer-functions li>span{display:block;font-size:11px;color:var(--teal);font-weight:700;margin-bottom:6px}
.layer-functions li>strong{display:block;font-size:17px;line-height:1.25;font-weight:600;letter-spacing:-.01em;min-height:42px}
.layer-functions li>p{font-size:14px;line-height:1.5;color:var(--ink-2);margin-top:10px}
#solution .section-foot{margin-top:16px}
/* Slide 5 */
.partner-cards{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:10px}
.partner-card{background:#ffffff;border:1px solid var(--line);border-radius:6px;padding:34px 38px 26px;display:flex;flex-direction:column;align-items:flex-start;gap:20px;min-height:232px;justify-content:center}
.partner-card img{display:block;height:auto;width:auto;max-width:100%;max-height:92px}
.partner-card span{font-size:12px;letter-spacing:.06em;text-transform:uppercase;font-weight:650;color:var(--muted)}
.results-band{margin-top:26px;background:var(--navy);color:#f5f7fa;border-radius:6px;padding:22px 30px 26px}
.results-head{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding-bottom:16px;border-bottom:1px solid #ffffff24}
.results-band .eyebrow{color:#7fd3e3;font-size:12px}
.results-note{font-size:11px;color:#a6bad0;letter-spacing:.02em}
.results-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:30px;padding-top:20px}
.results-grid>div+div{border-left:1px solid #ffffff24;padding-left:30px}
.results-grid strong{display:block;font-size:52px;line-height:1;letter-spacing:-.05em;font-weight:550;color:#ffffff;font-variant-numeric:tabular-nums;margin-bottom:10px}
.results-grid span{font-size:15px;line-height:1.5;color:#c5d6e8}
/* Slide 6 */
body.deck-mode .opportunity-section .section-heading{margin-bottom:30px}
.deck-mode .outcome-grid{gap:20px;flex:1;grid-template-rows:1fr 1fr;min-height:0}
.deck-mode .outcome-grid article{background:#ffffff;border-top:0;border-radius:6px;padding:26px 28px;border-left:4px solid var(--teal);display:flex;flex-direction:column;justify-content:center}
.deck-mode .outcome-grid h3{font-size:27px;margin:0 0 10px}
.deck-mode .outcome-grid p{font-size:19px;line-height:1.5}
.sizing-line{margin-top:auto;padding-top:16px;font-size:12px;line-height:1.5;color:var(--muted)}
#opportunity .section-foot{margin-top:12px}
/* Slide 7: financial model, decluttered */
body.deck-mode .financial-section{padding-top:30px}
.deck-mode .financial-slide-heading{margin-bottom:18px;align-items:center}
body.deck-mode .financial-slide-heading h2{font-size:38px}
.deck-mode .financial-slide-heading .section-kicker{margin-bottom:10px}
body.deck-mode .financial-workspace{flex:1;min-height:0;grid-template-columns:360px minmax(0,1fr);gap:34px}
.deck-mode .financial-controls{justify-content:flex-start}
.deck-mode .financial-controls .assumption-grid{margin:auto 0}
body.deck-mode .financial-controls .assumption{padding:14px 0 16px}
body.deck-mode .financial-controls .assumption-top{margin-bottom:10px}
body.deck-mode .financial-controls .assumption label{font-size:16px}
body.deck-mode .financial-controls .assumption output{font-size:32px}
body.deck-mode[data-orientation="landscape"] .financial-controls .assumption{padding:14px 0 16px}
body.deck-mode[data-orientation="landscape"] .financial-controls .assumption label{font-size:16px;line-height:1.3}
body.deck-mode[data-orientation="landscape"] .financial-controls .assumption output{font-size:32px}
body.deck-mode[data-orientation="landscape"] .financial-controls input[type="range"]{height:30px}
body.deck-mode[data-orientation="landscape"] .financial-controls .range-ends{font-size:11px}
.deck-mode .financial-results{gap:20px;min-height:0;flex:1}
.deck-mode .result-strip{padding:20px 26px;border-radius:6px;align-items:center}
.deck-mode .result-label{font-size:12px;max-width:none}
.deck-mode .main-result strong{font-size:58px;margin:6px 0 0}
.deck-mode .supporting-result strong{font-size:34px;margin:8px 0 0}
.deck-mode .financial-viz-grid{flex:1;min-height:0;gap:34px}
.deck-mode .viz-heading{min-height:0;margin-bottom:12px}
.deck-mode .viz-heading h3{font-size:21px}
.deck-mode .people-stats{min-height:0;margin-bottom:12px}
.deck-mode .people-stats strong{font-size:30px}
.deck-mode .people-stats span,.deck-mode .chart-summary span{display:none}
.deck-mode .people-grid{grid-template-rows:repeat(10,25px);gap:3px 2px}
.deck-mode .person-icon{height:25px}
.deck-mode .chart-summary{min-height:0;margin-bottom:8px;font-size:0}
.deck-mode .chart-summary b{font-size:30px}
.deck-mode .population-key{margin:12px 0 0;font-size:11px}
.deck-mode .calculation-chain{padding-top:16px;flex:none}
.deck-mode .calculation-chain b{font-size:20px}
.deck-mode .financial-section>.section-foot{margin-top:16px}
/* Slide 8 */
.phase-cards{list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.phase-card{border:1px solid var(--line);border-radius:6px;overflow:hidden;background:#ffffff;display:flex;flex-direction:column}
.phase-card header{display:flex;justify-content:space-between;align-items:center;padding:11px 18px;font-size:13px;font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.phase-a header{background:#dbe8f7;color:var(--navy)}
.phase-b header{background:var(--teal);color:#ffffff}
.phase-c header{background:var(--navy);color:#ffffff}
.phase-meter{display:flex;align-items:center;gap:10px;padding:12px 18px 0;font-size:11px;color:var(--muted)}
.phase-meter i{flex:1;height:6px;border-radius:3px;background:var(--panel);position:relative;overflow:hidden}
.phase-meter i:before{content:"";position:absolute;left:0;top:0;bottom:0;width:var(--share);background:var(--teal)}
.phase-a .phase-meter i:before{background:#5b8fd6}
.phase-c .phase-meter i:before{background:var(--navy)}
.phase-meter span{white-space:nowrap;font-variant-numeric:tabular-nums}
.phase-card h3{font-size:24px;padding:14px 18px 0;color:var(--navy)}
.phase-card p{font-size:17px;line-height:1.5;color:var(--ink-2);padding:10px 18px 20px}
.info-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:20px}
.info-card{background:var(--panel);border-radius:6px;padding:16px 18px 18px;border-top:3px solid var(--teal)}
.info-card .eyebrow{display:block;margin-bottom:10px}
.info-card p{font-size:15px;line-height:1.5;color:var(--ink-2)}
.info-card p strong{color:var(--navy)}
.info-card ul{list-style:none}
.info-card li{font-size:15px;line-height:1.45;color:var(--ink-2);padding:4px 0 4px 16px;position:relative}
.info-card li:before{content:"";position:absolute;left:0;top:13px;width:5px;height:5px;border-radius:50%;background:var(--teal)}
/* Slide 9 */
.metric-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.metric-card{border-top:4px solid var(--accent,#0a8fa6);background:var(--panel);border-radius:0 0 6px 6px;padding:16px 18px 18px;min-height:236px}
.metric-card h3{font-size:19px;color:var(--navy);display:flex;align-items:center;gap:10px}
.metric-card h3:before{content:"";width:10px;height:10px;border-radius:50%;background:var(--accent,#0a8fa6);flex:none}
.metric-desc{font-size:13px;color:var(--muted);line-height:1.45;margin:6px 0 12px}
.metric-card ul{list-style:none}
.metric-card li{font-size:16px;line-height:1.45;color:var(--ink-2);padding:7px 0 7px 14px;border-top:1px solid #ffffffaa;position:relative}
.metric-card li:before{content:"";position:absolute;left:0;top:15px;width:5px;height:5px;border-radius:50%;background:var(--accent,#0a8fa6)}
.cadence{margin-top:26px;border-top:1px solid var(--line);padding-top:18px}
.cadence-track{position:relative;display:grid;grid-template-columns:repeat(4,1fr);margin-top:20px}
.cadence-track:before{content:"";position:absolute;left:10px;right:10px;top:9px;height:2px;background:var(--line)}
.cadence-stop{position:relative;padding-right:28px}
.cadence-stop i{display:block;width:20px;height:20px;border-radius:50%;background:#ffffff;border:3px solid var(--teal);position:relative;z-index:1}
.cadence-stop.launch i{background:var(--teal)}
.cadence-stop strong{display:block;font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--navy);margin:12px 0 6px}
.cadence-stop p{font-size:15px;line-height:1.45;color:var(--ink-2);max-width:270px}
/* Slide 10 */
body.deck-mode .closing-section{padding-top:44px}
.closing-title{font-size:48px;line-height:1.1;letter-spacing:-.04em;font-weight:500;max-width:1180px;color:#ffffff}
.closing-title span{color:#7fd3e3}
.closing-intro{font-size:19px;line-height:1.5;color:#c3d2e3;max-width:1040px;margin-top:18px}
.step-cards{list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:30px}
.step-cards li{background:#ffffff10;border:1px solid #ffffff22;border-radius:6px;padding:24px 26px 26px;min-height:190px}
.step-cards li>span{display:inline-flex;width:30px;height:30px;border-radius:50%;background:var(--teal);color:#ffffff;font-size:12px;font-weight:700;align-items:center;justify-content:center;margin-bottom:14px}
.step-cards h3{font-size:22px;color:#ffffff;margin-bottom:10px}
.step-cards p{font-size:16px;line-height:1.5;color:#c3d2e3}
.closing-bottom{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;gap:30px;padding-top:26px;padding-bottom:4px}
.closing-signature{margin:0;letter-spacing:0;font-size:0}
.closing-logo{display:block;height:58px;width:auto;background:#ffffff;padding:8px 14px;border-radius:5px}
.closing-tag{font-size:14px;line-height:1.5;color:#c3d2e3;text-align:right;max-width:420px}
.closing-tag strong{display:block;color:#ffffff;font-size:18px;margin-bottom:4px}
#next-steps .section-foot{margin-top:16px}
/* Slide 4 — interactive five-layer waterfall */
body.deck-mode #solution .section-heading{margin-bottom:14px}
.layer-demo{display:grid;grid-template-columns:470px minmax(0,1fr);gap:56px;align-items:center;flex:1;min-height:0}
.cake{display:block;width:470px;height:auto;max-height:100%;overflow:visible}
.slab{cursor:pointer;outline:none;transition:transform .35s var(--ease-out),opacity .35s ease}
.slab polygon{stroke:transparent;stroke-width:2;stroke-linejoin:round;transition:stroke .25s ease,filter .25s ease}
.slab-num{font:700 17px "Segoe UI",Arial,sans-serif;fill:#0c3c75;pointer-events:none}
.slab.active{transform:translateY(-8px)}
.slab.active .face-t{stroke:#ffffff}
.slab.passed{opacity:1}
.slab.dim{opacity:.38}
.slab:focus-visible .face-t{stroke:#ffffff}
.flow-line{stroke:#7fd3e3;stroke-width:3;stroke-linecap:round;stroke-dasharray:4 6;opacity:.22}
.drop{fill:#bff0f8;opacity:0}
.gap.on .flow-line{opacity:.95;animation:flowdash .7s linear infinite}
.gap.on .drop{animation:dropfall 1s linear infinite}
.gap.on .drop.d2{animation-delay:.5s}
@keyframes flowdash{to{stroke-dashoffset:-20}}
@keyframes dropfall{0%{transform:translateY(0);opacity:0}20%{opacity:1}80%{opacity:1}100%{transform:translateY(30px);opacity:0}}
.fn-col{min-width:0}
.fn-list{list-style:none;display:flex;flex-direction:column;gap:9px}
.fn-row{display:grid;grid-template-columns:40px 1fr;gap:14px;align-items:start;padding:12px 18px;border-radius:6px;border:1px solid #ffffff22;background:#ffffff0c;outline:none;transition:background .3s ease,border-color .3s ease,opacity .3s ease}
.fn-num{width:34px;height:34px;border-radius:50%;background:#ffffff22;color:#ffffff;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;transition:background .3s ease,color .3s ease}
.fn-row strong{display:block;font-size:20px;line-height:1.25;color:#ffffff;font-weight:600;letter-spacing:-.01em}
.fn-row p{font-size:15px;line-height:1.45;color:#c5d6e8;margin-top:3px}
.fn-row.active{background:#ffffff22;border-color:#7fd3e3}
.fn-row.active .fn-num{background:#7fd3e3;color:#0c3c75}
.fn-row.dim{opacity:.5}
.layer-note{margin-top:14px;font-size:14px;line-height:1.5;color:#9fc0dc}
@media(prefers-reduced-motion:reduce){.gap.on .flow-line,.gap.on .drop{animation:none}.gap.on .drop{opacity:0}.slab{transition:none}}
/* Contents panel */
.deck-mode .toc-list a{font-size:12px;padding:11px 9px}
/* Portrait canvas */
body.deck-mode[data-orientation="portrait"] .report-cover{grid-template-columns:1fr;grid-template-rows:auto auto}
.deck-mode[data-orientation="portrait"] .cover-left{padding:34px 38px 20px}
.deck-mode[data-orientation="portrait"] .cover-body{padding:0 0 24px}
.deck-mode[data-orientation="portrait"] .cover-body h1{font-size:50px}
.deck-mode[data-orientation="portrait"] .cover-facts{grid-template-columns:1.4fr 1fr 1fr;gap:16px}
.deck-mode[data-orientation="portrait"] .cover-logo{height:46px}
.deck-mode[data-orientation="portrait"] .cover-panel{padding:30px 38px 28px}
.deck-mode[data-orientation="portrait"] .cover-panel:before{width:100%;height:6px;bottom:auto}
.deck-mode[data-orientation="portrait"] .glance-stat strong{font-size:40px}
.deck-mode[data-orientation="portrait"] .method-steps{grid-template-columns:1fr 1fr;gap:14px 24px}
.deck-mode[data-orientation="portrait"] .challenge-grid{grid-template-columns:1fr;gap:24px;flex:none}
.deck-mode[data-orientation="portrait"] .question-cards{grid-template-rows:auto}
.deck-mode[data-orientation="portrait"] .layer-demo{grid-template-columns:1fr;gap:20px;flex:none}
.deck-mode[data-orientation="portrait"] .cake{width:420px;margin:0 auto}
.deck-mode[data-orientation="portrait"] .partner-cards{grid-template-columns:1fr;gap:14px}
.deck-mode[data-orientation="portrait"] .partner-card{min-height:0;padding:22px 26px 18px}
.deck-mode[data-orientation="portrait"] .results-grid{grid-template-columns:1fr 1fr;gap:18px 24px}
.deck-mode[data-orientation="portrait"] .results-grid>div+div{border-left:0;padding-left:0}
.deck-mode[data-orientation="portrait"] .results-grid>div:nth-child(even){border-left:1px solid #ffffff24;padding-left:24px}
.deck-mode[data-orientation="portrait"] .financial-viz-grid{flex:none}
.deck-mode[data-orientation="portrait"] .financial-workspace,.deck-mode[data-orientation="portrait"] .financial-results{flex:none;min-height:auto}
.deck-mode[data-orientation="portrait"] .calculation-chain{margin-top:0}
.deck-mode[data-orientation="portrait"] .phase-cards{grid-template-columns:1fr;gap:14px}
.deck-mode[data-orientation="portrait"] .info-cards{grid-template-columns:1fr;gap:14px}
.deck-mode[data-orientation="portrait"] .metric-cards{grid-template-columns:1fr 1fr}
.deck-mode[data-orientation="portrait"] .metric-card{min-height:0}
.deck-mode[data-orientation="portrait"] .cadence-track{grid-template-columns:1fr 1fr;gap:18px 0}
.deck-mode[data-orientation="portrait"] .cadence-track:before{display:none}
.deck-mode[data-orientation="portrait"] .step-cards{grid-template-columns:1fr;gap:12px}
.deck-mode[data-orientation="portrait"] .closing-bottom{flex-direction:column;align-items:flex-start}
.deck-mode[data-orientation="portrait"] .closing-tag{text-align:left}
/* Round 8 (user, 2026-10-26) */
/* Cover: hospital photo fading in from the lower-right corner; partner logos */
.cover-left{position:relative;overflow:hidden}
.cover-photo{position:absolute;right:0;bottom:0;width:68%;height:74%;object-fit:cover;object-position:30% 62%;pointer-events:none;z-index:0;-webkit-mask-image:linear-gradient(to right,transparent 0%,#000 58%),linear-gradient(to bottom,transparent 0%,#000 46%),linear-gradient(to top,transparent 0,#000 110px);-webkit-mask-composite:source-in,source-in;mask-image:linear-gradient(to right,transparent 0%,#000 58%),linear-gradient(to bottom,transparent 0%,#000 46%),linear-gradient(to top,transparent 0,#000 110px);mask-composite:intersect,intersect}
.cover-body,.cover-left .section-foot{position:relative;z-index:1}
.cover-partners{margin-top:36px}
.cover-partners .eyebrow{display:block;font-size:11px;color:var(--muted);margin-bottom:12px}
.cover-partner-logos{display:flex;align-items:center;gap:28px}
.cover-partner-logos img{display:block;width:auto;height:30px}
.cover-partner-logos img+img{height:42px;padding-left:28px;border-left:1px solid var(--line)}
.deck-mode[data-orientation="portrait"] .cover-photo{display:none}
.deck-mode[data-orientation="portrait"] .cover-partners{margin-top:24px}
/* Slide 3: compact cards, natural-height flow card, consequence right below */
.challenge-grid{align-items:start;flex:none;margin-top:4px}
.question-cards{grid-template-rows:none;grid-auto-rows:1fr;gap:12px}
.question-cards li{padding:18px 20px;font-size:17px;line-height:1.4;min-height:82px}
.flow-card{padding:16px 18px}
.flow-steps{flex:none}
.flow-steps li{flex:none;padding:12px 14px}
.flow-steps li strong{font-size:16px}
.consequence-bar{margin-top:22px}
#challenge .section-foot{margin-top:auto}
/* Slide 4: thin timing bar on the active row; quicker water */
.fn-row{position:relative;overflow:hidden}
.fn-bar{position:absolute;left:0;bottom:0;width:100%;height:2px;background:#7fd3e3;transform:scaleX(0);transform-origin:left center;pointer-events:none}
.layer-demo.autoplay .fn-row.active .fn-bar{animation:fnbar 1.6s linear forwards}
@keyframes fnbar{to{transform:scaleX(1)}}
.gap.on .flow-line{animation-duration:.5s}
.gap.on .drop{animation-duration:.75s}
.gap.on .drop.d2{animation-delay:.37s}
/* Slide 7: bigger headline with a monthly / daily / three-year line */
.deck-mode .main-result strong{font-size:74px;line-height:1;letter-spacing:-.05em;font-variant-numeric:tabular-nums}
.result-sub{display:block;margin-top:10px;font-size:14px;line-height:1.3;font-weight:600;color:#7fd3e3;font-variant-numeric:tabular-nums;white-space:nowrap}
.deck-mode[data-orientation="portrait"] .result-sub{white-space:normal;font-size:13px}
'''
# Renumber kickers, footers and the contents list from the final slide order.
section_re = re.compile(r'<section class="report-section[^"]*" id="([^"]+)".*?</section>', re.S)
slide_ids = section_re.findall(html)
total = len(slide_ids)
def renumber(m):
    n = slide_ids.index(m.group(1)) + 1
    s = re.sub(r'(<div class="section-kicker"><span>)\d\d(</span>)', lambda k: k.group(1) + f'{n:02d}' + k.group(2), m.group(0))
    return re.sub(r'<span>\d\d / \d\d</span>', f'<span>{n:02d} / {total:02d}</span>', s)
html = section_re.sub(renumber, html)
html = re.sub(r'(<li><a href="#([^"]+)"[^>]*><span>)\d\d(</span>)',
              lambda m: m.group(1) + f'{slide_ids.index(m.group(2)) + 1:02d}' + m.group(3) if m.group(2) in slide_ids else m.group(0), html)
html = replace_once('aria-live="polite">01 / 10</strong>', f'aria-live="polite">01 / {total:02d}</strong>', 'position default')
html = replace_once("String(current + 1).padStart(2, '0') + ' / ' + sections.length", "String(current + 1).padStart(2, '0') + ' / ' + String(sections.length).padStart(2, '0')", 'position js')

html = replace_once('.deck-mode .model-notes-header h2{margin:0}\n\n</style>', '.deck-mode .model-notes-header h2{margin:0}' + refinement_css + '</style>', 'append css')

# ---------------------------------------------------------------------------
# 16. Palette: move every colour literal from the old green-teal scheme to the
#     logo's cobalt blue (#04569b family) and cyan-teal (#0a91a7 family).
# ---------------------------------------------------------------------------
palette = {
    '#112d42': '#0c3c75', '#244557': '#04569b', '#087f79': '#0a8fa6', '#e1eeea': '#e0f1f6',
    '#19313f': '#15283d', '#50616a': '#4a5b6e', '#738087': '#6e7e90', '#d6dcd7': '#d4dce6',
    '#fffef9': '#ffffff', '#f4f4ed': '#f4f6f9', '#e9ede6': '#e8edf3', '#c4d9d0': '#c3d8e6',
    '#c0e1d5': '#c5e6ef', '#e8ece4': '#e6ebf1', '#e8ece5': '#e7edf3', '#e4eae2': '#e2e9f1',
    '#89918e': '#8793a0', '#6e817f': '#6a7f96', '#e7eee5': '#e6edf5', '#f5f4ed': '#f5f7fa',
    '#c1cfd0': '#c3d2e3', '#94a9ad': '#94a9c0', '#91cbb7': '#7fd3e3', '#a0bdb7': '#9fc0dc',
    '#6ab99f': '#35b3c9', '#93c9b7': '#7fd3e3', '#c8d3c9': '#c6d2de', '#e9eee6': '#e9eef4',
    '#92ada0': '#9fbbd8', '#8a9d68': '#2f6fb5', '#a68c60': '#7a95ad', '#99c8b9': '#8fd4e2',
    '#8abcae': '#7fcbe0', '#b6cbc5': '#b3c8dc', '#dbe5e3': '#dbe3ec', '#143a32': '#0c3c75',
    '#c7d9dd': '#c5d6e8', '#96d5c7': '#8fdbe8', '#b0c6ce': '#b0c4da', '#9db6af': '#9fb3c6',
    '#cbd6d6': '#ccd6e0', '#dfe5e2': '#dde3ea', '#163d32': '#0c3c75', '#0d3023': '#0a2f5a',
    '#102c46': '#0a2f5a', '#f3f6f3': '#f5f7fa',
}
# Partner logos carry their own brand colours: protect them from the remap.
protected = {}
def protect(m):
    key = '\x00%d\x00' % len(protected)
    protected[key] = m.group(0)
    return key
html = re.sub(r'data:image/svg\+xml;base64,[A-Za-z0-9+/=]+', protect, html)
html = re.sub(r'#[0-9a-fA-F]{6}', lambda m: palette.get(m.group(0).lower(), m.group(0)), html)
for key, value in protected.items():
    html = html.replace(key, value)
html = html.replace('rgba(230,241,232,.2)', 'rgba(226,236,248,.2)').replace('rgba(244,244,237,.97)', 'rgba(244,246,249,.97)')
known = set(palette.values()) | {'#ffffff', '#b37d29', '#0a8fa6', '#025fb6', '#7fd3e3', '#c5d6e8', '#8ea4bb', '#a6bad0', '#c6d2de',
                                  '#dbe8f7', '#5b8fd6', '#2f6fb5', '#7a95ad', '#9fc0dc', '#c3d2e3', '#0c3c75', '#061f45', '#aebfd6', '#000000'}
leftovers = sorted(set(m.lower() for m in re.findall(r'#[0-9a-fA-F]{6}', html)) - known)
print('unmapped colour literals:', leftovers)

assert 'lfm-blender' not in html, 'blender references remain'
assert 'data:model/gltf-binary' not in html
with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)
print('written', out_path, len(html.encode("utf-8")), 'bytes')
