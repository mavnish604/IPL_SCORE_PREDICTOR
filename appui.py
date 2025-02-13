import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load model
model2 = pickle.load(open('model2.pkl', 'rb'))

# Team and venue lists
teams = ['Lucknow Super Giants', 'Rising Pune Supergiants', 'Punjab Kings', 'Pune Warriors', 'Kolkata Knight Riders', 'Mumbai Indians', 'Gujarat Lions', 'Kings XI Punjab', 'Delhi Capitals', 'Rising Pune Supergiant', 'Chennai Super Kings', 'Kochi Tuskers Kerala', 'Royal Challengers Bangalore', 'Gujarat Titans', 'Sunrisers Hyderabad', 'Delhi Daredevils', 'Deccan Chargers', 'Rajasthan Royals']

venue = ['M Chinnaswamy Stadium', 'Punjab Cricket Association Stadium, Mohali', 'Feroz Shah Kotla', 'Wankhede Stadium', 'Eden Gardens', 'Sawai Mansingh Stadium', 'Rajiv Gandhi International Stadium, Uppal', 'MA Chidambaram Stadium, Chepauk', 'Dr DY Patil Sports Academy', 'Newlands', "St George's Park", 'Kingsmead', 'SuperSport Park', 'Buffalo Park', 'New Wanderers Stadium', 'De Beers Diamond Oval', 'OUTsurance Oval', 'Brabourne Stadium', 'Sardar Patel Stadium, Motera', 'Barabati Stadium', 'Brabourne Stadium, Mumbai', 'Vidarbha Cricket Association Stadium, Jamtha', 'Himachal Pradesh Cricket Association Stadium', 'Nehru Stadium', 'Holkar Cricket Stadium', 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium', 'Subrata Roy Sahara Stadium', 'Maharashtra Cricket Association Stadium', 'Shaheed Veer Narayan Singh International Stadium', 'JSCA International Stadium Complex', 'Sheikh Zayed Stadium', 'Sharjah Cricket Stadium', 'Dubai International Cricket Stadium', 'Punjab Cricket Association IS Bindra Stadium, Mohali', 'Saurashtra Cricket Association Stadium', 'Green Park', 'M.Chinnaswamy Stadium', 'Punjab Cricket Association IS Bindra Stadium', 'Rajiv Gandhi International Stadium', 'MA Chidambaram Stadium', 'Arun Jaitley Stadium', 'MA Chidambaram Stadium, Chepauk, Chennai', 'Wankhede Stadium, Mumbai', 'Narendra Modi Stadium, Ahmedabad', 'Arun Jaitley Stadium, Delhi', 'Zayed Cricket Stadium, Abu Dhabi', 'Dr DY Patil Sports Academy, Mumbai', 'Maharashtra Cricket Association Stadium, Pune', 'Eden Gardens, Kolkata', 'Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh', 'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow', 'Rajiv Gandhi International Stadium, Uppal, Hyderabad', 'M Chinnaswamy Stadium, Bengaluru', 'Barsapara Cricket Stadium, Guwahati', 'Sawai Mansingh Stadium, Jaipur', 'Himachal Pradesh Cricket Association Stadium, Dharamsala']

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
    overs = st.number_input('⏳ OVERS (Min: 5)', min_value=5, step=1)
with col5:
    Wickets = st.number_input('❌ WICKETS LOST', min_value=0, max_value=10, step=1)
with col6:
    inning = st.selectbox("🔄 SELECT INNING", [1, 2])

last_five = st.number_input('🔥 Runs scored in last 5 overs', min_value=0, step=1)

if st.button("🎯 PREDICT SCORE"):
    ball_left = 120 - overs * 6
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
