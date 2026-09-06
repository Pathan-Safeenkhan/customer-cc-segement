
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Output file path
output_pdf_path = r"C:\CreditCard_AI_Project\Internship_Project_Report_Safeenkhan.pdf"

# Initialize Document
doc = SimpleDocTemplate(
    output_pdf_path,
    pagesize=letter,
    rightMargin=54,
    leftMargin=54,
    topMargin=54,
    bottomMargin=54
)

styles = getSampleStyleSheet()

# Custom Styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=26,
    alignment=1, # Center
    textColor=colors.HexColor('#0f172a')
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=17,
    alignment=1,
    textColor=colors.HexColor('#2563eb')
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=15,
    leading=19,
    textColor=colors.HexColor('#1e293b'),
    spaceAfter=6,
    spaceBefore=12,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'SectionH2',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=11.5,
    leading=15,
    textColor=colors.HexColor('#0284c7'),
    spaceAfter=4,
    spaceBefore=8,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'BodyTextCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=14,
    textColor=colors.HexColor('#334155'),
    spaceAfter=6
)

code_style = ParagraphStyle(
    'CodeSnippet',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor('#0f172a')
)

meta_style = ParagraphStyle(
    'MetaText',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=15,
    alignment=1,
    textColor=colors.HexColor('#475569')
)

story = []

# =========================================================================
# COVER PAGE
# =========================================================================
story.append(Spacer(1, 40))
story.append(Paragraph("AN INTERNSHIP REPORT", subtitle_style))
story.append(Spacer(1, 10))
story.append(Paragraph("DATA ANALYTICS & MACHINE LEARNING", title_style))
story.append(Spacer(1, 8))
story.append(Paragraph("Credit Card Customer Segmentation & Risk Intelligence Suite", subtitle_style))
story.append(Spacer(1, 20))
story.append(HRFlowable(width="60%", thickness=2, color=colors.HexColor('#2563eb'), spaceAfter=30))

meta_content = """
<b>Submitted by:</b><br/>
<b>PATHAN SAFEENKHAN R.</b><br/>
<b>Enrollment No.:</b> 230610107039<br/><br/>
<b>Academic Degree:</b><br/>
Bachelor of Engineering in Computer Engineering<br/>
Government Engineering College<br/>
Affiliated with Gujarat Technological University (GTU)<br/><br/>
<b>Internship Organization:</b><br/>
<b>INFOLABZ IT SERVICES PVT. LTD.</b><br/>
Ahmedabad, Gujarat (Tenure: 03 July 2026 to 17 July 2026)
"""
story.append(Paragraph(meta_content, meta_style))
story.append(PageBreak())

# =========================================================================
# DECLARATION & COMPANY PROFILE
# =========================================================================
story.append(Paragraph("DECLARATION", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))

declaration_text = """
I do hereby solemnly declare that the work presented in this Internship Report has been carried out by me during the summer internship tenure at <b>InfoLabz IT Services Pvt. Ltd.</b> and has not been previously submitted to any other University, College, or Organization for any academic qualification or certificate.<br/><br/>
I hereby warrant that the project implementation and technical documentation presented do not breach any existing copyright acts.
"""
story.append(Paragraph(declaration_text, body_style))
story.append(Spacer(1, 15))

sig_table_data = [
    [Paragraph("<b>Date:</b> 18-07-2026", body_style), Paragraph("<b>Pathan Safeenkhan R.</b><br/>(Student Signature)", body_style)]
]
sig_table = Table(sig_table_data, colWidths=[250, 250])
sig_table.setStyle(TableStyle([('ALIGN', (1,0), (1,0), 'RIGHT')]))
story.append(sig_table)
story.append(Spacer(1, 25))

story.append(Paragraph("COMPANY PROFILE: INFOLABZ IT SERVICES PVT. LTD.", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))
comp_profile = """
Established in 2016 in Ahmedabad, Gujarat, <b>InfoLabz IT Services Pvt. Ltd.</b> delivers specialized technical solutions in Web Development, Mobile Applications, Data Science, Machine Learning, and IoT architecture. Over a decade of operational excellence, InfoLabz has executed industry projects across international client bases with dedicated engineering teams. InfoLabz actively bridges the gap between academic curricula and industry engineering practices through structured technical internship programs.
"""
story.append(Paragraph(comp_profile, body_style))
story.append(Spacer(1, 15))

# Attached Documents Note Box
doc_notice = """
<b>Attached Institutional Documents:</b><br/>
&bull; <b>Section I:</b> Official Offer Letter (Dated: 24-06-2026, Ref: InfoLabz/Summer-26)<br/>
&bull; <b>Section II:</b> Completion Certificate (Dated: 18-07-2026, Enrollment: 230610107039)
"""
doc_box = Table([[Paragraph(doc_notice, body_style)]], colWidths=[504])
doc_box.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
    ('PADDING', (0,0), (-1,-1), 10),
]))
story.append(doc_box)
story.append(PageBreak())

