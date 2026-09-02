import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Theme
COLOR_BG = RGBColor(11, 15, 25)
COLOR_PANEL = RGBColor(17, 24, 39)
COLOR_PANEL_BORDER = RGBColor(37, 99, 235)
COLOR_ACCENT = RGBColor(239, 68, 68)
COLOR_CYAN = RGBColor(56, 189, 248)
COLOR_TEXT_MAIN = RGBColor(241, 245, 249)
COLOR_TEXT_MUTED = RGBColor(148, 163, 184)

def apply_bg(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

def add_header(slide, tagline_text, title_text):
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.04))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_CYAN
    top_bar.line.color.rgb = COLOR_CYAN
    
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.1))
    tf = txBox.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = tagline_text.upper()
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CYAN
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN

def add_footer(slide, slide_num):
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.4))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = f"SMART INDIA HACKATHON 2026  |  PROJECT TRACEGRAPH-INTELLIGENCE (PS ID: SIH26184)  |  SLIDE {slide_num} OF 6"
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_TEXT_MUTED

slide_layout = prs.slide_layouts[6]

# SLIDE 1: Title & Metadata
s1 = prs.slides.add_slide(slide_layout)
apply_bg(s1)
add_header(s1, "Smart India Hackathon 2026 | Official Idea Proposal", "PROJECT TRACEGRAPH-INTELLIGENCE: AI-Powered Mule Account Layering Forensics & Cash-Out Interception")

meta_items = [
    ("Problem Statement ID", "SIH26184", "Category: Software"),
    ("Theme / Organization", "Blockchain & Cybersecurity", "Ministry of Home Affairs / I4C"),
    ("Nominated Institution", "Anantha Lakshmi Inst. of Tech & Sci (ALTS)", "SPOC: Dr. Muralidhar Kurni"),
    ("Team Compliance", "6 Members (Strict Female Mandate Met)", "Submission Track: Internal SPOC Nomination Round")
]

for idx, (label, val, sub) in enumerate(meta_items):
    col = idx % 2
    row = idx // 2
    panel = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + col * 5.95), Inches(1.8 + row * 1.5), Inches(5.75), Inches(1.3))
    panel.fill.solid()
    panel.fill.fore_color.rgb = COLOR_PANEL
    panel.line.color.rgb = COLOR_PANEL_BORDER
    tf = panel.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = label.upper()
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CYAN
    p1 = tf.add_paragraph()
    p1.text = val
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN
    p2 = tf.add_paragraph()
    p2.text = sub
    p2.font.size = Pt(10)
    p2.font.color.rgb = COLOR_TEXT_MUTED

sum_panel = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.9), Inches(11.7), Inches(1.7))
sum_panel.fill.solid()
sum_panel.fill.fore_color.rgb = COLOR_PANEL
sum_panel.line.color.rgb = COLOR_ACCENT
stf = sum_panel.text_frame
stf.word_wrap = True
sp0 = stf.paragraphs[0]
sp0.text = "EXECUTIVE SUMMARY & OPERATIONAL VALUE"
sp0.font.size = Pt(11)
sp0.font.bold = True
sp0.font.color.rgb = COLOR_ACCENT
sp1 = stf.add_paragraph()
sp1.text = "Project TRACEGRAPH-INTELLIGENCE is an autonomous digital forensics and predictive law enforcement platform addressing the critical I4C 'Golden Hour' cash-out problem. By replacing manual 45-minute inter-bank tracing with deterministic NetworkX graph traversals (<15ms) and Google Gemini 2.5 structured agentic reasoning, the platform maps multi-tier mule account rings, pinpoints vulnerable cash-out ATMs via spatial decay algorithms, and automates Section 91 CrPC freeze webhooks before physical extraction occurs."
sp1.font.size = Pt(11)
sp1.font.color.rgb = COLOR_TEXT_MAIN
add_footer(s1, 1)

