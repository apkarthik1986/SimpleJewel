import streamlit as st
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="JWL CALC - Jewelry Estimation",
    page_icon="💎",
    layout="centered"
)

# Initialize session state for base values
if 'base_values' not in st.session_state:
    st.session_state.base_values = {
        'gold_22k_916': 5500,
        'gold_20k_833': 5044,
        'gold_18k_750': 4564,
        'silver_rate': 400,
        'value_addition_gold': 13,
        'gold_mc_per_gm': 80,
        'silver_mc_per_gm': 8
    }

# Sidebar for Base Values Configuration
with st.sidebar:
    st.title("⚙️ Base Values Configuration")
    st.markdown("---")

    st.subheader("Gold Rates (₹ per gram)")
    st.session_state.base_values['gold_22k_916'] = st.number_input(
        "Gold 22K/916 Rate", 
        min_value=0, 
        value=st.session_state.base_values['gold_22k_916'],
        step=10
    )

    st.session_state.base_values['gold_20k_833'] = st.number_input(
        "Gold 20K/833 Rate", 
        min_value=0, 
        value=st.session_state.base_values['gold_20k_833'],
        step=10
    )

    st.session_state.base_values['gold_18k_750'] = st.number_input(
        "Gold 18K/750 Rate", 
        min_value=0, 
        value=st.session_state.base_values['gold_18k_750'],
        step=10
    )

    st.markdown("---")
    st.subheader("Other Rates")

    st.session_state.base_values['silver_rate'] = st.number_input(
        "Silver Rate (₹ per gram)", 
        min_value=0, 
        value=st.session_state.base_values['silver_rate'],
        step=10
    )

    st.session_state.base_values['value_addition_gold'] = st.number_input(
        "Value Addition Gold's (%)", 
        min_value=0.0, 
        max_value=100.0,
        value=float(st.session_state.base_values['value_addition_gold']),
        step=0.5
    )

    st.session_state.base_values['gold_mc_per_gm'] = st.number_input(
        "Gold MC (₹ per gram)", 
        min_value=0, 
        value=st.session_state.base_values['gold_mc_per_gm'],
        step=5
    )

    st.session_state.base_values['silver_mc_per_gm'] = st.number_input(
        "Silver MC (₹ per gram)", 
        min_value=0, 
        value=st.session_state.base_values['silver_mc_per_gm'],
        step=1
    )

    st.markdown("---")
    if st.button("🔄 Reset to Defaults"):
        st.session_state.base_values = {
            'gold_22k_916': 5500,
            'gold_20k_833': 5044,
            'gold_18k_750': 4564,
            'silver_rate': 400,
            'value_addition_gold': 13,
            'gold_mc_per_gm': 80,
            'silver_mc_per_gm': 8
        }
        st.rerun()

# Main App
st.title("💎 JWL CALC - Jewelry Estimation")
st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# Create tabs for better organization
tab1, tab2 = st.tabs(["📝 Estimate Form", "📊 Calculations Summary"])

