# Requirements:
# streamlit
# requests
# beautifulsoup4

import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Real Estate Listing Estimator", layout="centered")
st.title("🏘️ Real Estate Listing Counter + Installment Calculator")

st.write("Enter a real estate website URL (e.g. https://www.realestatecroatia.com/hrv/) to estimate the number of property listings.")

# --- User input
url = st.text_input("Website URL", placeholder="https://www.example.com")

# --- Real estate keywords (localized)
listing_keywords = [
    "nekretnina", "nekretnine", "immobilien", "listings", "ads", "properties",
    "imóveis", "inmuebles", "αγγελίες", "ιδιοκτησίες", "annonser", "προϊόντα",
]

# --- Extraction logic
def find_listing_count(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")

    # Search for keywords with nearby numbers
    pattern = r"(\d{{1,3}}(?:[.,]\d{{3}})*)(?:\s*)(?:{})".format("|".join(listing_keywords))
    matches = re.findall(pattern, text, flags=re.IGNORECASE)

    if matches:
        cleaned = []
        for match in matches:
            num = match.replace('.', '').replace(',', '')
            try:
                cleaned.append(int(num))
            except:
                continue
        if cleaned:
            return max(cleaned)

    return None

# --- Fetch & run
if url:
    with st.spinner("🔍 Crawling and analyzing..."):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=10)
            html = res.text
            count = find_listing_count(html)
            if count:
                st.success(f"✅ Estimated number of listings: **{count:,}**")
            else:
                st.warning("⚠️ Could not find a valid number near real estate keywords.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- Installment Calculator
st.markdown("---")
st.subheader("💰 Estimate Installment Plan")

property_price = st.number_input("Average Property Price (€)", min_value=1000, step=1000, value=100000)
down_payment_percent = st.slider("Down Payment (%)", 0, 100, 20)
interest_rate = st.slider("Annual Interest Rate (%)", 0.0, 15.0, 3.0)
loan_years = st.slider("Loan Term (Years)", 1, 40, 25)

loan_amount = property_price * (1 - down_payment_percent / 100)
monthly_rate = interest_rate / 100 / 12
months = loan_years * 12

if monthly_rate > 0:
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
else:
    monthly_payment = loan_amount / months

total_cost = monthly_payment * months + property_price * (down_payment_percent / 100)

# Output
st.write(f"📉 Loan Amount: €{loan_amount:,.0f}")
st.write(f"💸 Estimated Monthly Payment: **€{monthly_payment:,.2f}**")
st.write(f"💰 Total Payable Over {loan_years} Years: €{total_cost:,.2f}")
