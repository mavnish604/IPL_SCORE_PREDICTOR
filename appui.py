import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load model
model2 = pickle.load(open('model2.pkl', 'rb'))

# Team and venue lists
teams = ['Lucknow Super Giants', 'Rising Pune Supergiants', 'Punjab Kings', 'Pune Warriors', 'Kolkata Knight Riders', 
         'Mumbai Indians', 'Gujarat Lions', 'Kings XI Punjab', 'Delhi Capitals', 'Rising Pune Supergiant', 
         'Chennai Super Kings', 'Kochi Tuskers Kerala', 'Royal Challengers Bangalore', 'Gujarat Titans', 
         'Sunrisers Hyderabad', 'Delhi Daredevils', 'Deccan Chargers', 'Rajasthan Royals']

venue = ['M Chinnaswamy Stadium', 'Punjab Cricket Association Stadium', 'Feroz Shah Kotla', 'Wankhede Stadium', 
         'Eden Gardens', 'Sawai Mansingh Stadium', 'Rajiv Gandhi International Stadium', 'MA Chidambaram Stadium', 
         'Dr DY Patil Sports Academy', 'Newlands', "St George's Park", 'Kingsmead', 'SuperSport Park', 'Buffalo Park', 
         'New Wanderers Stadium', 'De Beers Diamond Oval', 'OUTsurance Oval', 'Brabourne Stadium', 'Sardar Patel Stadium', 
         'Barabati Stadium', 'Vidarbha Cricket Association Stadium', 'Himachal Pradesh Cricket Association Stadium', 
         'Nehru Stadium', 'Holkar Cricket Stadium', 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium', 
         'Subrata Roy Sahara Stadium', 'Maharashtra Cricket Association Stadium', 'Shaheed Veer Narayan Singh International Stadium', 
         'JSCA International Stadium Complex', 'Sheikh Zayed Stadium', 'Sharjah Cricket Stadium', 'Dubai International Cricket Stadium', 
         'Punjab Cricket Association IS Bindra Stadium', 'Saurashtra Cricket Association Stadium', 'Green Park', 
         'Arun Jaitley Stadium', 'Narendra Modi Stadium', 'Zayed Cricket Stadium', 
         'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium', 'Barsapara Cricket Stadium']

# Streamlit UI
st.set_page_config(page_title='IPL Score Predictor', layout='wide')
st.markdown("""
    <style>
        body { background-color: #121212; color: white; }
        .stApp { background-color: #121212; }
        .stTextInput, .stSelectbox, .stNumberInput { font-size: 18px; }
        .stButton>button { background-color: #ff4b4b; color: white; font-size: 20px; font-weight: bold; padding: 10px; border-radius: 10px; }
        .stButton>button:hover { background-color: #e63946; }
    </style>
""", unsafe_allow_html=True)

st.title("🏏 IPL SCORE PREDICTOR")
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox("🏏 SELECT BATTING TEAM", sorted(teams))
with col2:
    bowling_team = st.selectbox("🎯 SELECT BOWLING TEAM", sorted(teams))

stadium = st.selectbox('🏟️ SELECT STADIUM', sorted(venue))

col3, col4, col5, col6 = st.columns(4)
with col3:
    curr_score = st.number_input('📊 CURRENT SCORE', min_value=0, step=1)

with col4:
    overs = st.number_input('⏳ OVERS DONE (Min: 5.0)', min_value=5.0, step=0.1, format="%.1f")

    # Convert overs into valid cricket format
    overs_int = int(overs)  # Get the over part (before decimal)
    balls = round((overs - overs_int) * 10)  # Get the ball count (after decimal)

    # If balls exceed 5, round up to next over
    if balls > 5:
        overs_int += 1
        balls = 0

    # Create valid overs format (ensures only X.0 to X.5)
    overs = float(f"{overs_int}.{balls}")

    # Display corrected value in Streamlit
    st.write(f"✅ Adjusted Overs: {overs}")


with col5:
    Wickets = st.number_input('❌ WICKETS LOST', min_value=0, max_value=10, step=1)
with col6:
    inning = st.selectbox("🔄 SELECT INNING", [1, 2])

last_five = st.number_input('🔥 Runs scored in last 5 overs', min_value=0, step=1)

if st.button("🎯 PREDICT SCORE"):
    ball_left = 120 - int(overs * 6)
    crr = curr_score / overs
    wkt = 10 - Wickets
    
    in_df = pd.DataFrame({
        'venue': [stadium],  
        'innings': [inning],
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'wickets_remaining': [wkt],
        'score': [curr_score],
        'runs_last_5_overs': [last_five],
        'balls_remaining': [ball_left],
        'crr': [crr]
    })
    
    res = model2.predict(in_df)
    st.subheader(f"🏆 Predicted Score: {int(res[0])}")
