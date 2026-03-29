# IPL Score Predictor

An IPL innings score prediction app built with Streamlit and machine learning. Enter the live match state and the app estimates the final total using venue, innings, wickets, current scoring rate, and recent momentum.

## Overview

This project predicts an IPL team's final innings score from live match inputs. The current app includes a redesigned UI with both dark and light themes and uses a trained model based on IPL ball-by-ball data through the 2025 season.

## Features

- Predicts final IPL innings totals from live match conditions
- Clean Streamlit interface with `Dark` and `Light` theme modes
- Uses batting team, bowling team, venue, innings, score, overs, wickets, and last 5 overs runs
- Displays a projected score with a small expected range
- Model trained on IPL data through the 2025 season

## Tech Stack

- Python
- Streamlit
- Pandas
- scikit-learn
- XGBoost

## Main Files

- `appui.py` - Streamlit application
- `model_3_latest.pkl` - trained prediction model used by the app
- `deliveries_updated_ipl_upto_2025.csv` - IPL delivery-level dataset through the 2025 season
- `final_scores.csv` - final score reference data

## Run Locally

1. Clone the repository:

```bash
git clone https://github.com/mavnish604/IPL_SCORE_PREDICTOR.git
cd IPL_SCORE_PREDICTOR
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the Streamlit app:

```bash
streamlit run appui.py
```

## How To Use

1. Choose the batting team and bowling team.
2. Select the venue and innings.
3. Enter the current score, completed overs, balls in the over, wickets lost, and runs in the last 5 overs.
4. Click `Predict final score` to see the projected total.

## Notes

- The model is trained on IPL data through the 2025 season.
- The prediction is an estimate and should be treated as directional, not guaranteed.

## Live App

- https://iplscorepredt.streamlit.app/

## Contributing

Issues and pull requests are welcome.

## Contact

- LinkedIn: https://www.linkedin.com/in/mavnish604/
