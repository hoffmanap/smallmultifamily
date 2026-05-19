import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Title 18 Value-Engineering Simulator", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Title 18 Building Code Value-Engineering Simulator")
st.markdown("Analyze how targeted amendments to small-scale multi-family and adaptive reuse paths remove regulatory 'cost cliffs' and unlock project capitalization.")
st.divider()

# ---------------------------------------------------------
# 2. Financial & Data Assumptions
# ---------------------------------------------------------
# Standard baseline construction cost per unit under full commercial compliance
BASE_COST_PER_UNIT = 180000 

# Multipliers mapping back to the baseline regulatory burdens
MULTIPLIERS = {
    "IRC Small Multifamily (≤8 Units)": 0.45,
    "Title 18 Single-Stair (9-16 Units)": 0.55,
    "IBC Transition (9-16 Units)": 0.75,
    "Full IBC Compliance (17+ Units)": 1.00
}

# The Technical Interdependency Matrix
code_matrix = {
    "IRC Small Multifamily (≤8 Units)": {
        "Sprinklers": "Not Required",
        "Egress Layout": "1 Exit (Single Stair Core)",
        "Fire-Resistance Separation": "1-Hour Unit Demising Walls",
        "Max Egress Travel Distance": "75 feet",
        "Max Building Height": "2 Stories"
    },
    "Title 18 Single-Stair (9-16 Units)": {
        "Sprinklers": "NFPA 13D System (Domestic Loop)",
        "Egress Layout": "1 Exit (Single Stair Allowed)",
        "Fire-Resistance Separation": "1-Hour Unit Walls (No Corridor)",
        "Max Egress Travel Distance": "125 feet",
        "Max Building Height": "3 Stories"
    },
    "IBC Transition (9-16 Units)": {
        "Sprinklers": "NFPA 13R System (Commercial Pipe)",
        "Egress Layout": "2 Remote Exits Required (Dual Stairs)",
        "Fire-Resistance Separation": "0.5-Hour Wall + Rated Corridor",
        "Max Egress Travel Distance": "125 feet",
        "Max Building Height": "3 Stories"
    },
    "Full IBC Compliance (17+ Units)": {
        "Sprinklers": "Full NFPA 13 (Dedicated Main Vault)",
        "Egress Layout": "2+ Remote Exits (Enclosed Masonry Stairs)",
        "Fire-Resistance Separation": "2-Hour Minimum + Compartmentalization",
        "Max Egress Travel Distance": "150 feet maximum to stair",
        "Max Building Height": "3+ Stories"
    }
}

# ---------------------------------------------------------
# 3. Sidebar Programming Constraints
# ---------------------------------------------------------
st.sidebar.header("Project Parameters")
target_units = st.sidebar.slider("Target Unit Count", min_value=2, max_value=30, value=12, step=1)

# Logic engine filtering pathways contextually based on size thresholds
if target_units <= 8:
    available_pathways = ["IRC Small Multifamily (≤8 Units)", "Full IBC Compliance (17+ Units)"]
elif 9 <= target_units <= 16:
    available_pathways = ["Title 18 Single-Stair (9-16 Units)", "IBC Transition (9-16 Units)", "Full IBC Compliance (17+ Units)"]
else:
    available_pathways = ["Full IBC Compliance (17+ Units)"]

selected_pathway = st.sidebar.radio("Compliance Framework Pathway", available_pathways)

# ---------------------------------------------------------
# 4. Mathematical Calculations
# ---------------------------------------------------------
ibc_baseline_total = target_units * BASE_COST_PER_UNIT
current_multiplier = MULTIPLIERS[selected_pathway]
projected_total_cost = ibc_baseline_total * current_multiplier
total_savings = ibc_baseline_total - projected_total_cost

# ---------------------------------------------------------
# 5. UI Layout: Core Interdependencies
# ---------------------------------------------------------
st.subheader("Triggered Code Interdependencies")
st.markdown("Adjusting parameters updates the bundled technical conditions established by code logic:")

req_cols = st.columns(5)
reqs = code_matrix[selected_pathway]

for index, (requirement_name, rule_text) in enumerate(reqs.items()):
    req_cols[index].info(f"**{requirement_name}**\n\n{rule_text}")

st.divider()

# ---------------------------------------------------------
# 6. UI Layout: Financial Summary Metrics
# ---------------------------------------------------------
st.subheader("Project Financial Summary")
m1, m2, m3 = st.columns(3)

m1.metric(
    label="Standard IBC Baseline Cost", 
    value=f"${ibc_baseline_total:,.0f}", 
    delta="Default Commercial Cost Matrix", 
    delta_color="off"
)
m2.metric(
    label="Projected Pathway Cost", 
    value=f"${projected_total_cost:,.0f}", 
    delta=f"Reduction Factor: {current_multiplier}x", 
    delta_color="off"
)
m3.metric(
    label="Total Red-Tape Capital Saved", 
    value=f"${total_savings:,.0f}", 
    delta="Reinvestable Project Capital", 
    delta_color="normal"
)

# ---------------------------------------------------------
# 7. Embedded Charts (Visualizing the Cost Savings)
# ---------------------------------------------------------
st.divider()
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("The Cost Curve Cliff vs. Title 18 Ramp")
    
    # Generate the step function regression index graph
    units_range = list(range(4, 21))
    ibc_curve = [100 if u <= 8 else 150 if u <= 16 else 220 for u in units_range]
    t18_curve = [100 if u <= 8 else 115 if u <= 16 else 220 for u in units_range]
    
    fig_step = go.Figure()
    fig_step.add_trace(go.Scatter(x=units_range, y=ibc_curve, mode='lines', line_shape='hv', name='Standard IBC Baseline', line=dict(color='#dc2626', width=3)))
    fig_step.add_trace(go.Scatter(x=units_range, y=t18_curve, mode='lines', line_shape='hv', name='Title 18 Framework', line=dict(color='#16a34a', width=4)))
    
    fig_step.update_layout(
        xaxis_title="Number of Housing Units",
        yaxis_title="Regulatory Infrastructure Cost Index",
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_step, use_container_width=True)

with chart_col2:
    st.subheader("Strategic Reinvestment of Saved Capital")
    
    reinvest_data = pd.DataFrame({
        "Allocation Category": [
            "Neighborhood Facade & High-Quality Masonry", 
            "Rent Attainability (Mitigating Base Floor Rents)", 
            "High-Efficiency Green Infrastructure (Heat Pumps/Solar)", 
            "Public Amenities (Courtyards/Secured Bike Storage)"
        ],
        "Percentage": [35, 30, 25, 10]
    })
    
    fig_pie = px.pie(
        reinvest_data, 
        values="Percentage", 
        names="Allocation Category", 
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Plotly3
    )
    fig_pie.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)