# SLIDE 2: Proposed Solution
s2 = prs.slides.add_slide(slide_layout)
apply_bg(s2)
add_header(s2, "Idea Title: Project TRACEGRAPH-INTELLIGENCE", "Proposed Solution: Autonomous Forensic Traversal & Intercept")

left_panel = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.75), Inches(4.8))
left_panel.fill.solid()
left_panel.fill.fore_color.rgb = COLOR_PANEL
left_panel.line.color.rgb = COLOR_ACCENT
ltf = left_panel.text_frame
ltf.word_wrap = True
lp0 = ltf.paragraphs[0]
lp0.text = "THE ROOT-CAUSE BOTTLENECK"
lp0.font.size = Pt(12)
lp0.font.bold = True
lp0.font.color.rgb = COLOR_ACCENT
bottlenecks = [
    ("Smurfing & Rapid Layering:", "Cybercrime syndicates splinter stolen funds across 3 to 5 intermediary mule hops within 180 seconds across disparate banks."),
    ("Manual Banking Inquiries:", "Police officers spend 45+ minutes manually issuing notices to individual payment gateways while cash is physically withdrawn."),
    ("ATM Location Blindspot:", "Traditional cyber cells lack spatial correlation engines to predict which regional ATM terminal will be used for physical cash extraction.")
]
for b_title, b_desc in bottlenecks:
    bp = ltf.add_paragraph()
    bp.text = f"• {b_title} {b_desc}"
    bp.font.size = Pt(10.5)
    bp.font.color.rgb = COLOR_TEXT_MAIN

right_panel = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(1.8), Inches(5.75), Inches(4.8))
right_panel.fill.solid()
right_panel.fill.fore_color.rgb = COLOR_PANEL
right_panel.line.color.rgb = COLOR_CYAN
rtf = right_panel.text_frame
rtf.word_wrap = True
rp0 = rtf.paragraphs[0]
rp0.text = "CORE INNOVATIONS & ARCHITECTURAL MOAT"
rp0.font.size = Pt(12)
rp0.font.bold = True
rp0.font.color.rgb = COLOR_CYAN
sol_points = [
    ("Sub-15ms Deterministic Traversal:", "Directed BFS graph engine traverses 5-tier mule trees locally in memory with mathematical zero-hallucination guarantees."),
    ("Spatial Decay Cash-Out Matrix:", "Evaluates terminal liquidity, historical transaction velocity, and Haversine distance to pinpoint target ATMs with 88%+ confidence."),
    ("Google Gemini 2.5 Structured Reasoning:", "Enforces strict Pydantic schemas to generate statutory I4C police dispatch orders and tactical mandates."),
    ("Automated Sec 91 CrPC Switch Lock:", "Simulates instant downstream webhook holds across intermediary mule accounts and destination terminal switches.")
]
for s_title, s_desc in sol_points:
    sp = rtf.add_paragraph()
    sp.text = f"• {s_title} {s_desc}"
    sp.font.size = Pt(10.5)
    sp.font.color.rgb = COLOR_TEXT_MAIN
add_footer(s2, 2)

# SLIDE 3: Technical Approach
s3 = prs.slides.add_slide(slide_layout)
apply_bg(s3)
add_header(s3, "Technical Architecture & System Methodology", "End-to-End Pipeline, Algorithmic Stack & Data Contracts")

p_banner = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(0.8))
p_banner.fill.solid()
p_banner.fill.fore_color.rgb = RGBColor(15, 23, 42)
p_banner.line.color.rgb = COLOR_CYAN
pbtf = p_banner.text_frame
pbtf.word_wrap = True
pbp = pbtf.paragraphs[0]
pbp.text = "[1930 FIR Ingestion]  ➔  [SHA-256 Hashing]  ➔  [NetworkX BFS Traversal (<15ms)]  ➔  [Spatial Softmax ATM Scoring]  ➔  [Gemini 2.5 Agent Schema]  ➔  [React Flow & Sec 91 Lock]"
pbp.font.size = Pt(10)
pbp.font.bold = True
pbp.font.color.rgb = COLOR_CYAN
pbp.alignment = PP_ALIGN.CENTER