# =========================================================================
# TABLE OF CONTENTS
# =========================================================================
story.append(Paragraph("TABLE OF CONTENTS", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))

toc_data = [
    [Paragraph("<b>Module / Date</b>", body_style), Paragraph("<b>Technical Topic & Syllabus Covered</b>", body_style), Paragraph("<b>Status</b>", body_style)],
    [Paragraph("Week 1: 03 July 2026", body_style), Paragraph("Data Source Taxonomies, Python Dictionaries, Requests Library", body_style), Paragraph("Completed", body_style)],
    [Paragraph("Week 1: 04 July 2026", body_style), Paragraph("REST API Ingestion, Dynamic JSON Traversal, Live COVID-19 Feed", body_style), Paragraph("Completed", body_style)],
    [Paragraph("Week 1: 06 July 2026", body_style), Paragraph("Pandas DataFrame Indexing, CSV Transformations, Matplotlib", body_style), Paragraph("Completed", body_style)],
    [Paragraph("Week 1: 07 July 2026", body_style), Paragraph("Excel Analytics with Pandas, Multi-variable Visuals, API Trends", body_style), Paragraph("Completed", body_style)],
    [Paragraph("Week 1: 08 July 2026", body_style), Paragraph("NumPy Matrix Computation & Data Cleaning Protocols", body_style), Paragraph("Completed", body_style)],
    [Paragraph("Week 1: 09 July 2026", body_style), Paragraph("OpenCV Frame Streaming & Simple Linear Regression Modeling", body_style), Paragraph("Completed", body_style)],
    [Paragraph("Week 2: 10 July 2026", body_style), Paragraph("Multiple Linear Regression & Multi-variable Correlation", body_style), Paragraph("Completed", body_style)],
    [Paragraph("Week 2: 11 July 2026", body_style), Paragraph("Polynomial Regression & Non-linear Curve Fitting", body_style), Paragraph("Completed", body_style)],
    [Paragraph("Week 2: 13-15 July 2026", body_style), Paragraph("Power BI Business Analytics, DAX Measures & Executive Dashboards", body_style), Paragraph("Completed", body_style)],
    [Paragraph("Week 2: 16 July 2026", body_style), Paragraph("K-Means Clustering Mathematical Theory & Euclidean Partitioning", body_style), Paragraph("Completed", body_style)],
    [Paragraph("Week 2: 17 July 2026", body_style), Paragraph("<b>Capstone Project:</b> Production Credit Card Segmentation Suite", body_style), Paragraph("Deployed", body_style)],
]

toc_table = Table(toc_data, colWidths=[110, 314, 80])
toc_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(toc_table)
story.append(PageBreak())

# =========================================================================
# DAILY TECHNICAL LOGS (WEEK 1 & WEEK 2)
# =========================================================================
story.append(Paragraph("WEEKLY TECHNICAL LOGS & IMPLEMENTATION", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))

def add_code_block(title, desc, code_str):
    story.append(Paragraph(title, h2_style))
    story.append(Paragraph(desc, body_style))
    code_table = Table([[Paragraph(code_str.replace(" ", "&nbsp;").replace("\n", "<br/>"), code_style)]], colWidths=[504])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(code_table)
    story.append(Spacer(1, 8))

add_code_block(
    "1. Data Ingestion via REST API (04 July 2026)",
    "Connected Python applications to live REST web services using HTTP GET requests and parsed nested JSON payloads into structured dictionaries.",
    """import requests
url = requests.get("https://data.covid19india.org/data.json")
data = url.json()
print("Tracking Days:", len(data["cases_time_series"]))
print("Total States Tracked:", len(data["statewise"]))"""
)

add_code_block(
    "2. Pandas DataFrame Manipulation & Vector Math (06 July 2026)",
    "Practiced DataFrame creation, multi-column indexing, array broadcasting, and exporting structured datasets to disk using Pandas.",
    """import pandas as pd
import numpy as np
empdata = np.array([[8000, 10000, 18000], [15000, 18000, 25000]])
df = pd.DataFrame(empdata, columns=[2024, 2025, 2026], index=["RAMESH", "MAHESH"])
df['TOTAL'] = 12 * (df[2024] + df[2025] + df[2026])
df.to_csv("prepareddata.csv")"""
)

add_code_block(
    "3. Supervised Learning: Linear Regression (09-10 July 2026)",
    "Built and fitted Ordinary Least Squares (OLS) and Multiple Linear Regression models using Scikit-Learn to evaluate feature weights and target predictions.",
    """from sklearn.linear_model import LinearRegression
import pandas as pd
df = pd.read_csv('orderdata.csv')
reg = LinearRegression().fit(df[['users', 'orders', 'age']], df['amount'])
pred = reg.predict([[2200, 5000, 34]])
print(f"Coefficients: {reg.coef_}, Intercept: {reg.intercept_}")"""
)

