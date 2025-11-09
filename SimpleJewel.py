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
    page_title="Jewel Calc - Jewellery Invoicing",
    page_icon="💎",
    layout="centered"
)

# Initialize session state for base values
if 'base_values' not in st.session_state:
    st.session_state.base_values = {
        'metal_rates': {
            'Gold 22K/916': 5500,
            'Gold 20K/833': 5044,
            'Gold 18K/750': 4564,
            'Silver': 400
        },
        'value_addition_gold': 13,
        'metal_mc_per_gm': 80
    }

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
    c.setFont("Helvetica-Bold", 10)
    
    # Starting position
    y = height - 10 * mm
    
    # Title
    c.drawCentredString(width / 2, y, "JEWELLERY INVOICE")
    y -= 5 * mm
    
    # Date and time in IST
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, y, current_time.strftime('%d/%m/%Y %H:%M:%S IST'))
    y -= 5 * mm
    
    c.drawString(5 * mm, y, "-" * 35)
    y -= 4 * mm
    
    # Customer Information
    c.setFont("Helvetica-Bold", 8)
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
    c.setFont("Helvetica-Bold", 8)
    c.drawString(5 * mm, y, "ITEM DETAILS")
    y -= 4 * mm
    
    c.setFont("Helvetica", 8)
    c.drawString(5 * mm, y, f"Type: {data['selected_type']}")
    y -= 4 * mm
    
    c.drawString(5 * mm, y, f"Rate: Rs.{data['rate_per_gram']}/gm")
    y -= 4 * mm
    
    c.drawString(5 * mm, y, f"Weight: {data['weight_gm']:.3f} gm")
    y -= 4 * mm
    
    c.drawString(5 * mm, y, f"Wastage: {data['wastage_gm']:.3f} gm")
    y -= 4 * mm
    
    c.setFont("Helvetica-Bold", 8)
    c.drawString(5 * mm, y, f"Net Weight: {data['net_weight_gm']:.3f} gm")
    y -= 5 * mm
    
    c.drawString(5 * mm, y, "-" * 35)
    y -= 4 * mm
    
    # Amount Calculation
    c.setFont("Helvetica-Bold", 8)
    c.drawString(5 * mm, y, "AMOUNT CALCULATION")
    y -= 4 * mm
    
    c.setFont("Helvetica", 8)
    c.drawString(5 * mm, y, f"J Amount:")
    c.drawRightString(width - 5 * mm, y, f"Rs.{data['j_amount']:.2f}")
    y -= 4 * mm
    
    c.drawString(5 * mm, y, f"Making Charges:")
    c.drawRightString(width - 5 * mm, y, f"Rs.{data['making_charges']:.2f}")
    y -= 4 * mm
    
    c.setFont("Helvetica-Bold", 8)
    c.drawString(5 * mm, y, f"Amount:")
    c.drawRightString(width - 5 * mm, y, f"Rs.{data['amount_before_gst']:.2f}")
    y -= 5 * mm
    
    # Add discount if exists
    if data.get('discount_amount', 0) > 0:
        c.setFont("Helvetica", 8)
        c.drawString(5 * mm, y, f"Discount:")
        c.drawRightString(width - 5 * mm, y, f"Rs.{data['discount_amount']:.2f}")
        y -= 4 * mm
        
        c.setFont("Helvetica-Bold", 8)
        c.drawString(5 * mm, y, f"After Discount:")
        c.drawRightString(width - 5 * mm, y, f"Rs.{data['amount_after_discount']:.2f}")
        y -= 5 * mm
    
    c.setFont("Helvetica", 8)
    c.drawString(5 * mm, y, f"CGST 1.5%:")
    c.drawRightString(width - 5 * mm, y, f"Rs.{data['cgst_amount']:.2f}")
    y -= 4 * mm
    
    c.drawString(5 * mm, y, f"SGST 1.5%:")
    c.drawRightString(width - 5 * mm, y, f"Rs.{data['sgst_amount']:.2f}")
    y -= 5 * mm
    
    c.drawString(5 * mm, y, "-" * 35)
    y -= 4 * mm
    
    # Final Amount
    c.setFont("Helvetica-Bold", 10)
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
        st.session_state.base_values['metal_rates'][metal_type] = st.number_input(
            f"{metal_type} Rate", 
            min_value=0, 
            value=st.session_state.base_values['metal_rates'][metal_type],
            step=10
        )

    st.markdown("---")
    st.subheader("Other Settings")

    st.session_state.base_values['value_addition_gold'] = st.number_input(
        "Value Addition Gold's (%)", 
        min_value=0.0, 
        max_value=100.0,
        value=float(st.session_state.base_values['value_addition_gold']),
        step=0.5
    )

    st.session_state.base_values['metal_mc_per_gm'] = st.number_input(
        "Metal MC (₹ per gram)", 
        min_value=0, 
        value=st.session_state.base_values['metal_mc_per_gm'],
        step=5
    )

    st.markdown("---")
    if st.button("🔄 Reset to Defaults"):
        st.session_state.base_values = {
            'metal_rates': {
                'Gold 22K/916': 5500,
                'Gold 20K/833': 5044,
                'Gold 18K/750': 4564,
                'Silver': 400
            },
            'value_addition_gold': 13,
            'metal_mc_per_gm': 80
        }
        st.rerun()

# Main App
st.title("💎 Jewel Calc - Jewellery Invoicing")

# Display time in IST
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)
st.caption(f"📅 {current_time.strftime('%d/%m/%Y %H:%M:%S IST')}")
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

# Making Charges - with option for rupees or percentage
st.subheader("Making Charges")
mc_type = st.radio(
    "Making Charge Type",
    options=["Rupees (₹)", "Percentage (%)"],
    horizontal=True
)

mc_per_gram = st.session_state.base_values['metal_mc_per_gm']

if mc_type == "Rupees (₹)":
    making_charges = st.number_input(
        f"Making Charges (₹) [Auto: {mc_per_gram * net_weight_gm:.2f}]",
        min_value=0.0,
        value=mc_per_gram * net_weight_gm,
        step=10.0,
        format="%.2f"
    )
else:
    mc_percentage = st.number_input(
        "Making Charge Percentage (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.5,
        format="%.2f"
    )
    making_charges = j_amount * (mc_percentage / 100)
    st.info(f"Making Charges: ₹{making_charges:.2f}")

# Base amount before GST
amount_before_gst = j_amount + making_charges

# Display amounts
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.metric("J Amount (₹)", f"{j_amount:.2f}")

with col2:
    st.metric("Amount (₹)", f"{amount_before_gst:.2f}")

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
    discount_amount = st.number_input(
        "Discount Amount (₹)",
        min_value=0.0,
        max_value=float(amount_before_gst),
        value=0.0,
        step=10.0,
        format="%.2f"
    )
elif discount_type == "Percentage (%)":
    discount_percentage = st.number_input(
        "Discount Percentage (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.5,
        format="%.2f"
    )
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
st.info("💡 Click the button above to download the PDF. You can then open it in a new tab and print it to your thermal printer.")

# Footer
st.markdown("---")
st.caption("💎 Jewel Calc - Professional Jewellery Invoicing System | Made with Streamlit")