with tab1:
    # Customer Information Section
    st.header("Customer Information")
    col1, col2 = st.columns(2)

    with col1:
        bill_number = st.text_input("Bill Number", placeholder="Enter bill number")
        customer_acc = st.text_input("Customer Acc Number", placeholder="Enter account number")
        customer_name = st.text_input("Name", placeholder="Enter customer name")

    with col2:
        address = st.text_area("Address", placeholder="Enter address", height=100)
        mobile_number = st.text_input("Mobile Number", placeholder="Enter mobile number")

    st.markdown("---")

    # Item Details Section
    st.header("Item Calculation")

    # Type Selection
    gold_types = {
        "Gold 22K/916": "gold_22k_916",
        "Gold 20K/833": "gold_20k_833",
        "Gold 18K/750": "gold_18k_750",
        "Silver": "silver_rate"
    }

    selected_type = st.selectbox(
        "Type",
        options=list(gold_types.keys()),
        index=0
    )

    # Get rate per gram based on selection
    rate_key = gold_types[selected_type]
    rate_per_gram = st.session_state.base_values[rate_key]

    st.info(f"📌 Current Rate: ₹{rate_per_gram} per gram")

    # Weight inputs
    col1, col2, col3 = st.columns(3)

    with col1:
        weight_gm = st.number_input(
            "Weight (gm)", 
            min_value=0.0, 
            value=0.0,
            step=0.1,
            format="%.3f"
        )

    with col2:
        wastage_gm = st.number_input(
            "Wastage (gm)", 
            min_value=0.0, 
            value=0.0,
            step=0.1,
            format="%.3f"
        )

    with col3:
        net_weight_gm = weight_gm + wastage_gm
        st.metric("Net Weight (gm)", f"{net_weight_gm:.3f}")

    # Calculations
    st.markdown("---")
    st.header("Amount Calculation")

    # J Amount (Jewelry Amount)
    j_amount = net_weight_gm * rate_per_gram

    # Making Charges
    if "Gold" in selected_type:
        mc_per_gram = st.session_state.base_values['gold_mc_per_gm']
    else:
        mc_per_gram = st.session_state.base_values['silver_mc_per_gm']

    making_charges = st.number_input(
        f"Making Charges (₹) [Auto: {mc_per_gram * net_weight_gm:.2f}]",
        min_value=0.0,
        value=mc_per_gram * net_weight_gm,
        step=10.0,
        format="%.2f"
    )

    # Base amount before GST
    amount_before_gst = j_amount + making_charges

    col1, col2 = st.columns(2)

    with col1:
        st.metric("J Amount (₹)", f"{j_amount:.2f}")
        cgst_amount = amount_before_gst * 0.015
        st.metric("CGST 1.5% (₹)", f"{cgst_amount:.2f}")

    with col2:
        st.metric("Amount (₹)", f"{amount_before_gst:.2f}")
        sgst_amount = amount_before_gst * 0.015
        st.metric("SGST 1.5% (₹)", f"{sgst_amount:.2f}")

    # Final Amount
    final_amount = amount_before_gst + cgst_amount + sgst_amount

    st.markdown("---")
    st.success(f"### 💰 Amount Incl. GST: ₹{final_amount:.2f}")

    # Action Buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("✅ Generate", type="primary", use_container_width=True):
            st.success("Estimate generated successfully!")
            st.balloons()

    with col2:
        if st.button("🖨️ Print", use_container_width=True):
            st.info("Print functionality ready")

    with col3:
        if st.button("💾 Save", use_container_width=True):
            st.info("Save functionality ready")

    with col4:
        if st.button("🔙 Back", use_container_width=True):
            st.rerun()

with tab2:
    st.header("Calculation Breakdown")

    if net_weight_gm > 0:
        # Create summary dataframe
        summary_data = {
            "Description": [
                "Gross Weight",
                "Wastage",
                "Net Weight",
                "Rate per gram",
                "Jewelry Amount (J Amount)",
                "Making Charges",
                "Subtotal",
                "CGST (1.5%)",
                "SGST (1.5%)",
                "**Total Amount**"
            ],
            "Value": [
                f"{weight_gm:.3f} gm",
                f"{wastage_gm:.3f} gm",
                f"{net_weight_gm:.3f} gm",
                f"₹{rate_per_gram}",
                f"₹{j_amount:.2f}",
                f"₹{making_charges:.2f}",
                f"₹{amount_before_gst:.2f}",
                f"₹{cgst_amount:.2f}",
                f"₹{sgst_amount:.2f}",
                f"**₹{final_amount:.2f}**"
            ]
        }

        df = pd.DataFrame(summary_data)
        st.table(df)

        # Visual breakdown
        st.subheader("Amount Distribution")
        breakdown = {
            "Component": ["Jewelry Amount", "Making Charges", "CGST", "SGST"],
            "Amount": [j_amount, making_charges, cgst_amount, sgst_amount]
        }
        st.bar_chart(pd.DataFrame(breakdown).set_index("Component"))
    else:
        st.info("Enter weight details in the Estimate Form to see calculations")

# Footer
st.markdown("---")
st.caption("💎 JWL CALC - Professional Jewelry Estimation System | Made with Streamlit")
