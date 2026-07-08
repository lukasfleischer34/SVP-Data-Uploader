import streamlit as st
from ExportDataGoogle import export_to_google, load_from_google

# logo and page title
st.set_page_config(
    page_title="SVP Data Uploader",
    page_icon="https://i.postimg.cc/QxQP6nqV/Summer-Village-People-Data-Upload.png",
    layout="wide"
)

# title
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://i.postimg.cc/pTxbmD2q/Summer-Village-transp.png", width=200)
with col2:
    st.markdown("""
    <p style='font-size:50px; font-weight:bold; text-align:left; margin-bottom:0;'>
    Summer Village People
    </p>

    <p style='font-size:40px; font-weight:bold; text-align:left; margin-top:0;'>
    Data Uploader
    </p>
    """, unsafe_allow_html=True)

players, heartsgp, heartsw, heartsl, \
crownsgp, crownsw, crownsl, \
dicegp, dicew, dicel, dicenp, diceiw, \
olymgp, olymw, olymg, olyms, olymb = load_from_google()


def newplayer(name):
    players.append(name.title())
    heartsgp.append(0)
    heartsw.append(0)
    heartsl.append(0)
    crownsgp.append(0)
    crownsw.append(0)
    crownsl.append(0)
    dicegp.append(0)
    dicew.append(0)
    dicel.append(0)
    dicenp.append(0)
    diceiw.append(0)
    olymgp.append(0)
    olymw.append(0)
    olymg.append(0)
    olyms.append(0)
    olymb.append(0)


# reset values
if "confirmed" not in st.session_state:
    st.session_state["confirmed"] = False

if "submitted" not in st.session_state:
    st.session_state["submitted"] = False


# instructions popup
@st.dialog("Instructions and Eligibility")
def instpopup():
    st.subheader("**Eligibility Requirements:**")
    st.write("Minimum of four players.")
    st.write("Minimum of two families.")
    st.write("players who leave the game are ineligible, players who join are eligible.")
    st.write("One winner per game.")
    st.write("Only the player(s) that finishes last is the loser.")
    st.subheader("**Instructions:**")
    st.write("Fill out all fields.")
    st.write("Before adding a new player, check existing players to avoid duplication.")
    st.write("Select 'Neither' for players who neither won or lost.")
    st.write("When finished, press submit. After pressing submit, double check the summary provided. Press 'Confirm' "
             "and 'Close' to finish")
    st.write("Mark physical game sheet to show it has been logged")


if st.button("Instructions"):
    instpopup()

# game selection
game = st.radio(
    "Select the Game:",
    ["Hearts", "5 Crowns", "Dice", "Olympics"],
    index=None,
    key="gamekey"
)

# hearts
if game == "Hearts":
    numplayers = st.number_input(
        "Number of Players:",
        value=4,
        min_value=4,
        step=1
    )

    # player input
    for i in range(numplayers):

        if f"mode_{i}" not in st.session_state:
            st.session_state[f"mode_{i}"] = "existing"

        col1, col2 = st.columns(2)

        with col1:
            if st.button("New Player", key=f"new_btn_{i}"):
                st.session_state[f"mode_{i}"] = "new"

        with col2:
            if st.button("Existing Player", key=f"exist_btn_{i}"):
                st.session_state[f"mode_{i}"] = "existing"

        if st.session_state[f"mode_{i}"] == "new":
            name = st.text_input("New Player:", placeholder="Enter Player Name", key=f"name_{i}")
        else:
            name = st.selectbox(
                "Select Player:",
                players,
                index=None,
                placeholder="Player",
                key=f"name_{i}"
            )

        # win/loss input
        win = st.radio(
            f"{name}:",
            ["Winner", "Loser", "Neither"],
            index=None,
            key=f"win_{i}"
        )

    # popup
    @st.dialog("Confirm Submission")
    def popup():
        st.write(st.session_state["gamekey"].upper())
        for j in range(numplayers):
            if st.session_state[f"win_{j}"] == "Winner":
                st.write(st.session_state[f"name_{j}"] + " - Winner")
            elif st.session_state[f"win_{j}"] == "Loser":
                st.write(st.session_state[f"name_{j}"] + " - Loser")
            else:
                st.write(st.session_state[f"name_{j}"])

        if st.button("Confirm"):
            if not st.session_state["submitted"]:
                # add code to lists, then files, then close files.
                for i in range(numplayers):
                    for j in range(len(players)):
                        if st.session_state[f"name_{i}"].lower() == players[j].lower():
                            heartsgp[j] += 1
                            break
                    else:
                        newplayer(st.session_state[f"name_{i}"])
                        for k in range(len(players)):
                            if st.session_state[f"name_{i}"].lower() == players[k].lower():
                                heartsgp[k] += 1

                    if st.session_state[f"win_{i}"] == "Winner":
                        for j in range(len(players)):
                            if st.session_state[f"name_{i}"].lower() == players[j].lower():
                                heartsw[j] += 1

                    if st.session_state[f"win_{i}"] == "Loser":
                        for j in range(len(players)):
                            if st.session_state[f"name_{i}"].lower() == players[j].lower():
                                heartsl[j] += 1

                export_to_google(players, heartsgp, heartsw, heartsl, crownsgp, crownsw, crownsl, dicegp, dicew, dicel, dicenp, diceiw,
                 olymgp, olymw, olymg, olyms, olymb)

                st.session_state["submitted"] = True
                st.session_state["confirmed"] = True
            else:
                st.warning("Already Submitted")

        if st.session_state["confirmed"]:
            st.success("Successfully Submitted")

            if st.button("Close"):

                st.session_state["gamekey"] = None
                st.session_state["confirmed"] = False
                st.session_state["submitted"] = False

                for i in range(numplayers):
                    st.session_state[f"name_{i}"] = None
                    st.session_state[f"win_{i}"] = None
                    st.session_state[f"mode_{i}"] = "existing"

                st.rerun()


    if st.button("Submit"):
        popup()

