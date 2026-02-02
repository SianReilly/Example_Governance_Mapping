import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx
from datetime import datetime
import json
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tempfile
import base64

# Custom CSS for Josefin Sans font and styling
st.set_page_config(page_title="Governance Mapping Tool", page_icon="🗺️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Josefin Sans', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Josefin Sans', sans-serif;
        font-weight: 600;
    }
    
    .stMetric {
        font-family: 'Josefin Sans', sans-serif;
    }
    
    .rag-green {
        background-color: #90EE90;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: 600;
    }
    
    .rag-amber {
        background-color: #FFD700;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: 600;
    }
    
    .rag-red {
        background-color: #DC143C;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced sample data with Fairer Westminster alignment and RAG status
SAMPLE_DATA = {
    "governance_bodies": [
        {
            "Name": "Cabinet", 
            "Type": "Cabinet", 
            "Level": "Strategic",
            "Outcome_Focus": "Fairer Westminster, Service Efficiency",
            "Fairer_Westminster_Alignment": "Strong Voice, Opportunity, Quality of Life",
            "Process_Type": "Explicit",
            "Efficiency_Score": 4,
            "Cost_Impact": "Very High",
            "Value_Added": 5,
            "Duplication_Risk": 1,
            "RAG_Status": "Green",
            "RAG_Recommendation": "Keep",
            "Primary_Stakeholders": "Council Members, Chief Executive, Directors",
            "Secondary_Stakeholders": "Residents, Media, Government",
            "Stakeholder_Power": "High",
            "Stakeholder_Interest": "High",
            "Value_Chain_Activities": "Strategic Decision-Making, Resource Allocation, Policy Setting",
            "Decision_Speed": "Slow",
            "Innovation_Posture": "Ambidextrous"
        },
        {
            "Name": "Commercial Gateway Review Board",
            "Type": "Board",
            "Level": "Tactical",
            "Outcome_Focus": "Service Efficiency",
            "Fairer_Westminster_Alignment": "Quality of Life",
            "Process_Type": "Mixed",
            "Efficiency_Score": 2,
            "Cost_Impact": "High",
            "Value_Added": 3,
            "Duplication_Risk": 4,
            "RAG_Status": "Amber",
            "RAG_Recommendation": "Merge",
            "Primary_Stakeholders": "Procurement, Finance, Legal",
            "Secondary_Stakeholders": "Suppliers, Service Directors",
            "Stakeholder_Power": "Medium",
            "Stakeholder_Interest": "High",
            "Value_Chain_Activities": "Procurement Approval, Contract Review, Risk Assessment",
            "Decision_Speed": "Slow",
            "Innovation_Posture": "Exploit"
        },
        {
            "Name": "Procuring Board",
            "Type": "Board",
            "Level": "Tactical",
            "Outcome_Focus": "Service Efficiency",
            "Fairer_Westminster_Alignment": "Quality of Life",
            "Process_Type": "Partially Explicit",
            "Efficiency_Score": 3,
            "Cost_Impact": "High",
            "Value_Added": 3,
            "Duplication_Risk": 5,
            "RAG_Status": "Red",
            "RAG_Recommendation": "Merge",
            "Primary_Stakeholders": "Procurement, Finance, Commercial",
            "Secondary_Stakeholders": "Suppliers, Market",
            "Stakeholder_Power": "Medium",
            "Stakeholder_Interest": "High",
            "Value_Chain_Activities": "Procurement Strategy, Supplier Management, Contract Awards",
            "Decision_Speed": "Slow",
            "Innovation_Posture": "Exploit"
        },
        {
            "Name": "Church Street JV Board",
            "Type": "Place-Based Board",
            "Level": "Community",
            "Outcome_Focus": "Place-Based, Fairer Westminster, Housing",
            "Fairer_Westminster_Alignment": "Strong Voice, Opportunity, Safe & Inclusive",
            "Process_Type": "Mixed",
            "Efficiency_Score": 3,
            "Cost_Impact": "Medium",
            "Value_Added": 4,
            "Duplication_Risk": 2,
            "RAG_Status": "Green",
            "RAG_Recommendation": "Keep",
            "Primary_Stakeholders": "Local Residents, Community Groups, Housing",
            "Secondary_Stakeholders": "Developers, GLA, Councillors",
            "Stakeholder_Power": "Medium",
            "Stakeholder_Interest": "Very High",
            "Value_Chain_Activities": "Community Engagement, Local Decision-Making, Project Approval",
            "Decision_Speed": "Medium",
            "Innovation_Posture": "Explore"
        },
        {
            "Name": "Climate Leadership Group",
            "Type": "Board",
            "Level": "Tactical",
            "Outcome_Focus": "Net Zero, Place-Based",
            "Fairer_Westminster_Alignment": "Quality of Life, Greener City",
            "Process_Type": "Explicit",
            "Efficiency_Score": 4,
            "Cost_Impact": "Medium",
            "Value_Added": 5,
            "Duplication_Risk": 1,
            "RAG_Status": "Green",
            "RAG_Recommendation": "Keep",
            "Primary_Stakeholders": "Environment Team, Cabinet, Service Directors",
            "Secondary_Stakeholders": "Residents, Climate Activists, Government",
            "Stakeholder_Power": "High",
            "Stakeholder_Interest": "Very High",
            "Value_Chain_Activities": "Climate Strategy, Carbon Monitoring, Innovation Projects",
            "Decision_Speed": "Medium",
            "Innovation_Posture": "Ambidextrous"
        },
        {
            "Name": "Joint Health and Wellbeing Board",
            "Type": "Board",
            "Level": "Strategic",
            "Outcome_Focus": "Public Health, Fairer Westminster",
            "Fairer_Westminster_Alignment": "Opportunity, Quality of Life, Safe & Inclusive",
            "Process_Type": "Explicit",
            "Efficiency_Score": 3,
            "Cost_Impact": "High",
            "Value_Added": 5,
            "Duplication_Risk": 2,
            "RAG_Status": "Green",
            "RAG_Recommendation": "Keep",
            "Primary_Stakeholders": "NHS, Public Health, Adult Social Care",
            "Secondary_Stakeholders": "GPs, Residents, Voluntary Sector",
            "Stakeholder_Power": "High",
            "Stakeholder_Interest": "High",
            "Value_Chain_Activities": "Health Strategy, Service Integration, Commissioning",
            "Decision_Speed": "Slow",
            "Innovation_Posture": "Ambidextrous"
        },
        {
            "Name": "Digital Governance Board",
            "Type": "Board",
            "Level": "Tactical",
            "Outcome_Focus": "Digital Transformation, Service Efficiency",
            "Fairer_Westminster_Alignment": "Strong Voice, Opportunity, Quality of Life",
            "Process_Type": "Explicit",
            "Efficiency_Score": 4,
            "Cost_Impact": "High",
            "Value_Added": 4,
            "Duplication_Risk": 1,
            "RAG_Status": "Green",
            "RAG_Recommendation": "Keep",
            "Primary_Stakeholders": "IT, Digital Services, Service Directors",
            "Secondary_Stakeholders": "Residents, Staff, Suppliers",
            "Stakeholder_Power": "Medium",
            "Stakeholder_Interest": "High",
            "Value_Chain_Activities": "Technology Strategy, Project Approval, Standards Setting",
            "Decision_Speed": "Fast",
            "Innovation_Posture": "Explore"
        },
        {
            "Name": "Beyond Lisson Grove Board",
            "Type": "Place-Based Board",
            "Level": "Community",
            "Outcome_Focus": "Place-Based, Fairer Westminster, Community Safety",
            "Fairer_Westminster_Alignment": "Strong Voice, Safe & Inclusive, Opportunity",
            "Process_Type": "Mixed",
            "Efficiency_Score": 2,
            "Cost_Impact": "Low",
            "Value_Added": 4,
            "Duplication_Risk": 2,
            "RAG_Status": "Amber",
            "RAG_Recommendation": "Keep",
            "Primary_Stakeholders": "Local Residents, Community Leaders, Housing",
            "Secondary_Stakeholders": "Police, Youth Services, Councillors",
            "Stakeholder_Power": "Low",
            "Stakeholder_Interest": "Very High",
            "Value_Chain_Activities": "Community Engagement, Local Priorities, Project Approval",
            "Decision_Speed": "Medium",
            "Innovation_Posture": "Explore"
        }
    ],
    "five_forces": {
        "Threat of New Entrants": 3,
        "Bargaining Power of Stakeholders": 4,
        "Threat of Alternative Models": 2,
        "Pressure for Accountability": 5,
        "Resource Competition": 4
    }
}

# Fairer Westminster principles
FAIRER_WESTMINSTER_PRINCIPLES = {
    "Strong Voice": "Residents have a strong voice and are at the heart of our decision-making",
    "Opportunity": "Everyone has the opportunity to participate and succeed in the city",
    "Quality of Life": "Everyone can enjoy a high quality of life in our city",
    "Safe & Inclusive": "Westminster is a safe and inclusive city for all",
    "Greener City": "Westminster is a greener city, leading on climate action"
}

# Initialise with sample data
if 'initialised' not in st.session_state:
    st.session_state.bodies_df = pd.DataFrame(SAMPLE_DATA['governance_bodies'])
    st.session_state.five_forces = SAMPLE_DATA['five_forces']
    st.session_state.initialised = True
    st.session_state.example_mode = True
    st.session_state.edit_mode = False

def get_rag_color(status):
    """Return HTML colour for RAG status"""
    if status == "Green":
        return "🟢"
    elif status == "Amber":
        return "🟡"
    elif status == "Red":
        return "🔴"
    return "⚪"

def create_pdf_report():
    """Generate comprehensive PDF report"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomTitle', parent=styles['Heading1'],
                             fontSize=24, textColor=colors.HexColor('#1f77b4'),
                             spaceAfter=30, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='CustomHeading', parent=styles['Heading2'],
                             fontSize=16, textColor=colors.HexColor('#1f77b4'),
                             spaceAfter=12))
    styles.add(ParagraphStyle(name='BodyJustify', parent=styles['BodyText'],
                             alignment=TA_JUSTIFY, fontSize=11))
    
    df = st.session_state.bodies_df
    
    # Title
    title = Paragraph("Westminster City Council<br/>Governance Mapping & Analysis Report", styles['CustomTitle'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    subtitle = Paragraph(f"Aligned with Fairer Westminster Principles<br/>Generated: {datetime.now().strftime('%d %B %Y')}", 
                        styles['Normal'])
    elements.append(subtitle)
    elements.append(Spacer(1, 24))
    
    # Executive Summary
    elements.append(Paragraph("Executive Summary", styles['CustomHeading']))
    
    summary_text = f"""
    This report presents a comprehensive analysis of {len(df)} governance bodies at Westminster City Council, 
    evaluated against the Fairer Westminster principles and assessed using multiple analytical frameworks 
    including Rogers' Diffusion of Innovations, Schilling's Stakeholder Analysis, Smith's Knowledge Management, 
    and Porter's Strategic Frameworks adapted for public sector use.
    """
    elements.append(Paragraph(summary_text, styles['BodyJustify']))
    elements.append(Spacer(1, 12))
    
    # Key Findings
    elements.append(Paragraph("Key Findings", styles['CustomHeading']))
    
    green_count = len(df[df['RAG_Status'] == 'Green'])
    amber_count = len(df[df['RAG_Status'] == 'Amber'])
    red_count = len(df[df['RAG_Status'] == 'Red'])
    avg_efficiency = df['Efficiency_Score'].mean()
    avg_value = df['Value_Added'].mean()
    high_dup = len(df[df['Duplication_Risk'] >= 4])
    
    findings_data = [
        ['Metric', 'Value'],
        ['Total Governance Bodies', str(len(df))],
        ['RAG Status - Green (Keep)', str(green_count)],
        ['RAG Status - Amber (Review)', str(amber_count)],
        ['RAG Status - Red (Urgent Action)', str(red_count)],
        ['Average Efficiency Score', f"{avg_efficiency:.1f}/5"],
        ['Average Value Added', f"{avg_value:.1f}/5"],
        ['High Duplication Risk Bodies', str(high_dup)],
    ]
    
    findings_table = Table(findings_data, colWidths=[4*inch, 2*inch])
    findings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(findings_table)
    elements.append(Spacer(1, 24))
    
    # Fairer Westminster Alignment
    elements.append(PageBreak())
    elements.append(Paragraph("Fairer Westminster Principles Alignment", styles['CustomHeading']))
    
    fw_text = """
    Westminster's governance has been assessed against the five Fairer Westminster principles:
    """
    elements.append(Paragraph(fw_text, styles['BodyJustify']))
    elements.append(Spacer(1, 12))
    
    for principle, description in FAIRER_WESTMINSTER_PRINCIPLES.items():
        elements.append(Paragraph(f"<b>{principle}:</b> {description}", styles['Normal']))
        elements.append(Spacer(1, 6))
        
        # Count bodies aligned with this principle
        aligned = len(df[df['Fairer_Westminster_Alignment'].str.contains(principle, na=False)])
        elements.append(Paragraph(f"Bodies aligned: {aligned}", styles['Normal']))
        elements.append(Spacer(1, 12))
    
    # Governance Bodies Detail
    elements.append(PageBreak())
    elements.append(Paragraph("Governance Bodies Assessment", styles['CustomHeading']))
    
    for _, row in df.iterrows():
        rag_symbol = "GREEN" if row['RAG_Status'] == 'Green' else "AMBER" if row['RAG_Status'] == 'Amber' else "RED"
        
        elements.append(Paragraph(f"<b>{row['Name']}</b> - RAG: {rag_symbol}", styles['Heading3']))
        
        body_data = [
            ['Attribute', 'Value'],
            ['Type', row['Type']],
            ['Level', row['Level']],
            ['RAG Recommendation', row['RAG_Recommendation']],
            ['Fairer Westminster Alignment', row['Fairer_Westminster_Alignment']],
            ['Efficiency Score', f"{row['Efficiency_Score']}/5"],
            ['Value Added', f"{row['Value_Added']}/5"],
            ['Duplication Risk', f"{row['Duplication_Risk']}/5"],
            ['Decision Speed', row['Decision_Speed']],
            ['Primary Stakeholders', row['Primary_Stakeholders']],
        ]
        
        body_table = Table(body_data, colWidths=[2.5*inch, 3.5*inch])
        body_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(body_table)
        elements.append(Spacer(1, 16))
    
    # Recommendations
    elements.append(PageBreak())
    elements.append(Paragraph("Strategic Recommendations", styles['CustomHeading']))
    
    # Merge recommendations
    merge_bodies = df[df['RAG_Recommendation'] == 'Merge']
    if len(merge_bodies) > 0:
        elements.append(Paragraph("<b>1. Consolidation Opportunities (MERGE)</b>", styles['Heading3']))
        for _, row in merge_bodies.iterrows():
            elements.append(Paragraph(f"• {row['Name']} - Duplication Risk: {row['Duplication_Risk']}/5", 
                                     styles['Normal']))
        elements.append(Spacer(1, 12))
    
    # Close recommendations
    close_bodies = df[df['RAG_Recommendation'] == 'Close']
    if len(close_bodies) > 0:
        elements.append(Paragraph("<b>2. Bodies to Close</b>", styles['Heading3']))
        for _, row in close_bodies.iterrows():
            elements.append(Paragraph(f"• {row['Name']} - Low value or high cost", styles['Normal']))
        elements.append(Spacer(1, 12))
    
    # Efficiency improvements
    low_eff = df[df['Efficiency_Score'] < 3]
    if len(low_eff) > 0:
        elements.append(Paragraph("<b>3. Efficiency Improvement Priorities</b>", styles['Heading3']))
        for _, row in low_eff.iterrows():
            elements.append(Paragraph(f"• {row['Name']} - Current efficiency: {row['Efficiency_Score']}/5", 
                                     styles['Normal']))
        elements.append(Spacer(1, 12))
    
    # Estimated savings
    elements.append(Paragraph("<b>4. Estimated Financial Impact</b>", styles['Heading3']))
    savings_text = """
    Based on analysis:
    • Commercial governance consolidation: £85,000 annually
    • Process documentation efficiency gains: £35,000 annually  
    • Streamlined reporting: £15,000 annually
    
    Total Estimated Annual Savings: £135,000+
    """
    elements.append(Paragraph(savings_text, styles['Normal']))
    elements.append(Spacer(1, 24))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Sidebar
st.sidebar.title("🗺️ Governance Mapping")
if st.session_state.get('example_mode'):
    st.sidebar.success("📚 EXAMPLE MODE")
    st.sidebar.markdown("*Westminster sample data*")

# Edit mode toggle
st.session_state.edit_mode = st.sidebar.checkbox("✏️ Edit Mode", value=st.session_state.edit_mode)

page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "🏛️ Governance Bodies", 
    "📊 Efficiency Analysis",
    "👥 Stakeholder Analysis",
    "⛓️ Value Chain Mapping",
    "⚡ Five Forces Analysis",
    "🌐 Network View",
    "🎯 Fairer Westminster Dashboard",
    "📥 Export"
])

# HOME
if page == "🏠 Home":
    st.title("🗺️ Governance Mapping & Analysis Tool")
    st.markdown("*Westminster City Council - Aligned with Fairer Westminster Principles*")
    
    if st.session_state.get('example_mode'):
        st.info("📚 **Westminster Example Data Loaded** - Demonstrating frameworks adapted for local government")
    
    # Fairer Westminster principles display
    st.markdown("### 🎯 Fairer Westminster Principles")
    
    cols = st.columns(5)
    principles_list = list(FAIRER_WESTMINSTER_PRINCIPLES.items())
    
    for idx, col in enumerate(cols):
        if idx < len(principles_list):
            principle, description = principles_list[idx]
            with col:
                st.markdown(f"**{principle}**")
                st.caption(description)
    
    st.markdown("---")
    
    st.markdown("""
    ### Multi-Framework Governance Analysis for Public Sector
    
    This tool integrates **five complementary frameworks** adapted for public sector governance:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Innovation & Change Frameworks
        
        **1. Rogers (2003)** - Diffusion of Innovations ✅
        - **Public sector fit:** Excellent - widely used in public services
        - Phase reforms by adopter categories
        - Sequence governance changes strategically
        - Manage resistance to organisational change
        
        **2. Schilling (2022)** - Innovation Management ✅
        - **Public sector fit:** Good - requires adaptation
        - Stakeholder analysis (highly applicable)
        - Lifecycle mapping (useful for project governance)
        - Structural design choices
        
        **3. Smith (2024)** - Knowledge Management ✅
        - **Public sector fit:** Excellent - critical for councils
        - Tacit→Explicit conversion
        - Efficiency through process documentation
        - Preserve institutional knowledge during turnover
        """)
    
    with col2:
        st.markdown("""
        #### Strategic Analysis Frameworks
        
        **4. Porter's Value Chain** ⚠️
        - **Public sector fit:** Limited - requires significant adaptation
        - **Private sector origin:** Designed for profit-seeking firms
        - **Public sector use:** Map governance activities to outcomes
        - Focus on service delivery value, not profit margins
        - Useful for identifying overhead vs value-adding governance
        
        **5. Porter's Five Forces** ⚠️
        - **Public sector fit:** Limited - requires reinterpretation
        - **Private sector origin:** Designed for competitive markets
        - **Public sector use:** Analyse pressures on governance:
          - Stakeholder power (residents, partners, government)
          - Accountability demands (media, regulators, voters)
          - Alternative service models (digital, community-led)
          - Resource competition (budget, senior time)
        - Not about profit/competition but governance effectiveness
        """)
    
    st.markdown("---")
    
    # Enhanced dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    df = st.session_state.bodies_df
    
    with col1:
        st.metric("Bodies Mapped", len(df))
        green_count = len(df[df['RAG_Status'] == 'Green'])
        st.metric("🟢 Green Status", green_count)
    
    with col2:
        amber_count = len(df[df['RAG_Status'] == 'Amber'])
        st.metric("🟡 Amber Status", amber_count)
        red_count = len(df[df['RAG_Status'] == 'Red'])
        st.metric("🔴 Red Status", red_count)
    
    with col3:
        avg_eff = df['Efficiency_Score'].mean()
        st.metric("Avg Efficiency", f"{avg_eff:.1f}/5")
        merge_count = len(df[df['RAG_Recommendation'] == 'Merge'])
        st.metric("Merge Recommended", merge_count)
    
    with col4:
        high_stake = len(df[df['Stakeholder_Interest'] == 'Very High'])
        st.metric("High Stakeholder Interest", high_stake)
        place_based = len(df[df['Type'] == 'Place-Based Board'])
        st.metric("Place-Based Boards", place_based)
    
    st.markdown("---")
    
    # RAG Status overview
    st.subheader("📊 RAG Status Overview")
    
    rag_counts = df['RAG_Status'].value_counts().reset_index()
    rag_counts.columns = ['Status', 'Count']
    
    fig = px.pie(
        rag_counts,
        values='Count',
        names='Status',
        title='Governance Bodies by RAG Status',
        color='Status',
        color_discrete_map={'Green': '#90EE90', 'Amber': '#FFD700', 'Red': '#DC143C'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Quick visualisation
    st.subheader("Quick Overview: Efficiency vs Value by Cost")
    
    fig = px.scatter(
        df, 
        x='Efficiency_Score', 
        y='Value_Added',
        size='Duplication_Risk',
        color='RAG_Status',
        hover_name='Name',
        title='Governance Bodies: Efficiency vs Value (bubble size = duplication risk)',
        labels={'Efficiency_Score': 'Efficiency Score', 'Value_Added': 'Value Added'},
        color_discrete_map={'Green': '#90EE90', 'Amber': '#FFD700', 'Red': '#DC143C'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# GOVERNANCE BODIES
elif page == "🏛️ Governance Bodies":
    st.title("🏛️ Governance Bodies Overview")
    
    df = st.session_state.bodies_df
    
    # Add new body option
    if st.session_state.edit_mode:
        with st.expander("➕ Add New Governance Body"):
            with st.form("add_body_form"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    new_name = st.text_input("Name*")
                    new_type = st.selectbox("Type*", ["Board", "Cabinet", "Committee", "Place-Based Board", "Partnership"])
                    new_level = st.selectbox("Level*", ["Strategic", "Tactical", "Operational", "Community"])
                    new_outcome = st.text_input("Outcome Focus*")
                
                with col2:
                    fw_options = list(FAIRER_WESTMINSTER_PRINCIPLES.keys())
                    new_fw = st.multiselect("Fairer Westminster Alignment*", fw_options)
                    new_process = st.selectbox("Process Type*", ["Explicit", "Partially Explicit", "Mixed", "Tacit"])
                    new_efficiency = st.slider("Efficiency Score*", 1, 5, 3)
                    new_cost = st.selectbox("Cost Impact*", ["Low", "Medium", "High", "Very High"])
                
                with col3:
                    new_value = st.slider("Value Added*", 1, 5, 3)
                    new_dup = st.slider("Duplication Risk*", 1, 5, 1)
                    new_rag = st.selectbox("RAG Status*", ["Green", "Amber", "Red"])
                    new_rag_rec = st.selectbox("RAG Recommendation*", ["Keep", "Merge", "Close"])
                
                col4, col5 = st.columns(2)
                
                with col4:
                    new_primary = st.text_area("Primary Stakeholders*")
                    new_secondary = st.text_area("Secondary Stakeholders")
                    new_power = st.selectbox("Stakeholder Power*", ["Low", "Medium", "High"])
                
                with col5:
                    new_interest = st.selectbox("Stakeholder Interest*", ["Low", "Medium", "High", "Very High"])
                    new_activities = st.text_area("Value Chain Activities*")
                    new_speed = st.selectbox("Decision Speed*", ["Fast", "Medium", "Slow"])
                    new_posture = st.selectbox("Innovation Posture*", ["Exploit", "Explore", "Ambidextrous"])
                
                submitted = st.form_submit_button("Add Governance Body")
                
                if submitted and new_name and new_outcome and new_fw and new_primary and new_activities:
                    new_body = {
                        "Name": new_name,
                        "Type": new_type,
                        "Level": new_level,
                        "Outcome_Focus": new_outcome,
                        "Fairer_Westminster_Alignment": ", ".join(new_fw),
                        "Process_Type": new_process,
                        "Efficiency_Score": new_efficiency,
                        "Cost_Impact": new_cost,
                        "Value_Added": new_value,
                        "Duplication_Risk": new_dup,
                        "RAG_Status": new_rag,
                        "RAG_Recommendation": new_rag_rec,
                        "Primary_Stakeholders": new_primary,
                        "Secondary_Stakeholders": new_secondary,
                        "Stakeholder_Power": new_power,
                        "Stakeholder_Interest": new_interest,
                        "Value_Chain_Activities": new_activities,
                        "Decision_Speed": new_speed,
                        "Innovation_Posture": new_posture
                    }
                    
                    st.session_state.bodies_df = pd.concat([st.session_state.bodies_df, pd.DataFrame([new_body])], ignore_index=True)
                    st.success(f"✅ Added {new_name}")
                    st.rerun()
    
    # Filter options
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        level_filter = st.multiselect("Filter by Level", df['Level'].unique(), default=df['Level'].unique())
    with col2:
        rag_filter = st.multiselect("Filter by RAG Status", df['RAG_Status'].unique(), default=df['RAG_Status'].unique())
    with col3:
        rec_filter = st.multiselect("Filter by Recommendation", df['RAG_Recommendation'].unique(), default=df['RAG_Recommendation'].unique())
    with col4:
        show_dup_only = st.checkbox("Show only high duplication risk (≥3)")
    
    filtered_df = df[
        df['Level'].isin(level_filter) & 
        df['RAG_Status'].isin(rag_filter) &
        df['RAG_Recommendation'].isin(rec_filter)
    ]
    
    if show_dup_only:
        filtered_df = filtered_df[filtered_df['Duplication_Risk'] >= 3]
    
    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} bodies**")
    
    # Bodies as cards
    for idx, row in filtered_df.iterrows():
        rag_emoji = get_rag_color(row['RAG_Status'])
        
        with st.expander(f"{rag_emoji} **{row['Name']}** ({row['Type']}) - {row['RAG_Recommendation']}"):
            if st.session_state.edit_mode:
                # Edit mode
                with st.form(f"edit_form_{idx}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**Profile**")
                        edit_type = st.selectbox("Type", ["Board", "Cabinet", "Committee", "Place-Based Board", "Partnership"], 
                                                index=["Board", "Cabinet", "Committee", "Place-Based Board", "Partnership"].index(row['Type']),
                                                key=f"type_{idx}")
                        edit_level = st.selectbox("Level", ["Strategic", "Tactical", "Operational", "Community"],
                                                 index=["Strategic", "Tactical", "Operational", "Community"].index(row['Level']),
                                                 key=f"level_{idx}")
                        edit_outcome = st.text_input("Outcome Focus", row['Outcome_Focus'], key=f"outcome_{idx}")
                        edit_process = st.selectbox("Process Type", ["Explicit", "Partially Explicit", "Mixed", "Tacit"],
                                                   index=["Explicit", "Partially Explicit", "Mixed", "Tacit"].index(row['Process_Type']),
                                                   key=f"process_{idx}")
                    
                    with col2:
                        st.markdown("**Performance & Status**")
                        edit_efficiency = st.slider("Efficiency", 1, 5, row['Efficiency_Score'], key=f"eff_{idx}")
                        edit_value = st.slider("Value Added", 1, 5, row['Value_Added'], key=f"val_{idx}")
                        edit_dup = st.slider("Duplication Risk", 1, 5, row['Duplication_Risk'], key=f"dup_{idx}")
                        edit_rag = st.selectbox("RAG Status", ["Green", "Amber", "Red"],
                                               index=["Green", "Amber", "Red"].index(row['RAG_Status']),
                                               key=f"rag_{idx}")
                        edit_rag_rec = st.selectbox("RAG Recommendation", ["Keep", "Merge", "Close"],
                                                   index=["Keep", "Merge", "Close"].index(row['RAG_Recommendation']),
                                                   key=f"rec_{idx}")
                    
                    with col3:
                        st.markdown("**Stakeholders**")
                        edit_primary = st.text_area("Primary Stakeholders", row['Primary_Stakeholders'], key=f"prim_{idx}")
                        edit_secondary = st.text_area("Secondary Stakeholders", row['Secondary_Stakeholders'], key=f"sec_{idx}")
                    
                    col4, col5 = st.columns(2)
                    with col4:
                        fw_current = row['Fairer_Westminster_Alignment'].split(", ")
                        edit_fw = st.multiselect("Fairer Westminster Alignment", 
                                                list(FAIRER_WESTMINSTER_PRINCIPLES.keys()),
                                                default=fw_current,
                                                key=f"fw_{idx}")
                    
                    with col5:
                        edit_activities = st.text_area("Value Chain Activities", row['Value_Chain_Activities'], key=f"act_{idx}")
                    
                    col_save, col_delete = st.columns([1, 1])
                    
                    with col_save:
                        save_button = st.form_submit_button("💾 Save Changes")
                    
                    with col_delete:
                        delete_button = st.form_submit_button("🗑️ Delete Body", type="secondary")
                    
                    if save_button:
                        # Update the dataframe
                        st.session_state.bodies_df.at[idx, 'Type'] = edit_type
                        st.session_state.bodies_df.at[idx, 'Level'] = edit_level
                        st.session_state.bodies_df.at[idx, 'Outcome_Focus'] = edit_outcome
                        st.session_state.bodies_df.at[idx, 'Process_Type'] = edit_process
                        st.session_state.bodies_df.at[idx, 'Efficiency_Score'] = edit_efficiency
                        st.session_state.bodies_df.at[idx, 'Value_Added'] = edit_value
                        st.session_state.bodies_df.at[idx, 'Duplication_Risk'] = edit_dup
                        st.session_state.bodies_df.at[idx, 'RAG_Status'] = edit_rag
                        st.session_state.bodies_df.at[idx, 'RAG_Recommendation'] = edit_rag_rec
                        st.session_state.bodies_df.at[idx, 'Primary_Stakeholders'] = edit_primary
                        st.session_state.bodies_df.at[idx, 'Secondary_Stakeholders'] = edit_secondary
                        st.session_state.bodies_df.at[idx, 'Fairer_Westminster_Alignment'] = ", ".join(edit_fw)
                        st.session_state.bodies_df.at[idx, 'Value_Chain_Activities'] = edit_activities
                        st.success(f"✅ Saved changes to {row['Name']}")
                        st.rerun()
                    
                    if delete_button:
                        st.session_state.bodies_df = st.session_state.bodies_df.drop(idx).reset_index(drop=True)
                        st.success(f"🗑️ Deleted {row['Name']}")
                        st.rerun()
            
            else:
                # View mode
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Profile**")
                    st.markdown(f"Level: {row['Level']}")
                    st.markdown(f"Outcome Focus: {row['Outcome_Focus']}")
                    st.markdown(f"Process Type: {row['Process_Type']}")
                    st.markdown(f"Decision Speed: {row['Decision_Speed']}")
                
                with col2:
                    st.markdown("**Performance Metrics**")
                    st.metric("Efficiency", f"{row['Efficiency_Score']}/5")
                    st.metric("Value Added", f"{row['Value_Added']}/5")
                    st.metric("Duplication Risk", f"{row['Duplication_Risk']}/5")
                    st.markdown(f"**RAG Status:** {get_rag_color(row['RAG_Status'])} {row['RAG_Status']}")
                    st.markdown(f"**Recommendation:** {row['RAG_Recommendation']}")
                
                with col3:
                    st.markdown("**Stakeholders**")
                    st.markdown(f"**Primary:** {row['Primary_Stakeholders']}")
                    st.markdown(f"**Secondary:** {row['Secondary_Stakeholders']}")
                    st.markdown(f"**Power:** {row['Stakeholder_Power']}")
                    st.markdown(f"**Interest:** {row['Stakeholder_Interest']}")
                
                st.markdown(f"**Fairer Westminster Alignment:** {row['Fairer_Westminster_Alignment']}")
                st.markdown(f"**Value Chain Activities:** {row['Value_Chain_Activities']}")

# EFFICIENCY ANALYSIS (keeping all original graphs)
elif page == "📊 Efficiency Analysis":
    st.title("📊 Efficiency Analysis")
    
    df = st.session_state.bodies_df
    
    # Priority reform opportunities
    st.subheader("🎯 Priority Reform Opportunities (RAG-Based)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔴 Red Status - Urgent Action Required")
        red_bodies = df[df['RAG_Status'] == 'Red']
        if len(red_bodies) > 0:
            for _, row in red_bodies.iterrows():
                st.error(f"**{row['Name']}** - {row['RAG_Recommendation']} - Duplication: {row['Duplication_Risk']}/5")
        else:
            st.success("✅ No red status bodies")
        
        st.markdown("### 🟡 Amber Status - Review Needed")
        amber_bodies = df[df['RAG_Status'] == 'Amber']
        if len(amber_bodies) > 0:
            for _, row in amber_bodies.iterrows():
                st.warning(f"**{row['Name']}** - {row['RAG_Recommendation']} - Efficiency: {row['Efficiency_Score']}/5")
        else:
            st.success("✅ No amber status bodies")
    
    with col2:
        st.markdown("### Merge Recommendations")
        merge_rec = df[df['RAG_Recommendation'] == 'Merge']
        if len(merge_rec) > 0:
            for _, row in merge_rec.iterrows():
                st.warning(f"**{row['Name']}** - Duplication: {row['Duplication_Risk']}/5")
            
            if len(merge_rec) >= 2:
                st.markdown("**💡 Consolidation Opportunity:**")
                st.markdown("Commercial Gateway Review Board + Procuring Board = Single Strategic Procurement Board")
                st.success("**Estimated saving: £85K annually**")
        else:
            st.success("✅ No merge recommendations")
        
        st.markdown("### Slow Decision-Making")
        slow = df[df['Decision_Speed'] == 'Slow']
        if len(slow) > 0:
            for _, row in slow.iterrows():
                st.info(f"**{row['Name']}** - {row['Cost_Impact']} cost, {row['Efficiency_Score']}/5 efficiency")
        else:
            st.success("✅ No slow decision bodies")
    
    st.markdown("---")
    
    # Enhanced cost-value matrix
    st.subheader("📊 Multi-Dimensional Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Cost-Value Matrix", "Efficiency Distribution", "Decision Speed Impact"])
    
    with tab1:
        df_viz = df.copy()
        df_viz['Cost_Numeric'] = df_viz['Cost_Impact'].map({'Low': 1, 'Medium': 2, 'High': 3, 'Very High': 4})
        
        fig = px.scatter(
            df_viz, 
            x='Cost_Numeric', 
            y='Value_Added',
            size='Duplication_Risk',
            color='RAG_Status',
            hover_name='Name',
            hover_data=['Efficiency_Score', 'Decision_Speed', 'RAG_Recommendation'],
            labels={'Cost_Numeric': 'Cost Impact', 'Value_Added': 'Value Added'},
            title='Cost vs Value Analysis (coloured by RAG status)',
            size_max=30,
            color_discrete_map={'Green': '#90EE90', 'Amber': '#FFD700', 'Red': '#DC143C'}
        )
        fig.add_hline(y=3, line_dash="dash", line_color="gray", annotation_text="Value threshold")
        fig.add_vline(x=2.5, line_dash="dash", line_color="gray", annotation_text="Cost threshold")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Quadrant Analysis:**
        - **High Value, Low Cost** (Top-Left): Optimal - maintain ✅
        - **High Value, High Cost** (Top-Right): Valuable but expensive - optimise ⚠️
        - **Low Value, Low Cost** (Bottom-Left): Marginal - review 🤔
        - **Low Value, High Cost** (Bottom-Right): Critical issue - eliminate or redesign ❌
        """)
    
    with tab2:
        # Efficiency distribution by level
        fig = px.box(
            df,
            x='Level',
            y='Efficiency_Score',
            color='Innovation_Posture',
            title='Efficiency Score Distribution by Level and Posture',
            points='all'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Insight:** Shows efficiency variation across organisational levels and innovation postures")
    
    with tab3:
        # Decision speed vs efficiency
        speed_order = ['Fast', 'Medium', 'Slow']
        df_speed = df.copy()
        df_speed['Decision_Speed'] = pd.Categorical(df_speed['Decision_Speed'], categories=speed_order, ordered=True)
        df_speed = df_speed.sort_values('Decision_Speed')
        
        fig = px.bar(
            df_speed,
            x='Name',
            y='Efficiency_Score',
            color='Decision_Speed',
            title='Decision Speed Impact on Efficiency',
            color_discrete_map={'Fast': '#90EE90', 'Medium': '#FFD700', 'Slow': '#DC143C'}
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        avg_by_speed = df.groupby('Decision_Speed')['Efficiency_Score'].mean()
        st.markdown("**Average Efficiency by Decision Speed:**")
        for speed in speed_order:
            if speed in avg_by_speed.index:
                st.markdown(f"- {speed}: {avg_by_speed[speed]:.1f}/5")

# STAKEHOLDER ANALYSIS (keeping all original content)
elif page == "👥 Stakeholder Analysis":
    st.title("👥 Stakeholder Analysis (Schilling Framework)")
    st.markdown("*Highly applicable to public sector - widely used in local government*")
    
    st.markdown("""
    **Schilling's Stakeholder Analysis** maps stakeholder power and interest to inform governance engagement strategies.
    
    This framework is **particularly well-suited to public sector** contexts where multiple stakeholders (residents, partners, 
    government, media) have different levels of power and interest in governance decisions.
    
    ### Four Engagement Strategies:
    
    - **High Power, High Interest**: Key players - engage closely and satisfy
    - **High Power, Low Interest**: Keep satisfied - maintain their support
    - **Low Power, High Interest**: Keep informed - leverage their enthusiasm
    - **Low Power, Low Interest**: Monitor - minimal effort required
    """)
    
    df = st.session_state.bodies_df
    
    # Power-Interest Matrix
    st.subheader("📊 Stakeholder Power-Interest Matrix")
    
    # Map power and interest to numeric
    power_map = {'Low': 1, 'Medium': 2, 'High': 3}
    interest_map = {'Low': 1, 'Medium': 2, 'High': 3, 'Very High': 4}
    
    df_stake = df.copy()
    df_stake['Power_Numeric'] = df_stake['Stakeholder_Power'].map(power_map)
    df_stake['Interest_Numeric'] = df_stake['Stakeholder_Interest'].map(interest_map)
    
    fig = px.scatter(
        df_stake,
        x='Power_Numeric',
        y='Interest_Numeric',
        size='Value_Added',
        color='RAG_Status',
        hover_name='Name',
        hover_data=['Primary_Stakeholders', 'Secondary_Stakeholders', 'Fairer_Westminster_Alignment'],
        labels={'Power_Numeric': 'Stakeholder Power', 'Interest_Numeric': 'Stakeholder Interest'},
        title='Stakeholder Power-Interest Matrix by Governance Body',
        color_discrete_map={'Green': '#90EE90', 'Amber': '#FFD700', 'Red': '#DC143C'}
    )
    
    # Add quadrant lines
    fig.add_hline(y=2.5, line_dash="dash", line_color="gray")
    fig.add_vline(x=2, line_dash="dash", line_color="gray")
    
    # Add quadrant labels
    fig.add_annotation(x=1.5, y=3.5, text="Keep Informed<br>(Low Power, High Interest)", showarrow=False, bgcolor="lightyellow", opacity=0.7)
    fig.add_annotation(x=2.75, y=3.5, text="Key Players<br>(High Power, High Interest)", showarrow=False, bgcolor="lightgreen", opacity=0.7)
    fig.add_annotation(x=1.5, y=1.5, text="Monitor<br>(Low Power, Low Interest)", showarrow=False, bgcolor="lightgray", opacity=0.7)
    fig.add_annotation(x=2.75, y=1.5, text="Keep Satisfied<br>(High Power, Low Interest)", showarrow=False, bgcolor="lightcoral", opacity=0.7)
    
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed stakeholder breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Key Players (Manage Closely)")
        key_players = df_stake[(df_stake['Power_Numeric'] >= 2) & (df_stake['Interest_Numeric'] >= 3)]
        if len(key_players) > 0:
            for _, row in key_players.iterrows():
                with st.expander(f"**{row['Name']}** {get_rag_color(row['RAG_Status'])}"):
                    st.markdown(f"**Primary Stakeholders:** {row['Primary_Stakeholders']}")
                    st.markdown(f"**Secondary Stakeholders:** {row['Secondary_Stakeholders']}")
                    st.markdown(f"**Fairer Westminster:** {row['Fairer_Westminster_Alignment']}")
                    st.markdown(f"**Strategy:** Engage closely, involve in decisions, satisfy needs")
        else:
            st.info("No bodies in this quadrant")
    
    with col2:
        st.subheader("📢 Keep Informed")
        keep_informed = df_stake[(df_stake['Power_Numeric'] < 2) & (df_stake['Interest_Numeric'] >= 3)]
        if len(keep_informed) > 0:
            for _, row in keep_informed.iterrows():
                with st.expander(f"**{row['Name']}** {get_rag_color(row['RAG_Status'])}"):
                    st.markdown(f"**Primary Stakeholders:** {row['Primary_Stakeholders']}")
                    st.markdown(f"**Fairer Westminster:** {row['Fairer_Westminster_Alignment']}")
                    st.markdown(f"**Strategy:** Regular communication, leverage enthusiasm, but don't overload")
        else:
            st.info("No bodies in this quadrant")
    
    st.markdown("---")
    
    # Stakeholder engagement effort
    st.subheader("📈 Stakeholder Engagement Effort Distribution")
    
    fig = px.sunburst(
        df,
        path=['Level', 'Name'],
        values='Value_Added',
        color='Stakeholder_Interest',
        title='Governance Structure by Level (sized by value, coloured by stakeholder interest)',
        color_discrete_map={'Low': '#90EE90', 'Medium': '#FFD700', 'High': '#FF8C00', 'Very High': '#DC143C'}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# VALUE CHAIN MAPPING (keeping all original content)
elif page == "⛓️ Value Chain Mapping":
    st.title("⛓️ Value Chain Mapping (Porter Framework)")
    st.markdown("*Private sector framework adapted for public sector use*")
    
    st.warning("""
    **⚠️ Public Sector Adaptation Note:**
    
    Porter's Value Chain was designed for profit-seeking firms to analyse competitive advantage. 
    For Westminster City Council, we adapt it to analyse **service delivery effectiveness**:
    
    - **Not about:** Profit margins, competitive advantage, market share
    - **Focus on:** Service outcomes, resident value, efficiency, statutory duties
    - **"Primary Activities"** = Core governance functions (decision-making, monitoring, approvals)
    - **"Support Activities"** = Enabling functions (admin, legal, data/analysis, communications)
    
    This helps identify governance that creates **public value** vs **overhead**.
    """)
    
    df = st.session_state.bodies_df
    
    # Value chain visualisation
    st.subheader("📊 Governance Value Chain Activities")
    
    # Parse value chain activities
    all_activities = []
    for _, row in df.iterrows():
        activities = [a.strip() for a in row['Value_Chain_Activities'].split(',')]
        for activity in activities:
            all_activities.append({
                'Body': row['Name'],
                'Activity': activity,
                'Level': row['Level'],
                'Efficiency': row['Efficiency_Score'],
                'Value': row['Value_Added'],
                'RAG_Status': row['RAG_Status']
            })
    
    df_activities = pd.DataFrame(all_activities)
    
    # Activity frequency
    activity_counts = df_activities['Activity'].value_counts().reset_index()
    activity_counts.columns = ['Activity', 'Count']
    
    fig = px.bar(
        activity_counts.head(10),
        x='Count',
        y='Activity',
        orientation='h',
        title='Most Common Governance Activities Across Bodies',
        labels={'Count': 'Number of Bodies', 'Activity': 'Value Chain Activity'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Activity efficiency analysis
    st.subheader("⚡ Activity Efficiency Analysis")
    
    activity_efficiency = df_activities.groupby('Activity').agg({
        'Efficiency': 'mean',
        'Value': 'mean',
        'Body': 'count'
    }).reset_index()
    activity_efficiency.columns = ['Activity', 'Avg_Efficiency', 'Avg_Value', 'Body_Count']
    
    fig = px.scatter(
        activity_efficiency,
        x='Avg_Efficiency',
        y='Avg_Value',
        size='Body_Count',
        hover_name='Activity',
        title='Activity Efficiency vs Value Created',
        labels={'Avg_Efficiency': 'Average Efficiency', 'Avg_Value': 'Average Value Added'}
    )
    fig.add_hline(y=3.5, line_dash="dash", line_color="green", annotation_text="High value threshold")
    fig.add_vline(x=3, line_dash="dash", line_color="green", annotation_text="High efficiency threshold")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🟢 High Value-Adding Activities")
        high_value = activity_efficiency[activity_efficiency['Avg_Value'] >= 4].sort_values('Avg_Value', ascending=False)
        if len(high_value) > 0:
            for _, row in high_value.iterrows():
                st.success(f"**{row['Activity']}** - {row['Body_Count']} bodies, {row['Avg_Value']:.1f} avg value")
        else:
            st.info("No activities scored >4 on average value")
    
    with col2:
        st.markdown("### 🔴 Low Efficiency Activities")
        low_eff = activity_efficiency[activity_efficiency['Avg_Efficiency'] < 3].sort_values('Avg_Efficiency')
        if len(low_eff) > 0:
            for _, row in low_eff.iterrows():
                st.warning(f"**{row['Activity']}** - {row['Body_Count']} bodies, {row['Avg_Efficiency']:.1f} avg efficiency")
            st.markdown("**💡 Recommendation:** Standardise and document these processes to improve efficiency")
        else:
            st.success("All activities have adequate efficiency")
    
    st.markdown("---")
    
    # Value chain by level
    st.subheader("🏢 Value Chain Activities by Organisational Level")
    
    fig = px.treemap(
        df_activities,
        path=['Level', 'Body', 'Activity'],
        title='Governance Activities Hierarchy',
        color='Efficiency',
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

# FIVE FORCES ANALYSIS (keeping all original content)
elif page == "⚡ Five Forces Analysis":
    st.title("⚡ Five Forces Analysis (Porter Framework)")
    st.markdown("*Private sector framework reinterpreted for public sector*")
    
    st.warning("""
    **⚠️ Public Sector Adaptation Note:**
    
    Porter's Five Forces was designed to analyse competitive market dynamics for profit-seeking firms. 
    For Westminster City Council, we **reinterpret** it to analyse **governance pressures**:
    
    **Original Private Sector Focus:**
    - Market competition, profit maximisation, barriers to entry, supplier/buyer bargaining
    
    **Adapted Public Sector Focus:**
    - Stakeholder demands, accountability pressures, alternative service models, resource constraints
    
    This framework is **less naturally suited** to public sector than Schilling's stakeholder analysis, 
    but can provide useful insights when properly adapted.
    """)
    
    five_forces = st.session_state.five_forces
    
    # Radar chart
    st.subheader("📊 Five Forces Radar Analysis")
    
    forces_list = list(five_forces.keys())
    values = list(five_forces.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=forces_list,
        fill='toself',
        name='Current State',
        line_color='rgb(99, 110, 250)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=True,
        title="Five Forces Intensity (1=Low, 5=High)",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Force-by-force analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Force Analysis")
        
        st.markdown("### 1️⃣ Threat of New Entrants")
        st.progress(five_forces['Threat of New Entrants'] / 5)
        st.markdown(f"**Intensity:** {five_forces['Threat of New Entrants']}/5 (Medium)")
        st.markdown("""
        **Definition (Adapted):** Risk of new governance bodies being created, fragmenting decision-making.
        
        **Westminster Context:**
        - Political pressure creates new boards/forums
        - Regulatory requirements mandate new bodies
        - Crisis responses spawn temporary structures that persist
        
        **Impact:** Medium - Some proliferation but Cabinet control constrains
        """)
        
        st.markdown("### 2️⃣ Bargaining Power of Stakeholders")
        st.progress(five_forces['Bargaining Power of Stakeholders'] / 5)
        st.markdown(f"**Intensity:** {five_forces['Bargaining Power of Stakeholders']}/5 (High)")
        st.markdown("""
        **Definition (Adapted):** Influence of key stakeholders (residents, partners, government) over governance.
        
        **Westminster Context:**
        - Strong community voice (Church Street, Lisson Grove)
        - NHS partnership power (Joint Health Board)
        - Central government mandates and inspections
        
        **Impact:** High - Stakeholders significantly shape governance structure
        
        **Note:** This overlaps with Schilling's stakeholder analysis, which is more sophisticated for public sector use.
        """)
        
        st.markdown("### 3️⃣ Threat of Alternative Models")
        st.progress(five_forces['Threat of Alternative Models'] / 5)
        st.markdown(f"**Intensity:** {five_forces['Threat of Alternative Models']}/5 (Low)")
        st.markdown("""
        **Definition (Adapted):** Risk that alternative governance approaches (self-regulation, informal networks) replace formal bodies.
        
        **Westminster Context:**
        - Digital platforms enable direct democracy
        - Community organising bypasses formal structures  
        - Agile/flat structures in private sector offer contrast
        
        **Impact:** Low - Statutory requirements maintain formal governance
        """)
    
    with col2:
        st.markdown("### 4️⃣ Pressure for Accountability")
        st.progress(five_forces['Pressure for Accountability'] / 5)
        st.markdown(f"**Intensity:** {five_forces['Pressure for Accountability']}/5 (Very High)")
        st.markdown("""
        **Definition (Adapted):** Demand from citizens, media, regulators for transparent, effective governance.
        
        **Westminster Context:**
        - Intense media scrutiny in capital city
        - High resident expectations
        - Government inspections and audits
        - Fairer Westminster outcome commitments
        
        **Impact:** Very High - Drives formalisation and overhead
        """)
        
        st.markdown("### 5️⃣ Resource Competition")
        st.progress(five_forces['Resource Competition'] / 5)
        st.markdown(f"**Intensity:** {five_forces['Resource Competition']}/5 (High)")
        st.markdown("""
        **Definition (Adapted):** Competition between governance bodies for budget, senior time, and influence.
        
        **Westminster Context:**
        - Cost-cutting pressures intensify competition
        - Senior officer time scarce resource
        - Political capital limited
        - Commercial vs Digital vs Climate boards compete
        
        **Impact:** High - Creates incentive for duplication and empire-building
        """)
    
    st.markdown("---")
    
    # Strategic implications
    st.subheader("💡 Strategic Implications")
    
    st.markdown("""
    ### Overall Assessment
    
    **Strongest Forces:**
    1. **Pressure for Accountability** (5/5) - Drives formalisation, creates overhead
    2. **Bargaining Power of Stakeholders** (4/5) - Shapes structure, resists change
    3. **Resource Competition** (4/5) - Incentivises duplication
    
    **Weaker Forces:**
    - **Threat of Alternative Models** (2/5) - Statutory requirements protect formal governance
    - **Threat of New Entrants** (3/5) - Cabinet control limits proliferation
    
    ### Strategic Responses
    
    **To Counter High Accountability Pressure:**
    - Streamline reporting without reducing transparency
    - Digital dashboards reduce manual reporting burden
    - Focus on outcome metrics vs process compliance
    
    **To Manage Stakeholder Power:**
    - Early engagement prevents later resistance
    - Co-design governance changes with key stakeholders
    - Use Rogers categories to sequence engagement
    
    **To Reduce Resource Competition:**
    - **Consolidate duplicative bodies** (Commercial Gateway + Procuring)
    - Clear mandate boundaries reduce turf battles
    - Shared services reduce overhead
    
    **Estimated Impact:** £120K+ annual savings through strategic responses
    """)

# NETWORK VIEW (keeping all original content)
elif page == "🌐 Network View":
    st.title("🌐 Governance Network Visualisation")
    
    st.markdown("""
    Network analysis reveals relationships, clustering, and information flow between governance bodies.
    This approach is **well-suited to public sector** where multiple bodies interact through shared stakeholders and overlapping remits.
    """)
    
    df = st.session_state.bodies_df
    
    # Create network graph
    st.subheader("📊 Governance Network Map")
    
    # Build network data
    G = nx.Graph()
    
    # Add nodes
    for _, row in df.iterrows():
        G.add_node(
            row['Name'],
            level=row['Level'],
            efficiency=row['Efficiency_Score'],
            value=row['Value_Added'],
            type=row['Type'],
            rag=row['RAG_Status']
        )
    
    # Add edges based on similar activities or stakeholder overlap
    for i, row1 in df.iterrows():
        for j, row2 in df.iterrows():
            if i < j:  # Avoid duplicates
                # Check for stakeholder overlap
                stake1 = set(row1['Primary_Stakeholders'].split(', '))
                stake2 = set(row2['Primary_Stakeholders'].split(', '))
                overlap = len(stake1.intersection(stake2))
                
                if overlap > 0:
                    G.add_edge(row1['Name'], row2['Name'], weight=overlap)
    
    # Calculate layout
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    edge_weights = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_weights.append(edge[2].get('weight', 1))
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Create node trace with RAG colouring
    node_x = []
    node_y = []
    node_text = []
    node_size = []
    node_color = []
    
    rag_color_map = {'Green': '#90EE90', 'Amber': '#FFD700', 'Red': '#DC143C'}
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        node_data = G.nodes[node]
        node_text.append(f"{node}<br>RAG: {node_data['rag']}<br>Efficiency: {node_data['efficiency']}/5<br>Value: {node_data['value']}/5")
        node_size.append(node_data['value'] * 10)
        node_color.append(rag_color_map.get(node_data['rag'], '#888'))
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[G.nodes[node]['type'][:10] for node in G.nodes()],
        textposition='top center',
        hovertext=node_text,
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color='white')
        )
    )
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Governance Network (connections = shared stakeholders, size = value, colour = RAG status)',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        height=600
                    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Network metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Network Density", f"{nx.density(G):.2f}")
        st.caption("Proportion of possible connections that exist (0-1)")
    
    with col2:
        st.metric("Average Connections", f"{sum(dict(G.degree()).values()) / len(G.nodes()):.1f}")
        st.caption("Average number of stakeholder overlaps per body")
    
    with col3:
        components = list(nx.connected_components(G))
        st.metric("Connected Groups", len(components))
        st.caption("Number of separate governance clusters")
    
    # Centrality analysis
    st.subheader("🎯 Centrality Analysis")
    
    centrality = nx.degree_centrality(G)
    centrality_df = pd.DataFrame(list(centrality.items()), columns=['Body', 'Centrality'])
    centrality_df = centrality_df.sort_values('Centrality', ascending=False)
    
    fig = px.bar(
        centrality_df.head(5),
        x='Centrality',
        y='Body',
        orientation='h',
        title='Most Connected Governance Bodies (by stakeholder overlap)',
        labels={'Centrality': 'Centrality Score', 'Body': 'Governance Body'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Interpretation:**
    - **High centrality** bodies are critical coordination points
    - These bodies have most stakeholder overlap with others
    - Information flows through these bodies
    - Changes to high-centrality bodies have network-wide effects
    """)

# FAIRER WESTMINSTER DASHBOARD
elif page == "🎯 Fairer Westminster Dashboard":
    st.title("🎯 Fairer Westminster Alignment Dashboard")
    
    st.markdown("""
    This dashboard shows how governance bodies align with Westminster's five key principles for building a fairer city.
    """)
    
    df = st.session_state.bodies_df
    
    # Principle alignment overview
    st.subheader("📊 Alignment with Fairer Westminster Principles")
    
    # Count bodies aligned with each principle
    principle_counts = {}
    for principle in FAIRER_WESTMINSTER_PRINCIPLES.keys():
        count = len(df[df['Fairer_Westminster_Alignment'].str.contains(principle, na=False)])
        principle_counts[principle] = count
    
    principle_df = pd.DataFrame(list(principle_counts.items()), columns=['Principle', 'Bodies Aligned'])
    
    fig = px.bar(
        principle_df,
        x='Bodies Aligned',
        y='Principle',
        orientation='h',
        title='Number of Governance Bodies Aligned with Each Fairer Westminster Principle',
        color='Bodies Aligned',
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed principle analysis
    st.subheader("🔍 Detailed Principle Analysis")
    
    for principle, description in FAIRER_WESTMINSTER_PRINCIPLES.items():
        with st.expander(f"**{principle}** - {description}"):
            aligned_bodies = df[df['Fairer_Westminster_Alignment'].str.contains(principle, na=False)]
            
            if len(aligned_bodies) > 0:
                st.markdown(f"**{len(aligned_bodies)} governance bodies aligned with this principle:**")
                
                for _, row in aligned_bodies.iterrows():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"{get_rag_color(row['RAG_Status'])} **{row['Name']}**")
                    with col2:
                        st.markdown(f"Efficiency: {row['Efficiency_Score']}/5")
                    with col3:
                        st.markdown(f"Value: {row['Value_Added']}/5")
                
                # Average metrics for this principle
                avg_eff = aligned_bodies['Efficiency_Score'].mean()
                avg_val = aligned_bodies['Value_Added'].mean()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Efficiency", f"{avg_eff:.1f}/5")
                with col2:
                    st.metric("Average Value", f"{avg_val:.1f}/5")
                with col3:
                    green_count = len(aligned_bodies[aligned_bodies['RAG_Status'] == 'Green'])
                    st.metric("Green RAG Status", f"{green_count}/{len(aligned_bodies)}")
            else:
                st.info(f"No governance bodies currently aligned with {principle}")
    
    st.markdown("---")
    
    # Multi-principle alignment
    st.subheader("🌐 Multi-Principle Alignment Analysis")
    
    df['Principle_Count'] = df['Fairer_Westminster_Alignment'].apply(lambda x: len(x.split(', ')))
    
    fig = px.scatter(
        df,
        x='Efficiency_Score',
        y='Value_Added',
        size='Principle_Count',
        color='RAG_Status',
        hover_name='Name',
        hover_data=['Fairer_Westminster_Alignment'],
        title='Bodies by Efficiency & Value (size = number of Fairer Westminster principles aligned)',
        labels={'Efficiency_Score': 'Efficiency', 'Value_Added': 'Value Added'},
        color_discrete_map={'Green': '#90EE90', 'Amber': '#FFD700', 'Red': '#DC143C'}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("**Insight:** Larger bubbles indicate bodies aligned with multiple Fairer Westminster principles, suggesting broader strategic value.")

# EXPORT
elif page == "📥 Export":
    st.title("📥 Export Analysis & Findings")
    
    df = st.session_state.bodies_df
    
    # Download options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Data Export")
        
        csv = df.to_csv(index=False)
        st.download_button(
            "Download Governance Bodies (CSV)",
            data=csv,
            file_name=f"governance_bodies_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        json_data = df.to_json(orient='records', indent=2)
        st.download_button(
            "Download Governance Bodies (JSON)",
            data=json_data,
            file_name=f"governance_bodies_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col2:
        st.subheader("📊 Analysis Export")
        
        five_forces_json = json.dumps(st.session_state.five_forces, indent=2)
        st.download_button(
            "Download Five Forces Analysis (JSON)",
            data=five_forces_json,
            file_name=f"five_forces_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    st.markdown("---")
    
    # PDF Export
    st.subheader("📑 PDF Report Generation")
    
    st.markdown("""
    Generate a comprehensive PDF report including:
    - Executive summary with key metrics
    - Fairer Westminster alignment analysis
    - Detailed assessment of all governance bodies
    - Strategic recommendations based on RAG status
    - Financial impact estimates
    """)
    
    if st.button("🔄 Generate PDF Report", type="primary"):
        with st.spinner("Generating comprehensive PDF report..."):
            pdf_buffer = create_pdf_report()
            
            st.success("✅ PDF Report Generated Successfully!")
            
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_buffer,
                file_name=f"Westminster_Governance_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
    
    st.markdown("---")
    
    # Executive summary (keeping all original content)
    st.subheader("📋 Executive Summary of Findings")
    
    st.markdown(f"""
    ## Westminster City Council Governance Analysis
    ### Multi-Framework Assessment Aligned with Fairer Westminster Principles
    
    **Report Date:** {datetime.now().strftime('%d %B %Y')}
    
    ---
    
    ### Framework Applicability to Public Sector
    
    **✅ Highly Applicable:**
    - **Rogers (2003)**: Diffusion of Innovations - Excellent for public sector change management
    - **Schilling (2022)**: Stakeholder Analysis - Widely used in local government
    - **Smith (2024)**: Knowledge Management - Critical for council organisational learning
    
    **⚠️ Requires Adaptation:**
    - **Porter**: Value Chain - Originally for profit-seeking firms, adapted for service delivery
    - **Porter**: Five Forces - Originally for market competition, reinterpreted for governance pressures
    
    ---
    
    ### 1. Efficiency Analysis (Rogers, Schilling, Smith)
    
    **Overall Performance:**
    - Total Governance Bodies: {len(df)}
    - 🟢 Green RAG Status: {len(df[df['RAG_Status'] == 'Green'])}
    - 🟡 Amber RAG Status: {len(df[df['RAG_Status'] == 'Amber'])}
    - 🔴 Red RAG Status: {len(df[df['RAG_Status'] == 'Red'])}
    - Average Efficiency Score: {df['Efficiency_Score'].mean():.1f}/5
    - Average Value Added: {df['Value_Added'].mean():.1f}/5
    - High Duplication Risk Bodies: {len(df[df['Duplication_Risk'] >= 4])}
    - Bodies Recommended for Merge: {len(df[df['RAG_Recommendation'] == 'Merge'])}
    
    **Key Findings:**
    """)
    
    merge_bodies = df[df['RAG_Recommendation'] == 'Merge']
    if len(merge_bodies) > 0:
        st.markdown("**Merge Recommendations:**")
        for _, row in merge_bodies.iterrows():
            st.markdown(f"- **{row['Name']}** - Duplication Risk: {row['Duplication_Risk']}/5")
        st.markdown("""
        **Recommendation:** Consolidate into single Strategic Procurement Board
        - Estimated annual saving: £85,000
        - Improved decision speed
        - Clearer accountability
        """)
    
    st.markdown("""
    ---
    
    ### 2. Fairer Westminster Alignment
    
    **Bodies aligned with each principle:**
    """)
    
    for principle in FAIRER_WESTMINSTER_PRINCIPLES.keys():
        count = len(df[df['Fairer_Westminster_Alignment'].str.contains(principle, na=False)])
        st.markdown(f"- **{principle}**: {count} bodies")
    
    st.markdown("""
    ---
    
    ### Summary Recommendations
    
    #### Immediate Actions (0-3 months)
    1. **Consolidate procurement governance** - Merge duplicative procurement boards
       - Saving: £85K annually
       - Quick win with clear efficiency gain
    
    2. **Document tacit processes** - Procurement Gate Reports, Community Engagement protocols
       - Saving: £35K annually
       - Reduces dependency on key individuals
    
    #### Medium-term (3-12 months)
    3. **Strengthen place-based governance** - Formalise Church Street and Lisson Grove models
       - More authentic community voice (Strong Voice principle)
       - Clearer decision rights
       - Scalable to other areas
    
    4. **Streamline reporting** - Digital dashboards reduce manual burden
       - Responds to accountability pressure
       - Maintains transparency with less overhead
    
    #### Strategic (12+ months)
    5. **Review decision speeds** - Address slow decision-making bodies
       - Clarify approval thresholds
       - Delegate more operational decisions
       - Cabinet focuses on strategic priorities
    
    ---
    
    ### Financial Impact Summary
    
    **Total Estimated Annual Savings: £135,000+**
    
    Breakdown:
    - Commercial governance consolidation: £85,000
    - Process documentation efficiency gains: £35,000
    - Streamlined reporting: £15,000 (estimated)
    
    **Plus Non-Financial Benefits:**
    - Faster decision-making aligned with Opportunity principle
    - Clearer accountability supporting Strong Voice
    - Reduced confusion about remits
    - Better stakeholder engagement (Safe & Inclusive)
    - Preserved institutional knowledge (Quality of Life)
    - Enhanced climate action (Greener City)
    
    ---
    
    *This analysis demonstrates the application of multiple frameworks to local government governance, 
    with appropriate adaptation where frameworks originated in private sector contexts, and full alignment 
    with Westminster's commitment to building a fairer city.*
    """)

st.sidebar.markdown("---")
st.sidebar.caption("Governance Mapping Tool v4.0")
st.sidebar.caption("Westminster City Council Edition")
st.sidebar.caption("Aligned with Fairer Westminster Principles")
