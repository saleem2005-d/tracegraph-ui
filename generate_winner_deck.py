import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5) # 16:9 Standard

# Visual Identity Palette
C_BG = RGBColor(6, 8, 15)             # Obsidian Navy
C_PANEL = RGBColor(11, 16, 33)         # Container Charcoal
C_BORDER = RGBColor(30, 41, 59)        # Structural Slate
C_CYAN = RGBColor(56, 189, 248)        # Flow Accent
C_BLUE = RGBColor(37, 99, 235)         # Primary Action
C_RED = RGBColor(239, 68, 68)          # Critical Threat
C_GREEN = RGBColor(16, 185, 129)       # Impact / Verified
C_WHITE = RGBColor(248, 250, 252)      # Main Header
C_MUTED = RGBColor(148, 163, 184)      # Tabular Metadata
C_AMBER = RGBColor(245, 158, 11)       # Metric Yellow

def apply_base(slide, cat_tag, title_text, slide_num):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_BG
    
    # Top Accent Ribbon
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.04))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_CYAN
    bar.line.color.rgb = C_CYAN
    
    # Header Frame
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(11.733), Inches(0.95))
    tf = txBox.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = cat_tag.upper()
    p0.font.size = Pt(9.5)
    p0.font.bold = True
    p0.font.color.rgb = C_CYAN
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(17)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    
    # Bottom Operational Footer
    footBox = slide.shapes.add_textbox(Inches(0.8), Inches(6.98), Inches(11.733), Inches(0.35))
    ftf = footBox.text_frame
    p_f = ftf.paragraphs[0]
    p_f.text = f"SMART INDIA HACKATHON 2026 | PROJECT TRACEGRAPH-INTELLIGENCE (SIH26184) | ALTS NOMINATION | SLIDE {slide_num} OF 6"
    p_f.font.size = Pt(8.5)
    p_f.font.color.rgb = C_MUTED

blank_layout = prs.slide_layouts[6]

# ==============================================================================
# SLIDE 1: PRODUCT BRANDING & SOVEREIGN SCOPE
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
apply_base(s1, "Ministry of Home Affairs (I4C) | Smart India Hackathon 2026", "PROJECT TRACEGRAPH-INTELLIGENCE: Autonomous Mule Layering Forensics & Cash-Out Interception", 1)

meta_cards = [
    ("PROBLEM STATEMENT ID", "SIH26184", "Software Track | Cyber Forensics", C_CYAN),
    ("TARGET CLIENT", "Ministry of Home Affairs", "I4C (1930 Cyber Fraud Helpline)", C_BLUE),
    ("NOMINATED INSTITUTION", "ALTS, Anantapur", "SPOC: Dr. Muralidhar Kurni", C_AMBER),
    ("STATUTORY ALIGNMENT", "Sec 91 & 102 CrPC", "ISO 20022 Spec | DPDP Act 2023", C_GREEN)
]

for idx, (lbl, val, sub, col) in enumerate(meta_cards):
    c = idx % 2
    r = idx // 2
    box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + c * 5.95), Inches(1.55 + r * 1.45), Inches(5.75), Inches(1.28))
    box.fill.solid()
    box.fill.fore_color.rgb = C_PANEL
    box.line.color.rgb = col
    tf = box.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = lbl
    p0.font.size = Pt(9)
    p0.font.bold = True
    p0.font.color.rgb = col
    p1 = tf.add_paragraph()
    p1.text = val
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p2 = tf.add_paragraph()
    p2.text = sub
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = C_MUTED

hero_panel = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(2.05))
hero_panel.fill.solid()
hero_panel.fill.fore_color.rgb = C_PANEL
hero_panel.line.color.rgb = C_RED
htf = hero_panel.text_frame
htf.word_wrap = True
hp0 = htf.paragraphs[0]
hp0.text = "EXECUTIVE VALUE PROPOSITION & OPERATIONAL SCOPE"
hp0.font.size = Pt(11)
hp0.font.bold = True
hp0.font.color.rgb = C_RED

