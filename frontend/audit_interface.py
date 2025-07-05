import streamlit as st

st.title("DeFi Sentinel – C++ Smart Contract Auditor")
uploaded_file = st.file_uploader("Upload a C++ contract file", type="cpp")

if uploaded_file:
    code = uploaded_file.read().decode("utf-8")
    st.code(code, language="cpp")
    st.success("Contract uploaded. Click 'Run Audit' to begin.")