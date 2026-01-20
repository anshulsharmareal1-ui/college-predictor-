import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="ExamCracker Predictor", layout="wide")

# Custom CSS for "Professional" Look
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .css-1d391kg { padding-top: 1rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("🚀 All-India Rank & College Predictor 2026")
st.markdown("Use the tabs below to switch between predicting your **Rank** and your **College**.")

# --- TABS SYSTEM ---
tab1, tab2 = st.tabs(["🏆 Predict My Rank (Marks vs Rank)", "🏛️ Predict My College (Rank vs College)"])

# =========================================================
# TAB 1: RANK PREDICTOR (Marks -> Rank)
# =========================================================
with tab1:
    st.header("Calculate Rank from Marks")
    st.info("💡 Accurate based on 2024-2025 trends.")
    
    col1, col2 = st.columns(2)
    with col1:
        rank_exam = st.selectbox("Select Exam", ["JEE Mains", "COMEDK", "WBJEE", "MHT-CET"], key="rank_exam")
    with col2:
        if rank_exam == "JEE Mains":
            max_marks = 300
        elif rank_exam == "COMEDK":
            max_marks = 180
        elif rank_exam == "WBJEE":
            max_marks = 200
        elif rank_exam == "MHT-CET":
            max_marks = 200
        
        marks = st.number_input(f"Enter Your Marks (out of {max_marks})", min_value=0, max_value=max_marks, value=100)

    if st.button("Predict Rank", type="primary"):
        predicted_rank_min = 0
        predicted_rank_max = 0
        
        # --- LOGIC: JEE MAINS ---
        if rank_exam == "JEE Mains":
            if marks > 280: range_val = (1, 50)
            elif marks > 250: range_val = (50, 500)
            elif marks > 200: range_val = (500, 2500)
            elif marks > 150: range_val = (2500, 10000)
            elif marks > 100: range_val = (10000, 50000)
            else: range_val = (50000, 200000)
            
        # --- LOGIC: COMEDK ---
        elif rank_exam == "COMEDK":
            if marks > 160: range_val = (1, 100)
            elif marks > 140: range_val = (100, 500)
            elif marks > 110: range_val = (500, 3000)
            elif marks > 90: range_val = (3000, 8000)
            elif marks > 70: range_val = (8000, 20000)
            else: range_val = (20000, 60000)

        # --- LOGIC: WBJEE ---
        elif rank_exam == "WBJEE":
            if marks > 150: range_val = (1, 100)
            elif marks > 120: range_val = (100, 500)
            elif marks > 100: range_val = (500, 2000)
            elif marks > 80: range_val = (2000, 5000)
            elif marks > 60: range_val = (5000, 15000)
            else: range_val = (15000, 80000)

        # --- LOGIC: MHT-CET ---
        elif rank_exam == "MHT-CET":
            # Usually percentile based, but mapping raw score to approx rank
            if marks > 180: range_val = (1, 500)
            elif marks > 160: range_val = (500, 2000)
            elif marks > 140: range_val = (2000, 6000)
            elif marks > 100: range_val = (6000, 25000)
            else: range_val = (25000, 100000)

        st.success(f"🎯 Expected Rank: {range_val[0]} - {range_val[1]}")
        st.write("*Note: This is an estimate based on previous year trends.*")

# =========================================================
# TAB 2: COLLEGE PREDICTOR (Rank -> College)
# =========================================================
with tab2:
    st.header("Find Colleges for Your Rank")
    
    # 1. Load Data
    @st.cache_data
    def load_data():
        try:
            # Try to load real data if you uploaded it
            df = pd.read_csv("college_data.csv")
            return df
        except:
            return pd.DataFrame() # Return empty if no file

    df = load_data()

    if df.empty:
        st.warning("⚠️ Data file not found. Please upload 'college_data.csv' to GitHub.")
        # --- FAKE DATA FOR DEMO (Deletes this when you have real data) ---
        data = []
        for i in range(1, 20):
            data.append({"College": f"Demo College {i}", "Exam": "MHT-CET", "Rank": 1000 * i, "Branch": "CSE", "Category": "Open"})
            data.append({"College": f"IIT Demo {i}", "Exam": "JEE Mains", "Rank": 500 * i, "Branch": "CSE", "Category": "Open"})
        df = pd.DataFrame(data)
        # ----------------------------------------------------------------

    # 2. Inputs
    c1, c2, c3 = st.columns(3)
    with c1:
        # Added MHT-CET here!
        exam = st.selectbox("Select Exam", ["JEE Mains", "COMEDK", "WBJEE", "MHT-CET"], key="college_exam")
    with c2:
        user_rank = st.number_input("Enter Your Rank", min_value=1, value=5000, step=100)
    with c3:
        # Check if Category exists in data, else default
        cats = df['Category'].unique() if 'Category' in df.columns else ["Open", "OBC", "SC", "ST"]
        category = st.selectbox("Category", cats)

    if st.button("🚀 Find Colleges", type="primary"):
        # Filter Logic
        # (Make sure your CSV has 'Exam' column!)
        if 'Exam' in df.columns:
            results = df[(df['Exam'] == exam) & (df['Rank'] > user_rank)].sort_values(by='Rank')
        else:
            results = df[df['Rank'] > user_rank].sort_values(by='Rank')
            
        st.write(f"Showing best options for **{exam}** Rank **{user_rank}**:")
        st.dataframe(results, hide_index=True, use_container_width=True)
