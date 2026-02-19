import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- APP CONFIGURATION ---
st.set_page_config(page_title="COREnergy Sales Tool", layout="wide", page_icon="⚡")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("⚙️ Offer Configuration")
    core_rate = st.number_input("CORE Fixed Rate (PHP/kWh)", value=5.00, step=0.05)
    st.divider()
    st.caption("Sales Tool v1.0")

# --- MAIN HEADER ---
st.title("⚡ Client Savings Calculator")
st.markdown("Enter details from the client's current **Distribution Utility (DU)** bill.")
st.divider()

# --- INPUT SECTION ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 Client Profile")
    client_name = st.text_input("Client / Business Name", placeholder="e.g. ABC Corp")
    
    st.subheader("🧾 Bill Details")
    consumption = st.number_input("Monthly Consumption (kWh)", min_value=0.0, value=55000.0, step=100.0)
    demand = st.number_input("Actual/Billed Demand (kW)", min_value=0.0, value=120.0, step=1.0)
    
    st.subheader("💰 Current Pricing")
    du_rate = st.number_input("Current Gen. Rate (PHP/kWh)", min_value=0.0, value=5.85, step=0.01)

# --- CALCULATIONS ---
du_cost = consumption * du_rate
core_cost = consumption * core_rate
monthly_savings = du_cost - core_cost
annual_savings = monthly_savings * 12
savings_percent = ((du_rate - core_rate) / du_rate) * 100

# Eligibility Logic
if demand >= 500:
    status = "RCOA ELIGIBLE (Direct Switch)"
    msg = "Matches 500kW threshold."
    icon = "✅"
else:
    status = "RAP ELIGIBLE (Aggregation)"
    msg = "Demand < 500kW. Needs aggregation."
    icon = "🤝"

# --- OUTPUT SECTION ---
with col2:
    st.subheader(f"Proposal for: {client_name if client_name else 'Prospect'}")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Monthly Savings", f"₱{monthly_savings:,.2f}")
    m2.metric("Annual Savings", f"₱{annual_savings:,.2f}", delta=f"{savings_percent:.1f}% Reduction")
    m3.metric("Effective Rate", f"₱{core_rate:.2f}", delta=f"-₱{du_rate - core_rate:.2f}")

    # Chart
    fig = go.Figure(data=[
        go.Bar(name='Current Provider', x=['Monthly Cost'], y=[du_cost], marker_color='#bdc3c7'),
        go.Bar(name='COREnergy', x=['Monthly Cost'], y=[core_cost], marker_color='#27ae60')
    ])
    fig.update_layout(barmode='group', height=300, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"**{icon} {status}**: {msg}")

# --- TEXT GENERATOR ---
proposal_text = f"""
PROPOSAL FOR {client_name.upper() if client_name else 'CLIENT'}
Current Rate: ₱{du_rate:.2f} | CORE Rate: ₱{core_rate:.2f}
Est. Annual Savings: ₱{annual_savings:,.2f} ({savings_percent:.1f}%)
"""
with st.expander("📄 Copy Proposal Text"):
    st.code(proposal_text)
