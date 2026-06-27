import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
import streamlit as st
from google.oauth2.service_account import Credentials

# Authenticate
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)

# Open Google Sheet by ID
spreadsheet_id = "1Ln8fVHSCOueiw64-6IrFMGokYRHoewe-EiVObFDfoEg"
sheet = client.open_by_key(spreadsheet_id).sheet1


def export_to_google(players, heartsgp, heartsw, heartsl,
                    crownsgp, crownsw, crownsl,
                    dicegp, dicew, dicel, dicenp, diceiw,
                    olymgp, olymw, olymg, olyms, olymb):
    # Build dictionary
    data = {
        "Player": players,
        "Hearts Games Played": heartsgp,
        "Hearts Wins": heartsw,
        "Hearts Losses": heartsl,
        "5 Crowns Games Played": crownsgp,
        "5 Crowns Wins": crownsw,
        "5 Crowns Losses": crownsl,
        "Dice Games Played": dicegp,
        "Dice Wins": dicew,
        "Dice Losses": dicel,
        "Dice No Points": dicenp,
        "Dice Instant Wins": diceiw,
        "Olympics Participated": olymgp,
        "Olympic Wins": olymw,
        "Olympic Gold Medals": olymg,
        "Olympic Silver Medals": olyms,
        "Olympic Bronze Medals": olymb
    }

    # Convert dictionary to DataFrame
    df = pd.DataFrame(data)

    # Write dataframe to Google Sheets
    set_with_dataframe(sheet, df)
