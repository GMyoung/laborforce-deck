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
          <div class="cover-body">
            <p class="cover-pretitle">You deliver care. We recover revenue.</p>
            <h1 id="cover-title">Uncovering revenue.<br><span>Strengthening hospital performance.</span></h1>
            <p class="cover-deck">A strategic revenue identification and recovery partnership — extending Cook County Health's revenue cycle, not replacing it.</p>
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
replace_section('solution', '''<section class="report-section solution-section" id="solution" data-label="Our approach" aria-labelledby="solution-title">
        <div class="section-kicker"><span>04</span> The LaborForce solution</div>
        <div class="section-heading"><h2 id="solution-title">A specialized operational layer.<br><span class="title-muted">Five critical functions.</span></h2></div>
        <div class="layer-stack" aria-label="LaborForce as a layer on top of the existing revenue cycle">
          <div class="layer layer-top"><span class="layer-tag">Outcome</span><div class="layer-body"><strong>Correct payer identified · lien documented · reimbursement recovered</strong><span>Verified findings flow back into the hospital's own billing and collections.</span></div></div>
          <div class="layer-join" aria-hidden="true"></div>
          <div class="layer layer-mid"><span class="layer-tag">The LaborForce layer</span>
            <ol class="layer-functions">
              <li><span>01</span><strong>Proactive Revenue Identification</strong><p>Review injury-related encounters, identify potentially responsible payers, and prioritize accounts for investigation.</p></li>
              <li><span>02</span><strong>Dedicated Patient Engagement</strong><p>Outreach to verify injury circumstances and collect missing claim, employer, insurer, or attorney information.</p></li>
              <li><span>03</span><strong>Payer Verification &amp; RCM Coordination</strong><p>Coordinate findings with registration, billing, and revenue cycle teams for payer determination and follow-up.</p></li>
              <li><span>04</span><strong>Revenue Auditing &amp; Reconciliation</strong><p>Monitor unresolved cases, flag missing or inconsistent information, and track case status and reimbursement.</p></li>
              <li><span>05</span><strong>Lien Administration &amp; Recovery</strong><p>Support approved lien documentation, follow-up, and reimbursement tracking within the legal and contractual framework.</p></li>
            </ol>
          </div>
          <div class="layer-join" aria-hidden="true"></div>
          <div class="layer layer-base"><span class="layer-tag">Existing hospital revenue cycle</span><div class="layer-body"><strong>Registration · Billing · Collections · Revenue cycle teams</strong><span>Unchanged. LaborForce works alongside these teams — uncovering and advancing opportunities they may not have the specialized resources to fully investigate.</span></div></div>
        </div>
        <div class="section-foot"><span>LaborForce Medical Management</span><span>04 / 10</span></div>
      </section>''')

# ---------------------------------------------------------------------------
# 7. Slide 5: partner logos + the results band; the generic bullet list is gone.
# ---------------------------------------------------------------------------
replace_section('experience', '''<section class="report-section" id="experience" data-label="Operating experience" aria-labelledby="experience-title">
        <div class="section-kicker"><span>05</span> Experience with healthcare partners</div>
        <div class="section-heading"><h2 id="experience-title">Proven operating experience<br><span class="title-muted">in Chicago-area hospitals.</span></h2></div>
        <div class="partner-cards" aria-label="Current program partners">
          <div class="partner-card"><img src="''' + nm_uri + '''" alt="Northwestern Medicine" width="730" height="137" decoding="async"><span>Northwestern Medicine · Current program partner</span></div>
          <div class="partner-card"><img src="''' + hph_uri + '''" alt="Humboldt Park Health" width="782" height="227" decoding="async"><span>Humboldt Park Health · Current program partner</span></div>
        </div>
        <div class="results-band" aria-label="Program results, March to July 2026">
          <div class="results-head"><span class="eyebrow">Program results · March – July 2026</span><span class="results-note">Program-reported; not independently attributed</span></div>
          <div class="results-grid">
            <div><strong>+336%</strong><span>Monthly TPL recoveries<br>$33K → $144K</span></div>
            <div><strong>90%+</strong><span>Payer identification accuracy<br>up from under 30%</span></div>
            <div><strong>141 / 178</strong><span>July encounters verified<br>79% of those screened</span></div>
            <div><strong>$198,940</strong><span>Charges on 32 Workers' Comp<br>cases identified in July</span></div>
          </div>
        </div>
        <div class="section-foot"><span>LaborForce Medical Management</span><span>05 / 10</span></div>
      </section>''')

# ---------------------------------------------------------------------------
# 8. Slide 6: title, six outcome cards, one small sizing line at the bottom.
# ---------------------------------------------------------------------------
replace_section('opportunity', '''<section class="report-section opportunity-section" id="opportunity" data-label="The CCH opportunity" aria-labelledby="opportunity-title">
        <div class="section-kicker"><span>06</span> Opportunity at Cook County Health</div>
        <div class="section-heading"><h2 id="opportunity-title">A focused TPL/WC program for a high-volume safety-net system.</h2></div>
        <div class="outcome-grid">
          <article><h3>Find coverage</h3><p>Evaluate whether additional responsible-party coverage exists for selected encounters.</p></article>
          <article><h3>Document claims</h3><p>Improve identification and documentation of injury-related claims.</p></article>
          <article><h3>Bill accurately</h3><p>Strengthen billing accuracy and reimbursement follow-up.</p></article>
          <article><h3>Stop leakage</h3><p>Reduce avoidable revenue leakage.</p></article>
          <article><h3>Gain visibility</h3><p>Establish clearer visibility into potentially recoverable accounts.</p></article>
          <article><h3>Protect the mission</h3><p>Support financial sustainability without compromising access to care.</p></article>
        </div>
        <p class="sizing-line">Illustrative sizing: 150,000 ED encounters × 6% with additional coverage × $4,000 net per encounter ≈ $36M per year — a planning model, not a forecast.</p>
        <div class="section-foot"><span>LaborForce Medical Management</span><span>06 / 10</span></div>
      </section>''')

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
html = bounds.sub('  function collectionBounds() {\n    return {min:config.collectionMin, max:config.collectionMax};\n  }\n', html)
html = replace_once('You deliver care. We recover revenue.', 'You Deliver Care, We Optimize Revenue.', 'tagline')

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

  const toggle = document.getElementById('toc-toggle');''', 'model intro')
html = replace_once('''    closeContents();
    fitDeck();
  }''', '''    closeContents();
    fitDeck();
    if (sections[current].id === 'financial') animateModel();
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
.closing-bottom{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;gap:30px;padding-top:26px}
.closing-signature{margin:0;letter-spacing:0;font-size:0}
.closing-logo{display:block;height:96px;width:auto;background:#ffffff;padding:12px 20px;border-radius:6px}
.closing-tag{font-size:14px;line-height:1.5;color:#c3d2e3;text-align:right;max-width:420px}
.closing-tag strong{display:block;color:#ffffff;font-size:18px;margin-bottom:4px}
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
.deck-mode[data-orientation="portrait"] .layer-stack{flex:none}
.deck-mode[data-orientation="portrait"] .layer-functions{grid-template-columns:1fr 1fr}
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
'''
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
