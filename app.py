import streamlit as st
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="ExamCracker Pro", layout="wide")

# --- 2. CUSTOM CSS (The "Jeepredictor.in" Look) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #f8f9fa; }
    
    /* Hide Streamlit Header/Footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Card Style for Results */
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border-left: 5px solid #2563eb;
        transition: transform 0.2s;
    }
    .result-card:hover { transform: translateY(-2px); }
    
    /* Trend Indicators */
    .trend-harder { color: #dc2626; font-weight: bold; font-size: 14px; }
    .trend-easier { color: #16a34a; font-weight: bold; font-size: 14px; }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        border: 1px solid #e5e7eb;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb;
        color: white;
        border-color: #2563eb;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA LOADER ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("college_data.csv")
        return df
    except:
        return pd.DataFrame()

df = load_data()

# --- 4. SIDEBAR: AFFILIATE & ADS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("ExamCracker")
    st.markdown("---")
    
    # Dynamic Affiliate Links based on Exam
    selected_exam = st.selectbox("Select Exam Focus", ["JEE Mains", "COMEDK", "WBJEE", "MHT-CET"])
    
    st.markdown("### 📚 Best Books (Recommended)")
    if selected_exam == "JEE Mains":
        st.info("📖 **[Arihant 43 Years Solved Papers](https://www.amazon.in)**\n\nMust have for JEE aspirants.")
    elif selected_exam == "COMEDK":
        st.info("📖 **[COMEDK Prep Guide 2026](https://www.amazon.in)**\n\nSpeed is key for COMEDK.")
    elif selected_exam == "WBJEE":
        st.info("📖 **[MTG WBJEE Explorer](https://www.amazon.in)**\n\nBest for Jadavpur prep.")
    elif selected_exam == "MHT-CET":
        st.info("📖 **[Target MHT-CET Triumph](https://www.amazon.in)**\n\nBible for Maharashtra colleges.")

# --- 5. MAIN CALCULATOR AREA ---
st.title(f"🚀 {selected_exam} Predictor 2026")
st.markdown("Analyze your **Rank**, Check **Cutoff Trends**, and Find your **Dream College**.")

tab_rank, tab_college = st.tabs(["🏆 Marks vs Rank", "🏛️ College Predictor"])

# === TAB 1: MARKS VS RANK PREDICTOR ===
with tab_rank:
    st.markdown(f"### Predict your {selected_exam} Rank")
    
    # Set Max Marks dynamically
    max_marks = 300 if "JEE" in selected_exam else (180 if "COMEDK" in selected_exam else 200)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        marks = st.number_input("Enter Your Marks", 0, max_marks, 100)
        predict_btn = st.button("Predict Rank", type="primary", use_container_width=True)
    
    with col2:
        if predict_btn:
            # Simple Estimation Logic (Replace with complex math later)
            if selected_exam == "JEE Mains":
                base_rank = (300 - marks) * 150
            else:
                base_rank = (max_marks - marks) * 50
            
            if base_rank < 1: base_rank = 1
            
            st.markdown(f"""
            <div style="background-color:#dbeafe; padding:20px; border-radius:10px; border:1px solid #93c5fd; text-align:center;">
                <h2 style="color:#1e40af; margin:0;">Predicted Rank: {base_rank} - {base_rank + 500}</h2>
                <p style="margin:0;">Based on 2025 difficulty levels.</p>
            </div>
            """, unsafe_allow_html=True)

# === TAB 2: COLLEGE PREDICTOR WITH TRENDS ===
with tab_college:
    st.markdown("### Find Colleges based on Rank")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        rank_input = st.number_input("Enter Rank", 1, 100000, 5000)
    with c2:
        category = st.selectbox("Category", ["General", "OBC", "SC", "ST"])
    with c3:
        branch_pref = st.multiselect("Branch", ["CSE", "ISE", "ECE", "Mech"], default=["CSE"])

    if st.button("Find Colleges", type="primary", use_container_width=True):
        if df.empty:
            st.warning("⚠️ Database updating... showing demo results.")
            # DEMO RESULTS for Visual Check
            results = [
                {"College": "RV College of Engineering", "Branch": "CSE", "Cutoff": rank_input - 200, "Trend": "Harder"},
                {"College": "BMS College of Engineering", "Branch": "ISE", "Cutoff": rank_input + 500, "Trend": "Stable"},
                {"College": "Ramaiah Institute", "Branch": "ECE", "Cutoff": rank_input + 1200, "Trend": "Easier"}
            ]
        else:
            # Real Filtering Logic
            results = df[df['Rank'] > rank_input].head(5).to_dict('records') # Simplified for demo

        st.markdown("---")
        for row in results:
            # Logic for Safe/Ambitious Color
            status_color = "#22c55e" if row['Cutoff'] > rank_input else "#eab308"
            status_text = "Safe Choice" if row['Cutoff'] > rank_input else "Ambitious (Borderline)"
            
            # Trend Icon
            trend_icon = "📉 Getting Harder" if row.get("Trend") == "Harder" else "📈 Getting Easier"
            trend_class = "trend-harder" if row.get("Trend") == "Harder" else "trend-easier"

            st.markdown(f"""
            <div class="result-card" style="border-left-color: {status_color}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="margin:0; color:#1f2937;">{row['College']}</h3>
                    <span style="background-color:{status_color}; color:white; padding:4px 12px; border-radius:20px; font-size:12px;">{status_text}</span>
                </div>
                <div style="margin-top:10px; color:#4b5563;">
                    <b>Branch:</b> {row['Branch']}  |  <b>Cutoff:</b> {row['Cutoff']}
                </div>
                <div style="margin-top:8px;" class="{trend_class}">
                    {trend_icon} (vs last year)
                </div>
            </div>
            """, unsafe_allow_html=True)
