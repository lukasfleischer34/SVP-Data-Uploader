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

def load_from_google():
    data = sheet.get_all_values()

    players = []
    heartsgp = []
    heartsw = []
    heartsl = []
    crownsgp = []
    crownsw = []
    crownsl = []
    dicegp = []
    dicew = []
    dicel = []
    dicenp = []
    diceiw = []
    olymgp = []
    olymw = []
    olymg = []
    olyms = []
    olymb = []

    for row in data[1:]:  
        players.append(row[0])
        heartsgp.append(int(row[1]))
        heartsw.append(int(row[2]))
        heartsl.append(int(row[3]))
        crownsgp.append(int(row[4]))
        crownsw.append(int(row[5]))
        crownsl.append(int(row[6]))
        dicegp.append(int(row[7]))
        dicew.append(int(row[8]))
        dicel.append(int(row[9]))
        dicenp.append(int(row[10]))
        diceiw.append(int(row[11]))
        olymgp.append(int(row[12]))
        olymw.append(int(row[13]))
        olymg.append(int(row[14]))
        olyms.append(int(row[15]))
        olymb.append(int(row[16]))

    return (
        players, heartsgp, heartsw, heartsl,
        crownsgp, crownsw, crownsl,
        dicegp, dicew, dicel, dicenp, diceiw,
        olymgp, olymw, olymg, olyms, olymb
    )


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
