import streamlit as st
import pickle
import pandas as pd
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="IPL Victory Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED CUSTOM CSS ---
st.markdown("""
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        /* Main Background: Deep Space Gradient */
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #ffffff;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Glassmorphic Container Class */
        .glass-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 25px;
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .glass-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* Customizing Input Widgets to blend in */
        .stSelectbox > div > div {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: white !important;
        }
        .stNumberInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: white !important;
        }

        /* Predict Button Styling */
        .stButton>button {
            background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%);
            color: white;
            font-size: 20px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            border: none;
            border-radius: 50px;
            padding: 1rem 3rem;
            width: 100%;
            cursor: pointer;
            box-shadow: 0 10px 20px rgba(255, 75, 43, 0.3);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 15px 30px rgba(255, 75, 43, 0.5);
        }

        /* Scoreboard Animation */
        .scoreboard {
            background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 15px 35px rgba(0, 176, 155, 0.3);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: slideUp 0.8s ease-out;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .metric-label {
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 28px;
            font-weight: 700;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA & MODEL LOADING ---

@st.cache_resource
def load_model():
    """Load the model only once to boost performance."""
    try:
        return pickle.load(open('model2.pkl', 'rb'))
    except FileNotFoundError:
        st.error("⚠️ Model file 'model2.pkl' not found. Please upload it to the directory.")
        return None

model2 = load_model()

# Teams List
TEAMS = [
    'Chennai Super Kings', 'Deccan Chargers', 'Delhi Capitals', 'Delhi Daredevils',
    'Gujarat Lions', 'Gujarat Titans', 'Kings XI Punjab', 'Kochi Tuskers Kerala',
    'Kolkata Knight Riders', 'Lucknow Super Giants', 'Mumbai Indians', 'Pune Warriors',
    'Punjab Kings', 'Rajasthan Royals', 'Rising Pune Supergiant', 'Rising Pune Supergiants',
    'Royal Challengers Bangalore', 'Sunrisers Hyderabad'
]

# Venue Mapping
VENUE_MAPPING = {
    'Arun Jaitley Stadium (Delhi)': 'Arun Jaitley Stadium',
    'Barabati Stadium (Cuttack)': 'Barabati Stadium',
    'Barsapara Cricket Stadium (Guwahati)': 'Barsapara Cricket Stadium, Guwahati',
    'Ekana Cricket Stadium (Lucknow)': 'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow',
    'Brabourne Stadium (Mumbai)': 'Brabourne Stadium',
    'Buffalo Park': 'Buffalo Park',
    'De Beers Diamond Oval': 'De Beers Diamond Oval',
    'DY Patil Stadium (Mumbai)': 'Dr DY Patil Sports Academy',
    'ACA-VDCA Stadium (Visakhapatnam)': 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
    'Dubai International Stadium': 'Dubai International Cricket Stadium',
    'Eden Gardens (Kolkata)': 'Eden Gardens',
    'Feroz Shah Kotla (Delhi)': 'Feroz Shah Kotla',
    'Green Park (Kanpur)': 'Green Park',
    'HPCA Stadium (Dharamsala)': 'Himachal Pradesh Cricket Association Stadium',
    'Holkar Cricket Stadium (Indore)': 'Holkar Cricket Stadium',
    'JSCA Stadium (Ranchi)': 'JSCA International Stadium Complex',
    'Kingsmead (Durban)': 'Kingsmead',
    'M Chinnaswamy Stadium (Bangalore)': 'M Chinnaswamy Stadium',
    'MA Chidambaram Stadium (Chennai)': 'MA Chidambaram Stadium',
    'MCA Stadium (Pune)': 'Maharashtra Cricket Association Stadium',
    'Narendra Modi Stadium (Ahmedabad)': 'Narendra Modi Stadium, Ahmedabad',
    'Nehru Stadium': 'Nehru Stadium',
    'New Wanderers Stadium': 'New Wanderers Stadium',
    'Newlands (Cape Town)': 'Newlands',
    'OUTsurance Oval': 'OUTsurance Oval',
    'PCA Stadium (Mohali)': 'Punjab Cricket Association IS Bindra Stadium',
    'Rajiv Gandhi Intl Stadium (Hyderabad)': 'Rajiv Gandhi International Stadium',
    'Sardar Patel Stadium (Ahmedabad)': 'Sardar Patel Stadium, Motera',
    'Saurashtra Cricket Assoc. Stadium': 'Saurashtra Cricket Association Stadium',
    'Sawai Mansingh Stadium (Jaipur)': 'Sawai Mansingh Stadium',
    'Shaheed Veer Narayan Singh Stadium': 'Shaheed Veer Narayan Singh International Stadium',
    'Sharjah Cricket Stadium': 'Sharjah Cricket Stadium',
    'Sheikh Zayed Stadium (Abu Dhabi)': 'Sheikh Zayed Stadium',
    "St George's Park": "St George's Park",
    'Subrata Roy Sahara Stadium': 'Subrata Roy Sahara Stadium',
    'SuperSport Park': 'SuperSport Park',
    'Vidarbha Cricket Assoc. Stadium (Nagpur)': 'Vidarbha Cricket Association Stadium, Jamtha',
    'Wankhede Stadium (Mumbai)': 'Wankhede Stadium',
    'Zayed Cricket Stadium (Abu Dhabi)': 'Zayed Cricket Stadium, Abu Dhabi'
}

# --- 4. APP LAYOUT ---

# Sidebar for Team Selection
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/8/84/Indian_Premier_League_Official_Logo.svg", width=180)
    st.markdown("<h2 style='text-align: center; color: white;'>MATCH CONFIG</h2>", unsafe_allow_html=True)
    
    st.markdown("### 🏏 Batting Team")
    batting_team = st.selectbox("Select Batting Team", sorted(TEAMS), label_visibility="collapsed")
    
    st.markdown("### 🎯 Bowling Team")
    bowling_team = st.selectbox("Select Bowling Team", sorted(TEAMS), index=1, label_visibility="collapsed")
    
    st.markdown("---")
    st.info("💡 **Tip:** Ensure you select different teams for batting and bowling.")

# Main Content
st.title("🏏 IPL AI Predictor")
st.markdown("<p style='font-size: 18px; opacity: 0.8;'>Advanced Machine Learning model to forecast innings scores.</p>", unsafe_allow_html=True)

# SECTION 1: MATCH CONDITIONS (Glass Card)
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.markdown("### 🏟️ Match Conditions")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("**Stadium**")
    selected_venue_clean = st.selectbox('Stadium', sorted(VENUE_MAPPING.keys()), label_visibility="collapsed")
with col2:
    st.markdown("**Innings**")
    inning = st.selectbox("Innings", [1, 2], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# SECTION 2: CURRENT GAMEPLAY (Glass Card)
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.markdown("### 📊 Live Score Details")
col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("**Current Score**")
    curr_score = st.number_input('Runs', min_value=0, step=1, label_visibility="collapsed")

with col4:
    st.markdown("**Overs Done**")
    # Logic to handle Overs input cleanly
    overs_input = st.number_input('Overs', min_value=5.0, max_value=19.5, step=0.1, format="%.1f", label_visibility="collapsed")
    if overs_input - int(overs_input) > 0.5:
        st.warning("⚠️ Overs cannot exceed .5")

with col5:
    st.markdown("**Wickets Lost**")
    wickets = st.number_input('Wickets', min_value=0, max_value=9, step=1, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("**🔥 Recent Performance (Last 5 Overs Runs)**")
last_five = st.number_input('Runs in last 5 overs', min_value=0, step=1, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. PREDICTION LOGIC ---

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 PREDICT SCORE"):
    if model2 is None:
        st.error("Model not loaded.")
    else:
        # 1. Validation and Math
        overs_val = float(overs_input)
        overs_int = int(overs_val)
        balls_fraction = round((overs_val - overs_int) * 10)
        
        if balls_fraction > 5:
            st.error("Invalid over input. Balls cannot be > 5")
            st.stop()
            
        total_balls_bowled = (overs_int * 6) + balls_fraction
        balls_remaining = 120 - total_balls_bowled
        wickets_remaining = 10 - wickets
        
        if total_balls_bowled == 0:
            crr = 0
        else:
            crr = curr_score / (total_balls_bowled / 6)

        # 2. Prepare Data
        model_venue_name = VENUE_MAPPING[selected_venue_clean]

        input_df = pd.DataFrame({
            'venue': [model_venue_name],
            'innings': [inning],
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'wickets_remaining': [wickets_remaining],
            'score': [curr_score],
            'runs_last_5_overs': [last_five],
            'balls_remaining': [balls_remaining],
            'crr': [crr]
        })

        # 3. Predict & Display
        try:
            prediction = model2.predict(input_df)
            final_score = int(prediction[0])
            low_range = final_score - 5
            high_range = final_score + 5
            
            # ANIMATED SCOREBOARD HTML
            st.markdown(f"""
                <div class="scoreboard">
                    <h2 style="margin:0; opacity:0.9;">PREDICTED SCORE</h2>
                    <h1 style="font-size: 80px; font-weight: 800; margin: 10px 0;">{final_score}</h1>
                    <p style="font-size: 20px;">Range: {low_range} - {high_range}</p>
                    <div style="display: flex; justify-content: center; gap: 40px; margin-top: 20px;">
                        <div>
                            <div class="metric-label">Current Run Rate</div>
                            <div class="metric-value">{round(crr, 2)}</div>
                        </div>
                        <div>
                            <div class="metric-label">Balls Left</div>
                            <div class="metric-value">{balls_remaining}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Prediction Error: {e}")