# 5 Crowns
if game == "5 Crowns":
    numplayers = st.number_input(
        "Number of Players:",
        value=4,
        min_value=4,
        step=1
    )

    # player input
    for i in range(numplayers):

        if f"mode_{i}" not in st.session_state:
            st.session_state[f"mode_{i}"] = "existing"

        col1, col2 = st.columns(2)

        with col1:
            if st.button("New Player", key=f"new_btn_{i}"):
                st.session_state[f"mode_{i}"] = "new"

        with col2:
            if st.button("Existing Player", key=f"exist_btn_{i}"):
                st.session_state[f"mode_{i}"] = "existing"

        if st.session_state[f"mode_{i}"] == "new":
            name = st.text_input("New Player:", placeholder="Enter Player Name", key=f"name_{i}")
        else:
            name = st.selectbox(
                "Select Player:",
                players,
                index=None,
                placeholder="Player",
                key=f"name_{i}"
            )

        # win/loss input
        win = st.radio(
            f"{name}:",
            ["Winner", "Loser", "Neither"],
            index=None,
            key=f"win_{i}"
        )

    # popup
    @st.dialog("Confirm Submission")
    def popup():
        st.write(st.session_state["gamekey"].upper())
        for j in range(numplayers):
            if st.session_state[f"win_{j}"] == "Winner":
                st.write(st.session_state[f"name_{j}"] + " - Winner")
            elif st.session_state[f"win_{j}"] == "Loser":
                st.write(st.session_state[f"name_{j}"] + " - Loser")
            else:
                st.write(st.session_state[f"name_{j}"])

        if st.button("Confirm"):
            if not st.session_state["submitted"]:
                # add code to lists, then files, then close files.
                for i in range(numplayers):
                    for j in range(len(players)):
                        if st.session_state[f"name_{i}"].lower() == players[j].lower():
                            crownsgp[j] += 1
                            break
                    else:
                        newplayer(st.session_state[f"name_{i}"])
                        for k in range(len(players)):
                            if st.session_state[f"name_{i}"].lower() == players[k].lower():
                                crownsgp[k] += 1

                    if st.session_state[f"win_{i}"] == "Winner":
                        for j in range(len(players)):
                            if st.session_state[f"name_{i}"].lower() == players[j].lower():
                                crownsw[j] += 1

                    if st.session_state[f"win_{i}"] == "Loser":
                        for j in range(len(players)):
                            if st.session_state[f"name_{i}"].lower() == players[j].lower():
                                crownsl[j] += 1

                export_to_google(players, heartsgp, heartsw, heartsl, crownsgp, crownsw, crownsl, dicegp, dicew, dicel, dicenp, diceiw,
                 olymgp, olymw, olymg, olyms, olymb)
                
                st.session_state["submitted"] = True
                st.session_state["confirmed"] = True
            else:
                st.warning("Already Submitted")

        if st.session_state["confirmed"]:
            st.success("Successfully Submitted")

            if st.button("Close"):

                st.session_state["gamekey"] = None
                st.session_state["confirmed"] = False
                st.session_state["submitted"] = False

                for i in range(numplayers):
                    st.session_state[f"name_{i}"] = None
                    st.session_state[f"win_{i}"] = None
                    st.session_state[f"mode_{i}"] = "existing"

                st.rerun()


    if st.button("Submit"):
        popup()

