import pickle

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="IPL Score Predictor | AI Cricket Score Prediction Through 2025",
    layout="wide",
    initial_sidebar_state="expanded",
)


if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark"


THEMES = {
    "Dark": {
        "bg_top": "#08111d",
        "bg_bottom": "#111c2b",
        "bg_accent_one": "rgba(231, 111, 81, 0.18)",
        "bg_accent_two": "rgba(42, 157, 143, 0.16)",
        "card": "rgba(12, 23, 38, 0.78)",
        "card_strong": "rgba(14, 27, 43, 0.92)",
        "ink": "#f4efe7",
        "muted": "#a7b4c7",
        "line": "rgba(255, 255, 255, 0.1)",
        "accent": "#f2a46f",
        "accent_deep": "#f6d5bd",
        "accent_soft": "#7ed7c8",
        "shadow": "0 24px 60px rgba(0, 0, 0, 0.34)",
        "sidebar_bg": "linear-gradient(180deg, #08121f 0%, #122235 100%)",
        "sidebar_border": "rgba(255, 255, 255, 0.08)",
        "sidebar_text": "#f4efe7",
        "sidebar_text_soft": "rgba(244, 239, 231, 0.78)",
        "sidebar_kicker": "rgba(244, 239, 231, 0.7)",
        "sidebar_text_muted": "rgba(244, 239, 231, 0.64)",
        "sidebar_panel": "rgba(255, 255, 255, 0.06)",
        "sidebar_panel_border": "rgba(255, 255, 255, 0.1)",
        "sidebar_input_bg": "rgba(255, 255, 255, 0.08)",
        "sidebar_input_border": "rgba(255, 255, 255, 0.12)",
        "sidebar_button_bg": "linear-gradient(135deg, #f2a46f 0%, #e76f51 100%)",
        "sidebar_button_text": "#0b1320",
        "sidebar_button_shadow": "0 18px 40px rgba(0, 0, 0, 0.34)",
        "sidebar_button_hover_shadow": "0 20px 46px rgba(0, 0, 0, 0.42)",
        "hero_bg": "linear-gradient(135deg, rgba(11, 21, 33, 0.94) 0%, rgba(14, 27, 43, 0.86) 100%)",
        "hero_glow": "rgba(231, 111, 81, 0.22)",
        "hero_pill_bg": "rgba(255, 255, 255, 0.06)",
        "hero_pill_border": "rgba(255, 255, 255, 0.1)",
        "chip_bg": "rgba(255, 255, 255, 0.06)",
        "chip_border": "rgba(255, 255, 255, 0.1)",
        "result_bg": "linear-gradient(135deg, #1a2740 0%, #203b5c 52%, #e76f51 150%)",
        "result_shadow": "0 30px 70px rgba(0, 0, 0, 0.35)",
        "result_glow": "rgba(255, 255, 255, 0.1)",
        "alert_border": "rgba(242, 164, 111, 0.2)",
    },
    "Light": {
        "bg_top": "#fbf7f1",
        "bg_bottom": "#f0e8dc",
        "bg_accent_one": "rgba(231, 111, 81, 0.16)",
        "bg_accent_two": "rgba(42, 157, 143, 0.14)",
        "card": "rgba(255, 255, 255, 0.78)",
        "card_strong": "rgba(255, 255, 255, 0.92)",
        "ink": "#122033",
        "muted": "#5f6977",
        "line": "rgba(18, 32, 51, 0.1)",
        "accent": "#e76f51",
        "accent_deep": "#15314b",
        "accent_soft": "#2a9d8f",
        "shadow": "0 24px 60px rgba(17, 24, 39, 0.1)",
        "sidebar_bg": "linear-gradient(180deg, #102239 0%, #18314a 100%)",
        "sidebar_border": "rgba(255, 255, 255, 0.08)",
        "sidebar_text": "#f5f0e8",
        "sidebar_text_soft": "rgba(245, 240, 232, 0.78)",
        "sidebar_kicker": "rgba(245, 240, 232, 0.74)",
        "sidebar_text_muted": "rgba(245, 240, 232, 0.68)",
        "sidebar_panel": "rgba(255, 255, 255, 0.08)",
        "sidebar_panel_border": "rgba(255, 255, 255, 0.12)",
        "sidebar_input_bg": "rgba(255, 255, 255, 0.1)",
        "sidebar_input_border": "rgba(255, 255, 255, 0.12)",
        "sidebar_button_bg": "linear-gradient(135deg, #f4ede3 0%, #f5b78b 100%)",
        "sidebar_button_text": "#102239",
        "sidebar_button_shadow": "0 18px 40px rgba(0, 0, 0, 0.2)",
        "sidebar_button_hover_shadow": "0 20px 46px rgba(0, 0, 0, 0.24)",
        "hero_bg": "linear-gradient(135deg, rgba(255, 255, 255, 0.92) 0%, rgba(255, 255, 255, 0.72) 100%)",
        "hero_glow": "rgba(231, 111, 81, 0.26)",
        "hero_pill_bg": "rgba(18, 32, 51, 0.05)",
        "hero_pill_border": "rgba(18, 32, 51, 0.08)",
        "chip_bg": "rgba(18, 32, 51, 0.05)",
        "chip_border": "rgba(18, 32, 51, 0.08)",
        "result_bg": "linear-gradient(135deg, #112338 0%, #1d3b5b 58%, #e76f51 140%)",
        "result_shadow": "0 30px 70px rgba(17, 35, 56, 0.24)",
        "result_glow": "rgba(255, 255, 255, 0.14)",
        "alert_border": "rgba(231, 111, 81, 0.18)",
    },
}


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

        :root {
            --bg-top: #fbf7f1;
            --bg-bottom: #f0e8dc;
            --card: rgba(255, 255, 255, 0.78);
            --card-strong: rgba(255, 255, 255, 0.92);
            --ink: #122033;
            --muted: #5f6977;
            --line: rgba(18, 32, 51, 0.1);
            --accent: #e76f51;
            --accent-deep: #15314b;
            --accent-soft: #2a9d8f;
            --shadow: 0 24px 60px rgba(17, 24, 39, 0.1);
        }

        html, body, [class*="css"] {
            font-family: 'Manrope', sans-serif;
            color: var(--ink);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, var(--bg-accent-one) 0%, transparent 28%),
                radial-gradient(circle at top right, var(--bg-accent-two) 0%, transparent 24%),
                linear-gradient(180deg, var(--bg-top) 0%, var(--bg-bottom) 100%);
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        div.block-container {
            max-width: 1180px;
            padding-top: 2.4rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            color: var(--ink);
            letter-spacing: -0.03em;
        }

        section[data-testid="stSidebar"] {
            background: var(--sidebar-bg);
            border-right: 1px solid var(--sidebar-border);
        }

        section[data-testid="stSidebar"] * {
            color: var(--sidebar-text);
        }

        .sidebar-brand {
            background: var(--sidebar-panel);
            border: 1px solid var(--sidebar-panel-border);
            border-radius: 28px;
            padding: 1.35rem 1.2rem;
            margin-bottom: 1rem;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
        }

        .sidebar-kicker {
            margin: 0;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--sidebar-kicker);
        }

        .sidebar-brand h2 {
            margin: 0.45rem 0 0.55rem;
            font-family: 'Playfair Display', serif;
            font-size: 1.7rem;
            line-height: 1.05;
            color: var(--sidebar-text);
        }

        .sidebar-brand p {
            margin: 0;
            color: var(--sidebar-text-soft);
            line-height: 1.55;
        }

        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
            color: var(--sidebar-text) !important;
            font-weight: 700;
            font-size: 0.97rem;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
        section[data-testid="stSidebar"] div[data-testid="stNumberInput"] input {
            background: var(--sidebar-input-bg) !important;
            border: 1px solid var(--sidebar-input-border) !important;
            border-radius: 16px !important;
            color: var(--sidebar-text) !important;
            min-height: 50px;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] svg,
        section[data-testid="stSidebar"] div[data-testid="stNumberInput"] button {
            color: var(--sidebar-text) !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
            background: var(--sidebar-panel);
            border: 1px solid var(--sidebar-panel-border);
            border-radius: 999px;
            padding: 0.2rem 0.85rem;
            margin-right: 0.45rem;
        }

        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
            color: var(--sidebar-text-muted) !important;
        }

        section[data-testid="stSidebar"] .stButton > button {
            width: 100%;
            min-height: 54px;
            border: none;
            border-radius: 18px;
            background: var(--sidebar-button-bg);
            color: var(--sidebar-button-text);
            font-size: 0.98rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            box-shadow: var(--sidebar-button-shadow);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: var(--sidebar-button-hover-shadow);
        }

        .hero-card {
            position: relative;
            overflow: hidden;
            background: var(--hero-bg);
            border: 1px solid var(--line);
            border-radius: 32px;
            padding: 2.25rem 2.2rem;
            box-shadow: var(--shadow);
        }

        .hero-card::after {
            content: "";
            position: absolute;
            right: -70px;
            top: -70px;
            width: 240px;
            height: 240px;
            border-radius: 50%;
            background: radial-gradient(circle, var(--hero-glow), transparent 70%);
        }

        .hero-kicker {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.45rem 0.9rem;
            border-radius: 999px;
            background: var(--hero-pill-bg);
            border: 1px solid var(--hero-pill-border);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--accent-deep);
        }

        .hero-card h1 {
            margin: 0.8rem 0 0.9rem;
            font-size: clamp(2.6rem, 5vw, 4.9rem);
            line-height: 0.95;
            max-width: 820px;
            color: var(--ink) !important;
        }

        .hero-card p {
            max-width: 780px;
            margin: 0;
            font-size: 1.08rem;
            line-height: 1.7;
            color: var(--muted);
        }

        .chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
            margin-top: 1.25rem;
        }

        .chip {
            padding: 0.56rem 0.9rem;
            border-radius: 999px;
            background: var(--chip-bg);
            border: 1px solid var(--chip-border);
            color: var(--ink);
            font-size: 0.93rem;
            font-weight: 700;
        }

        .snapshot-grid,
        .feature-grid,
        .result-grid {
            display: grid;
            gap: 1rem;
        }

        .snapshot-grid {
            grid-template-columns: repeat(4, minmax(0, 1fr));
            margin: 1.2rem 0 1rem;
        }

        .snapshot-card,
        .feature-card,
        .copy-card {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 24px;
            box-shadow: var(--shadow);
        }

        .snapshot-card {
            padding: 1.1rem 1.2rem;
        }

        .snapshot-label {
            margin: 0;
            font-size: 0.73rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--muted);
            font-weight: 800;
        }

        .snapshot-value {
            margin: 0.35rem 0 0;
            font-size: 1.7rem;
            font-weight: 800;
            color: var(--ink);
        }

        .snapshot-note {
            margin: 0 0 1.5rem;
            color: var(--muted);
            font-size: 0.98rem;
        }

        .result-card {
            position: relative;
            overflow: hidden;
            background: var(--result-bg);
            border-radius: 32px;
            padding: 2rem;
            box-shadow: var(--result-shadow);
            color: #ffffff;
            margin: 0.9rem 0 1.4rem;
        }

        .result-card::before {
            content: "";
            position: absolute;
            inset: auto -40px -40px auto;
            width: 220px;
            height: 220px;
            border-radius: 50%;
            background: radial-gradient(circle, var(--result-glow), transparent 68%);
        }

        .result-kicker {
            margin: 0;
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: rgba(255, 255, 255, 0.72);
        }

        .result-score {
            margin: 0.5rem 0 0.3rem;
            font-size: clamp(4rem, 9vw, 6.4rem);
            font-weight: 800;
            line-height: 0.92;
            color: #ffffff;
        }

        .result-range {
            margin: 0;
            font-size: 1.08rem;
            color: rgba(255, 255, 255, 0.84);
        }

        .result-grid {
            grid-template-columns: repeat(3, minmax(0, 1fr));
            margin-top: 1.4rem;
        }

        .result-pill {
            padding: 1rem 1.05rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }

        .result-pill p {
            margin: 0;
        }

        .result-pill-label {
            font-size: 0.72rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: rgba(255, 255, 255, 0.72);
            font-weight: 800;
        }

        .result-pill-value {
            margin-top: 0.35rem;
            font-size: 1.28rem;
            font-weight: 800;
            color: #ffffff;
        }

        .section-heading {
            margin: 1.8rem 0 0.75rem;
            font-size: 1.65rem;
            color: var(--ink) !important;
        }

        .feature-grid {
            grid-template-columns: repeat(3, minmax(0, 1fr));
            margin-top: 0.8rem;
        }

        .feature-card {
            padding: 1.35rem;
        }

        .feature-card h3 {
            margin: 0 0 0.55rem;
            font-family: 'Manrope', sans-serif;
            font-size: 1.04rem;
            letter-spacing: -0.02em;
            color: var(--ink) !important;
        }

        .feature-card p {
            margin: 0;
            color: var(--muted);
            line-height: 1.65;
        }

        .copy-card {
            margin-top: 1rem;
            padding: 1.45rem 1.55rem;
            background: var(--card-strong);
        }

        .copy-card h3 {
            margin: 0 0 0.65rem;
            font-size: 1.4rem;
            color: var(--ink) !important;
        }

        .copy-card p {
            margin: 0;
            color: var(--muted);
            line-height: 1.75;
            font-size: 1rem;
        }

        [data-testid="stAlert"] {
            border-radius: 18px;
            border: 1px solid var(--alert-border);
        }

        @media (max-width: 900px) {
            div.block-container {
                padding-top: 1.35rem;
            }

            .hero-card {
                padding: 1.5rem;
                border-radius: 24px;
            }

            .snapshot-grid,
            .feature-grid,
            .result-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


active_theme = THEMES.get(st.session_state.theme_mode, THEMES["Dark"])

st.markdown(
    f"""
    <style>
        :root {{
            --bg-top: {active_theme["bg_top"]};
            --bg-bottom: {active_theme["bg_bottom"]};
            --bg-accent-one: {active_theme["bg_accent_one"]};
            --bg-accent-two: {active_theme["bg_accent_two"]};
            --card: {active_theme["card"]};
            --card-strong: {active_theme["card_strong"]};
            --ink: {active_theme["ink"]};
            --muted: {active_theme["muted"]};
            --line: {active_theme["line"]};
            --accent: {active_theme["accent"]};
            --accent-deep: {active_theme["accent_deep"]};
            --accent-soft: {active_theme["accent_soft"]};
            --shadow: {active_theme["shadow"]};
            --sidebar-bg: {active_theme["sidebar_bg"]};
            --sidebar-border: {active_theme["sidebar_border"]};
            --sidebar-text: {active_theme["sidebar_text"]};
            --sidebar-text-soft: {active_theme["sidebar_text_soft"]};
            --sidebar-kicker: {active_theme["sidebar_kicker"]};
            --sidebar-text-muted: {active_theme["sidebar_text_muted"]};
            --sidebar-panel: {active_theme["sidebar_panel"]};
            --sidebar-panel-border: {active_theme["sidebar_panel_border"]};
            --sidebar-input-bg: {active_theme["sidebar_input_bg"]};
            --sidebar-input-border: {active_theme["sidebar_input_border"]};
            --sidebar-button-bg: {active_theme["sidebar_button_bg"]};
            --sidebar-button-text: {active_theme["sidebar_button_text"]};
            --sidebar-button-shadow: {active_theme["sidebar_button_shadow"]};
            --sidebar-button-hover-shadow: {active_theme["sidebar_button_hover_shadow"]};
            --hero-bg: {active_theme["hero_bg"]};
            --hero-glow: {active_theme["hero_glow"]};
            --hero-pill-bg: {active_theme["hero_pill_bg"]};
            --hero-pill-border: {active_theme["hero_pill_border"]};
            --chip-bg: {active_theme["chip_bg"]};
            --chip-border: {active_theme["chip_border"]};
            --result-bg: {active_theme["result_bg"]};
            --result-shadow: {active_theme["result_shadow"]};
            --result-glow: {active_theme["result_glow"]};
            --alert-border: {active_theme["alert_border"]};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    """Load the trained model once for the session."""
    try:
        with open("model_3_latest.pkl", "rb") as model_file:
            return pickle.load(model_file)
    except FileNotFoundError:
        st.error("Model file `model_3_latest.pkl` was not found in the project directory.")
        return None


model = load_model()


TEAMS = [
    "Chennai Super Kings",
    "Deccan Chargers",
    "Delhi Capitals",
    "Delhi Daredevils",
    "Gujarat Lions",
    "Gujarat Titans",
    "Kings XI Punjab",
    "Kochi Tuskers Kerala",
    "Kolkata Knight Riders",
    "Lucknow Super Giants",
    "Mumbai Indians",
    "Pune Warriors",
    "Punjab Kings",
    "Rajasthan Royals",
    "Rising Pune Supergiant",
    "Rising Pune Supergiants",
    "Royal Challengers Bangalore",
    "Sunrisers Hyderabad",
]


VENUE_MAPPING = {
    "Arun Jaitley Stadium (Delhi)": "Arun Jaitley Stadium",
    "Barabati Stadium (Cuttack)": "Barabati Stadium",
    "Barsapara Cricket Stadium (Guwahati)": "Barsapara Cricket Stadium",
    "Brabourne Stadium (Mumbai)": "Brabourne Stadium",
    "Buffalo Park": "Buffalo Park",
    "De Beers Diamond Oval": "De Beers Diamond Oval",
    "DY Patil Stadium (Mumbai)": "Dr DY Patil Sports Academy",
    "ACA-VDCA Stadium (Visakhapatnam)": "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium",
    "Dubai International Stadium": "Dubai International Cricket Stadium",
    "Eden Gardens (Kolkata)": "Eden Gardens",
    "Ekana Cricket Stadium (Lucknow)": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium",
    "Feroz Shah Kotla (Delhi)": "Feroz Shah Kotla",
    "Green Park (Kanpur)": "Green Park",
    "HPCA Stadium (Dharamsala)": "Himachal Pradesh Cricket Association Stadium",
    "Holkar Cricket Stadium (Indore)": "Holkar Cricket Stadium",
    "JSCA Stadium (Ranchi)": "JSCA International Stadium Complex",
    "Kingsmead (Durban)": "Kingsmead",
    "M Chinnaswamy Stadium (Bangalore)": "M Chinnaswamy Stadium",
    "MA Chidambaram Stadium (Chennai)": "MA Chidambaram Stadium",
    "Maharaja Yadavindra Singh Stadium (Mullanpur)": "Punjab Cricket Association IS Bindra Stadium",
    "MCA Stadium (Pune)": "Maharashtra Cricket Association Stadium",
    "Narendra Modi Stadium (Ahmedabad)": "Narendra Modi Stadium",
    "Nehru Stadium": "Nehru Stadium",
    "New Wanderers Stadium": "New Wanderers Stadium",
    "Newlands (Cape Town)": "Newlands",
    "OUTsurance Oval": "OUTsurance Oval",
    "PCA Stadium (Mohali)": "Punjab Cricket Association IS Bindra Stadium",
    "Rajiv Gandhi Intl Stadium (Hyderabad)": "Rajiv Gandhi International Stadium",
    "Sardar Patel Stadium (Ahmedabad)": "Sardar Patel Stadium",
    "Saurashtra Cricket Assoc. Stadium": "Saurashtra Cricket Association Stadium",
    "Sawai Mansingh Stadium (Jaipur)": "Sawai Mansingh Stadium",
    "Shaheed Veer Narayan Singh Stadium": "Shaheed Veer Narayan Singh International Stadium",
    "Sharjah Cricket Stadium": "Sharjah Cricket Stadium",
    "Sheikh Zayed Stadium (Abu Dhabi)": "Sheikh Zayed Stadium",
    "St George's Park": "St George's Park",
    "Subrata Roy Sahara Stadium": "Subrata Roy Sahara Stadium",
    "SuperSport Park": "SuperSport Park",
    "Vidarbha Cricket Assoc. Stadium (Nagpur)": "Vidarbha Cricket Association Stadium",
    "Wankhede Stadium (Mumbai)": "Wankhede Stadium",
    "Zayed Cricket Stadium (Abu Dhabi)": "Zayed Cricket Stadium",
}


def render_hero():
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-kicker">AI Cricket Analytics</div>
            <h1>IPL Score Predictor</h1>
            <p>
                Estimate live Indian Premier League innings totals with a polished IPL score predictor
                powered by machine learning. The model is trained on IPL ball-by-ball data through the
                2025 season, giving you a fast cricket score prediction based on teams, venue, overs,
                wickets, and recent scoring momentum.
            </p>
            <div class="chip-row">
                <span class="chip">Live innings forecast</span>
                <span class="chip">Venue-aware prediction</span>
                <span class="chip">Model trained through 2025</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_snapshot(curr_score, wickets, overs_display, crr, balls_remaining):
    wickets_in_hand = 10 - wickets
    st.markdown(
        f"""
        <div class="snapshot-grid">
            <div class="snapshot-card">
                <p class="snapshot-label">Current Score</p>
                <p class="snapshot-value">{curr_score}/{wickets}</p>
            </div>
            <div class="snapshot-card">
                <p class="snapshot-label">Overs</p>
                <p class="snapshot-value">{overs_display}</p>
            </div>
            <div class="snapshot-card">
                <p class="snapshot-label">Run Rate</p>
                <p class="snapshot-value">{crr:.2f}</p>
            </div>
            <div class="snapshot-card">
                <p class="snapshot-label">Balls Left</p>
                <p class="snapshot-value">{balls_remaining}</p>
            </div>
        </div>
        <p class="snapshot-note">
            Wickets in hand: <strong>{wickets_in_hand}</strong>. Use the live inputs on the left to
            refine the forecast before running the prediction.
        </p>
        """,
        unsafe_allow_html=True,
    )


def render_result(final_score, low_range, high_range, crr, balls_remaining, last_five):
    st.markdown(
        f"""
        <div class="result-card">
            <p class="result-kicker">Predicted Finish</p>
            <p class="result-score">{final_score}</p>
            <p class="result-range">Expected range: {low_range} to {high_range}</p>
            <div class="result-grid">
                <div class="result-pill">
                    <p class="result-pill-label">Current Run Rate</p>
                    <p class="result-pill-value">{crr:.2f}</p>
                </div>
                <div class="result-pill">
                    <p class="result-pill-label">Balls Remaining</p>
                    <p class="result-pill-value">{balls_remaining}</p>
                </div>
                <div class="result-pill">
                    <p class="result-pill-label">Runs Last 5 Overs</p>
                    <p class="result-pill-value">{last_five}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


sorted_teams = sorted(TEAMS)
default_batting_index = sorted_teams.index("Chennai Super Kings")
default_bowling_index = sorted_teams.index("Mumbai Indians")


with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <p class="sidebar-kicker">IPL Score Prediction</p>
            <h2>Build the live match state</h2>
            <p>
                Keep the inputs focused and clean. The model reads venue, innings pressure,
                wickets in hand, and recent acceleration to estimate the final total.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.radio("Theme", ["Dark", "Light"], horizontal=True, key="theme_mode")
    batting_team = st.selectbox("Batting team", sorted_teams, index=default_batting_index)
    bowling_team = st.selectbox("Bowling team", sorted_teams, index=default_bowling_index)
    selected_venue_clean = st.selectbox("Venue", sorted(VENUE_MAPPING.keys()))
    inning = st.radio("Innings", [1, 2], horizontal=True)

    curr_score = st.number_input("Current score", min_value=0, step=1, value=82)
    overs_completed = st.slider("Completed overs", min_value=5, max_value=19, value=10)
    balls_in_over = st.select_slider("Balls into the current over", options=[0, 1, 2, 3, 4, 5], value=2)
    wickets = st.number_input("Wickets lost", min_value=0, max_value=9, step=1, value=3)
    last_five = st.number_input("Runs in the last 5 overs", min_value=0, step=1, value=44)

    st.caption("Predictions are calibrated for innings states from 5.0 to 19.5 overs.")
    predict_now = st.button("Predict final score")


overs_display = f"{overs_completed}.{balls_in_over}"
total_balls_bowled = (overs_completed * 6) + balls_in_over
balls_remaining = 120 - total_balls_bowled
crr = curr_score / (total_balls_bowled / 6) if total_balls_bowled else 0


render_hero()
render_snapshot(curr_score, wickets, overs_display, crr, balls_remaining)


if predict_now:
    if model is None:
        st.error("The model could not be loaded.")
    elif batting_team == bowling_team:
        st.error("Choose different teams for batting and bowling.")
    elif last_five > curr_score:
        st.error("Runs in the last 5 overs cannot be greater than the current score.")
    else:
        wickets_remaining = 10 - wickets
        model_venue_name = VENUE_MAPPING[selected_venue_clean]

        input_df = pd.DataFrame(
            {
                "venue": [model_venue_name],
                "innings": [inning],
                "batting_team": [batting_team],
                "bowling_team": [bowling_team],
                "wickets_remaining": [wickets_remaining],
                "score": [curr_score],
                "runs_last_5_overs": [last_five],
                "balls_remaining": [balls_remaining],
                "crr": [crr],
            }
        )

        try:
            prediction = model.predict(input_df)
            final_score = int(prediction[0])
            low_range = final_score - 5
            high_range = final_score + 5
            render_result(final_score, low_range, high_range, crr, balls_remaining, last_five)
            st.caption("Forecasts are estimates, not guarantees, and should be read as directional match intelligence.")
        except Exception as exc:
            st.error(f"Prediction error: {exc}")


st.markdown(
    """
    <div class="copy-card">
        <p>
            Fast IPL innings forecasting based on venue, wickets, run rate, and recent momentum.
            The model is trained on IPL data through the 2025 season.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
