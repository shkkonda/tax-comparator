import yaml
import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()


def load_tax_config(file_path="config.yaml"):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    # Parse tax slabs
    tax_slabs = []
    for slab in data["tax_slabs"]:
        limit = float("inf") if slab["limit"] == "inf" else slab["limit"]
        tax_slabs.append((limit, slab["rate"]))

    # Parse config
    config = data["tax_config"]
    rebate_limit = config["rebate_limit"]
    rebate_amount = config["rebate_amount"]
    cess_rate = config["cess_rate"]
    usd_inr = config["usd_inr"]

    return usd_inr, tax_slabs, rebate_limit, rebate_amount, cess_rate

USD_TO_INR, TAX_SLABS, REBATE_LIMIT, REBATE_AMOUNT, CESS_RATE = load_tax_config()


def convert_to_annual(salary, period):
    return salary * 12 if period == "Monthly" else salary


def fetch_usd_to_inr():
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    try:
        if not api_key:
            raise ValueError("Missing API key in environment variables.")
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
        response = requests.get(url)
        data = response.json()
        if data['result'] == 'success':
            return data['conversion_rates'].get('INR', USD_TO_INR)
        st.warning("Using fallback rate: Failed to fetch live USD to INR.")
    except Exception as e:
        st.warning(f"Using fallback rate: {e}")
    return USD_TO_INR


def convert_currency(amount, currency):
    if currency == "INR":
        return amount, 1.0
    rate = fetch_usd_to_inr()
    return amount * rate, rate


def calculate_taxable_income_44ada(gross_income):
    return gross_income * 0.50


def calculate_tax(income):
    tax = 0
    prev_limit = 0
    for limit, rate in TAX_SLABS:
        if income > limit:
            tax += (limit - prev_limit) * rate
            prev_limit = limit
        else:
            tax += (income - prev_limit) * rate
            break
    if income <= REBATE_LIMIT:
        tax = max(0, tax - REBATE_AMOUNT)
    cess = tax * CESS_RATE
    return tax, cess


def compute_standard_tax(gross_income):
    taxable = gross_income
    tax, cess = calculate_tax(taxable)
    net_income = gross_income - tax - cess
    return gross_income, taxable, tax, cess, net_income


def compute_44ada_tax(gross_income):
    taxable = calculate_taxable_income_44ada(gross_income)
    tax, cess = calculate_tax(taxable)
    net_income = gross_income - tax - cess
    return gross_income, taxable, tax, cess, net_income


def reverse_engineer_ctc(target_inhand):
    for ctc in range(int(target_inhand), int(target_inhand * 3)):
        _, _, _, _, net = compute_standard_tax(ctc)
        if net >= target_inhand:
            return ctc
    return None


def render_tax_breakdown(title, gross, taxable, tax, cess, net):
    st.markdown(f"### {title}")
    st.write(f"**Gross Income:** ₹{gross:,.2f}")
    st.write(f"**Taxable Income:** ₹{taxable:,.2f}")
    st.write(f"**Tax Payable:** ₹{tax:,.2f}")
    st.write(f"**Cess:** ₹{cess:,.2f}")
    st.write(f"**Net In-hand:** ₹{net:,.2f}")
    st.write(f"**Monthly In-hand:** ₹{net/12:,.2f}")


def main():
    st.title("💰 Salary Tax Comparator: Standard vs 44ADA")

    # --- Inputs ---
    salary_input = st.number_input("Enter your Salary / Package", min_value=0.0, value=0.0)
    period = st.selectbox("Select Input Type", ["Annual", "Monthly"])
    currency = st.selectbox("Currency", ["INR", "USD"])

    # --- Conversion ---
    annual_salary = convert_to_annual(salary_input, period)
    salary_in_inr, fx_rate = convert_currency(annual_salary, currency)

    if currency == "USD":
        st.info(f"💱 1 USD = ₹{fx_rate:.2f} INR (live rate or fallback)")

    # --- Tax Calculations ---
    std = compute_standard_tax(salary_in_inr)
    ada = compute_44ada_tax(salary_in_inr)

    # --- Output ---
    st.subheader("📊 Tax Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        render_tax_breakdown("Standard Tax Method", *std)
    with col2:
        render_tax_breakdown("44ADA Method", *ada)

    # --- Reverse Calculation ---
    if salary_input > 0:
        required_ctc = reverse_engineer_ctc(ada[-1])
        if required_ctc:
            st.markdown("---")
            st.success(
                f"💼 Required CTC to get same In-hand as 44ADA under Standard Tax Method: ₹{required_ctc:,.2f}"
            )


if __name__ == "__main__":
    main()