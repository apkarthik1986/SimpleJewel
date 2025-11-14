# 💎 Jewel Calc - Jewellery Invoicing Application

A simple and intuitive jewellery invoicing application built with Streamlit. Calculate gold and silver jewellery prices with automatic GST calculations, making charges, discount options, and detailed breakdowns.

## 🌟 Features

- **Multiple Gold Types Support**: Calculate for Gold 22K/916, 20K/833, 18K/750, and Silver
- **Real-time Calculations**: Automatic calculation of jewellery amounts, making charges, and GST
- **Discount Options**: Apply discounts in rupees or percentage
- **Configurable Base Values**: Easily adjust gold/silver rates and making charges
- **Customer Information**: Capture bill number, customer details, and contact information
- **PDF Invoice Generation**: Dynamic-sized PDF invoices optimized for thermal printers
- **Clean Interface**: Simple, user-friendly design focused on essential features

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/apkarthik1986/SimpleJewel.git
cd SimpleJewel
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run SimpleJewel.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 How to Use

### Configure Base Values (Sidebar)

1. **Fetch Rates**: Click "Fetch Rates from Website" to automatically fetch current rates (if fetch fails, rates are set to 0)
2. **Set Gold Rates**: Manually adjust rates for different gold purities (22K, 20K, 18K)
3. **Set Silver Rate**: Configure silver price per gram
4. **Set Wastage**: Define wastage percentage (default 13%)
5. **Set Gold MC**: Define Gold making charges per gram
6. **Set Silver MC**: Define Silver making charges per gram (separate from Gold MC)
7. **Reset**: Use "Reset to Defaults" button to restore default values (all rates to 0)

### Create an Estimate

#### Step 1: Enter Customer Information
- Bill Number
- Customer Account Number
- Customer Name
- Address
- Mobile Number

#### Step 2: Calculate Item Details
1. **Select Type**: Choose from Gold 22K/916, 20K/833, 18K/750, or Silver
2. **Enter Weight**: Input the gross weight in grams
3. **Enter Wastage**: Add wastage amount in grams
4. **Review Net Weight**: Automatically calculated (Weight + Wastage)

#### Step 3: Review Amounts
- **J Amount**: Jewellery base amount (Net Weight × Rate)
- **Making Charges**: Calculated automatically (can be adjusted manually)
- **Discount**: Apply discount in rupees or percentage
- **CGST/SGST**: 1.5% each on amount after discount
- **Final Amount**: Total amount including GST

#### Step 4: Download Invoice
- Click "Download PDF" button to generate invoice
- PDF opens in new tab optimized for thermal printer
- Print directly to thermal printer from browser

## 🎯 Calculation Formula

```
Net Weight = Gross Weight + Wastage
J Amount = Net Weight × Rate per gram
Subtotal = J Amount + Making Charges
Amount After Discount = Subtotal - Discount
CGST = Amount After Discount × 1.5%
SGST = Amount After Discount × 1.5%
Total Amount = Amount After Discount + CGST + SGST
```

## 🛠️ Recommendations for Keeping the App Simple

The application is intentionally designed to be simple and focused. Here are recommendations to maintain simplicity:

### Current Simple Design ✅
- **Single Page Focus**: All essential features on one screen
- **Minimal Input Fields**: Only necessary customer and item information
- **Automatic Calculations**: No manual calculation required
- **Two-Tab Interface**: Estimate Form and Summary view
- **Configurable Sidebar**: Easy access to base rate adjustments

### Future Enhancements (Keep Simple) 💡
If adding features, consider these simple additions:
1. **CSV History**: Save invoices to a CSV file for record-keeping
2. **Currency Symbol**: Make ₹ symbol configurable for other currencies
3. **Dark Mode**: Simple toggle for dark/light theme
4. **Multiple Items**: Allow adding 2-3 items per invoice with simple "Add Item" button

### Avoid These Complexities ⚠️
To keep the app simple, avoid:
- ❌ Complex database integrations
- ❌ User authentication and multi-user support
- ❌ Inventory management features
- ❌ Advanced reporting and analytics
- ❌ Online payment integrations
- ❌ Customer management systems
- ❌ Complex discount/offer systems

## 📁 Project Structure

```
SimpleJewel/
├── SimpleJewel.py      # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Configuration

Default values in the application:
- Gold 22K/916: ₹0/gram (to be configured manually or fetched)
- Gold 20K/833: ₹0/gram (to be configured manually or fetched)
- Gold 18K/750: ₹0/gram (to be configured manually or fetched)
- Silver: ₹0/gram (to be configured manually or fetched)
- Wastage: 13%
- Gold Making Charges: ₹0/gram (to be configured manually)
- Silver Making Charges: ₹0/gram (to be configured manually)
- GST: 3% (1.5% CGST + 1.5% SGST)

All values can be adjusted via the sidebar during runtime.

## 🤝 Contributing

This is a simple application focused on ease of use. When contributing:
1. Keep changes minimal and focused
2. Maintain the simple, clean interface
3. Test thoroughly before submitting
4. Update README if adding features

## 📝 License

This project is open source and available for personal and commercial use.

## 💬 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ using Streamlit**