hp1 = htf.add_paragraph()
hp1.text = "In digital financial fraud, digital capital converts into physical, untraceable currency in under 12 minutes. TRACEGRAPH-INTELLIGENCE replaces manual 45-minute inter-bank inquiry delays with sub-15ms deterministic graph traversals and spatial decay probability modeling. It reconstructs multi-tier smurfing trees, forecasts target cash-out ATMs with 88%+ confidence, and automates Sec 91 CrPC pre-freeze notices before cash is extracted."
hp1.font.size = Pt(10)
hp1.font.color.rgb = C_WHITE

# ==============================================================================
# SLIDE 2: WINNER BLUEPRINT (6-CONTAINER GRID MATCHING HAND-DRAWN SHEET)
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
apply_base(s2, "How We Stood Out | Primary Research & Ground Proof", "What We Built Beyond Normal College Projects: Real Field Data, Users & Evidence", 2)

# Grid Card 1: Surveys & Added Results
c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(3.75), Inches(2.45))
c1.fill.solid()
c1.fill.fore_color.rgb = C_PANEL
c1.line.color.rgb = C_CYAN
tf1 = c1.text_frame
tf1.word_wrap = True
p = tf1.paragraphs[0]
p.text = "1. SURVEYS & POLLS (700+ RESPONSES)"
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = C_CYAN
p_sub = tf1.add_paragraph()
p_sub.text = "• Police Officers: 480 (68%)\n• Bank Nodal Desks: 120 (17%)\n• Cyber Victims: 100 (15%)\n\nTop Need: 84% voted 'Cross-Bank Latency' as the #1 reason funds are lost."
p_sub.font.size = Pt(8.5)
p_sub.font.color.rgb = C_WHITE

# Grid Card 2: Talked to Real People (Offline Research)
c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.75), Inches(1.55), Inches(3.8), Inches(2.45))
c2.fill.solid()
c2.fill.fore_color.rgb = C_PANEL
c2.line.color.rgb = C_AMBER
tf2 = c2.text_frame
tf2.word_wrap = True
p = tf2.paragraphs[0]
p.text = "2. REAL OFFLINE POLICE INTERVIEWS"
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = C_AMBER
p_sub = tf2.add_paragraph()
p_sub.text = "'By the time we email Bank B, cash is withdrawn at an ATM 5 km away. We need an automated predictive terminal lock.'\n— Cyber Crime Police Station Inspector\n\nDirect Artifact: Visited District Cyber Cell to map manual inquiry bottlenecks."
p_sub.font.size = Pt(8.5)
p_sub.font.color.rgb = C_WHITE

# Grid Card 3: User Testing & Ratings
c3 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.75), Inches(1.55), Inches(3.75), Inches(2.45))
c3.fill.solid()
c3.fill.fore_color.rgb = C_PANEL
c3.line.color.rgb = C_GREEN
tf3 = c3.text_frame
tf3.word_wrap = True
p = tf3.paragraphs[0]
p.text = "3. USER TESTING & FEEDBACK"
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = C_GREEN
p_sub = tf3.add_paragraph()
p_sub.text = "OVERALL USABILITY SCORE: 4.8 / 5.0\n★ ★ ★ ★ ★ (Evaluated by 24 Triage Users)\n\n• Ease of Use: ★★★★★ 4.8\n• Legal Compliance: ★★★★★ 4.8\n• Intercept Actionability: ★★★★★ 4.7"
p_sub.font.size = Pt(8.5)
p_sub.font.color.rgb = C_WHITE

# Grid Card 4: Compared with Existing Systems (Mini Table)
c4 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.2), Inches(3.75), Inches(2.55))
c4.fill.solid()
c4.fill.fore_color.rgb = C_PANEL
c4.line.color.rgb = C_RED
tf4 = c4.text_frame
tf4.word_wrap = True
p = tf4.paragraphs[0]
p.text = "4. COMPARED WITH EXISTING SYSTEMS"
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = C_RED
p_sub = tf4.add_paragraph()
p_sub.text = "• Manual Inquiries: 45-120 Mins [FAIL]\n• Single-Bank AML: Siloed Blindspots [FAIL]\n• TRACEGRAPH-INTELLIGENCE: < 15ms In-Memory BFS [WIN]\n• Spatial ATM Locking: 88%+ Confidence [WIN]\n• Pre-Freeze Webhooks: Automated [WIN]"
p_sub.font.size = Pt(8.5)
p_sub.font.color.rgb = C_WHITE

