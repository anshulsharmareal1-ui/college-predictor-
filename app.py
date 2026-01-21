import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="ExamCracker Pro", layout="centered", page_icon="🎓")

# --- 2. PROFESSIONAL CSS (The "CrackIT" Look) ---
st.markdown("""
    <style>
    /* Clean White Background */
    .stApp { background-color: #ffffff; }
    
    /* Remove default red/orange Streamlit bars */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Input Fields Styling */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    
    /* The "Result Card" - This makes it look pro */
    .result-card {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 16px;
        transition: all 0.2s;
    }
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Status Badges */
    .badge-safe {
        background-color: #dcfce7; color: #166534; 
        padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600;
    }
    .badge-risk {
        background-color: #fee2e2; color: #991b1b; 
        padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600;
    }
    
    /* Titles */
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #111827; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data
def load_data():
    try:
        # Expecting columns: College, Branch, Category, Rank, Exam
        return pd.read_csv("college_data.csv")
    except:
        return pd.DataFrame() # Return empty if no file found

df = load_data()

# --- 4. HEADER ---
st.image("https://cdn-icons-png.flaticon.com/512/2997/2997295.png", width=60)
st.title("ExamCracker Official Predictor")
st.markdown("### The most accurate tool for **JEE Mains & COMEDK**.")

# --- 5. MAIN TABS ---
tab_rank, tab_college = st.tabs(["📊 Rank Predictor", "🏛️ College Predictor"])

# =========================================================
# TAB 1: RANK PREDICTOR (Percentile -> Rank)
# =========================================================
with tab_rank:
    st.markdown("#### Calculate your All India Rank (AIR)")
    
    rank_exam = st.radio("Select Exam", ["JEE Mains (Percentile)", "COMEDK (Marks)"], horizontal=True)
    
    st.markdown("---")
    
    if "JEE" in rank_exam:
        # LOGIC: JEE Rank = (100 - Percentile) * Total Candidates / 100
        # Estimated Candidates for 2026: 14,50,000
        total_candidates = 1450000 
        
        percentile = st.number_input("Enter Your JEE Percentile", 0.0, 100.0, 90.0, step=0.1, format="%.2f")
        
        if st.button("Calculate JEE Rank", type="primary", use_container_width=True):
            if percentile > 0:
                rank = (100 - percentile) * total_candidates / 100
                rank = int(rank)
                if rank == 0: rank = 1
                
                st.markdown(f"""
                <div class="result-card" style="border-left: 5px solid #2563eb; text-align: center;">
                    <h3 style="margin:0; color:#6b7280; font-size:16px;">Predicted All India Rank (AIR)</h3>
                    <h1 style="margin:10px 0; color:#2563eb; font-size:42px;">{rank:,}</h1>
                    <p style="font-size:12px; color:#9ca3af;">Based on ~14.5 Lakh Unique Candidates</p>
                </div>
                """, unsafe_allow_html=True)

    else: # COMEDK Logic (Marks vs Rank)
        marks = st.number_input("Enter COMEDK Marks (out of 180)", 0, 180, 100)
        
        if st.button("Calculate COMEDK Rank", type="primary", use_container_width=True):
            # 2025 Trend Approximation
            if marks > 160: r_min, r_max = 1, 100
            elif marks > 140: r_min, r_max = 100, 500
            elif marks > 110: r_min, r_max = 500, 3500
            elif marks > 90: r_min, r_max = 3500, 9000
            elif marks > 70: r_min, r_max = 9000, 25000
            else: r_min, r_max = 25000, 60000
            
            st.markdown(f"""
            <div class="result-card" style="border-left: 5px solid #ea580c; text-align: center;">
                <h3 style="margin:0; color:#6b7280; font-size:16px;">Predicted COMEDK Rank</h3>
                <h1 style="margin:10px 0; color:#ea580c; font-size:42px;">{r_min} - {r_max}</h1>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# TAB 2: COLLEGE PREDICTOR (Rank -> College)
# =========================================================
with tab_college:
    st.markdown("#### Find your Dream College")
    
    c1, c2 = st.columns(2)
    with c1:
        exam_select = st.selectbox("Exam", ["JEE Mains", "COMEDK"])
    with c2:
        user_rank = st.number_input("Enter Your Rank", 1, 1000000, 5000)
        
    category = st.selectbox("Category", ["General", "OBC", "SC", "ST", "EWS"])

    if st.button("Find My Colleges", type="primary", use_container_width=True):
        
        # 1. FILTER DATA (If CSV exists)
        if not df.empty:
            # Filter logic (ensure your CSV has 'Exam' column)
            mask = (df['Exam'] == exam_select) & (df['Rank'] > user_rank)
            results = df[mask].sort_values(by='Rank').head(10) # Top 10 options
        else:
            # 2. DUMMY DATA (For Design Demo Only - Delete later)
            results = pd.DataFrame([
                {"College": "National Institute of Technology (NIT), Trichy", "Branch": "Civil Engineering", "Rank": user_rank + 500, "Chance": "High"},
                {"College": "IIIT Allahabad", "Branch": "ECE", "Rank": user_rank + 1200, "Chance": "Medium"},
                {"College": "RV College of Engineering", "Branch": "Mechanical", "Rank": user_rank + 2000, "Chance": "High"},
            ])
            if exam_select == "COMEDK":
                results = pd.DataFrame([
                    {"College": "RV College of Engineering", "Branch": "Civil", "Rank": user_rank + 100, "Chance": "Low"},
                    {"College": "BMS College of Engineering", "Branch": "CSE", "Rank": user_rank + 4000, "Chance": "High"},
                ])

        # 3. DISPLAY RESULTS AS CARDS (Professional Look)
        st.write(f"Showing best options for **{exam_select}** Rank **{user_rank}**")
        
        for index, row in results.iterrows():
            # Logic for Badge
            cutoff = row['Rank']
            status = "Safe Choice" if cutoff > user_rank + 1000 else "Ambitious"
            badge_class = "badge-safe" if cutoff > user_rank + 1000 else "badge-risk"
            
            st.markdown(f"""
            <div class="result-card">
                <div style="display:flex; justify-content:space-between; align-items:start;">
                    <div>
                        <h3 style="margin:0; font-size:18px; font-weight:600;">{row['College']}</h3>
                        <p style="margin:4px 0 0 0; color:#4b5563; font-size:14px;">Branch: <b>{row['Branch']}</b></p>
                    </div>
                    <span class="{badge_class}">{status}</span>
                </div>
                <div style="margin-top:12px; display:flex; gap:15px; font-size:13px; color:#6b7280;">
                    <span>⚡ Cutoff Rank: <b>{row['Rank']}</b></span>
                    <span>📂 Category: <b>{category}</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        if results.empty:
            st.warning("No colleges found in this rank range. Try increasing the rank.")