p1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.8), Inches(5.75), Inches(3.8))
p1.fill.solid()
p1.fill.fore_color.rgb = COLOR_PANEL
p1.line.color.rgb = COLOR_PANEL_BORDER
t1 = p1.text_frame
t1.word_wrap = True
tp0 = t1.paragraphs[0]
tp0.text = "FULL-STACK TECHNOLOGY MATRIX"
tp0.font.size = Pt(11)
tp0.font.bold = True
tp0.font.color.rgb = COLOR_CYAN
stack = [
    ("Backend API Engine:", "Python 3.11/3.14, FastAPI (Asynchronous microservices)"),
    ("Graph Compute Layer:", "NetworkX (In-memory directed multigraphs), NumPy"),
    ("Agentic Reasoning AI:", "Google Gemini 2.5 Flash via google-genai SDK"),
    ("Data Contract Enforcement:", "Pydantic v2 (Guaranteed zero-hallucination JSON schema)"),
    ("Tactical Frontend Console:", "React 18, TypeScript, TailwindCSS, Vite"),
    ("Graph & GIS Visualization:", "@xyflow/react (Dynamic DAGs), React-Leaflet (Esri Canvas)")
]
for k, v in stack:
    tp = t1.add_paragraph()
    tp.text = f"• {k} {v}"
    tp.font.size = Pt(9.5)
    tp.font.color.rgb = COLOR_TEXT_MAIN

p2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(2.8), Inches(5.75), Inches(3.8))
p2.fill.solid()
p2.fill.fore_color.rgb = COLOR_PANEL
p2.line.color.rgb = COLOR_PANEL_BORDER
t2 = p2.text_frame
t2.word_wrap = True
tp1 = t2.paragraphs[0]
tp1.text = "PYDANTIC DISPATCH CONTRACT (SCHEMA-VERIFIED)"
tp1.font.size = Pt(11)
tp1.font.bold = True
tp1.font.color.rgb = COLOR_CYAN
schema_code = (
    "class PoliceDispatchAlert(BaseModel):\n"
    "    alert_id: str\n"
    "    severity: Literal['CRITICAL', 'HIGH', 'ELEVATED']\n"
    "    victim_initial_loss: float\n"
    "    layering_hops_detected: int\n"
    "    mule_chain_hashes: List[str]\n"
    "    target_atm_id: str; target_bank: str\n"
    "    target_atm_lat: float; target_atm_long: float\n"
    "    predicted_cashout_window_mins: int = 12\n"
    "    confidence_score: float = Field(ge=0.0, le=1.0)\n"
    "    dispatch_recommended_action: str\n"
    "    timestamp_utc: str"
)
tp_code = t2.add_paragraph()
tp_code.text = schema_code
tp_code.font.size = Pt(8.5)
tp_code.font.name = "Consolas"
tp_code.font.color.rgb = COLOR_CYAN
add_footer(s3, 3)

# SLIDE 4: Feasibility & Roadmap
s4 = prs.slides.add_slide(slide_layout)
apply_bg(s4)
add_header(s4, "Feasibility, Viability & Defensive Engineering", "Risk Mitigation, Privacy Compliance & 36-Hour Hackathon Plan")