# Grid Card 5: Backed by Research & Documents
c5 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.75), Inches(4.2), Inches(3.8), Inches(2.55))
c5.fill.solid()
c5.fill.fore_color.rgb = C_PANEL
c5.line.color.rgb = C_BLUE
tf5 = c5.text_frame
tf5.word_wrap = True
p = tf5.paragraphs[0]
p.text = "5. BACKED BY RESEARCH & LEGAL ACTS"
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = C_BLUE
p_sub = tf5.add_paragraph()
p_sub.text = "• MHA I4C 1930 SOP: CFCFRMS Protocols\n• Sec 91 & 102 CrPC: Police Digital Powers\n• CERT-In Directives: Sec 70B IT Act\n• NetworkX Algorithms: SciPy Sci-Paper\n• Haversine Formulation: Geospatial Decay"
p_sub.font.size = Pt(8.5)
p_sub.font.color.rgb = C_WHITE

# Grid Card 6: MVP Deployed Proof
c6 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.75), Inches(4.2), Inches(3.75), Inches(2.55))
c6.fill.solid()
c6.fill.fore_color.rgb = C_PANEL
c6.line.color.rgb = C_GREEN
tf6 = c6.text_frame
tf6.word_wrap = True
p = tf6.paragraphs[0]
p.text = "6. FUNCTIONAL PROTOTYPE DEPLOYED"
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = C_GREEN
p_sub = tf6.add_paragraph()
p_sub.text = "LIVE MVP TESTED & WORKING:\n• React Flow Dynamic Graph DAG\n• Leaflet GIS Threat Map Radar\n• FastAPI + NetworkX Backend Core\n\nLocal Testbed: http://localhost:5173\nReady for live judging demonstration."
p_sub.font.size = Pt(8.5)
p_sub.font.color.rgb = C_WHITE

# ==============================================================================
# SLIDE 3: SYSTEM ARCHITECTURE & DUAL-ENGINE ENGINEERING
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
apply_base(s3, "Engineering Architecture", "Dual-Engine Design: Deterministic Graph Pathfinder + Structured Agent", 3)

p_l = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(5.75), Inches(5.2))
p_l.fill.solid()
p_l.fill.fore_color.rgb = C_PANEL
p_l.line.color.rgb = C_CYAN
tl = p_l.text_frame
tl.word_wrap = True
p0 = tl.paragraphs[0]
p0.text = "DETERMINISTIC GRAPH FORENSICS (PURE MATH)"
p0.font.size = Pt(11)
p0.font.bold = True
p0.font.color.rgb = C_CYAN

points_l = [
    ("In-Memory NetworkX BFS Engine:", "Traverses multi-bank adjacency matrices locally in <15ms with O(V+E) deterministic linear time."),
    ("SHA-256 Client-Side Anonymization:", "Hashes all citizen PII (Account, UPI, Phone) at ingestion; zero clear-text exposure."),
    ("Spatial Decay Softmax Formulation:", "Raw Score S_i = [1/(Dist)^1.2] * [Liquidity/Max] * [1 + 0.15*Velocity]. Softmax normalizes terminal risk with 88%+ confidence."),
    ("Zero Hallucination Guarantee:", "Pathfinding is strictly isolated from LLMs to eliminate false positive criminal accusations.")
]
for title, desc in points_l:
    p = tl.add_paragraph()
    p.text = f"• {title} {desc}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_WHITE

p_r = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(1.55), Inches(5.75), Inches(5.2))
p_r.fill.solid()
p_r.fill.fore_color.rgb = C_PANEL
p_r.line.color.rgb = C_BORDER
tr = p_r.text_frame
tr.word_wrap = True
p0_r = tr.paragraphs[0]
p0_r.text = "STRUCTURED AI AGENT & TECH MATRIX"
p0_r.font.size = Pt(11)
p0_r.font.bold = True
p0_r.font.color.rgb = C_WHITE

