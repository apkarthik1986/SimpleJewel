import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os
import base64

# Page configuration
st.set_page_config(
    page_title="Jewel Calc",
    page_icon="💎",
    layout="centered"
)

# Initialize session state for base values
if 'base_values' not in st.session_state:
    st.session_state.base_values = {
        'metal_rates': {
            'Gold 22K/916': 0,
            'Gold 20K/833': 0,
            'Gold 18K/750': 0,
            'Silver': 0
        },
        'gold_wastage_percentage': 0,
        'silver_wastage_percentage': 0,
        'gold_mc_per_gm': 0,
        'silver_mc_per_gm': 0
    }

# Initialize customer details expand state
if 'customer_details_expanded' not in st.session_state:
    st.session_state.customer_details_expanded = False

# Function to generate PDF for thermal printer
def generate_thermal_pdf(data):
    """Generate a PDF formatted for thermal printer (80mm width) with dynamic height"""
    # Create PDF in temp directory
    pdf_filename = f"/tmp/jewel_estimate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Thermal printer width is typically 80mm (about 226.77 points)
    width = 80 * mm
    
    # Calculate dynamic height based on content
    line_height = 4 * mm
    content_lines = 0
    
    # Count lines for customer information
    content_lines += 5  # Title, date, separator lines
    if data['bill_number']:
        content_lines += 1
    if data['customer_acc']:
        content_lines += 1
    if data['customer_name']:
        content_lines += 1
    if data['address']:
        content_lines += 1
    if data['mobile_number']:
        content_lines += 1
    
    # Item details section (fixed lines)
    content_lines += 10  # Section headers, item details
    
    # Amount calculation section
    content_lines += 10  # Amount details, GST, total
    
    # Add discount line if discount exists
    if data.get('discount_amount', 0) > 0:
        content_lines += 1
    
    # Calculate height with some padding
    height = (content_lines * line_height) + (20 * mm)
    
    c = canvas.Canvas(pdf_filename, pagesize=(width, height))
    
    # Set font
    c.setFont("Helvetica-Bold", 14)
    
    # Starting position
    y = height - 10 * mm
    
    # Title
    c.drawCentredString(width / 2, y, "ESTIMATE")
    y -= 5 * mm
    
    # Date and time in IST
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, y, current_time.strftime('%d/%m/%Y %H:%M:%S IST'))
    y -= 5 * mm
    
    c.drawString(5 * mm, y, "-" * 35)
    y -= 4 * mm
    
    # Customer Information
    c.setFont("Helvetica-Bold", 10)
    if data['bill_number']:
        c.drawString(5 * mm, y, f"Bill No: {data['bill_number']}")
        y -= 4 * mm
    
    if data['customer_acc']:
        c.drawString(5 * mm, y, f"Acc No: {data['customer_acc']}")
        y -= 4 * mm
    
    if data['customer_name']:
        c.drawString(5 * mm, y, f"Name: {data['customer_name']}")
        y -= 4 * mm
    
    if data['address']:
        c.drawString(5 * mm, y, f"Address: {data['address']}")
        y -= 4 * mm
    
    if data['mobile_number']:
        c.drawString(5 * mm, y, f"Mobile: {data['mobile_number']}")
        y -= 4 * mm
    
    c.drawString(5 * mm, y, "-" * 35)
    y -= 4 * mm
    
    # Item Details
    c.setFont("Helvetica-Bold", 11)
    c.drawString(5 * mm, y, "ITEM DETAILS")
    y -= 4 * mm
    
    c.setFont("Helvetica", 10)
    c.drawString(5 * mm, y, f"Type: {data['selected_type']}")
    y -= 4 * mm
    
    c.drawString(5 * mm, y, f"Rate: Rs.{data['rate_per_gram']}/gm")
    y -= 4 * mm
    
    c.drawString(5 * mm, y, f"Weight: {data['weight_gm']:.3f} gm")
    y -= 4 * mm
    
    c.drawString(5 * mm, y, f"Wastage: {data['wastage_gm']:.3f} gm")
    y -= 4 * mm
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5 * mm, y, f"Net Weight: {data['net_weight_gm']:.3f} gm")
    y -= 5 * mm
    
    c.drawString(5 * mm, y, "-" * 35)
    y -= 4 * mm
    
    # Amount Calculation
    c.setFont("Helvetica-Bold", 11)
    c.drawString(5 * mm, y, "AMOUNT CALCULATION")
    y -= 4 * mm
    
    c.setFont("Helvetica", 10)
    c.drawString(5 * mm, y, f"J Amount:")
    c.drawRightString(width - 5 * mm, y, f"Rs.{round(data['j_amount'])}")
    y -= 4 * mm
    
    c.drawString(5 * mm, y, f"Making Charges:")
    c.drawRightString(width - 5 * mm, y, f"Rs.{data['making_charges']:.2f}")
    y -= 4 * mm
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5 * mm, y, f"Amount:")
    c.drawRightString(width - 5 * mm, y, f"Rs.{round(data['amount_before_gst'])}")
    y -= 5 * mm
    
    # Add discount if exists
    if data.get('discount_amount', 0) > 0:
        c.setFont("Helvetica", 10)
        c.drawString(5 * mm, y, f"Discount:")
        c.drawRightString(width - 5 * mm, y, f"Rs.{data['discount_amount']:.2f}")
        y -= 4 * mm
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(5 * mm, y, f"After Discount:")
        c.drawRightString(width - 5 * mm, y, f"Rs.{data['amount_after_discount']:.2f}")
        y -= 5 * mm
    
    c.setFont("Helvetica", 10)
    c.drawString(5 * mm, y, f"CGST 1.5%:")
    c.drawRightString(width - 5 * mm, y, f"Rs.{data['cgst_amount']:.2f}")
    y -= 4 * mm
    
    c.drawString(5 * mm, y, f"SGST 1.5%:")
    c.drawRightString(width - 5 * mm, y, f"Rs.{data['sgst_amount']:.2f}")
    y -= 5 * mm
    
    c.drawString(5 * mm, y, "-" * 35)
    y -= 4 * mm
    
    # Final Amount
    c.setFont("Helvetica-Bold", 13)
    c.drawString(5 * mm, y, "Total Amount:")
    c.drawRightString(width - 5 * mm, y, f"Rs.{data['final_amount']:.2f}")
    y -= 5 * mm
    
    c.drawString(5 * mm, y, "-" * 35)
    
    # Save PDF
    c.save()
    
    return pdf_filename