risks = [
    ("Citizen PII & Banking Privacy", "SHA-256 local client-side hashing anonymizes all account numbers and UPI IDs prior to graph evaluation or LLM context ingestion.", "100% Compliant"),
    ("Model Hallucinations in Law Enforcement", "Graph pathfinding is strictly isolated to deterministic algorithms. LLMs are constrained via Pydantic response schemas.", "Zero Hallucination"),
    ("Third-Party Live Dependency Failure", "Runs entirely on local high-throughput simulated transaction graphs; functions seamlessly even with zero internet connectivity.", "Offline Robust")
]
for idx, (rtitle, rdesc, rtag) in enumerate(risks):
    panel = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 3.95), Inches(1.8), Inches(3.8), Inches(2.6))
    panel.fill.solid()
    panel.fill.fore_color.rgb = COLOR_PANEL
    panel.line.color.rgb = COLOR_PANEL_BORDER
    tf = panel.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = f"RISK: {rtitle.upper()}"
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_ACCENT
    p1 = tf.add_paragraph()
    p1.text = rdesc
    p1.font.size = Pt(9.5)
    p1.font.color.rgb = COLOR_TEXT_MAIN
    p2 = tf.add_paragraph()
    p2.text = f"Status: {rtag}"
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CYAN

r_strip = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(1.9))
r_strip.fill.solid()
r_strip.fill.fore_color.rgb = COLOR_PANEL
r_strip.line.color.rgb = COLOR_CYAN
stf = r_strip.text_frame
stf.word_wrap = True
sp0 = stf.paragraphs[0]
sp0.text = "36-HOUR SPRINT EXECUTION ROADMAP"
sp0.font.size = Pt(11)
sp0.font.bold = True
sp0.font.color.rgb = COLOR_CYAN
milestones = [
    ("Hours 00–08", "NetworkX In-Memory Ingestion & SHA-256 Obfuscator Engine"),
    ("Hours 08–16", "Spatial Decay Haversine Solver & ATM Terminal Probability Engine"),
    ("Hours 16–24", "Gemini 2.5 Structured Dispatch Agent & Pydantic Validation"),
    ("Hours 24–36", "React Flow Tactical UI, Leaflet Risk Grid & Simulated Freeze API")
]
for m_time, m_task in milestones:
    mp = stf.add_paragraph()
    mp.text = f"• [{m_time}]: {m_task}"
    mp.font.size = Pt(9.5)
    mp.font.color.rgb = COLOR_TEXT_MAIN
add_footer(s4, 4)

# SLIDE 5: Impact & Metrics
s5 = prs.slides.add_slide(slide_layout)
apply_bg(s5)
add_header(s5, "Impact, Quantifiable Benefits & Beneficiaries", "Institutional Scale, I4C Golden Hour Optimization & Financial Defense")

metrics = [
    ("< 15 ms", "Graph Traversal Latency", "99.9% faster than manual banking inquiries"),
    ("12 Mins", "Golden Intercept Window", "Predictive physical patrol arrival window"),
    ("88%+", "Cash-Out Confidence", "Multi-factor velocity, proximity & topology score"),
    ("₹ Multi-Cr", "Estimated Funds Protected", "Instant Sec 91 CrPC auto-freeze execution")
]
for idx, (m_val, m_label, m_sub) in enumerate(metrics):
    m_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 2.95), Inches(1.8), Inches(2.8), Inches(1.5))
    m_box.fill.solid()
    m_box.fill.fore_color.rgb = COLOR_PANEL
    m_box.line.color.rgb = COLOR_CYAN
    tf = m_box.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = m_val
    p0.font.size = Pt(18)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CYAN
    p0.alignment = PP_ALIGN.CENTER
    p1 = tf.add_paragraph()
    p1.text = m_label
    p1.font.size = Pt(9.5)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN
    p1.alignment = PP_ALIGN.CENTER

b1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.5), Inches(5.75), Inches(3.1))
b1.fill.solid()
b1.fill.fore_color.rgb = COLOR_PANEL
b1.line.color.rgb = COLOR_PANEL_BORDER
t1 = b1.text_frame
t1.word_wrap = True
bp0 = t1.paragraphs[0]
bp0.text = "TARGET BENEFICIARIES & LAW ENFORCEMENT"
bp0.font.size = Pt(11)
bp0.font.bold = True
bp0.font.color.rgb = COLOR_CYAN
b_points = [
    ("Ministry of Home Affairs & I4C:", "Unified command interface for National Cybercrime Reporting Portal (1930) triage."),
    ("State Cyber Crime Police Stations:", "Provides ground officers with actionable GPS coordinates and intercept countdowns for PCR vans."),
    ("Banking Fraud Management Units:", "Automated API webhooks eliminate latency in placing administrative holds on mule accounts.")
]
for k, v in b_points:
    p = t1.add_paragraph()
    p.text = f"• {k} {v}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MAIN