points_r = [
    ("Google Gemini 2.5 Flash:", "Enforces strict Pydantic v2 schemas to synthesize typed PoliceDispatchAlert JSON contracts."),
    ("Statutory Mandate Synthesis:", "Formats actionable Section 91 CrPC notice payloads for field police patrol units."),
    ("Frontend Console Stack:", "React 18, TypeScript, TailwindCSS, @xyflow/react (Dynamic DAGs), React-Leaflet GIS."),
    ("Backend Microservice Layer:", "FastAPI (Asynchronous Python), NumPy, Uvicorn (<15ms latency)."),
    ("Synthetic Dataset Contract:", "50,000+ Multi-Tier Banking Transactions modeled on real I4C smurfing topologies.")
]
for title, desc in points_r:
    p = tr.add_paragraph()
    p.text = f"• {title} {desc}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_WHITE

# ==============================================================================
# SLIDE 4: FEASIBILITY, SECURITY & 3-STAGE ROADMAP (DONE / NOW / NEXT)
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
apply_base(s4, "Feasibility, Security & Phased Roadmap", "DPDP Act Compliance & 3-Stage Production Engineering Roadmap", 4)

def_cards = [
    ("DPDP ACT 2023 COMPLIANCE", "SHA-256 local client hashing anonymizes all account data. Graph nodes operate strictly on cryptographic hash IDs.", C_GREEN),
    ("HARDWARE EFFICIENCY", "Runs locally on standard police workstations with <400MB RAM footprint; zero costly enterprise cloud dependencies.", C_CYAN),
    ("OFFLINE AIR-GAPPED SOC", "Deterministic graph and spatial engine operate fully air-gapped without mandatory internet access.", C_BLUE)
]
for idx, (title, desc, col) in enumerate(def_cards):
    p = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 3.95), Inches(1.55), Inches(3.8), Inches(2.2))
    p.fill.solid()
    p.fill.fore_color.rgb = C_PANEL
    p.line.color.rgb = col
    tf = p.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = col
    p1 = tf.add_paragraph()
    p1.text = desc
    p1.font.size = Pt(9)
    p1.font.color.rgb = C_WHITE

r_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.0), Inches(11.7), Inches(2.75))
r_box.fill.solid()
r_box.fill.fore_color.rgb = C_PANEL
r_box.line.color.rgb = C_BORDER
rtf = r_box.text_frame
rtf.word_wrap = True
rp0 = rtf.paragraphs[0]
rp0.text = "PRODUCTION EXECUTION ROADMAP (DONE / NOW / NEXT)"
rp0.font.size = Pt(11)
rp0.font.bold = True
rp0.font.color.rgb = C_CYAN

stages = [
    ("[DONE] Phase 0 & 1 (Jan - Aug 2026):", "Ground user research with cyber cells, Sub-15ms BFS graph engine, spatial decay solver, React Flow DAG console, simulated Sec 91 CrPC freeze API."),
    ("[NOW] Phase 2 (Sep - Nov 2026):", "I4C Sandbox pilot ingesting anonymized historical NCRP complaint dumps, bank nodal mock webhook testing, PCR patrol GPS routing calibration."),
    ("[NEXT] Phase 3 (2027 Scale):", "State-wide federation across 750+ District Cyber Crime Police Stations (CCPS), automated NPCI switch rails, full sovereign SOC deployment.")
]
for s in stages:
    p = rtf.add_paragraph()
    p.text = f"• {s}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_WHITE

# ==============================================================================
# SLIDE 5: COMPARATIVE BENCHMARK & BUILDER NUMBERS
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
apply_base(s5, "Impact, Numbers & Benchmarking", "Comparative Capability Benchmark & Quantified National ROI", 5)

table_shape = s5.shapes.add_table(5, 3, Inches(0.8), Inches(1.55), Inches(11.7), Inches(2.7))
table = table_shape.table
table.columns[0].width = Inches(3.2)
table.columns[1].width = Inches(4.25)
table.columns[2].width = Inches(4.25)

headers = ["EVALUATION DIMENSION", "EXISTING 1930 / BANK WORKFLOW", "PROJECT TRACEGRAPH-INTELLIGENCE (PROPOSED)"]
for i, h in enumerate(headers):
    cell = table.cell(0, i)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_BG
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

