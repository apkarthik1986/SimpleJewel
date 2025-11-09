# 💎 SimpleJewel - Jewelry Estimation Calculator

A simple and intuitive jewelry estimation calculator built with Streamlit. Calculate gold and silver jewelry prices with automatic GST calculations, making charges, and detailed breakdowns.

![SimpleJewel App](https://github.com/user-attachments/assets/fb9a768b-dcf3-4b90-a174-fcbff1a3c013)

## 🌟 Features

- **Multiple Gold Types Support**: Calculate for Gold 22K/916, 20K/833, 18K/750, and Silver
- **Real-time Calculations**: Automatic calculation of jewelry amounts, making charges, and GST
- **Configurable Base Values**: Easily adjust gold/silver rates and making charges
- **Customer Information**: Capture bill number, customer details, and contact information
- **Detailed Breakdown**: View comprehensive calculation summaries with visual charts
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

1. **Set Gold Rates**: Adjust rates for different gold purities (22K, 20K, 18K)
2. **Set Silver Rate**: Configure silver price per gram
3. **Set Making Charges**: Define making charges per gram for gold and silver
4. **Value Addition**: Set value addition percentage for gold
5. **Reset**: Use "Reset to Defaults" button to restore default values

![Configuration](https://github.com/user-attachments/assets/fb9a768b-dcf3-4b90-a174-fcbff1a3c013)

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

![Item Calculation](https://github.com/user-attachments/assets/22137f80-e9f0-48a1-aa54-6193246ca496)

#### Step 3: Review Amounts
- **J Amount**: Jewelry base amount (Net Weight × Rate)
- **Making Charges**: Calculated automatically (can be adjusted manually)
- **CGST/SGST**: 1.5% each on subtotal
- **Final Amount**: Total amount including GST

#### Step 4: View Calculation Summary
Switch to the "Calculations Summary" tab to see:
- Complete breakdown of all calculations
- Visual chart showing amount distribution
- Detailed line-by-line summary

![Calculations Summary](https://github.com/user-attachments/assets/4f86597b-058e-45d0-b532-e20968250892)

## 🎯 Calculation Formula

```
Net Weight = Gross Weight + Wastage
J Amount = Net Weight × Rate per gram
Subtotal = J Amount + Making Charges
CGST = Subtotal × 1.5%
SGST = Subtotal × 1.5%
Total Amount = Subtotal + CGST + SGST
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
1. **PDF Export**: Add simple PDF download of the estimate (replace Print button)
2. **CSV History**: Save estimates to a CSV file for record-keeping (replace Save button)
3. **Currency Symbol**: Make ₹ symbol configurable for other currencies
4. **Dark Mode**: Simple toggle for dark/light theme
5. **Multiple Items**: Allow adding 2-3 items per estimate with simple "Add Item" button

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
- Gold 22K/916: ₹5,500/gram
- Gold 20K/833: ₹5,044/gram
- Gold 18K/750: ₹4,564/gram
- Silver: ₹400/gram
- Value Addition (Gold): 13%
- Gold Making Charges: ₹80/gram
- Silver Making Charges: ₹8/gram
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