import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Marketing Campaign Lifecycle",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("# 📊 Marketing Campaign Lifecycle Dashboard")
st.markdown("### Enterprise-Grade Marketing Operations Blueprint | 26-Phase Framework")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('marketing_campaign_lifecycle.csv', on_bad_lines='skip', engine='python')
    return df

df = load_data()

# Statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Phases", value="26")

with col2:
    st.metric(label="Lifecycle Stages", value="7")

with col3:
    st.metric(label="Enterprise Tools", value="50+")

with col4:
    st.metric(label="Years of Excellence", value="15+")

st.markdown("---")

# Sidebar filters
st.sidebar.header("🔍 Filters & Controls")

# Search functionality
search_term = st.sidebar.text_input("Search by Phase ID, Action, or KPI", "")

# Stage filter
stages = ['All Stages'] + sorted(df['Lifecycle Stage'].unique().tolist())
selected_stage = st.sidebar.selectbox("Filter by Lifecycle Stage", stages)

# Filter data
filtered_df = df.copy()

if search_term:
    filtered_df = filtered_df[
        (filtered_df['Phase ID'].str.contains(search_term, case=False)) |
        (filtered_df['Process Action'].str.contains(search_term, case=False)) |
        (filtered_df['Critical KPI'].str.contains(search_term, case=False))
    ]

if selected_stage != 'All Stages':
    filtered_df = filtered_df[filtered_df['Lifecycle Stage'] == selected_stage]

# Display data
st.markdown("## 📋 Campaign Lifecycle Phases")
st.markdown(f"**Showing {len(filtered_df)} of {len(df)} phases**")

# Create tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📊 Table View", "🎯 By Stage", "🛠️ Tech Stack", "📈 KPIs"])

with tab1:
    st.dataframe(filtered_df, use_container_width=True, height=600)

with tab2:
    # Group by stage
    st.subheader("Phases by Lifecycle Stage")
    for stage in df['Lifecycle Stage'].unique():
        stage_data = df[df['Lifecycle Stage'] == stage]
        with st.expander(f"**{stage}** ({len(stage_data)} phases)"):
            for idx, row in stage_data.iterrows():
                st.markdown(f"**{row['Phase ID']}: {row['Process Action']}**")
                st.caption(f"🎯 KPI: {row['Critical KPI']}")
                st.caption(f"👥 RACI: {row['RACI Matrix Role']}")

with tab3:
    # Tech stack analysis
    st.subheader("Enterprise Technology Stack")
    all_tools = []
    for tools_str in df['Tech Stack'].fillna('').astype(str):
        tools = [t.strip() for t in tools_str.split('|')]
        all_tools.extend(tools)
    
    if all_tools:
        tool_df = pd.DataFrame({'Tool': all_tools})
        tool_counts = tool_df['Tool'].value_counts()
        
        st.bar_chart(tool_counts)
        st.markdown("### Most Used Tools")
        for tool, count in tool_counts.head(10).items():
            st.write(f"- **{tool}**: Used in {count} phases")
    else:
        st.info("No tech stack data available")

with tab4:
    # KPI Analysis
    st.subheader("Critical KPIs by Phase")
    kpi_df = df[['Phase ID', 'Lifecycle Stage', 'Critical KPI']]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### KPI by Stage")
        stage_kpis = df.groupby('Lifecycle Stage').size()
        st.bar_chart(stage_kpis)
    
    with col2:
        st.markdown("### KPI Categories")
        st.write(kpi_df.to_html(escape=False), unsafe_allow_html=True)

# Detailed view
st.markdown("---")
st.markdown("## 🔍 Detailed Phase Analysis")

selected_phase = st.selectbox(
    "Select a phase for detailed information",
    df['Phase ID'].tolist()
)

if selected_phase:
    phase_data = df[df['Phase ID'] == selected_phase].iloc[0]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"### {phase_data['Phase ID']}")
        st.markdown(f"**Stage:** {phase_data['Lifecycle Stage']}")
        st.markdown(f"**Action:** {phase_data['Process Action']}")
    
    with col2:
        st.markdown("### Standard Operating Procedure")
        st.info(phase_data['Standard Operating Procedure (SOP)'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### RACI Matrix")
        st.warning(phase_data['RACI Matrix Role'])
    
    with col2:
        st.markdown("### Critical KPI")
        st.success(phase_data['Critical KPI'])
    
    st.markdown("### Tech Stack")
    tools = phase_data['Tech Stack'].split(' | ')
    cols = st.columns(len(tools))
    for col, tool in zip(cols, tools):
        with col:
            st.markdown(f"🛠️ **{tool}**")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    © 2026 Enterprise Marketing Operations | Data Architecture: Senior Marketing Operations Director & Data Architect
</div>
""", unsafe_allow_html=True)
