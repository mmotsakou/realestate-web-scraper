# Requirements:
# streamlit
# playwright
# playwright install

import streamlit as st
import asyncio
from playwright.async_api import async_playwright
import re

# ------------- Setup page
st.set_page_config(page_title="Real Estate Listings Counter", layout="wide")
st.title("🏘️ Real Estate Listings Counter (Accurate with Playwright)")

# ------------- Helper functions
def clean_number(text):
    match = re.search(r"\d[\d.,]*", text)
    if match:
        return int(match.group(0).replace('.', '').replace(',', ''))
    return None

# ------------- Site configuration
SITES = {
    "https://www.njuskalo.hr/nekretnine": {
        "selector": "span.page-title-num-adverts",
    },
    "https://www.nekretnine.rs/": {
        "selector": "h1:has-text('oglasa')",
    },
    "https://www.4zida.rs/": {
        "selector": "span:has-text('oglasa')",
    },
    "https://www.bolha.com/nepremicnine": {
        "selector": "div.result-filter-count",  # placeholder
    },
    "https://imot.bg/": {
        "selector": "div.broi_oferti",
    },
    "https://www.alo.bg/realni-imoti/": {
        "selector": "h1.page-title",  # placeholder
    },
    "https://homes.bg/": {
        "selector": "div.box > div > h2",  # placeholder
    },
    "https://imoti.net/bg/obiavi": {
        "selector": "span.counter",  # placeholder
    },
    "https://www.domaza.bg/": {
        "selector": "div.hits",  # placeholder
    },
    "https://www.franksalt.com.mt/": {
        "selector": "h3:has-text('Properties')",  # placeholder
    },
    "https://www.dhalia.com/": {
        "selector": "div.total-count",  # placeholder
    },
    "https://www.olx.ba/nekretnine": {
        "selector": "h1",  # placeholder
    },
    "https://www.nekretnine.ba/": {
        "selector": "h1",  # placeholder
    },
}

# ------------- Scraper function
async def fetch_listing_counts():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        results = {}

        for url, config in SITES.items():
            with st.spinner(f"Scraping {url}..."):
                try:
                    await page.goto(url, timeout=30000)
                    await page.wait_for_timeout(2000)
                    element = await page.query_selector(config["selector"])
                    if element:
                        text = await element.text_content()
                        count = clean_number(text or "")
                        results[url] = count if count else "❌ Not found"
                    else:
                        results[url] = "❌ Element not found"
                except Exception as e:
                    results[url] = f"❌ Error: {str(e)}"

        await browser.close()
        return results

# ------------- Run scraping on button click
if st.button("🔍 Start Scraping All Sites"):
    counts = asyncio.run(fetch_listing_counts())

    st.markdown("### 📊 Results")
    for site, result in counts.items():
        st.write(f"**{site}** → {result}")