# Sidebar for Base Values Configuration
with st.sidebar:
    st.title("⚙️ Base Values Configuration")
    st.markdown("---")

    st.subheader("Metal Rates (₹ per gram)")
    
    # Update metal rates
    for metal_type in st.session_state.base_values['metal_rates'].keys():
        # Use a unique key for each input to ensure proper state management
        current_value = st.session_state.base_values['metal_rates'][metal_type]
        # Convert to float for display, use None if value is 0
        display_value = None if current_value == 0 else (float(current_value) if current_value != 0 else None)
        
        input_value = st.number_input(
            f"{metal_type} Rate", 
            min_value=0.0, 
            value=display_value,
            step=1.0,
            format="%.3f",
            placeholder="0.000",
            key=f"rate_{metal_type}"
        )
        # Update session state only if input is not None
        if input_value is not None:
            st.session_state.base_values['metal_rates'][metal_type] = int(input_value) if input_value == int(input_value) else input_value
        elif current_value != 0:
            # If user cleared the field, reset to 0
            st.session_state.base_values['metal_rates'][metal_type] = 0

    st.markdown("---")
    st.subheader("Wastage Settings")

    gold_wastage_input = st.number_input(
        "Gold Wastage (%)", 
        min_value=0.0, 
        max_value=100.0,
        value=None if st.session_state.base_values['gold_wastage_percentage'] == 0 else float(st.session_state.base_values['gold_wastage_percentage']),
        step=0.5,
        placeholder="0.0",
        key="gold_wastage_percentage"
    )
    if gold_wastage_input is not None:
        st.session_state.base_values['gold_wastage_percentage'] = gold_wastage_input

    silver_wastage_input = st.number_input(
        "Silver Wastage (%)", 
        min_value=0.0, 
        max_value=100.0,
        value=None if st.session_state.base_values['silver_wastage_percentage'] == 0 else float(st.session_state.base_values['silver_wastage_percentage']),
        step=0.5,
        placeholder="0.0",
        key="silver_wastage_percentage"
    )
    if silver_wastage_input is not None:
        st.session_state.base_values['silver_wastage_percentage'] = silver_wastage_input

    st.markdown("---")
    st.subheader("Making Charges")

    gold_mc_input = st.number_input(
        "Gold MC (₹ per gram)", 
        min_value=0, 
        value=None if st.session_state.base_values['gold_mc_per_gm'] == 0 else st.session_state.base_values['gold_mc_per_gm'],
        step=5,
        placeholder="0",
        key="gold_mc_per_gm"
    )
    if gold_mc_input is not None:
        st.session_state.base_values['gold_mc_per_gm'] = gold_mc_input

    silver_mc_input = st.number_input(
        "Silver MC (₹ per gram)", 
        min_value=0, 
        value=None if st.session_state.base_values['silver_mc_per_gm'] == 0 else st.session_state.base_values['silver_mc_per_gm'],
        step=5,
        placeholder="0",
        key="silver_mc_per_gm"
    )
    if silver_mc_input is not None:
        st.session_state.base_values['silver_mc_per_gm'] = silver_mc_input

    st.markdown("---")
    if st.button("🔄 Reset to Defaults"):
        st.session_state.base_values = {
            'metal_rates': {
                'Gold 22K/916': 0,
                'Gold 20K/833': 0,
                'Gold 18K/750': 0,
                'Silver': 0
            },
            'gold_wastage_percentage': 0,
            'silver_wastage_percentage': 0,
            'gold_mc_per_gm': 0,
            'silver_mc_per_gm': 0
        }
        st.rerun()

