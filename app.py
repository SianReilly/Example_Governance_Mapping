import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Governance Mapping Tool",
    page_icon="🗺️",
    layout="wide"
)

# Initialize session state
if 'governance_bodies' not in st.session_state:
    st.session_state.governance_bodies = pd.DataFrame(columns=[
        'Name', 'Type', 'Level', 'Mandate', 'Outcome_Focus', 'Process_Type',
        'Lifecycle_Stage', 'Innovation_Posture', 'Rogers_Category',
        'Structure_Type', 'Decision_Rights', 'Inputs', 'Outputs',
        'Escalation_To', 'Escalation_From', 'Networks', 'Meeting_Cadence',
        'Efficiency_Score', 'Cost_Impact', 'Value_Added', 'Duplication_Risk'
    ])

if 'processes' not in st.session_state:
    st.session_state.processes = pd.DataFrame(columns=[
        'Process_Name', 'Process_Type', 'Purpose', 'Current_State',
        'Lifecycle_Stage', 'Governance_Touchpoints', 'Timeline_Position',
        'Rogers_Stage', 'Efficiency_Rating', 'Cost_Driver'
    ])

if 'diagnostic_notes' not in st.session_state:
    st.session_state.diagnostic_notes = {
        'commercial': '',
        'place_based_prevention': '',
        'data_gathering': '',
        'general_observations': ''
    }

