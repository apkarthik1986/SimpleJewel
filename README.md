# 💎 Jewel Calc - Jewellery Invoicing Application

A simple and intuitive jewellery invoicing application built with Streamlit. Calculate gold and silver jewellery prices with automatic GST calculations, making charges, discount options, and detailed breakdowns.

## 🌟 Features

- **Multiple Gold Types Support**: Calculate for Gold 22K/916, 20K/833, 18K/750, and Silver
- **Separate Wastage Settings**: Different wastage percentages for gold and silver
- **Real-time Calculations**: Automatic calculation of jewellery amounts, making charges, and GST
- **Discount Options**: Apply discounts in rupees or percentage
- **Configurable Base Values**: Easily adjust gold/silver rates, wastage percentages, and making charges
- **Customer Information**: Capture bill number, customer details, and contact information
- **PDF Invoice Generation**: Dynamic-sized PDF invoices optimized for thermal printers with download confirmation
- **Daily Persistence**: Base values (rates, wastage, making charges) persist throughout the day and automatically reset to zero at midnight IST
- **Clean Interface**: Simple, user-friendly design focused on essential features with no placeholder zeros

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

1. **Set Gold Rates**: Manually adjust rates for different gold purities (22K, 20K, 18K) - Input fields are empty by default for easy data entry
2. **Set Silver Rate**: Configure silver price per gram - Input field is empty by default for easy data entry
3. **Set Gold Wastage**: Define wastage percentage for gold (no default, start typing directly)
4. **Set Silver Wastage**: Define wastage percentage for silver (no default, start typing directly)
5. **Set Gold MC**: Define Gold making charges per gram - Input field is empty by default for easy data entry
6. **Set Silver MC**: Define Silver making charges per gram (separate from Gold MC) - Input field is empty by default for easy data entry
7. **Reset**: Use "Reset to Defaults" button in sidebar or "Reset All" button on main page to restore default values (all rates to 0)

**Note**: All input fields allow direct typing without needing to delete placeholder zeros, making data entry faster and more intuitive.

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
- A success message will confirm the PDF has been saved to your default download folder
- PDF is optimized for thermal printer
- Print directly to thermal printer from your download folder

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

## 💾 Data Persistence

The application automatically saves your base values (metal rates, wastage percentages, and making charges) to a local file on your computer at `~/.simplejewel_base_values.json`. This ensures that:

- **Your settings persist** across browser refreshes and app restarts
- **Values are maintained** throughout the entire day
- **Automatic reset** occurs at midnight IST (India Standard Time)
- **No manual intervention** needed - the app handles everything automatically

The automatic reset to zero at the end of each day ensures you start fresh each morning with default values, ready to configure for the current day's market rates.

## 🔧 Configuration

Default values in the application:
- Gold 22K/916: ₹0/gram (to be configured manually)
- Gold 20K/833: ₹0/gram (to be configured manually)
- Gold 18K/750: ₹0/gram (to be configured manually)
- Silver: ₹0/gram (to be configured manually)
- Gold Wastage: 0%
- Silver Wastage: 0%
- Gold Making Charges: ₹0/gram (to be configured manually)
- Silver Making Charges: ₹0/gram (to be configured manually)
- GST: 3% (1.5% CGST + 1.5% SGST)

All values can be adjusted via the sidebar during runtime. Base values are automatically saved to a local file (`~/.simplejewel_base_values.json`) and persist throughout the day. At midnight IST, all values automatically reset to zero (0) for the new day.

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
**Special thanks to Ashwin Prakash Chand**