add_code_block(
    "4. Power BI Business Intelligence Dashboarding (13-15 July 2026)",
    "Designed commercial analytics dashboards incorporating DAX measures, custom KPI filters, donut category breakdowns, and geospatial region maps.",
    """// Sample DAX Measure Implementation
Total_Profit_Margin = DIVIDE(SUM(Orders[Profit]), SUM(Orders[Sales]), 0)
TOP_100_Orders = EVALUATE TOPN(100, 'Orders')"""
)

story.append(PageBreak())

# =========================================================================
# CAPSTONE PROJECT DOCUMENTATION
# =========================================================================
story.append(Paragraph("CAPSTONE PROJECT: PRODUCTION CUSTOMER SEGMENTATION ENGINE", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))

project_intro = """
<b>1. Problem Statement & Architecture</b><br/>
Credit card financial institutions manage portfolios where cardholders exhibit widely divergent financial behaviors across spending velocity, cash draw frequency, balance revolving rates, and repayment compliance. This capstone project engineered an unsupervised machine learning suite that compresses 17 behavioral dimensions into 3 principal components (PCA) and partitions cardholders into 4 distinct, actionable clusters via K-Means clustering.
"""
story.append(Paragraph(project_intro, body_style))
story.append(Spacer(1, 6))

story.append(Paragraph("2. Cluster Profiles & Business Strategic Actions", h2_style))

cluster_data = [
    [Paragraph("<b>Cluster</b>", body_style), Paragraph("<b>Persona Title</b>", body_style), Paragraph("<b>Key Financial Characteristics</b>", body_style), Paragraph("<b>Business Strategy & Retention Plan</b>", body_style)],
    [Paragraph("<b>Cluster 0</b>", body_style), Paragraph("<b>Retail Installment Planner</b>", body_style), Paragraph("High installment frequency, low cash draws, consistent full repayments.", body_style), Paragraph("Deploy 0% merchant EMI conversion campaigns and POS discount partnerships.", body_style)],
    [Paragraph("<b>Cluster 1</b>", body_style), Paragraph("<b>VIP High Spender</b>", body_style), Paragraph("High one-off spend, elevated credit limits, minimal revolving balances.", body_style), Paragraph("Offer premium travel concierge, airport lounge access, and credit line expansion.", body_style)],
    [Paragraph("<b>Cluster 2</b>", body_style), Paragraph("<b>Cash Advance Revolver</b>", body_style), Paragraph("Heavy cash draws, high revolving balance utilization, minimum payments.", body_style), Paragraph("Provide lower-interest debt consolidation loans and monitor default risk indices.", body_style)],
    [Paragraph("<b>Cluster 3</b>", body_style), Paragraph("<b>Dormant / Low Activity</b>", body_style), Paragraph("Low balances, infrequent purchases, conservative card activity.", body_style), Paragraph("Deploy lifecycle activation cashback vouchers and annual maintenance fee waivers.", body_style)],
]

cluster_table = Table(cluster_data, colWidths=[65, 110, 160, 169])
cluster_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(cluster_table)
story.append(Spacer(1, 10))

story.append(Paragraph("3. Production System Architecture", h2_style))
sys_arch = """
The final system was structured into a clean modular architecture under <code>C:\\CreditCard_AI_Project</code>:<br/>
&bull; <b><code>config.py</code>:</b> Centralizes system paths, feature definitions, and persona business dictionaries.<br/>
&bull; <b><code>train.py</code>:</b> Preprocesses raw data (median imputation + log transform), standardizes variance, fits PCA & K-Means, and serializes <code>.pkl</code> artifacts.<br/>
&bull; <b><code>ml_pipeline.py</code>:</b> Handles end-to-end vector transformations for single and bulk batch inference.<br/>
&bull; <b><code>visualizations.py</code>:</b> Generates interactive 3D cluster manifold projections, default risk meters, credit utilization dials, and radar benchmark charts using Plotly.<br/>
&bull; <b><code>app.py</code>:</b> Streamlit frontend providing real-time inference, batch CSV scoring, policy What-If simulation, and portfolio EDA profiling.<br/>
&bull; <b><code>assets/style.css</code>:</b> Provides a dark-mode fintech HUD aesthetic.
"""
story.append(Paragraph(sys_arch, body_style))
story.append(Spacer(1, 15))

story.append(Paragraph("CONCLUSION & FUTURE SCOPE", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))
conclusion_text = """
The summer internship at <b>InfoLabz IT Services Pvt. Ltd.</b> successfully reinforced core engineering principles in data manipulation, supervised regression, business intelligence reporting, and unsupervised clustering algorithms. The capstone project translated theoretical machine learning workflows into a production-ready credit intelligence suite with interactive web interfaces and batch processing capabilities. Future scope includes deploying real-time API webhooks for continuous live transaction ingestion and automated churn risk prediction.
"""
story.append(Paragraph(conclusion_text, body_style))

# Build Document
doc.build(story)
print(f" PDF Report successfully generated at: {output_pdf_path}")