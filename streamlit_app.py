# Requirements:
# streamlit
# requests
# beautifulsoup4

import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Real Estate Listings Monitor", layout="wide")
st.title("🏘️ Real Estate Listing Counter (Custom per Website)")

# --- Utility: clean numbers like '138.330' or '138,330'
def parse_number(text):
    num = text.replace('.', '').replace(',', '')
    try:
        return int(num)
    except:
        return None

# --- Site-specific scraping functions

def scrape_njuskalo():
    url = "https://www.njuskalo.hr/nekretnine"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.find("span", class_="page-title-num-adverts")
    if tag:
        return parse_number(tag.text)
    return None

def scrape_nekretnine_rs():
    url = "https://www.nekretnine.rs/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.find("h1")
    if tag and "oglasa" in tag.text:
        match = re.search(r"(\d[\d\.\,]*)\s+oglasa", tag.text)
        if match:
            return parse_number(match.group(1))
    return None

def scrape_4zida():
    url = "https://www.4zida.rs/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.find("span", string=re.compile("oglasa"))
    if tag:
        match = re.search(r"(\d[\d\.\,]*)", tag.text)
        return parse_number(match.group(1))
    return None

def scrape_imoti_bg():
    url = "https://imot.bg/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.find("div", class_="broi_oferti")
    if tag:
        match = re.search(r"(\d[\d\.\,]*)", tag.text)
        return parse_number(match.group(1))
    return None

def scrape_realestatecroatia():
    url = "https://www.realestatecroatia.com/hrv/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.find("div", class_="hero-search-title")
    if tag:
        match = re.search(r"(\d[\d\.\,]*)\s+nekretnina", tag.text)
        if match:
            return parse_number(match.group(1))
    return None

# --- TODO placeholders for unsupported (JS-heavy or unknown) sites
def placeholder_site(name):
    return f"❌ Requires JavaScript rendering or custom logic for {name}"

# --- Mapping of all sites
SITES = {
    "njuskalo.hr": scrape_njuskalo,
    "nekretnine.rs": scrape_nekretnine_rs,
    "4zida.rs": scrape_4zida,
    "bolha.com": lambda: placeholder_site("bolha.com"),
    "imot.bg": scrape_imoti_bg,
    "alo.bg": lambda: placeholder_site("alo.bg"),
    "homes.bg": lambda: placeholder_site("homes.bg"),
    "imoti.net": lambda: placeholder_site("imoti.net"),
    "domaza.bg": lambda: placeholder_site("domaza.bg"),
    "franksalt.com.mt": lambda: placeholder_site("franksalt.com.mt"),
    "dhalia.com": lambda: placeholder_site("dhalia.com"),
    "olx.ba": lambda: placeholder_site("olx.ba"),
    "nekretnine.ba": lambda: placeholder_site("nekretnine.ba"),
}

# --- Run scrapers and show results
st.subheader("📊 Listing Counts by Website")

results = {}
for site, scraper in SITES.items():
    with st.spinner(f"Scraping {site}..."):
        try:
            count = scraper()
            results[site] = count
        except Exception as e:
            results[site] = f"❌ Error: {e}"

# --- Display results
for site, result in results.items():
    st.markdown(f"**{site}**: {result if result else '⚠️ Not Found'}")