# Main App
col_title, col_reset = st.columns([3, 1])
with col_title:
    st.title("💎 Jewel Calc 💎")
with col_reset:
    if st.button("🔄 Reset All", help="Reset all base values to defaults"):
        st.session_state.base_values = {
            'metal_rates': {
                'Gold 22K/916': 0,
                'Gold 20K/833': 0,
                'Gold 18K/750': 0,
                'Silver': 0
            },
            'gold_wastage_percentage': 0,
            'silver_wastage_percentage': 0,
            'gold_mc_per_gm': 0,
            'silver_mc_per_gm': 0
        }
        st.rerun()

# Display time in IST
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)
st.caption(f"📅 {current_time.strftime('%d/%m/%Y %H:%M:%S IST')}")

# Customer Information Section with collapse/expand
customer_expander = st.expander("Customer Information", expanded=st.session_state.customer_details_expanded)
with customer_expander:
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

# Type Selection - Using metal rates
selected_type = st.selectbox(
    "Type",
    options=list(st.session_state.base_values['metal_rates'].keys()),
    index=0
)

# Get rate per gram based on selection
rate_per_gram = st.session_state.base_values['metal_rates'][selected_type]

st.info(f"📌 Current Rate: ₹{rate_per_gram} per gram")

# Weight inputs
col1, col2, col3 = st.columns(3)

with col1:
    weight_gm = st.number_input(
        "Weight (gm)", 
        min_value=0.0, 
        value=None,
        step=0.1,
        format="%.3f",
        placeholder="0.000"
    )
    if weight_gm is None:
        weight_gm = 0.0

with col2:
    # Calculate wastage based on wastage percentage if weight is provided
    # Determine wastage percentage based on metal type
    is_gold = 'Gold' in selected_type
    wastage_percentage = st.session_state.base_values['gold_wastage_percentage'] if is_gold else st.session_state.base_values['silver_wastage_percentage']
    suggested_wastage = (weight_gm * wastage_percentage) / 100 if weight_gm > 0 else 0.0
    
    wastage_gm = st.number_input(
        "Wastage (gm)", 
        min_value=0.0, 
        value=suggested_wastage if weight_gm > 0 else None,
        step=0.1,
        format="%.3f",
        placeholder="0.000",
        help=f"Suggested: {suggested_wastage:.3f} gm ({wastage_percentage}%)"
    )
    if wastage_gm is None:
        wastage_gm = 0.0

with col3:
    net_weight_gm = weight_gm + wastage_gm
    st.metric("Net Weight (gm)", f"{net_weight_gm:.3f}")

# Calculations
st.markdown("---")
st.header("Amount Calculation")

# J Amount (Jewelry Amount)
j_amount = net_weight_gm * rate_per_gram

# Making Charges - with option for rupees or percentage
st.subheader("Making Charges")
mc_type = st.radio(
    "Making Charge Type",
    options=["Rupees (₹)", "Percentage (%)"],
    horizontal=True
)

# Determine MC per gram based on metal type
is_gold = 'Gold' in selected_type
is_silver = 'Silver' in selected_type
mc_per_gram = st.session_state.base_values['gold_mc_per_gm'] if is_gold else st.session_state.base_values['silver_mc_per_gm']

# Determine minimum making charge based on metal type
min_making_charge = 250.0 if is_gold else (200.0 if is_silver else 0.0)

