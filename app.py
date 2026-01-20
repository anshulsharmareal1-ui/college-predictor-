import streamlit as st
import pandas as pd

st.set_page_config(page_title="College Predictor", layout="wide")

# Clean styling
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .css-1d391kg { padding-top: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 JEE & COMEDK College Predictor")
st.write("Enter your rank to see your best college options.")

col1, col2 = st.columns(2)
with col1:
    exam = st.selectbox("Select Exam", ["JEE Mains", "COMEDK", "WBJEE"])
    rank = st.number_input("Enter Your Rank", min_value=1, value=5000, step=100)
with col2:
    category = st.selectbox("Category", ["General", "OBC", "SC", "ST"])
    branch = st.multiselect("Preferred Branch", ["CSE", "ECE", "Mech", "Civil"], default=["CSE"])

if st.button("🚀 Predict My Colleges"):
    st.success(f"Searching best {branch} colleges for Rank {rank} in {exam}...")
    # Placeholder data for now - we will connect real data later!
    st.info("Top Recommendation: RV College of Engineering (95% Chance)")
    st.info("Safe Option: BMS College of Engineering (100% Chance)")
