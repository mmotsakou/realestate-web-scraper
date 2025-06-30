import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Real Estate Listing Estimator", layout="centered")

st.title("🏘️ Real Estate Listing Counter")
st.write("Enter a real estate website URL to estimate the number of property listings.")

url = st.text_input("Website URL", placeholder="https://www.example.com")

keywords = [
    'real estate', 'properties', 'listings', 'apartments', 'houses',
    'immobilien', 'imoti', 'nekretnine', 'nepremičnine', 'домове', 'недвижими', 'stanova'
]

def fetch_listing_count(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract visible text
        text_blocks = soup.find_all(text=True)
        candidate_blocks = []

        for t in text_blocks:
            txt = t.strip().lower()
            if any(k in txt for k in keywords):
                candidate_blocks.append(txt)

        filtered_text = " ".join(candidate_blocks)
        numbers = re.findall(r'\b\d{3,}\b', filtered_text)
        numbers = [int(n.replace('.', '').replace(',', '')) for n in numbers]

        if numbers:
            return max(numbers)
        else:
            return None
    except Exception as e:
        return f"Error: {e}"

if url:
    with st.spinner("🔍 Crawling and analyzing..."):
        result = fetch_listing_count(url)

    if isinstance(result, int):
        st.success(f"✅ Estimated number of listings: **{result:,}**")
    else:
        st.error(result if isinstance(result, str) else "⚠️ No listing-related numbers found.")