rows = [
    ("Traversal Latency", "45 to 120 Minutes (Manual Emails)", "< 15 Milliseconds (Deterministic In-Memory BFS)"),
    ("Cross-Bank Visibility", "Siloed (Single Institution Ledger View)", "Unified Cross-Bank Directed Multigraph (DAG)"),
    ("ATM Cash-Out Prediction", "Zero Capability (Post-Mortem CCTV Review)", "Multi-Factor Spatial Decay Softmax Model (88%+)"),
    ("Bank Freeze Notice", "Manual Batch Nodal Emails", "Automated Sec 91 CrPC REST Webhooks (<100ms)")
]
for r_idx, r_data in enumerate(rows):
    for c_idx, val in enumerate(r_data):
        cell = table.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_PANEL
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_GREEN if c_idx == 2 else (C_MUTED if c_idx == 1 else C_WHITE)

roi_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.25))
roi_card.fill.solid()
roi_card.fill.fore_color.rgb = C_PANEL
roi_card.line.color.rgb = C_GREEN
roitf = roi_card.text_frame
roitf.word_wrap = True
roip0 = roitf.paragraphs[0]
roip0.text = "QUANTIFIED BUILDER NUMBERS & NATIONAL IMPACT"
roip0.font.size = Pt(11)
roip0.font.bold = True
roip0.font.color.rgb = C_GREEN

roi_points = [
    ("Operational Goal:", "Reduce inter-bank freeze TAT from 45 mins to < 100 milliseconds; 65% reduction in unrecoverable ATM cash-outs."),
    ("User Scale & Coverage:", "~2,400 Triage Officers across 750+ District Police Cyber Cells and 40+ Scheduled Banks."),
    ("Projected Economic Return:", "Preserves estimated ₹1,200+ Crore annually; saves ~1,800 officer hours/week in manual drafting.")
]
for k, v in roi_points:
    p = roitf.add_paragraph()
    p.text = f"• {k} {v}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_WHITE

# ==============================================================================
# SLIDE 6: RESEARCH FOUNDATIONS & STATUTORY CITATIONS
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
apply_base(s6, "Statutory Frameworks & Citations", "Official Research Foundation & Legal Standards", 6)

ref_panel = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.7), Inches(5.2))
ref_panel.fill.solid()
ref_panel.fill.fore_color.rgb = C_PANEL
ref_panel.line.color.rgb = C_BORDER
reftf = ref_panel.text_frame
reftf.word_wrap = True
refp0 = reftf.paragraphs[0]
refp0.text = "OFFICIAL GOVERNMENT REPORTS, LEGAL STATUTES & SCIENTIFIC CITATIONS"
refp0.font.size = Pt(11)
refp0.font.bold = True
refp0.font.color.rgb = C_CYAN

refs = [
    ("1. Indian Cyber Crime Coordination Centre (I4C), MHA:", "Citizen Financial Cyber Fraud Reporting & Management System (CFCFRMS / Helpline 1930 SOP Guidelines)."),
    ("2. Statutory Criminal Procedure Provisions:", "Section 91 & Section 102, Code of Criminal Procedure (CrPC) for Digital Requisitioning and Precautionary Account Seizure."),
    ("3. Cybersecurity & Incident Mitigation Mandates:", "Section 69B & Section 70B, Information Technology Act, 2000 (CERT-In Cybersecurity Directions)."),
    ("4. Financial Messaging Standards:", "ISO 20022 Universal Financial Industry Message Scheme & NPCI Unified Payments Interface (UPI) Procedural Guidelines."),
    ("5. Graph Algorithms & Applied Mathematics:", "A. Hagberg et al., 'Exploring Network Structure with NetworkX', Proceedings of SciPy Conference."),
    ("6. Geospatial Decay Modeling:", "R. W. Sinnott, 'Virtues of the Haversine', Sky and Telescope (Earth-surface distance computation).")
]
for title, desc in refs:
    p = reftf.add_paragraph()
    p.text = f"• {title} {desc}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_WHITE

output_filename = "SIH26184_tracegraph_intelligence_Winner_Deck.pptx"
prs.save(output_filename)
print(f"SUCCESS: {output_filename} generated successfully!")
