# 💰 Salary Tax Comparator: Standard vs 44ADA

A Streamlit web application that helps freelancers and consultants in India compare taxation under standard employment vs. Section 44ADA presumptive taxation schemes.

## 📝 Overview

This application allows users to:
- Calculate tax liability under standard employment taxation
- Calculate tax liability under Section 44ADA presumptive taxation (50% of gross receipts considered as profit)
- Compare both methods side-by-side
- Convert USD salaries to INR using live exchange rates
- Determine the equivalent CTC required under standard taxation to match 44ADA take-home income

## 🔍 Features

- **Dual Tax Calculation**: Compare standard and presumptive taxation side by side
- **Currency Conversion**: Support for both INR and USD inputs with live exchange rates
- **Flexible Input**: Enter salary as monthly or annual figures
- **Detailed Breakdown**: View comprehensive tax calculation including tax, cess, and net income
- **Reverse Engineering**: Determine equivalent CTC under standard taxation to match 44ADA benefits

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shkkonda/tax-comparator.git
   cd tax-comparator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   EXCHANGE_RATE_API_KEY=your_api_key_here
   ```
   Get your free API key from [ExchangeRate-API](https://www.exchangerate-api.com/)

## 📊 Configuration

The application uses a YAML configuration file (`config.yaml`) to define tax slabs and rates. Example structure:

```yaml
tax_slabs:
  - limit: 250000
    rate: 0.0
  - limit: 500000
    rate: 0.05
  - limit: 750000
    rate: 0.10
  - limit: 1000000
    rate: 0.15
  - limit: 1250000
    rate: 0.20
  - limit: 1500000
    rate: 0.25
  - limit: inf
    rate: 0.30

tax_config:
  rebate_limit: 500000
  rebate_amount: 12500
  cess_rate: 0.04
  usd_inr: 83.0  # Fallback rate when API is unavailable
```

## 🚀 Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Navigate to the provided URL (typically http://localhost:8501) in your web browser.

## 📖 How to Use

1. Enter your salary or package amount
2. Select whether the amount is monthly or annual
3. Choose your currency (INR or USD)
4. View the tax breakdown for both standard and 44ADA taxation methods
5. See the equivalent CTC needed under standard taxation to match 44ADA benefits

## 📋 Requirements

- Python 3.7+
- Streamlit
- PyYAML
- Requests
- python-dotenv

These dependencies are listed in `requirements.txt`.

## ⚠️ Disclaimer

This tool is provided for informational purposes only and should not be considered as professional tax advice. Tax laws and regulations are subject to change, and individual circumstances may vary. Please consult with a qualified tax professional for advice specific to your situation.

## 📜 License

[MIT License](LICENSE)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/salary-tax-comparator/issues).

## 📬 Contact

Your Name - [shriharsha@appweave.tech](mailto:shriharsha@appweave.tech)

Project Link: [https://github.com/shkkonda/tax-comparator](https://github.com/shkkonda/tax-comparator)
