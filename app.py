import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Fairer Westminster – Governance Mapping",
    page_icon="🏛️",
    layout="wide"
)

DATA_FILE = "governance_bodies.csv"

# --------------------------------------------------
# FAIRER WESTMINSTER PRINCIPLES
# --------------------------------------------------

FW_PRINCIPLES = [
    "FW_Fairer_Communities",
    "FW_Fairer_Housing",
    "FW_Fairer_Economy",
    "FW_Fairer_Environment",
    "FW_Fairer_Council"
]

FW_LABELS = {
    "FW_Fairer_Communities": "Fairer Communities",
    "FW_Fairer_Housing": "Fairer Housing",
    "FW_Fairer_Economy": "Fairer Economy",
    "FW_Fairer_Environment": "Fairer Environment",
    "FW_Fairer_Council": "Fairer Council"
}

# --------------------------------------------------
# DATA LOAD / SAVE
# --------------------------------------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        st.stop()
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# --------------------------------------------------
# SIDEBAR – ROLE
# --------------------------------------------------

st.sidebar.title("🏛️ Governance Mapping")
role = st.sidebar.radio("Role", ["Viewer", "Editor"])

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Overview",
        "🏛️ Governance Bodies",
        "📊 Fairer Westminster Analysis",
        "🔥 Risks & Insights",
        "✍️ Add / Edit Body",
        "📥 Export"
    ]
)

# --------------------------------------------------
# OVERVIEW (CABINET-STYLE)
# --------------------------------------------------

if page == "🏠 Overview":
    st.title("Fairer Westminster – Governance Overview")

    st.markdown("""
    **Purpose:**  
    To assess whether Westminster’s governance architecture is proportionate,
    efficient, and aligned to the Council’s *Fairer Westminster* priorities.
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("Bodies mapped", len(df))
    col2.metric(
        "Avg Fairer Council score",
        f"{df['FW_Fairer_Council'].mean():.1f} / 5"
    )
    col3.metric(
        "High duplication risks",
        len(df[df["Duplication_Risk"] >= 4])
    )

# --------------------------------------------------
# GOVERNANCE BODIES (READ-ONLY)
# --------------------------------------------------

elif page == "🏛️ Governance Bodies":
    st.title("Governance Bodies (Read-only)")
    st.dataframe(df, use_container_width=True)

# --------------------------------------------------
# FAIRER WESTMINSTER HEATMAPS
# --------------------------------------------------

elif page == "📊 Fairer Westminster Analysis":
    st.title("Fairer Westminster Alignment")

    fw_df = df[["Name"] + FW_PRINCIPLES].set_index("Name")
    fw_df = fw_df.rename(columns=FW_LABELS)

    fig = px.imshow(
        fw_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Fairer Westminster Alignment Heatmap (1–5)"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# RISKS & INSIGHTS (AUTO-GENERATED)
# --------------------------------------------------

elif page == "🔥 Risks & Insights":
    st.title("Key Governance Risks (Fairer Westminster lens)")

    for _, r in df.iterrows():
        if r["FW_Fairer_Council"] <= 2 and r["Duplication_Risk"] >= 4:
            st.error(
                f"⚠️ **{r['Name']}** poses a **high risk to Fairer Council** "
                "(low alignment + high duplication)."
            )
        elif r["FW_Fairer_Economy"] <= 2 and r["Cost_Impact"] in ["High", "Very High"]:
            st.warning(
                f"⚠️ **{r['Name']}** shows weak alignment with **Fairer Economy** "
                "despite high cost impact."
            )

# --------------------------------------------------
# ADD / EDIT BODY (EDITOR ONLY)
# --------------------------------------------------

elif page == "✍️ Add / Edit Body":

    if role != "Editor":
        st.warning("You are in Viewer mode. Editing is disabled.")
        st.stop()

    st.title("Add or Edit Governance Body")

    mode = st.radio("Mode", ["Add new body", "Edit existing body"])

    if mode == "Edit existing body":
        selected = st.selectbox("Select body", df["Name"].tolist())
        row = df[df["Name"] == selected].iloc[0]
    else:
        row = {}

    with st.form("body_form"):
        name = st.text_input("Name", row.get("Name", ""))
        body_type = st.selectbox("Type", ["Cabinet", "Board", "Place-Based Board"])
        level = st.selectbox("Level", ["Strategic", "Tactical", "Community"])
        efficiency = st.slider("Efficiency Score", 1, 5, int(row.get("Efficiency_Score", 3)))
        duplication = st.slider("Duplication Risk", 1, 5, int(row.get("Duplication_Risk", 1)))
        cost = st.selectbox("Cost Impact", ["Low", "Medium", "High", "Very High"])

        st.markdown("### Fairer Westminster Alignment (1–5)")
        fw_scores = {}
        for k in FW_PRINCIPLES:
            fw_scores[k] = st.slider(
                FW_LABELS[k], 1, 5, int(row.get(k, 3))
            )

        submitted = st.form_submit_button("Save")

        if submitted:
            new_row = {
                "Name": name,
                "Type": body_type,
                "Level": level,
                "Efficiency_Score": efficiency,
                "Duplication_Risk": duplication,
                "Cost_Impact": cost,
                **fw_scores
            }

            if mode == "Edit existing body":
                df = df[df["Name"] != selected]

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success("Saved successfully")

# --------------------------------------------------
# EXPORT
# --------------------------------------------------

elif page == "📥 Export":
    st.title("Export Data")

    st.download_button(
        "Download governance_bodies.csv",
        df.to_csv(index=False),
        "governance_bodies.csv",
        "text/csv"
    )