# Dice
if game == "Dice":
    numplayers = st.number_input(
        "Number of Players:",
        value=4,
        min_value=4,
        step=1
    )

    # player input
    for i in range(numplayers):

        if f"mode_{i}" not in st.session_state:
            st.session_state[f"mode_{i}"] = "existing"

        col1, col2 = st.columns(2)

        with col1:
            if st.button("New Player", key=f"new_btn_{i}"):
                st.session_state[f"mode_{i}"] = "new"

        with col2:
            if st.button("Existing Player", key=f"exist_btn_{i}"):
                st.session_state[f"mode_{i}"] = "existing"

        if st.session_state[f"mode_{i}"] == "new":
            name = st.text_input("New Player:", placeholder="Enter Player Name", key=f"name_{i}")
        else:
            name = st.selectbox(
                "Select Player:",
                players,
                index=None,
                placeholder="Player",
                key=f"name_{i}"
            )

        # win/loss
        win = st.radio(
            f"{name}:",
            ["Winner", "Loser", "Neither"],
            index=None,
            key=f"win_{i}"
            )

        if win == "Winner":
            st.radio(
                "Instant Win?",
                ["Yes", "No"],
                index=None,
                key=f"instant_{i}"
                )
            st.session_state[f"board_{i}"] = "Yes"
        
        if win == "Loser":
            st.radio(
                "On Board?",
                ["Yes", "No"],
                index=None,
                key=f"board_{i}"
                )
            st.session_state[f"instant_{i}"] = "No"

        if win == "Neither":
            st.session_state[f"instant_{i}"] = "No"
            st.session_state[f"board_{i}"] = "Yes"
    

    # popup
    @st.dialog("Confirm Submission")
    def popup():
        st.write(st.session_state["gamekey"].upper())
        for j in range(numplayers):
            if st.session_state[f"win_{j}"] == "Winner":
                if st.session_state[f"instant_{j}"] == "Yes":
                    st.write(st.session_state[f"name_{j}"] + " - Winner by Instant Win")
                else:
                    st.write(st.session_state[f"name_{j}"] + " - Winner")
            elif st.session_state[f"win_{j}"] == "Loser":
                if st.session_state[f"board_{j}"] == "No":
                    st.write(st.session_state[f"name_{j}"] + " - Loser, Not on Board")
                else:
                    st.write(st.session_state[f"name_{j}"] + " - Loser")
            else:
                st.write(st.session_state[f"name_{j}"])

        if st.button("Confirm"):
            if not st.session_state["submitted"]:
                # add code to lists, then files, then close files.
                for i in range(numplayers):
                    for j in range(len(players)):
                        if st.session_state[f"name_{i}"].lower() == players[j].lower():
                            dicegp[j] += 1
                            break
                    else:
                        newplayer(st.session_state[f"name_{i}"])
                        for k in range(len(players)):
                            if st.session_state[f"name_{i}"].lower() == players[k].lower():
                                dicegp[k] += 1

                    if st.session_state[f"win_{i}"] == "Winner":
                        for j in range(len(players)):
                            if st.session_state[f"name_{i}"].lower() == players[j].lower():
                                dicew[j] += 1

                    if st.session_state[f"win_{i}"] == "Loser":
                        for j in range(len(players)):
                            if st.session_state[f"name_{i}"].lower() == players[j].lower():
                                dicel[j] += 1

                    if st.session_state[f"board_{i}"] == "No":
                        for j in range(len(players)):
                            if st.session_state[f"name_{i}"].lower() == players[j].lower():
                                dicenp[j] += 1
                                
                    if st.session_state[f"instant_{i}"] == "Yes":
                        for j in range(len(players)):
                            if st.session_state[f"name_{i}"].lower() == players[j].lower():
                                diceiw[j] += 1

                export_to_google(players, heartsgp, heartsw, heartsl, crownsgp, crownsw, crownsl, dicegp, dicew, dicel, dicenp, diceiw,
                 olymgp, olymw, olymg, olyms, olymb)
                
                st.session_state["submitted"] = True
                st.session_state["confirmed"] = True
            else:
                st.warning("Already Submitted")

        if st.session_state["confirmed"]:
            st.success("Successfully Submitted")

            if st.button("Close"):

                st.session_state["gamekey"] = None
                st.session_state["confirmed"] = False
                st.session_state["submitted"] = False

                for i in range(numplayers):
                    st.session_state[f"name_{i}"] = None
                    st.session_state[f"win_{i}"] = None
                    st.session_state[f"mode_{i}"] = "existing"

                st.rerun()


    if st.button("Submit"):
        popup()