# Sidebar navigation
st.sidebar.title("🗺️ Governance Mapping Tool")
st.sidebar.markdown("*Achieving Small, Effective Governance*")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["Home", "Governance Bodies", "Processes & Diagnostic", "Tacit vs Explicit Knowledge", 
     "Efficiency Analysis", "Visualisations", "Export Data"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Theoretical Framework")
st.sidebar.markdown("""
**Rogers (2003)**: Diffusion of Innovations
- Adopter categories guide governance phasing

**Schilling (2022)**: Innovation Management
- Lifecycle stages for process mapping
- Structural choices for governance design

**Smith (2024)**: Innovation Strategy
- Exploration vs exploitation balance
- Value creation through efficiency
""")

# Helper functions
def add_governance_body(data):
    """Add a new governance body to the dataframe"""
    new_row = pd.DataFrame([data])
    st.session_state.governance_bodies = pd.concat(
        [st.session_state.governance_bodies, new_row], 
        ignore_index=True
    )

def add_process(data):
    """Add a new process to the dataframe"""
    new_row = pd.DataFrame([data])
    st.session_state.processes = pd.concat(
        [st.session_state.processes, new_row], 
        ignore_index=True
    )

def calculate_governance_efficiency():
    """Calculate overall governance efficiency metrics"""
    if len(st.session_state.governance_bodies) == 0:
        return None
    
    df = st.session_state.governance_bodies
    return {
        'avg_efficiency': df['Efficiency_Score'].mean(),
        'high_cost_bodies': len(df[df['Cost_Impact'] == 'High']),
        'duplication_risk': len(df[df['Duplication_Risk'] >= 3]),
        'total_bodies': len(df)
    }

# HOME PAGE
if page == "Home":
    st.title("🗺️ Governance Mapping Tool")
    st.markdown("### Achieving Small, Effective Governance Through Strategic Analysis")
    
    st.markdown("""
    ---
    
    ## Purpose and Context
    
    This governance mapping tool supports organisations in achieving **small, effective governance** 
    by systematically analysing and optimising governance structures. In the current climate of 
    **cost-cutting pressures** and the **need for efficiency**, this tool helps identify:
    
    - **Duplication and overlap** in governance structures
    - **High-cost, low-value** boards and forums
    - **Gaps** in decision-making coverage
    - **Opportunities** for consolidation and streamlining
    
    ### Ongoing Process Diagnostic Context
    
    This tool complements your **process diagnostic work** currently underway with consultants. 
    As you gather data across:
    - Commercial processes
    - Place-based prevention initiatives  
    - Other operational areas
    
    This governance mapping will reveal how decision-making structures align (or fail to align) 
    with operational processes, enabling evidence-based recommendations for governance reform.
    
    ---
    
    ## Goal: Small, Effective Governance
    
    The primary objective is to move from complex, duplicative governance to **lean, effective** structures that:
    
    ✅ **Minimise overhead costs** - Fewer unnecessary meetings and boards  
    ✅ **Reduce bureaucracy** - Clearer decision rights and faster approvals  
    ✅ **Eliminate duplication** - Consolidate overlapping functions  
    ✅ **Enhance accountability** - Clear ownership and outcomes focus  
    ✅ **Improve efficiency** - Streamlined processes and governance touchpoints  
    
    ### Different Approaches to Achieving Effective Governance
    
    Organisations can achieve small, effective governance through different strategic approaches:
    
    **1. Consolidation Approach** (Centralised)
    - Merge multiple boards into fewer, more powerful bodies
    - Centralised decision-making with delegated operational authority
    - *Benefit*: Reduced overhead, faster strategic decisions
    - *Risk*: Distance from frontline, slower operational decisions
    
    **2. Distributed Approach** (Decentralised)
    - Push decisions closer to delivery, reduce central oversight
    - Outcome-focused governance with local autonomy
    - *Benefit*: Faster operational decisions, better local context
    - *Risk*: Coordination challenges, potential inconsistency
    
    **3. Hybrid Approach** (Strategic-Operational Split)
    - Small strategic layer for policy and resources
    - Distributed operational layer for delivery decisions
    - *Benefit*: Combines strategic coherence with operational flexibility
    - *Risk*: Requires clear mandate boundaries
    
    **4. Outcome-Based Approach** (Fairer Westminster Principles)
    - Organise governance around outcome themes (e.g., Fairer Westminster)
    - Cross-cutting boards focused on measurable results
    - *Benefit*: Clear accountability for outcomes, reduced silos
    - *Risk*: Matrix complexity, shared accountability challenges
    
    **5. Place-Based Approach** (Community & Geographic)
    - Governance organised by place (e.g., Church Street, Queen's Park)
    - Community-led boards with local decision-making
    - *Benefit*: Community engagement, context-appropriate decisions
    - *Risk*: Postcode lottery, scaling challenges
    
    This tool helps you analyse your current governance through these lenses and design 
    your optimal approach based on your organisational context and strategic priorities.
    
    ---
    
    ## Theoretical Foundations
    
    This tool integrates three complementary frameworks to support evidence-based governance design:
    
    ### Rogers' Diffusion of Innovation (2003)
    
    **Application to Governance**: Rogers' adopter categories help phase governance reforms:
    
    - **Innovators (2.5%)** - Pilot governance reforms in progressive areas first
    - **Early Adopters (13.5%)** - Demonstrate success before wider rollout
    - **Early Majority (34%)** - Roll out proven reforms to mainstream services
    - **Late Majority (34%)** - Address concerns and provide support for cautious adopters
    - **Laggards (16%)** - Mandate changes once established across organisation
    
    **Key Insight**: Governance change is an innovation adoption challenge. Understanding which 
    services/teams fall into which category enables strategic sequencing of reforms.
    
    ### Schilling's Strategic Innovation Management (2022)
    
    **Application to Governance**: Schilling's frameworks inform governance structure design:
    
    **Innovation Lifecycle Stages**:
    - Idea Generation → Selection → Development → Deployment → Learning
    - Map governance to lifecycle stages to ensure coverage without gaps or overlaps
    
    **Structural Choices**:
    - **Centralised vs Distributed**: Where should decisions be made?
    - **Formal vs Informal**: What level of structure is needed?
    - **Mechanistic vs Organic**: How adaptive should governance be?
    
    **Innovation Posture**:
    - **Exploit**: Efficiency-focused, incremental improvement (cost reduction)
    - **Explore**: Innovation-focused, radical change (transformation)
    - **Ambidextrous**: Balance both approaches
    
    **Key Insight**: Effective governance requires explicit structural choices aligned with 
    organisational strategy. Cost reduction demands exploitation-focused structures.
    
    ### Smith's Innovation Management Principles (2024)
    
    **Application to Governance**: Smith's concepts guide governance optimisation:
    
    **Exploration vs Exploitation Balance**:
    - Too much exploration (numerous experimental pilots) → High costs, no efficiency gains
    - Too much exploitation (rigid process compliance) → Inability to adapt and improve
    - Optimal balance → Disciplined exploitation with targeted exploration
    
    **Value Creation Through Efficiency**:
    - Innovation is not just "new things" but includes process improvement and cost reduction
    - Governance should enable efficient value delivery, not create bureaucratic overhead
    - Measure governance value through cost-benefit analysis
    
    **Knowledge Management** (Tacit vs Explicit):
    - Document processes to preserve institutional knowledge
    - Convert tacit knowledge (in people's heads) to explicit knowledge (documented)
    - Prevent knowledge loss when people leave, reduce dependency on individuals
    
    **Key Insight**: Governance structures should actively create value through efficiency 
    rather than simply controlling activity. Knowledge codification reduces governance burden.
    
    ---
    
    ## How This Tool Addresses Key Governance Challenges
    
    ### Challenge 1: Identifying Duplication and Overlap
    
    **Tool Response**: 
    - Map all boards/forums/networks with their mandates and decision rights
    - Identify overlapping remits and unclear boundaries
    - Flag high "Duplication Risk" bodies
    - Visualise governance landscape to reveal redundancy
    
    ### Challenge 2: Understanding True Costs
    
    **Tool Response**:
    - Capture meeting cadence, attendee seniority, and preparation requirements
    - Calculate governance overhead costs
    - Identify high-cost, low-value bodies for elimination
    - Compare cost against measurable value added
    
    ### Challenge 3: Process Diagnostic Integration
    
    **Tool Response**:
    - Map processes (commercial, place-based, etc.) to governance touchpoints
    - Identify processes with excessive governance burden
    - Reveal processes with insufficient governance
    - Document tacit vs explicit process knowledge
    
    ### Challenge 4: Outcome Focus
    
    **Tool Response**:
    - Categorise boards by outcome focus (Fairer Westminster principles)
    - Identify input-focused vs outcome-focused governance
    - Support redesign around outcomes rather than functions
    - Enable accountability for measurable results
    
    ### Challenge 5: Community and Geographic Governance
    
    **Tool Response**:
    - Distinguish place-based boards (Church Street, etc.) from functional boards
    - Analyse community-led vs corporate-led governance models
    - Balance local autonomy with strategic coherence
    - Support appropriate governance design for place-based initiatives
    
    ---
    
    ## Getting Started
    
    1. **Governance Bodies**: Document all boards, forums, networks, and committees
    2. **Processes & Diagnostic**: Map processes and capture diagnostic findings
    3. **Tacit vs Explicit**: Identify knowledge that needs codification
    4. **Efficiency Analysis**: Calculate costs, identify duplication, prioritise reforms
    5. **Visualisations**: Generate evidence for recommendations
    6. **Export**: Create governance reform proposals
    
    Use the navigation menu on the left to begin your governance mapping.
    """)
    
    # Quick stats
    st.markdown("---")
    st.subheader("📊 Current Mapping Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Governance Bodies Mapped", len(st.session_state.governance_bodies))
    with col2:
        st.metric("Processes Documented", len(st.session_state.processes))
    with col3:
        efficiency_data = calculate_governance_efficiency()
        if efficiency_data:
            st.metric("Average Efficiency Score", f"{efficiency_data['avg_efficiency']:.1f}/5")
        else:
            st.metric("Average Efficiency Score", "N/A")
    with col4:
        if efficiency_data and efficiency_data['duplication_risk'] > 0:
            st.metric("Duplication Risk Bodies", efficiency_data['duplication_risk'], 
                     delta="Review needed", delta_color="inverse")
        else:
            st.metric("Duplication Risk Bodies", "0")

# GOVERNANCE BODIES PAGE
elif page == "Governance Bodies":
    st.title("🏛️ Governance Bodies Mapping")
    st.markdown("Document boards, forums, networks, and committees with focus on efficiency and cost impact.")
    
    tab1, tab2 = st.tabs(["➕ Add New Body", "📋 View & Edit Bodies"])
    
    with tab1:
        st.subheader("Add a New Governance Body")
        st.markdown("*Focus on capturing information needed for efficiency analysis and duplication identification.*")
        
        with st.form("add_body_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Basic Information")
                name = st.text_input("Name*", help="e.g., Service Innovation Forum, Cabinet, Church Street Board")
                
                body_type = st.selectbox(
                    "Type*",
                    ["Board", "Cabinet", "Committee", "Forum", "Network", "Community Board", 
                     "Place-Based Board", "Programme Board", "Panel", "Working Group"]
                )
                
                level = st.selectbox(
                    "Organisational Level*",
                    ["Strategic (Cabinet/Corporate)", "Tactical (Service/Programme)", 
                     "Operational (Delivery/Project)", "Community (Place-Based)"]
                )
                
                mandate = st.text_area(
                    "Mandate and Purpose",
                    help="What is this body responsible for? Be specific about decision-making authority."
                )
                
                outcome_focus = st.multiselect(
                    "Outcome Focus (Fairer Westminster Principles)*",
                    ["Fairer Westminster (Reducing Inequality)", "Net Zero and Climate Resilience",
                     "Inclusive Economic Growth", "Housing Affordability and Quality", 
                     "Public Health and Wellbeing", "Community Safety", "Place-Based Outcomes",
                     "Service Efficiency and Cost Reduction", "Digital Transformation",
                     "Not Outcome-Focused (Input/Activity Focused)"],
                    help="Which outcomes does this body focus on achieving?"
                )
                
                process_type = st.selectbox(
                    "Dominant Process Type",
                    ["Explicit (Documented Processes)", "Tacit (Undocumented/Experience-Based)", 
                     "Mixed (Some Documented, Some Tacit)"],
                    help="Are the body's processes well-documented or do they rely on tacit knowledge?"
                )
            
            with col2:
                st.markdown("### Strategic Positioning")
                
                lifecycle_stage = st.multiselect(
                    "Innovation Lifecycle Coverage (Schilling)*",
                    ["Idea Generation", "Selection/Prioritisation", "Development", 
                     "Deployment/Implementation", "Post-Implementation Learning"],
                    help="Which stages of innovation does this body govern?"
                )
                
                innovation_posture = st.selectbox(
                    "Innovation Posture (Schilling)*",
                    ["Exploit (Efficiency/Cost Reduction)", "Explore (Transformation/Innovation)", 
                     "Ambidextrous (Both)"],
                    help="Is this body focused on efficiency or transformation?"
                )
                
                rogers_category = st.selectbox(
                    "Rogers Adopter Category Focus*",
                    ["Innovators", "Early Adopters", "Early Majority", "Late Majority", 
                     "Laggards", "Multiple Categories"],
                    help="Which adopter category does this body primarily serve?"
                )
                
                structure_type = st.text_input(
                    "Structure Characteristics (Schilling)",
                    help="e.g., Centralised/Distributed, Formal/Informal, Mechanistic/Organic",
                    value="Centralised, Formal"
                )
                
                decision_rights = st.text_area(
                    "Decision Rights*",
                    help="What can this body approve, recommend, or note? Be specific about thresholds."
                )
            
            st.markdown("---")
            st.markdown("### Governance Relationships")
            
            col3, col4, col5 = st.columns(3)
            
            with col3:
                inputs = st.text_input("Inputs", help="What information/requests does it receive?")
                outputs = st.text_input("Outputs", help="What decisions/artefacts does it produce?")
            
            with col4:
                escalation_to = st.text_input("Escalates To", help="Which bodies does it escalate to?")
                escalation_from = st.text_input("Receives From", help="Which bodies escalate to it?")
            
            with col5:
                networks = st.text_input("Networks", help="Which networks does it rely on?")
                meeting_cadence = st.text_input("Meeting Cadence", help="e.g., Weekly, Monthly, Quarterly")
            
            st.markdown("---")
            st.markdown("### Efficiency and Cost Analysis")
            st.markdown("*These ratings inform prioritisation of governance reform opportunities.*")
            
            col6, col7, col8, col9 = st.columns(4)
            
            with col6:
                efficiency_score = st.select_slider(
                    "Efficiency Score*",
                    options=[1, 2, 3, 4, 5],
                    value=3,
                    help="1=Highly inefficient, 5=Highly efficient"
                )
            
            with col7:
                cost_impact = st.selectbox(
                    "Cost Impact*",
                    ["Low", "Medium", "High", "Very High"],
                    help="Consider meeting frequency, attendee seniority, preparation time"
                )
            
            with col8:
                value_added = st.select_slider(
                    "Value Added*",
                    options=[1, 2, 3, 4, 5],
                    value=3,
                    help="1=Low value, 5=High value in terms of decisions/outcomes"
                )
            
            with col9:
                duplication_risk = st.select_slider(
                    "Duplication Risk*",
                    options=[1, 2, 3, 4, 5],
                    value=1,
                    help="1=Unique remit, 5=Significant overlap with other bodies"
                )
            
            submitted = st.form_submit_button("Add Governance Body")
            
            if submitted:
                if name and body_type and level and outcome_focus and lifecycle_stage and innovation_posture and rogers_category and decision_rights:
                    body_data = {
                        'Name': name,
                        'Type': body_type,
                        'Level': level,
                        'Mandate': mandate,
                        'Outcome_Focus': ', '.join(outcome_focus),
                        'Process_Type': process_type,
                        'Lifecycle_Stage': ', '.join(lifecycle_stage),
                        'Innovation_Posture': innovation_posture,
                        'Rogers_Category': rogers_category,
                        'Structure_Type': structure_type,
                        'Decision_Rights': decision_rights,
                        'Inputs': inputs,
                        'Outputs': outputs,
                        'Escalation_To': escalation_to,
                        'Escalation_From': escalation_from,
                        'Networks': networks,
                        'Meeting_Cadence': meeting_cadence,
                        'Efficiency_Score': efficiency_score,
                        'Cost_Impact': cost_impact,
                        'Value_Added': value_added,
                        'Duplication_Risk': duplication_risk
                    }
                    add_governance_body(body_data)
                    st.success(f"✅ Added '{name}' successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")
    
    with tab2:
        st.subheader("Mapped Governance Bodies")
        
        if len(st.session_state.governance_bodies) > 0:
            # Add filtering
            st.markdown("**Filter Bodies:**")
            filter_col1, filter_col2, filter_col3 = st.columns(3)
            
            with filter_col1:
                level_filter = st.multiselect("Level", 
                    st.session_state.governance_bodies['Level'].unique(), 
                    default=None)
            with filter_col2:
                posture_filter = st.multiselect("Innovation Posture",
                    st.session_state.governance_bodies['Innovation_Posture'].unique(),
                    default=None)
            with filter_col3:
                risk_filter = st.select_slider("Min Duplication Risk", 
                    options=[1,2,3,4,5], value=1)
            
            # Apply filters
            df_filtered = st.session_state.governance_bodies.copy()
            if level_filter:
                df_filtered = df_filtered[df_filtered['Level'].isin(level_filter)]
            if posture_filter:
                df_filtered = df_filtered[df_filtered['Innovation_Posture'].isin(posture_filter)]
            df_filtered = df_filtered[df_filtered['Duplication_Risk'] >= risk_filter]
            
            st.markdown(f"Showing {len(df_filtered)} of {len(st.session_state.governance_bodies)} bodies")
            
            # Display as expandable sections
            for idx, row in df_filtered.iterrows():
                # Create header with efficiency indicators
                efficiency_emoji = "🟢" if row['Efficiency_Score'] >= 4 else "🟡" if row['Efficiency_Score'] >= 3 else "🔴"
                duplication_emoji = "⚠️" if row['Duplication_Risk'] >= 3 else ""
                
                with st.expander(f"{efficiency_emoji} {duplication_emoji} **{row['Name']}** ({row['Type']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**Core Details**")
                        st.markdown(f"**Level:** {row['Level']}")
                        st.markdown(f"**Type:** {row['Type']}")
                        st.markdown(f"**Posture:** {row['Innovation_Posture']}")
                        st.markdown(f"**Rogers Focus:** {row['Rogers_Category']}")
                        st.markdown(f"**Meeting Cadence:** {row['Meeting_Cadence']}")
                        st.markdown(f"**Process Type:** {row['Process_Type']}")
                    
                    with col2:
                        st.markdown("**Mandate & Outcomes**")
                        st.markdown(f"**Mandate:** {row['Mandate']}")
                        st.markdown(f"**Outcome Focus:** {row['Outcome_Focus']}")
                        st.markdown(f"**Decision Rights:** {row['Decision_Rights']}")
                        st.markdown(f"**Lifecycle Coverage:** {row['Lifecycle_Stage']}")
                    
                    with col3:
                        st.markdown("**Efficiency Metrics**")
                        st.metric("Efficiency Score", f"{row['Efficiency_Score']}/5")
                        st.metric("Value Added", f"{row['Value_Added']}/5")
                        st.metric("Cost Impact", row['Cost_Impact'])
                        st.metric("Duplication Risk", f"{row['Duplication_Risk']}/5")
                    
                    if st.button(f"Delete", key=f"delete_{idx}"):
                        st.session_state.governance_bodies = st.session_state.governance_bodies.drop(idx).reset_index(drop=True)
                        st.rerun()
            
            st.markdown("---")
            st.dataframe(df_filtered, use_container_width=True)
        else:
            st.info("No governance bodies added yet. Use the 'Add New Body' tab to get started.")

# PROCESSES & DIAGNOSTIC PAGE  
elif page == "Processes & Diagnostic":
    st.title("⚙️ Processes & Diagnostic Findings")
    st.markdown("Map processes and capture insights from your ongoing diagnostic work.")
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Process", "📋 View Processes", "📝 Diagnostic Notes"])
    
    with tab1:
        st.subheader("Add a New Process")
        st.markdown("*Document processes identified in your diagnostic work with consultants.*")
        
        with st.form("add_process_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                process_name = st.text_input("Process Name*", help="e.g., Commercial Procurement, Place-Based Prevention Planning")
                
                process_type = st.selectbox(
                    "Process Knowledge Type*",
                    ["Explicit (Fully Documented)", "Partially Explicit (Some Documentation)", 
                     "Mainly Tacit (Minimal Documentation)", "Entirely Tacit (No Documentation)"],
                    help="How well is this process documented?"
                )
                
                purpose = st.text_area("Purpose*", help="What is this process meant to achieve?")
                
                current_state = st.selectbox(
                    "Current State*",
                    ["Efficient and Effective", "Effective but Inefficient", "Inefficient and Ineffective",
                     "Under Review (Diagnostic)", "Requires Redesign", "Unknown"],
                    help="Based on diagnostic findings, what is the current state?"
                )
            
            with col2:
                lifecycle_stage = st.multiselect(
                    "Lifecycle Stage (Schilling)*",
                    ["Idea Generation", "Selection/Prioritisation", "Development", 
                     "Deployment", "Post-Implementation Learning"]
                )
                
                body_names = st.session_state.governance_bodies['Name'].tolist() if len(st.session_state.governance_bodies) > 0 else []
                governance_touchpoints = st.multiselect(
                    "Governance Touchpoints",
                    body_names,
                    help="Which boards/forums govern this process?"
                )
                
                timeline_position = st.text_input(
                    "Timeline Position",
                    help="e.g., Q1, Continuous, Ad-hoc, Annual Budget Cycle"
                )
                
                rogers_stage = st.selectbox(
                    "Rogers Adopter Stage*",
                    ["Innovators", "Early Adopters", "Early Majority", "Late Majority", "Laggards"]
                )
                
                efficiency_rating = st.select_slider(
                    "Efficiency Rating*",
                    options=[1, 2, 3, 4, 5],
                    value=3,
                    help="1=Highly inefficient, 5=Highly efficient"
                )
                
                cost_driver = st.selectbox(
                    "Cost Driver Classification",
                    ["Low Cost", "Medium Cost", "High Cost", "Very High Cost", "Unknown"],
                    help="How much does this process cost to operate?"
                )
            
            submitted = st.form_submit_button("Add Process")
            
            if submitted:
                if process_name and process_type and purpose and current_state and lifecycle_stage and rogers_stage:
                    process_data = {
                        'Process_Name': process_name,
                        'Process_Type': process_type,
                        'Purpose': purpose,
                        'Current_State': current_state,
                        'Lifecycle_Stage': ', '.join(lifecycle_stage),
                        'Governance_Touchpoints': ', '.join(governance_touchpoints),
                        'Timeline_Position': timeline_position,
                        'Rogers_Stage': rogers_stage,
                        'Efficiency_Rating': efficiency_rating,
                        'Cost_Driver': cost_driver
                    }
                    add_process(process_data)
                    st.success(f"✅ Added '{process_name}' successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")
    
    with tab2:
        st.subheader("Documented Processes")
        
        if len(st.session_state.processes) > 0:
            # Summary metrics
            tacit_count = len(st.session_state.processes[st.session_state.processes['Process_Type'].str.contains('Tacit')])
            inefficient_count = len(st.session_state.processes[st.session_state.processes['Efficiency_Rating'] <= 2])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Processes", len(st.session_state.processes))
            with col2:
                st.metric("Tacit/Undocumented", tacit_count, 
                         help="Processes requiring documentation")
            with col3:
                st.metric("Inefficient (≤2/5)", inefficient_count,
                         help="Processes requiring redesign")
            
            st.markdown("---")
            
            for idx, row in st.session_state.processes.iterrows():
                efficiency_emoji = "🟢" if row['Efficiency_Rating'] >= 4 else "🟡" if row['Efficiency_Rating'] >= 3 else "🔴"
                tacit_emoji = "📋" if "Explicit" in row['Process_Type'] else "🤔"
                
                with st.expander(f"{efficiency_emoji} {tacit_emoji} **{row['Process_Name']}**"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Process Type:** {row['Process_Type']}")
                        st.markdown(f"**Purpose:** {row['Purpose']}")
                        st.markdown(f"**Current State:** {row['Current_State']}")
                        st.markdown(f"**Lifecycle Stage:** {row['Lifecycle_Stage']}")
                    
                    with col2:
                        st.markdown(f"**Rogers Stage:** {row['Rogers_Stage']}")
                        st.markdown(f"**Cost Driver:** {row['Cost_Driver']}")
                        st.markdown(f"**Timeline:** {row['Timeline_Position']}")
                        st.metric("Efficiency Rating", f"{row['Efficiency_Rating']}/5")
                    
                    st.markdown(f"**Governance Touchpoints:** {row['Governance_Touchpoints'] if row['Governance_Touchpoints'] else 'None mapped'}")
                    
                    if st.button(f"Delete", key=f"delete_process_{idx}"):
                        st.session_state.processes = st.session_state.processes.drop(idx).reset_index(drop=True)
                        st.rerun()
            
            st.markdown("---")
            st.dataframe(st.session_state.processes, use_container_width=True)
        else:
            st.info("No processes documented yet. Use the 'Add Process' tab to get started.")
    
    with tab3:
        st.subheader("Process Diagnostic Notes")
        st.markdown("""
        Use this space to capture findings from your ongoing diagnostic work with consultants. 
        Document insights on commercial processes, place-based prevention, and other areas as 
        data gathering progresses.
        """)
        
        st.markdown("### Commercial Processes")
        commercial_notes = st.text_area(
            "Findings on commercial processes",
            value=st.session_state.diagnostic_notes['commercial'],
            height=150,
            help="Document findings from consultant review of commercial processes"
        )
        st.session_state.diagnostic_notes['commercial'] = commercial_notes
        
        st.markdown("### Place-Based Prevention")
        prevention_notes = st.text_area(
            "Findings on place-based prevention initiatives",
            value=st.session_state.diagnostic_notes['place_based_prevention'],
            height=150,
            help="Document findings on place-based governance and prevention work"
        )
        st.session_state.diagnostic_notes['place_based_prevention'] = prevention_notes
        
        st.markdown("### Data Gathering Progress")
        data_notes = st.text_area(
            "Data gathering status and insights",
            value=st.session_state.diagnostic_notes['data_gathering'],
            height=150,
            help="Track data gathering progress across diagnostic workstreams"
        )
        st.session_state.diagnostic_notes['data_gathering'] = data_notes
        
        st.markdown("### General Observations")
        general_notes = st.text_area(
            "Other diagnostic observations",
            value=st.session_state.diagnostic_notes['general_observations'],
            height=150,
            help="Capture other insights from diagnostic work"
        )
        st.session_state.diagnostic_notes['general_observations'] = general_notes
        
        if st.button("💾 Save Diagnostic Notes"):
            st.success("✅ Diagnostic notes saved!")

# TACIT VS EXPLICIT PAGE
elif page == "Tacit vs Explicit Knowledge":
    st.title("📚 Tacit vs Explicit Knowledge Analysis")
    st.markdown("""
    Understanding which knowledge is tacit (in people's heads) versus explicit (documented) 
    is critical for governance efficiency and organisational resilience.
    """)
    
    st.markdown("---")
    
    # Theoretical explanation
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🤔 Tacit Knowledge")
        st.markdown("""
        **Definition**: Knowledge that lives in people's heads and practices. It is experiential, 
        context-dependent, and difficult to articulate or transfer.
        
        **Examples**:
        - Knowing exactly how to handle a difficult stakeholder
        - Reading subtle cues in committee dynamics
        - Understanding unwritten rules about what Cabinet will approve
        - Experience-based judgment on which governance route to take
        - Knowing who really makes decisions in your organisation
        
        **Characteristics**:
        - Hard to document
        - Learned through experience
        - Lost when people leave
        - Transferred through mentoring and observation
        - Often drives breakthrough thinking
        
        **Governance Implications**:
        - Creates dependency on key individuals
        - Makes processes fragile (knowledge walks out the door)
        - Can be source of innovation and nuanced decision-making
        - Difficult to audit or improve systematically
        """)
    
    with col2:
        st.markdown("### 📋 Explicit Knowledge")
        st.markdown("""
        **Definition**: Knowledge that has been codified, documented, and can be easily stored, 
        shared, and transmitted with minimal loss.
        
        **Examples**:
        - Documented decision-making processes
        - Terms of reference for boards
        - Meeting procedures and standing orders
        - Approval thresholds and delegations
        - Process flowcharts and playbooks
        
        **Characteristics**:
        - Can be written down
        - Easily shared and replicated
        - Preserved when people leave
        - Can be improved systematically
        - Enables consistency and compliance
        
        **Governance Implications**:
        - Reduces dependency on individuals
        - Makes processes resilient and scalable
        - Enables training and onboarding
        - Facilitates audit and improvement
        - Can become rigid if not regularly updated
        """)
    
    st.markdown("---")
    
    # Smith's framework
    st.subheader("Smith's Framework: Converting Tacit to Explicit Knowledge")
    st.markdown("""
    Smith (2024) identifies four types of knowledge conversion that organisations should actively manage:
    """)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        **1. Tacit to Tacit** (Socialisation)
        - One person shares experience directly with another
        - Example: Shadowing a senior officer in committee meetings
        - *Risk*: Knowledge remains undocumented
        
        **2. Tacit to Explicit** (Externalisation) ✅
        - Converting people's knowledge into documented artefacts
        - Example: Creating a "Committee Chair's Playbook" from experienced chairs
        - *Benefit*: Preserves knowledge, enables scaling
        """)
    
    with col4:
        st.markdown("""
        **3. Explicit to Explicit** (Combination)
        - Integrating multiple documents and systems
        - Example: Consolidating multiple governance guides into unified framework
        - *Benefit*: Creates coherent knowledge base
        
        **4. Explicit to Tacit** (Internalisation)
        - People absorb documented knowledge and apply with judgment
        - Example: Officer learns procedures then applies them intelligently
        - *Benefit*: Combines consistency with contextual adaptation
        """)
    
    st.markdown("""
    ### 🎯 Strategic Priority: Tacit to Explicit Conversion
    
    In the context of **cost-cutting and efficiency**, the most valuable knowledge conversion 
    is **Tacit to Explicit**. This:
    
    - Reduces dependency on expensive senior expertise
    - Enables faster onboarding and training
    - Prevents knowledge loss when people leave
    - Allows systematic process improvement
    - Reduces errors and rework
    - Supports automation and digitalisation
    
    However, not all tacit knowledge should be made explicit. Preserve tacit knowledge for:
    - Complex political judgment
    - Nuanced stakeholder management  
    - Innovation and creative problem-solving
    - Situations requiring deep context
    """)
    
    st.markdown("---")
    
    # Analysis of current state
    if len(st.session_state.governance_bodies) > 0 or len(st.session_state.processes) > 0:
        st.subheader("📊 Your Current Tacit vs Explicit Analysis")
        
        col5, col6 = st.columns(2)
        
        with col5:
            st.markdown("### Governance Bodies")
            if len(st.session_state.governance_bodies) > 0:
                body_process_counts = st.session_state.governance_bodies['Process_Type'].value_counts()
                
                fig_bodies = px.pie(
                    values=body_process_counts.values,
                    names=body_process_counts.index,
                    title="Governance Bodies by Process Type"
                )
                st.plotly_chart(fig_bodies, use_container_width=True)
                
                st.markdown("**Bodies requiring process documentation:**")
                tacit_bodies = st.session_state.governance_bodies[
                    st.session_state.governance_bodies['Process_Type'].str.contains('Tacit')
                ]
                if len(tacit_bodies) > 0:
                    for _, row in tacit_bodies.iterrows():
                        st.markdown(f"- **{row['Name']}** ({row['Process_Type']})")
                else:
                    st.success("All governance bodies have explicit processes documented!")
            else:
                st.info("Add governance bodies to analyse process documentation.")
        
        with col6:
            st.markdown("### Operational Processes")
            if len(st.session_state.processes) > 0:
                process_type_counts = st.session_state.processes['Process_Type'].value_counts()
                
                fig_processes = px.pie(
                    values=process_type_counts.values,
                    names=process_type_counts.index,
                    title="Processes by Documentation Level"
                )
                st.plotly_chart(fig_processes, use_container_width=True)
                
                st.markdown("**Processes requiring documentation:**")
                tacit_processes = st.session_state.processes[
                    st.session_state.processes['Process_Type'].str.contains('Tacit')
                ]
                if len(tacit_processes) > 0:
                    for _, row in tacit_processes.iterrows():
                        st.markdown(f"- **{row['Process_Name']}** ({row['Process_Type']})")
                else:
                    st.success("All processes have explicit documentation!")
            else:
                st.info("Add processes to analyse documentation coverage.")
        
        st.markdown("---")
        st.markdown("### 💡 Recommendations")
        
        if len(tacit_bodies) > 0 or (len(st.session_state.processes) > 0 and len(tacit_processes) > 0):
            st.warning("""
            **Priority Action**: Convert tacit knowledge to explicit documentation
            
            For each governance body or process identified above:
            1. Interview experienced practitioners to extract tacit knowledge
            2. Document current practices, decision criteria, and unwritten rules
            3. Create process maps, playbooks, or standard operating procedures
            4. Test documentation with less experienced staff
            5. Iterate based on feedback and edge cases
            
            **Expected Benefits**:
            - Reduced reliance on expensive senior staff for routine decisions
            - Faster onboarding of new staff (estimated 30-40% reduction in time to competency)
            - Prevention of knowledge loss when staff leave
            - Foundation for process improvement and efficiency gains
            - Enablement of automation and digitalisation
            """)
        else:
            st.success("""
            **Good practice**: Your documented governance and processes have explicit knowledge capture.
            
            Continue to:
            - Review and update documentation regularly
            - Capture new tacit insights as they emerge
            - Balance explicit processes with space for judgment
            - Ensure documentation is accessible and used
            """)

# EFFICIENCY ANALYSIS PAGE
elif page == "Efficiency Analysis":
    st.title("📈 Governance Efficiency Analysis")
    st.markdown("Identify opportunities for cost reduction and governance streamlining.")
    
    if len(st.session_state.governance_bodies) == 0:
        st.warning("⚠️ No governance bodies mapped yet. Add bodies in the 'Governance Bodies' page to see efficiency analysis.")
    else:
        df = st.session_state.governance_bodies.copy()
        
        # Overall metrics
        st.subheader("📊 Overall Governance Efficiency")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_efficiency = df['Efficiency_Score'].mean()
            st.metric("Average Efficiency", f"{avg_efficiency:.2f}/5")
        
        with col2:
            avg_value = df['Value_Added'].mean()
            st.metric("Average Value Added", f"{avg_value:.2f}/5")
        
        with col3:
            high_cost = len(df[df['Cost_Impact'].isin(['High', 'Very High'])])
            st.metric("High Cost Bodies", high_cost)
        
        with col4:
            high_dup = len(df[df['Duplication_Risk'] >= 3])
            st.metric("Duplication Risk Bodies", high_dup)
        
        st.markdown("---")
        
        # Priority reform opportunities
        st.subheader("🎯 Priority Reform Opportunities")
        
        # High cost, low value bodies
        st.markdown("### ❌ High Cost, Low Value Bodies")
        st.markdown("*These bodies are prime candidates for elimination or redesign.*")
        
        high_cost_low_value = df[
            (df['Cost_Impact'].isin(['High', 'Very High'])) & 
            (df['Value_Added'] <= 2)
        ]
        
        if len(high_cost_low_value) > 0:
            for _, row in high_cost_low_value.iterrows():
                with st.expander(f"🔴 {row['Name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Cost Impact:** {row['Cost_Impact']}")
                        st.markdown(f"**Value Added:** {row['Value_Added']}/5")
                        st.markdown(f"**Efficiency:** {row['Efficiency_Score']}/5")
                    with col2:
                        st.markdown(f"**Mandate:** {row['Mandate']}")
                        st.markdown(f"**Meeting Cadence:** {row['Meeting_Cadence']}")
                    
                    st.markdown("**💡 Recommendation:** Consider eliminating this body or consolidating its functions into existing structures.")
        else:
            st.success("✅ No high-cost, low-value bodies identified.")
        
        st.markdown("---")
        
        # High duplication risk
        st.markdown("### ⚠️ Bodies with High Duplication Risk")
        st.markdown("*These bodies may have overlapping remits with others.*")
        
        high_duplication = df[df['Duplication_Risk'] >= 3].sort_values('Duplication_Risk', ascending=False)
        
        if len(high_duplication) > 0:
            for _, row in high_duplication.iterrows():
                with st.expander(f"⚠️ {row['Name']} (Risk: {row['Duplication_Risk']}/5)"):
                    st.markdown(f"**Mandate:** {row['Mandate']}")
                    st.markdown(f"**Decision Rights:** {row['Decision_Rights']}")
                    st.markdown(f"**Outcome Focus:** {row['Outcome_Focus']}")
                    st.markdown(f"**Lifecycle Coverage:** {row['Lifecycle_Stage']}")
                    
                    st.markdown("**💡 Recommendation:** Review against other bodies with similar mandates. Consider merging or clarifying boundaries.")
        else:
            st.success("✅ No bodies with high duplication risk identified.")
        
        st.markdown("---")
        
        # Inefficient bodies
        st.markdown("### 🐌 Inefficient Bodies")
        st.markdown("*Bodies with low efficiency scores that could be improved through process redesign.*")
        
        inefficient = df[df['Efficiency_Score'] <= 2].sort_values('Efficiency_Score')
        
        if len(inefficient) > 0:
            for _, row in inefficient.iterrows():
                with st.expander(f"🟡 {row['Name']} (Efficiency: {row['Efficiency_Score']}/5)"):
                    st.markdown(f"**Level:** {row['Level']}")
                    st.markdown(f"**Process Type:** {row['Process_Type']}")
                    st.markdown(f"**Cost Impact:** {row['Cost_Impact']}")
                    
                    if 'Tacit' in row['Process_Type']:
                        st.markdown("**💡 Recommendation:** This body relies on tacit processes. Document procedures to improve efficiency and consistency.")
                    else:
                        st.markdown("**💡 Recommendation:** Review meeting structure, decision-making processes, and information flows for improvement opportunities.")
        else:
            st.success("✅ No significantly inefficient bodies identified.")
        
        st.markdown("---")
        
        # Visualisations
        st.subheader("📊 Efficiency Visualisations")
        
        tab1, tab2, tab3 = st.tabs(["Cost vs Value", "Duplication Matrix", "Efficiency Distribution"])
        
        with tab1:
            st.markdown("### Cost-Value Analysis")
            
            # Create cost-value scatter
            df_scatter = df.copy()
            df_scatter['Cost_Numeric'] = df_scatter['Cost_Impact'].map({
                'Low': 1, 'Medium': 2, 'High': 3, 'Very High': 4
            })
            
            fig_scatter = px.scatter(
                df_scatter,
                x='Cost_Numeric',
                y='Value_Added',
                size='Duplication_Risk',
                color='Innovation_Posture',
                hover_name='Name',
                labels={'Cost_Numeric': 'Cost Impact', 'Value_Added': 'Value Added'},
                title='Governance Bodies: Cost vs Value',
                size_max=20
            )
            
            # Add quadrant lines
            fig_scatter.add_hline(y=3, line_dash="dash", line_color="gray", opacity=0.5)
            fig_scatter.add_vline(x=2.5, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Add quadrant labels
            fig_scatter.add_annotation(x=1.5, y=4.5, text="Low Cost<br>High Value<br>✅ Keep", showarrow=False, bgcolor="lightgreen", opacity=0.7)
            fig_scatter.add_annotation(x=3.5, y=4.5, text="High Cost<br>High Value<br>⚠️ Optimise", showarrow=False, bgcolor="lightyellow", opacity=0.7)
            fig_scatter.add_annotation(x=1.5, y=1.5, text="Low Cost<br>Low Value<br>🤔 Review", showarrow=False, bgcolor="lightyellow", opacity=0.7)
            fig_scatter.add_annotation(x=3.5, y=1.5, text="High Cost<br>Low Value<br>❌ Eliminate", showarrow=False, bgcolor="lightcoral", opacity=0.7)
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            st.markdown("""
            **Interpretation:**
            - **Top-left quadrant**: Keep these - low cost, high value
            - **Top-right quadrant**: Optimise these - high value justifies cost, but look for efficiencies
            - **Bottom-left quadrant**: Review these - low cost but also low value
            - **Bottom-right quadrant**: Eliminate or redesign these - high cost, low value
            
            *Bubble size indicates duplication risk - larger bubbles have higher risk.*
            """)
        
        with tab2:
            st.markdown("### Duplication Risk Matrix")
            
            # Group by level and calculate average duplication
            dup_by_level = df.groupby(['Level', 'Innovation_Posture']).agg({
                'Duplication_Risk': 'mean',
                'Name': 'count'
            }).reset_index()
            dup_by_level.columns = ['Level', 'Innovation_Posture', 'Avg_Duplication', 'Count']
            
            fig_dup = px.scatter(
                dup_by_level,
                x='Level',
                y='Innovation_Posture',
                size='Avg_Duplication',
                color='Avg_Duplication',
                hover_data=['Count'],
                title='Duplication Risk by Level and Posture',
                color_continuous_scale='Reds',
                size_max=60
            )
            
            st.plotly_chart(fig_dup, use_container_width=True)
            
            st.markdown("""
            **Interpretation:**
            - Larger/redder bubbles indicate areas with higher duplication risk
            - Numbers show count of bodies in each category
            - Consider consolidation in high-duplication areas
            """)
        
        with tab3:
            st.markdown("### Efficiency Score Distribution")
            
            fig_dist = px.histogram(
                df,
                x='Efficiency_Score',
                nbins=5,
                title='Distribution of Efficiency Scores',
                labels={'Efficiency_Score': 'Efficiency Score', 'count': 'Number of Bodies'},
                color_discrete_sequence=['steelblue']
            )
            
            fig_dist.add_vline(x=3, line_dash="dash", line_color="red", 
                              annotation_text="Target: ≥3", annotation_position="top")
            
            st.plotly_chart(fig_dist, use_container_width=True)
            
            bodies_below_target = len(df[df['Efficiency_Score'] < 3])
            st.markdown(f"""
            **Summary:**
            - **{bodies_below_target}** bodies ({bodies_below_target/len(df)*100:.0f}%) are below target efficiency (score < 3)
            - Focus improvement efforts on these underperforming bodies
            - Target: Move all bodies to efficiency score ≥ 3
            """)

# VISUALISATIONS PAGE
elif page == "Visualisations":
    st.title("📈 Governance Landscape Visualisations")
    st.markdown("Strategic views of your governance structure for analysis and communication.")
    
    if len(st.session_state.governance_bodies) == 0:
        st.warning("⚠️ No governance bodies mapped yet. Add bodies to see visualisations.")
    else:
        df = st.session_state.governance_bodies.copy()
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "Outcome Focus Matrix",
            "Innovation Posture Landscape",
            "Rogers Adoption Readiness",
            "Process Documentation Status"
        ])
        
        with tab1:
            st.subheader("Governance by Outcome Focus (Fairer Westminster Principles)")
            st.markdown("Shows how governance is organised around strategic outcomes.")
            
            # Parse outcome focus
            outcome_lists = df['Outcome_Focus'].str.split(', ')
            outcome_data = []
            for idx, outcomes in enumerate(outcome_lists):
                for outcome in outcomes:
                    if outcome:
                        outcome_data.append({
                            'Outcome': outcome,
                            'Body': df.iloc[idx]['Name'],
                            'Level': df.iloc[idx]['Level'],
                            'Value': 1
                        })
            
            if outcome_data:
                outcome_df = pd.DataFrame(outcome_data)
                outcome_counts = outcome_df.groupby('Outcome').size().reset_index(name='Count')
                outcome_counts = outcome_counts.sort_values('Count', ascending=False)
                
                fig_outcomes = px.bar(
                    outcome_counts,
                    x='Outcome',
                    y='Count',
                    title='Governance Bodies by Outcome Focus',
                    labels={'Count': 'Number of Bodies', 'Outcome': 'Outcome Area'},
                    color='Count',
                    color_continuous_scale='Blues'
                )
                
                fig_outcomes.update_layout(xaxis_tickangle=-45, height=500)
                st.plotly_chart(fig_outcomes, use_container_width=True)
                
                # Show input-focused bodies
                input_focused = df[df['Outcome_Focus'].str.contains('Not Outcome-Focused')]
                if len(input_focused) > 0:
                    st.warning(f"""
                    **⚠️ {len(input_focused)} bodies are not outcome-focused:**
                    """)
                    for _, row in input_focused.iterrows():
                        st.markdown(f"- **{row['Name']}** ({row['Level']})")
                    st.markdown("""
                    **Recommendation:** Consider redesigning these bodies to focus on measurable outcomes 
                    rather than inputs or activities. This aligns with Fairer Westminster principles.
                    """)
                
                # List bodies by outcome
                st.markdown("---")
                st.markdown("### Bodies by Outcome Area")
                for outcome in outcome_counts['Outcome']:
                    with st.expander(f"**{outcome}** ({len(outcome_df[outcome_df['Outcome']==outcome])} bodies)"):
                        outcome_bodies = outcome_df[outcome_df['Outcome']==outcome]
                        for _, row in outcome_bodies.iterrows():
                            st.markdown(f"- {row['Body']} ({row['Level']})")
        
        with tab2:
            st.subheader("Innovation Posture Landscape")
            st.markdown("Balance of exploitation (efficiency) vs exploration (transformation).")
            
            posture_level = df.groupby(['Level', 'Innovation_Posture']).size().reset_index(name='Count')
            
            fig_posture = px.sunburst(
                posture_level,
                path=['Innovation_Posture', 'Level'],
                values='Count',
                title='Governance Structure: Innovation Posture by Level'
            )
            
            st.plotly_chart(fig_posture, use_container_width=True)
            
            # Calculate balance
            exploit_count = len(df[df['Innovation_Posture'].str.contains('Exploit')])
            explore_count = len(df[df['Innovation_Posture'].str.contains('Explore')])
            ambidextrous_count = len(df[df['Innovation_Posture'] == 'Ambidextrous (Both)'])
            
            st.markdown("### Innovation Posture Balance")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Exploit (Efficiency)", exploit_count)
            with col2:
                st.metric("Explore (Transformation)", explore_count)
            with col3:
                st.metric("Ambidextrous", ambidextrous_count)
            
            if exploit_count > explore_count * 3:
                st.success("""
                ✅ **Good balance for cost-reduction focus:** Your governance is appropriately 
                weighted towards exploitation (efficiency), which aligns with cost-cutting objectives.
                """)
            elif explore_count > exploit_count:
                st.warning("""
                ⚠️ **Imbalance:** Too much focus on exploration (transformation) relative to 
                exploitation (efficiency). Consider whether this aligns with cost-reduction goals.
                """)
            else:
                st.info("""
                ℹ️ **Balanced:** You have a reasonable balance between efficiency and transformation. 
                Ensure this aligns with current strategic priorities.
                """)
        
        with tab3:
            st.subheader("Rogers Adoption Readiness")
            st.markdown("Governance capacity across adopter categories for phased reforms.")
            
            rogers_counts = df['Rogers_Category'].value_counts().reset_index()
            rogers_counts.columns = ['Category', 'Count']
            
            # Order by Rogers sequence
            rogers_order = ['Innovators', 'Early Adopters', 'Early Majority', 'Late Majority', 'Laggards', 'Multiple Categories']
            rogers_counts['Category'] = pd.Categorical(rogers_counts['Category'], categories=rogers_order, ordered=True)
            rogers_counts = rogers_counts.sort_values('Category')
            
            fig_rogers = go.Figure()
            
            # Add curve background
            x_curve = list(range(0, 101))
            y_curve = [(1/(10*2.5066)) * 2.71828**(-0.5*((x-50)/10)**2) * 100 for x in x_curve]
            
            fig_rogers.add_trace(go.Scatter(
                x=x_curve,
                y=y_curve,
                fill='tozeroy',
                name='Diffusion Curve',
                line=dict(color='lightblue'),
                opacity=0.3
            ))
            
            # Add bars
            x_positions = [2.5, 16, 50, 84, 98]  # Approximate midpoints
            for i, cat in enumerate(rogers_order[:5]):
                count = rogers_counts[rogers_counts['Category']==cat]['Count'].values
                if len(count) > 0:
                    fig_rogers.add_trace(go.Bar(
                        x=[x_positions[i]],
                        y=[count[0] * 5],  # Scale for visibility
                        name=cat,
                        width=10
                    ))
            
            fig_rogers.update_layout(
                title='Governance Capacity Across Rogers Categories',
                xaxis_title='Adopter Categories',
                yaxis_title='Number of Bodies (scaled)',
                showlegend=True,
                height=500
            )
            
            st.plotly_chart(fig_rogers, use_container_width=True)
            
            st.markdown("### Implications for Governance Reform")
            innovators_count = len(df[df['Rogers_Category'] == 'Innovators'])
            early_adopters_count = len(df[df['Rogers_Category'] == 'Early Adopters'])
            
            if innovators_count > 0 or early_adopters_count > 0:
                st.success(f"""
                ✅ **Good foundation for reform:** You have {innovators_count + early_adopters_count} 
                bodies positioned as Innovators or Early Adopters. Start governance reforms here to 
                demonstrate success before wider rollout.
                """)
            else:
                st.warning("""
                ⚠️ **Reform challenge:** No bodies positioned as Innovators or Early Adopters. 
                You'll need to build early success stories to enable wider adoption of governance reforms.
                """)
        
        with tab4:
            st.subheader("Process Documentation Status")
            st.markdown("Tacit vs Explicit knowledge across governance structures.")
            
            process_counts = df['Process_Type'].value_counts().reset_index()
            process_counts.columns = ['Type', 'Count']
            
            fig_process = px.pie(
                process_counts,
                values='Count',
                names='Type',
                title='Governance Bodies by Process Documentation',
                color='Type',
                color_discrete_map={
                    'Explicit (Documented Processes)': 'lightgreen',
                    'Mixed (Some Documented, Some Tacit)': 'lightyellow',
                    'Tacit (Undocumented/Experience-Based)': 'lightcoral'
                }
            )
            
            st.plotly_chart(fig_process, use_container_width=True)
            
            # Show bodies needing documentation
            tacit_bodies = df[df['Process_Type'].str.contains('Tacit')]
            if len(tacit_bodies) > 0:
                st.warning(f"""
                **⚠️ {len(tacit_bodies)} bodies have undocumented processes:**
                """)
                for _, row in tacit_bodies.iterrows():
                    st.markdown(f"- **{row['Name']}** ({row['Process_Type']})")
                
                st.markdown("""
                **Priority Action:** Document these processes to:
                - Reduce dependency on key individuals
                - Enable faster onboarding
                - Support process improvement
                - Prevent knowledge loss
                - Reduce governance costs
                """)
            else:
                st.success("✅ All governance bodies have explicit process documentation!")

# EXPORT PAGE
elif page == "Export Data":
    st.title("📥 Export Your Governance Map")
    st.markdown("Download data for reporting, sharing, or further analysis.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Governance Bodies")
        if len(st.session_state.governance_bodies) > 0:
            st.metric("Total Bodies", len(st.session_state.governance_bodies))
            
            csv_bodies = st.session_state.governance_bodies.to_csv(index=False)
            st.download_button(
                label="📄 Download Governance Bodies (CSV)",
                data=csv_bodies,
                file_name=f"governance_bodies_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            json_bodies = st.session_state.governance_bodies.to_json(orient='records', indent=2)
            st.download_button(
                label="📋 Download Governance Bodies (JSON)",
                data=json_bodies,
                file_name=f"governance_bodies_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        else:
            st.info("No governance bodies to export.")
    
    with col2:
        st.subheader("Processes")
        if len(st.session_state.processes) > 0:
            st.metric("Total Processes", len(st.session_state.processes))
            
            csv_processes = st.session_state.processes.to_csv(index=False)
            st.download_button(
                label="📄 Download Processes (CSV)",
                data=csv_processes,
                file_name=f"processes_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            json_processes = st.session_state.processes.to_json(orient='records', indent=2)
            st.download_button(
                label="📋 Download Processes (JSON)",
                data=json_processes,
                file_name=f"processes_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        else:
            st.info("No processes to export.")
    
    st.markdown("---")
    st.subheader("Diagnostic Notes")
    if any(st.session_state.diagnostic_notes.values()):
        notes_text = f"""# Process Diagnostic Notes
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Commercial Processes
{st.session_state.diagnostic_notes['commercial']}

## Place-Based Prevention
{st.session_state.diagnostic_notes['place_based_prevention']}

## Data Gathering Progress
{st.session_state.diagnostic_notes['data_gathering']}

## General Observations
{st.session_state.diagnostic_notes['general_observations']}
"""
        st.download_button(
            label="📝 Download Diagnostic Notes (Markdown)",
            data=notes_text,
            file_name=f"diagnostic_notes_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
    else:
        st.info("No diagnostic notes to export.")
    
    st.markdown("---")
    st.subheader("Complete Governance Map Package")
    st.markdown("Download all data in a single file for comprehensive analysis.")
    
    complete_data = {
        'metadata': {
            'export_date': datetime.now().isoformat(),
            'tool_version': '2.0.0',
            'total_bodies': len(st.session_state.governance_bodies),
            'total_processes': len(st.session_state.processes)
        },
        'governance_bodies': st.session_state.governance_bodies.to_dict('records'),
        'processes': st.session_state.processes.to_dict('records'),
        'diagnostic_notes': st.session_state.diagnostic_notes,
        'efficiency_summary': calculate_governance_efficiency()
    }
    
    json_complete = json.dumps(complete_data, indent=2)
    st.download_button(
        label="📦 Download Complete Governance Map (JSON)",
        data=json_complete,
        file_name=f"governance_map_complete_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )
    
    st.markdown("---")
    st.subheader("Import Previous Work")
    st.markdown("Upload a previously exported JSON file to restore your governance map.")
    
    uploaded_file = st.file_uploader("Choose a JSON file", type=['json'])
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            
            if 'governance_bodies' in data:
                st.session_state.governance_bodies = pd.DataFrame(data['governance_bodies'])
            if 'processes' in data:
                st.session_state.processes = pd.DataFrame(data['processes'])
            if 'diagnostic_notes' in data:
                st.session_state.diagnostic_notes = data['diagnostic_notes']
            
            st.success("✅ Data imported successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error importing data: {str(e)}")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Governance Mapping Tool • v2.0.0")
st.sidebar.caption("For achieving small, effective governance")
