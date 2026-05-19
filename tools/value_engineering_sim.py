Python
import streamlit as st

# Financial Assumptions
BASE_COST_PER_UNIT = 180000 

# Multipliers based on code pathway bundles
MULTIPLIERS = {
    "IRC Small Multifamily (≤8 Units)": 0.45,
    "Title 18 Single-Stair (9-16 Units)": 0.55,
    "IBC Transition (9-16 Units)": 0.75,
    "Full IBC Compliance (17+ Units)": 1.00
}

# Code Logic Matrix
code_matrix = {
    "IRC Small Multifamily (≤8 Units)": {
        "Sprinklers": "Not Required",
        "Egress": "1 Exit (Single Stair)",
        "Fire Separation": "1-Hour Walls",
        "Travel Distance": "75 ft"
    },
    "Title 18 Single-Stair (9-16 Units)": {
        "Sprinklers": "NFPA 13D (Domestic Loop)",
        "Egress": "1 Exit (Single Stair)",
        "Fire Separation": "1-Hour Walls",
        "Travel Distance": "125 ft"
    },
    "IBC Transition (9-16 Units)": {
        "Sprinklers": "NFPA 13R (Commercial)",
        "Egress": "2 Exits Required (Dual Stair)",
        "Fire Separation": "0.5-Hour + Corridor",
        "Travel Distance": "125 ft"
    },
    "Full IBC Compliance (17+ Units)": {
        "Sprinklers": "Full NFPA 13 (Commercial)",
        "Egress": "2+ Exits Required",
        "Fire Separation": "2-Hour Minimum",
        "Travel Distance": "150 ft"
    }
}

st.title("Building Code Value-Engineering Simulator")

# Controls
target_units = st.sidebar.slider("Target Unit Count", 2, 30, 12)

if target_units <= 8:
    options = ["IRC Small Multifamily (≤8 Units)", "Full IBC Compliance (17+ Units)"]
elif target_units <= 16:
    options = ["Title 18 Single-Stair (9-16 Units)", "IBC Transition (9-16 Units)", "Full IBC Compliance (17+ Units)"]
else:
    options = ["Full IBC Compliance (17+ Units)"]

selected = st.sidebar.radio("Compliance Pathway", options)

# Calculations
baseline = target_units * BASE_COST_PER_UNIT
cost = baseline * MULTIPLIERS[selected]
savings = baseline - cost

# Display
st.subheader("Triggered Code Interdependencies")
reqs = code_matrix[selected]
cols = st.columns(4)
for i, (k, v) in enumerate(reqs.items()):
    cols[i].info(f"**{k}**\n\n{v}")

st.divider()

# Metrics
m1, m2, m3 = st.columns(3)
m1.metric("IBC Baseline Cost", f"${baseline:,.0f}")
m2.metric("Projected Cost", f"${cost:,.0f}")
m3.metric("Capital Saved", f"${savings:,.0f}")