b2 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(3.5), Inches(5.75), Inches(3.1))
b2.fill.solid()
b2.fill.fore_color.rgb = COLOR_PANEL
b2.line.color.rgb = COLOR_PANEL_BORDER
t2 = b2.text_frame
t2.word_wrap = True
bp1 = t2.paragraphs[0]
bp1.text = "NATIONAL ALIGNMENT & ECONOMIC VALUE"
bp1.font.size = Pt(11)
bp1.font.bold = True
bp1.font.color.rgb = COLOR_CYAN
n_points = [
    ("CERT-In Directives Compliance:", "Direct adherence to statutory 6-hour incident disclosure and tracing mandates."),
    ("Prevention of Capital Outflow:", "Prevents illicit conversion of cybercrime proceeds into unrecoverable physical cash."),
    ("Zero Proprietary Licensing:", "Built entirely with open forensic architectures, avoiding costly commercial enterprise lock-in.")
]
for k, v in n_points:
    p = t2.add_paragraph()
    p.text = f"• {k} {v}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MAIN
add_footer(s5, 5)

# SLIDE 6: References & Citations
s6 = prs.slides.add_slide(slide_layout)
apply_bg(s6)
add_header(s6, "Statutory Frameworks, Protocols & Technical Citations", "References & Research Foundation")

ref_panel = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
ref_panel.fill.solid()
ref_panel.fill.fore_color.rgb = COLOR_PANEL
ref_panel.line.color.rgb = COLOR_PANEL_BORDER
rtf = ref_panel.text_frame
rtf.word_wrap = True
rp0 = rtf.paragraphs[0]
rp0.text = "GOVERNMENT FRAMEWORKS, LEGAL STATUTES & SCIENTIFIC CITATIONS"
rp0.font.size = Pt(12)
rp0.font.bold = True
rp0.font.color.rgb = COLOR_CYAN

refs = [
    ("1. Indian Cyber Crime Coordination Centre (I4C):", "Citizen Financial Cyber Fraud Reporting and Management System (CFCFRMS / 1930 SOP Guidelines)."),
    ("2. Statutory Law Enforcement Provisions:", "Section 91 of the Code of Criminal Procedure (CrPC) & Section 69B of the Information Technology Act, 2000 (Directions for Interception and Blocking)."),
    ("3. Financial Messaging & Interoperability:", "ISO 20022 Universal Financial Industry Message Scheme & NPCI Unified Payments Interface (UPI) Procedural Guidelines."),
    ("4. Graph Theory & Network Optimization:", "A. Hagberg, D. Schult, P. Swart, 'Exploring Network Structure, Dynamics, and Function using NetworkX', Proceedings of the 7th Python in Science Conference (SciPy2008)."),
    ("5. LLM Structured Outputs & Reasoning:", "Google DeepMind, 'Gemini: A Family of Highly Capable Multimodal Models', Technical Documentation for Structured Pydantic Output Generation (2024–2026)."),
    ("6. Geospatial Distance & Optimization:", "R. W. Sinnott, 'Virtues of the Haversine', Sky and Telescope 68 (2): 159 (1984) for Earth-Surface Spatial Traversal Calculations.")
]
for r_num, r_body in refs:
    p = rtf.add_paragraph()
    p.text = f"{r_num} {r_body}"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MAIN
add_footer(s6, 6)

pptx_filename = "SIH26184_Project_TRACEGRAPH-INTELLIGENCE_Presentation.pptx"
prs.save(pptx_filename)
print(f"SUCCESS: {pptx_filename} created successfully!")