if mc_type == "Rupees (₹)":
    calculated_mc = mc_per_gram * net_weight_gm
    # Apply minimum making charge
    default_mc = max(calculated_mc, min_making_charge)
    
    making_charges = st.number_input(
        f"Making Charges (₹) [Auto: {calculated_mc:.2f}, Min: {min_making_charge:.0f}]",
        min_value=min_making_charge,
        value=default_mc if net_weight_gm > 0 else None,
        step=10.0,
        format="%.2f",
        placeholder=f"{min_making_charge:.0f}"
    )
    if making_charges is None:
        making_charges = min_making_charge
else:
    mc_percentage = st.number_input(
        "Making Charge Percentage (%)",
        min_value=0.0,
        max_value=100.0,
        value=None,
        step=0.5,
        format="%.2f",
        placeholder="0.0"
    )
    if mc_percentage is None:
        mc_percentage = 0.0
    calculated_mc = j_amount * (mc_percentage / 100)
    # Apply minimum making charge
    making_charges = max(calculated_mc, min_making_charge)
    st.info(f"Making Charges: ₹{making_charges:.2f} (Min: ₹{min_making_charge:.0f})")

# Base amount before GST
amount_before_gst = j_amount + making_charges

# Display amounts
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.metric("J Amount (₹)", f"{round(j_amount):,}")

with col2:
    st.metric("Amount (₹)", f"{round(amount_before_gst):,}")

# Discount Section
st.markdown("---")
st.subheader("Discount")
discount_type = st.radio(
    "Discount Type",
    options=["None", "Rupees (₹)", "Percentage (%)"],
    horizontal=True
)

discount_amount = 0.0
if discount_type == "Rupees (₹)":
    discount_input = st.number_input(
        "Discount Amount (₹)",
        min_value=0.0,
        max_value=float(amount_before_gst),
        value=None,
        step=10.0,
        format="%.2f",
        placeholder="0.00"
    )
    discount_amount = discount_input if discount_input is not None else 0.0
elif discount_type == "Percentage (%)":
    discount_percentage_input = st.number_input(
        "Discount Percentage (%)",
        min_value=0.0,
        max_value=100.0,
        value=None,
        step=0.5,
        format="%.2f",
        placeholder="0.00"
    )
    discount_percentage = discount_percentage_input if discount_percentage_input is not None else 0.0
    discount_amount = amount_before_gst * (discount_percentage / 100)
    st.info(f"Discount Amount: ₹{discount_amount:.2f}")

# Amount after discount
amount_after_discount = amount_before_gst - discount_amount

if discount_amount > 0:
    st.metric("Amount After Discount (₹)", f"{amount_after_discount:.2f}")

# CGST and SGST on amount after discount
st.markdown("---")
cgst_amount = amount_after_discount * 0.015
st.metric("CGST 1.5% (₹)", f"{cgst_amount:.2f}")

sgst_amount = amount_after_discount * 0.015
st.metric("SGST 1.5% (₹)", f"{sgst_amount:.2f}")

# Final Amount
final_amount = amount_after_discount + cgst_amount + sgst_amount

st.markdown("---")
st.success(f"### 💰 Amount Incl. GST: ₹{final_amount:.2f}")

# Download PDF Button
st.markdown("---")

# Collect all data
estimate_data = {
    'bill_number': bill_number,
    'customer_acc': customer_acc,
    'customer_name': customer_name,
    'address': address,
    'mobile_number': mobile_number,
    'selected_type': selected_type,
    'rate_per_gram': rate_per_gram,
    'weight_gm': weight_gm,
    'wastage_gm': wastage_gm,
    'net_weight_gm': net_weight_gm,
    'j_amount': j_amount,
    'making_charges': making_charges,
    'amount_before_gst': amount_before_gst,
    'discount_amount': discount_amount,
    'amount_after_discount': amount_after_discount,
    'cgst_amount': cgst_amount,
    'sgst_amount': sgst_amount,
    'final_amount': final_amount
}

# Generate PDF
pdf_file = generate_thermal_pdf(estimate_data)

# Read PDF file
with open(pdf_file, "rb") as f:
    pdf_data = f.read()

# Display download button directly
st.download_button(
    label="📄 Download PDF",
    data=pdf_data,
    file_name=f"jewel_invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
    mime="application/pdf",
    type="primary",
    use_container_width=True
)

# Display success message about download location
st.success("✅ When you click the Download PDF button above, the file will be saved to your default download folder")
