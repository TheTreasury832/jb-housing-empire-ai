
import streamlit as st
from pathlib import Path
import pandas as pd
import markdown
import json
from openai import OpenAI

st.set_page_config(page_title="JB Housing Empire AI", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: cyan;'>JB Housing Empire AI System</h1>",
    unsafe_allow_html=True
)
st.image("logo.jpg", width=200)

# Sidebar navigation
page = st.sidebar.selectbox("Navigation", [
    "Home", "Settings (API Key)", "Dashboard", "Lead Intake", "Deal Analyzer",
    "Calculators", "Script Generator", "LOI Builder", "Empire Manual"
])

# Session state for API key
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if page == "Settings (API Key)":
    st.header("🔐 OpenAI GPT Key Setup")
    st.session_state.api_key = st.text_input("Enter your OpenAI API Key", type="password")
    if st.session_state.api_key:
        st.success("✅ API Key saved in session.")

elif page == "Home":
    st.header("Welcome to JB Housing Empire AI System")
    st.markdown("### Modules:")
    st.write("- Lead Scraping & CRM")
    st.write("- Full Deal Analyzer")
    st.write("- GPT-Powered Script Builder")
    st.write("- LOI Templates")
    st.write("- Multifamily Underwriting")
    st.write("- Empire Training Manual")

elif page == "Dashboard":
    st.header("📊 KPI Dashboard")
    kpi_data = json.load(open("KPI.json"))
    st.write("**Total Leads:**", kpi_data.get("totalLeads", 0))
    st.write("**Response Rate:**", f"{kpi_data.get('responseRate', 0)}%")
    st.write("**Conversions:**", kpi_data.get("conversions", 0))
    st.write("**Cash Flow:**", f"${kpi_data.get('cashFlow', 0)}")
    st.write("**ROI:**", f"{kpi_data.get('roi', 0)}%")

elif page == "Lead Intake":
    st.header("📁 Deal Flow Leads")
    uploaded = st.file_uploader("Upload deal_flow.csv", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df)

elif page == "Deal Analyzer":
    st.header("📈 Deal Analyzer")
    address = st.text_input("Enter Property Address")
    if st.button("Analyze with GPT"):
        if not st.session_state.api_key:
            st.warning("Please enter your API key in the Settings tab.")
        else:
            client = OpenAI(api_key = st.session_state.api_key
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a real estate underwriting assistant."},
                        {"role": "user", "content": f"/analyze {address}"}
                    ]
                )
                st.success("GPT Analysis:")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

elif page == "Calculators":
    st.header("🧮 Deal Calculators")
    st.info("Use other tabs for full calculators (SubTo, Seller Finance, etc.)")

elif page == "Script Generator":
    st.header("🤖 GPT Script Generator")
    deal_type = st.selectbox("Deal Type", ["SubTo", "Wrap", "Seller Finance", "Cash", "Hybrid"])
    if st.button("Generate Script with GPT"):
        if not st.session_state.api_key:
            st.warning("Please enter your API key in the Settings tab.")
        else:
            client = OpenAI(api_key = st.session_state.api_key
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You generate real estate negotiation scripts in a 5x5 format."},
                        {"role": "user", "content": f"/script {deal_type}"}
                    ]
                )
                st.success("GPT Script:")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

elif page == "LOI Builder":
    st.header("📄 LOI Generator")
    structure = st.selectbox("Deal Structure", ["SubTo", "Seller Finance", "Wrap", "Hybrid"])
    name = st.text_input("Seller Name")
    price = st.number_input("Offer Price")
    if st.button("Generate LOI with GPT"):
        if not st.session_state.api_key:
            st.warning("Please enter your API key in the Settings tab.")
        else:
            client = OpenAI(api_key = st.session_state.api_key
            try:
                prompt = f"/loi {structure}\nSeller: {name}\nPrice: ${price}"
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You write formal real estate Letters of Intent."},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.success("GPT LOI:")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

elif page == "Empire Manual":
    st.header("📘 Empire Manual")
    with open("empire_manual.md", "r") as md_file:
        st.markdown(md_file.read())