# olympics
if game == "Olympics":
    numteams = st.number_input(
        "Number of Teams:",
        value=0,
        min_value=0,
        step=1
    )

    perteam = st.number_input(
        "Number of Players per Team",
        value=0,
        min_value=0,
        step=1
    )

    for i in range(numteams):
        st.write("Team " + str(i + 1))
        for j in range(perteam):
            if f"mode_{(i * perteam) + j}" not in st.session_state:
                st.session_state[f"mode_{(i * perteam) + j}"] = "existing"

            col1, col2 = st.columns(2)

            with col1:
                if st.button("New Player", key=f"new_btn_{(i * perteam) + j}"):
                    st.session_state[f"mode_{(i * perteam) + j}"] = "new"

            with col2:
                if st.button("Existing Player", key=f"exist_btn_{(i * perteam) + j}"):
                    st.session_state[f"mode_{(i * perteam) + j}"] = "existing"

            if st.session_state[f"mode_{(i * perteam) + j}"] == "new":
                name = st.text_input("New Player:", placeholder="Enter Player Name",
                                     key=f"name_{(i * perteam) + j}")
            else:
                name = st.selectbox(
                    "Select Player:",
                    players,
                    index=None,
                    placeholder="Player",
                    key=f"name_{(i * perteam) + j}"
                )

        golds = st.number_input(
            "Golds:",
            value=0,
            min_value=0,
            step=1,
            key=f"golds_{i}"
        )
        silvers = st.number_input(
            "Silvers:",
            value=0,
            min_value=0,
            step=1,
            key=f"silvers_{i}"
        )
        bronzes = st.number_input(
            "Bronzes:",
            value=0,
            min_value=0,
            step=1,
            key=f"bronzes_{i}"
        )
        win = st.radio(
            "Winner?",
            ["Yes", "No"],
            index=None,
            key=f"win_{i}"
        )

    # popup
    @st.dialog("Confirm Submission")
    def popup():
        st.write(st.session_state["gamekey"].upper())
        for j in range(numteams):
            if st.session_state[f"win_{j}"] == "Yes":
                st.write(f"Team {1 + j}: **Winners**")
                st.write("Golds: " + str(st.session_state[f"golds_{j}"]) + " Silvers: " +
                         str(st.session_state[f"silvers_{j}"]) + " Bronzes: " + str(st.session_state[f"bronzes_{j}"]))
            else:
                st.write(f"Team {int(1) + j}:")
                st.write("Golds: " + str(st.session_state[f"golds_{j}"]) + " Silvers: " +
                         str(st.session_state[f"silvers_{j}"]) + " Bronzes: " + str(st.session_state[f"bronzes_{j}"]))
            for i in range(perteam):
                st.write(st.session_state[f"name_{(j * perteam) + i}"])

        if st.button("Confirm"):
            if not st.session_state["submitted"]:
                # add code to lists, then files, then close files.
                for i in range(perteam * numteams):
                    team = i // perteam
                    for j in range(len(players)):
                        if st.session_state[f"name_{i}"].lower() == players[j].lower():
                            olymgp[j] += 1
                            olymg[j] += st.session_state[f"golds_{team}"]
                            olyms[j] += st.session_state[f"silvers_{team}"]
                            olymb[j] += st.session_state[f"bronzes_{team}"]
                            if st.session_state[f"win_{team}"] == "Yes":
                                olymw[j] += 1
                            break
                    else:
                        newplayer(st.session_state[f"name_{i}"])
                        for j in range(len(players)):
                            if st.session_state[f"name_{i}"].lower() == players[j].lower():
                                olymgp[j] += 1
                                olymg[j] += st.session_state[f"golds_{team}"]
                                olyms[j] += st.session_state[f"silvers_{team}"]
                                olymb[j] += st.session_state[f"bronzes_{team}"]
                                if st.session_state[f"win_{team}"] == "Yes":
                                    olymw[j] += 1
                                break
                                    
                export_to_google(players, heartsgp, heartsw, heartsl, crownsgp, crownsw, crownsl, dicegp, dicew, dicel, dicenp, diceiw,
                 olymgp, olymw, olymg, olyms, olymb)
                            
                st.session_state["submitted"] = True
                st.session_state["confirmed"] = True
            else:
                st.warning("Already Submitted")

        if st.session_state["confirmed"]:
            st.success("Successfully Submitted")

            if st.button("Close"):

                st.session_state["gamekey"] = None
                st.session_state["confirmed"] = False
                st.session_state["submitted"] = False

                for i in range(numteams):
                    st.session_state[f"golds_{i}"] = None
                    st.session_state[f"silvers_{i}"] = None
                    st.session_state[f"bronzes_{i}"] = None
                    st.session_state[f"win_{i}"] = None
                    st.session_state[f"mode_{i}"] = "existing"

                for i in range(perteam * numteams):
                    st.session_state[f"name_{i}"] = None

                st.rerun()

    if st.button("Submit"):
        popup()
