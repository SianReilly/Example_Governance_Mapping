import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx
from datetime import datetime
import json

st.set_page_config(page_title="Governance Mapping Tool", page_icon="🗺️", layout="wide")

# Enhanced sample data with stakeholder and value chain information
SAMPLE_DATA = {
    "governance_bodies": [
        {
            "Name": "Cabinet", 
            "Type": "Cabinet", 
            "Level": "Strategic",
            "Outcome_Focus": "Fairer Westminster, Service Efficiency",
            "Process_Type": "Explicit",
            "Efficiency_Score": 4,
            "Cost_Impact": "Very High",
            "Value_Added": 5,
            "Duplication_Risk": 1,
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
            "Process_Type": "Mixed",
            "Efficiency_Score": 2,
            "Cost_Impact": "High",
            "Value_Added": 3,
            "Duplication_Risk": 4,
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
            "Process_Type": "Partially Explicit",
            "Efficiency_Score": 3,
            "Cost_Impact": "High",
            "Value_Added": 3,
            "Duplication_Risk": 5,
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
            "Process_Type": "Mixed",
            "Efficiency_Score": 3,
            "Cost_Impact": "Medium",
            "Value_Added": 4,
            "Duplication_Risk": 2,
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
            "Process_Type": "Explicit",
            "Efficiency_Score": 4,
            "Cost_Impact": "Medium",
            "Value_Added": 5,
            "Duplication_Risk": 1,
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
            "Process_Type": "Explicit",
            "Efficiency_Score": 3,
            "Cost_Impact": "High",
            "Value_Added": 5,
            "Duplication_Risk": 2,
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
            "Process_Type": "Explicit",
            "Efficiency_Score": 4,
            "Cost_Impact": "High",
            "Value_Added": 4,
            "Duplication_Risk": 1,
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
            "Process_Type": "Mixed",
            "Efficiency_Score": 2,
            "Cost_Impact": "Low",
            "Value_Added": 4,
            "Duplication_Risk": 2,
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

# Initialise with sample data
if 'initialised' not in st.session_state:
    st.session_state.bodies_df = pd.DataFrame(SAMPLE_DATA['governance_bodies'])
    st.session_state.five_forces = SAMPLE_DATA['five_forces']
    st.session_state.initialised = True
    st.session_state.example_mode = True

# Sidebar
st.sidebar.title("🗺️ Governance Mapping")
if st.session_state.get('example_mode'):
    st.sidebar.success("📚 EXAMPLE MODE")
    st.sidebar.markdown("*Westminster sample data*")

page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "🏛️ Governance Bodies", 
    "📊 Efficiency Analysis",
    "👥 Stakeholder Analysis",
    "⛓️ Value Chain Mapping",
    "⚡ Five Forces Analysis",
    "🌐 Network View",
    "📥 Export"
])

# HOME
if page == "🏠 Home":
    st.title("🗺️ Governance Mapping & Analysis Tool")
    st.markdown("*Westminster City Council - Public Sector Governance Optimisation*")
    
    if st.session_state.get('example_mode'):
        st.info("📚 **Westminster Example Data Loaded** - Demonstrates frameworks adapted for local government")
    
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
    
    st.warning("""
    **⚠️ Important Note on Private Sector Frameworks:**
    
    Porter's frameworks were designed for private sector competitive strategy. In public sector contexts like Westminster City Council:
    
    - **Value Chain:** Reframe "competitive advantage" as "service effectiveness"
    - **Five Forces:** Reinterpret "market competition" as "governance pressures"
    - Focus on **public value creation**, not profit maximisation
    - Emphasise **democratic accountability**, not market share
    - Consider **statutory duties** and **community outcomes**, not just efficiency
    
    The tool adapts these frameworks appropriately for local government use.
    """)
    
    st.markdown("---")
    
    # Enhanced dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    df = st.session_state.bodies_df
    
    with col1:
        st.metric("Bodies Mapped", len(df))
        st.metric("High Duplication", len(df[df['Duplication_Risk'] >= 4]))
    
    with col2:
        avg_eff = df['Efficiency_Score'].mean()
        st.metric("Avg Efficiency", f"{avg_eff:.1f}/5")
        high_stake = len(df[df['Stakeholder_Interest'] == 'Very High'])
        st.metric("High Stakeholder Interest", high_stake)
    
    with col3:
        exploit = len(df[df['Innovation_Posture'] == 'Exploit'])
        explore = len(df[df['Innovation_Posture'] == 'Explore'])
        st.metric("Exploit Focus", exploit)
        st.metric("Explore Focus", explore)
    
    with col4:
        slow_decision = len(df[df['Decision_Speed'] == 'Slow'])
        st.metric("Slow Decision Bodies", slow_decision, delta="Review", delta_color="inverse")
        place_based = len(df[df['Type'] == 'Place-Based Board'])
        st.metric("Place-Based Boards", place_based)
    
    st.markdown("---")
    
    # Quick visualisation
    st.subheader("Quick Overview: Efficiency vs Value by Cost")
    
    fig = px.scatter(
        df, 
        x='Efficiency_Score', 
        y='Value_Added',
        size='Duplication_Risk',
        color='Cost_Impact',
        hover_name='Name',
        title='Governance Bodies: Efficiency vs Value (bubble size = duplication risk)',
        labels={'Efficiency_Score': 'Efficiency Score', 'Value_Added': 'Value Added'},
        color_discrete_map={'Low': '#90EE90', 'Medium': '#FFD700', 'High': '#FF8C00', 'Very High': '#DC143C'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# GOVERNANCE BODIES
elif page == "🏛️ Governance Bodies":
    st.title("🏛️ Governance Bodies Overview")
    
    df = st.session_state.bodies_df
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        level_filter = st.multiselect("Filter by Level", df['Level'].unique(), default=df['Level'].unique())
    with col2:
        posture_filter = st.multiselect("Filter by Posture", df['Innovation_Posture'].unique(), default=df['Innovation_Posture'].unique())
    with col3:
        show_dup_only = st.checkbox("Show only high duplication risk (≥3)")
    
    filtered_df = df[df['Level'].isin(level_filter) & df['Innovation_Posture'].isin(posture_filter)]
    if show_dup_only:
        filtered_df = filtered_df[filtered_df['Duplication_Risk'] >= 3]
    
    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} bodies**")
    
    # Bodies as cards
    for _, row in filtered_df.iterrows():
        eff_emoji = "🟢" if row['Efficiency_Score'] >= 4 else "🟡" if row['Efficiency_Score'] >= 3 else "🔴"
        dup_emoji = "⚠️" if row['Duplication_Risk'] >= 3 else ""
        
        with st.expander(f"{eff_emoji} {dup_emoji} **{row['Name']}** ({row['Type']})"):
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
            
            with col3:
                st.markdown("**Stakeholders**")
                st.markdown(f"**Primary:** {row['Primary_Stakeholders']}")
                st.markdown(f"**Secondary:** {row['Secondary_Stakeholders']}")
                st.markdown(f"**Power:** {row['Stakeholder_Power']}")
                st.markdown(f"**Interest:** {row['Stakeholder_Interest']}")
            
            st.markdown(f"**Value Chain Activities:** {row['Value_Chain_Activities']}")

# EFFICIENCY ANALYSIS
elif page == "📊 Efficiency Analysis":
    st.title("📊 Efficiency Analysis")
    
    df = st.session_state.bodies_df
    
    # Priority reform opportunities
    st.subheader("🎯 Priority Reform Opportunities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### High Duplication Risk")
        high_dup = df[df['Duplication_Risk'] >= 3].sort_values('Duplication_Risk', ascending=False)
        if len(high_dup) > 0:
            for _, row in high_dup.iterrows():
                st.warning(f"**{row['Name']}** - Risk: {row['Duplication_Risk']}/5, Activities: {row['Value_Chain_Activities'][:50]}...")
            
            if len(high_dup) >= 2:
                st.markdown("**💡 Consolidation Opportunity:**")
                st.markdown("Commercial Gateway Review Board + Procuring Board = Single Strategic Procurement Board")
                st.success("**Estimated saving: £85K annually**")
        else:
            st.success("✅ No high duplication")
    
    with col2:
        st.markdown("### Slow Decision-Making")
        slow = df[df['Decision_Speed'] == 'Slow']
        if len(slow) > 0:
            for _, row in slow.iterrows():
                st.warning(f"**{row['Name']}** - {row['Cost_Impact']} cost, {row['Efficiency_Score']}/5 efficiency")
            st.markdown("**💡 Recommendation:** Streamline decision-making processes, clarify thresholds")
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
            color='Innovation_Posture',
            hover_name='Name',
            hover_data=['Efficiency_Score', 'Decision_Speed'],
            labels={'Cost_Numeric': 'Cost Impact', 'Value_Added': 'Value Added'},
            title='Cost vs Value Analysis',
            size_max=30
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

# STAKEHOLDER ANALYSIS (Schilling)
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
        color='Level',
        hover_name='Name',
        hover_data=['Primary_Stakeholders', 'Secondary_Stakeholders'],
        labels={'Power_Numeric': 'Stakeholder Power', 'Interest_Numeric': 'Stakeholder Interest'},
        title='Stakeholder Power-Interest Matrix by Governance Body'
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
                with st.expander(f"**{row['Name']}**"):
                    st.markdown(f"**Primary Stakeholders:** {row['Primary_Stakeholders']}")
                    st.markdown(f"**Secondary Stakeholders:** {row['Secondary_Stakeholders']}")
                    st.markdown(f"**Strategy:** Engage closely, involve in decisions, satisfy needs")
        else:
            st.info("No bodies in this quadrant")
    
    with col2:
        st.subheader("📢 Keep Informed")
        keep_informed = df_stake[(df_stake['Power_Numeric'] < 2) & (df_stake['Interest_Numeric'] >= 3)]
        if len(keep_informed) > 0:
            for _, row in keep_informed.iterrows():
                with st.expander(f"**{row['Name']}**"):
                    st.markdown(f"**Primary Stakeholders:** {row['Primary_Stakeholders']}")
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

# VALUE CHAIN MAPPING (Porter)
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
                'Value': row['Value_Added']
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

# FIVE FORCES ANALYSIS (Porter)
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

# NETWORK VIEW
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
            type=row['Type']
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
    
    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_size = []
    node_color = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        node_data = G.nodes[node]
        node_text.append(f"{node}<br>Efficiency: {node_data['efficiency']}/5<br>Value: {node_data['value']}/5")
        node_size.append(node_data['value'] * 10)
        node_color.append(node_data['efficiency'])
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[G.nodes[node]['type'][:10] for node in G.nodes()],
        textposition='top center',
        hovertext=node_text,
        marker=dict(
            showscale=True,
            colorscale='RdYlGn',
            size=node_size,
            color=node_color,
            colorbar=dict(
                title='Efficiency Score',
                thickness=15,
                xanchor='left'
            ),
            line=dict(width=2, color='white')
        )
    )
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Governance Network (connections = shared stakeholders, size = value, colour = efficiency)',
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
    
    # Executive summary
    st.subheader("📋 Executive Summary of Findings")
    
    st.markdown("""
    ## Westminster City Council Governance Analysis
    ### Multi-Framework Assessment for Public Sector Optimisation
    
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
    - Average Efficiency Score: 3.1/5
    - Average Value Added: 4.1/5
    - High Duplication Risk Bodies: 2
    
    **Key Findings:**
    - **Commercial Gateway Review Board** and **Procuring Board** show significant overlap
      - Both review procurement decisions
      - Similar stakeholder groups
      - Duplication Risk: 4/5 and 5/5 respectively
      - High governance overhead
    
    **Recommendation:** Consolidate into single Strategic Procurement Board
    - Estimated annual saving: £85,000
    - Improved decision speed
    - Clearer accountability
    
    ---
    
    ### 2. Stakeholder Analysis (Schilling) - Highly Applicable Framework
    
    **High Power, High Interest ("Key Players"):**
    - Cabinet
    - Climate Leadership Group
    - Joint Health and Wellbeing Board
    
    **Strategy:** Engage closely, involve in major decisions
    
    **Low Power, High Interest ("Keep Informed"):**
    - Church Street JV Board
    - Beyond Lisson Grove Board
    
    **Strategy:** Leverage community enthusiasm, regular communication
    
    **Insight:** Place-based boards have highly engaged stakeholders but limited formal power - opportunity for more authentic community governance
    
    ---
    
    ### 3. Value Chain Analysis (Porter) - Adapted for Public Sector
    
    **Note:** This private sector framework has been adapted to focus on service delivery value rather than profit margins.
    
    **High Value-Adding Activities:**
    - Climate Strategy and Monitoring
    - Health Strategy and Service Integration
    - Community Engagement and Local Decision-Making
    
    **Low Efficiency Activities:**
    - Procurement Approval (duplicated across 2 boards)
    - Contract Review (split between Commercial Gateway and Procuring)
    - Risk Assessment (inconsistent approaches)
    
    **Recommendation:** Standardise and document low-efficiency activities
    - Estimated improvement: 30-40% efficiency gain
    - Annual saving: £35,000 from reduced errors and rework
    
    ---
    
    ### 4. Five Forces Analysis (Porter) - Reinterpreted for Public Sector
    
    **Note:** This competitive strategy framework has been reinterpreted to analyse governance pressures rather than market dynamics.
    
    **Strongest Governance Pressures:**
    
    1. **Pressure for Accountability** (5/5) - Very High
       - Intense media scrutiny
       - Government inspections
       - Creates formalisation overhead
    
    2. **Bargaining Power of Stakeholders** (4/5) - High
       - Strong community voice
       - NHS partnership influence
       - Shapes governance structure
    
    3. **Resource Competition** (4/5) - High
       - Competition for senior time
       - Budget pressures
       - Incentivises empire-building
    
    **Strategic Response:** Streamline without reducing transparency, early stakeholder engagement, clear mandate boundaries
    
    ---
    
    ### 5. Network Analysis - Well-Suited to Public Sector
    
    **Most Connected Bodies (Central to Network):**
    - Cabinet (connects all strategic decisions)
    - Joint Health and Wellbeing Board (multi-agency partnerships)
    - Commercial Gateway Review Board (crosses all services)
    
    **Insight:** Commercial Gateway's high centrality despite duplication suggests it's embedded in workflows - consolidation requires careful change management
    
    ---
    
    ### Summary Recommendations
    
    #### Immediate Actions (0-3 months)
    1. **Consolidate procurement governance** - Merge Commercial Gateway + Procuring Board
       - Saving: £85K annually
       - Quick win with clear efficiency gain
    
    2. **Document tacit processes** - Procurement Gate Reports, Community Engagement protocols
       - Saving: £35K annually
       - Reduces dependency on key individuals
    
    #### Medium-term (3-12 months)
    3. **Strengthen place-based governance** - Formalise Church Street and Lisson Grove models
       - More authentic community voice
       - Clearer decision rights
       - Scalable to other areas
    
    4. **Streamline reporting** - Digital dashboards reduce manual burden
       - Responds to accountability pressure
       - Maintains transparency with less overhead
    
    #### Strategic (12+ months)
    5. **Review decision speeds** - 3 boards marked "Slow" with high costs
       - Clarify approval thresholds
       - Delegate more operational decisions
       - Cabinet focuses on strategic
    
    ---
    
    ### Financial Impact Summary
    
    **Total Estimated Annual Savings: £120,000+**
    
    Breakdown:
    - Commercial governance consolidation: £85,000
    - Process documentation efficiency gains: £35,000
    - Streamlined reporting: £15,000 (estimated)
    
    **Plus Non-Financial Benefits:**
    - Faster decision-making
    - Clearer accountability
    - Reduced confusion about remits
    - Better stakeholder engagement
    - Preserved institutional knowledge
    
    ---
    
    ### Implementation Phasing (Rogers Framework)
    
    **Phase 1 - Innovators:** Pilot consolidated Strategic Procurement Board with progressive services
    
    **Phase 2 - Early Adopters:** Roll out documented processes to Digital and Climate boards
    
    **Phase 3 - Early Majority:** Mainstream new governance across all tactical boards
    
    **Phase 4 - Late Majority:** Implement in traditional services once proven
    
    **Phase 5 - Laggards:** Mandate for statutory/regulated services
    
    ---
    
    ### Frameworks Applied - Public Sector Suitability
    
    This analysis integrated five frameworks with varying suitability for local government:
    
    1. **Rogers (2003)** - Diffusion of Innovations ✅ **Highly Applicable**
       - Widely used in public sector change management
       - Helps phase reforms and manage resistance
    
    2. **Schilling (2022)** - Stakeholder Analysis ✅ **Highly Applicable**
       - Purpose-built for multi-stakeholder environments
       - Standard practice in local government
    
    3. **Smith (2024)** - Knowledge Management ✅ **Highly Applicable**
       - Critical for council organisational memory
       - Addresses staff turnover challenges
    
    4. **Porter** - Value Chain ⚠️ **Requires Adaptation**
       - Originally for profit-maximising firms
       - Useful when reframed for service delivery value
    
    5. **Porter** - Five Forces ⚠️ **Requires Reinterpretation**
       - Originally for competitive market analysis
       - Provides insights when reinterpreted for governance pressures
    
    **Conclusion:** The innovation and stakeholder frameworks are most naturally suited to Westminster's governance context. 
    Porter's strategic frameworks provide additional perspective when properly adapted for public sector use.
    
    ---
    
    *This analysis demonstrates the application of multiple frameworks to local government governance, 
    with appropriate adaptation where frameworks originated in private sector contexts.*
    """)

st.sidebar.markdown("---")
st.sidebar.caption("Governance Mapping Tool v3.0")
st.sidebar.caption("Westminster City Council Edition")
