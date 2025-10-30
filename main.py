# main.py
import streamlit as st
import utilities

# -------------------------------
# Initialize session state
# -------------------------------
if "nickname" not in st.session_state:
    st.session_state.nickname = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "loading" not in st.session_state:
    st.session_state.loading = False

# -------------------------------
# Load player data
# -------------------------------
df_players = utilities.load_players()

# -------------------------------
# LOGIN PAGE
# -------------------------------
def show_login():
    st.title("🎮 Login")

    selected_nickname = st.selectbox(
        "Seleziona il tuo nome:",
        ["-- Nessun selezionato --"] + df_players['nickname'].to_list()
    )

    if st.button("Login") and selected_nickname != "-- Nessun selezionato --":
        # Set session state
        st.session_state.nickname = selected_nickname
        st.session_state.logged_in = True
        st.session_state.loading = True
        st.experimental_rerun()


# -------------------------------
# LOADING PAGE
# -------------------------------
def show_loading():
    st.markdown("<h3 style='text-align:center;'>Caricamento...</h3>", unsafe_allow_html=True)
    my_bar = st.progress(0)
    import time

    for percent_complete in range(100):
        time.sleep(0.00001)  # adjust speed
        my_bar.progress(percent_complete + 1)

    time.sleep(0.2)
    my_bar.empty()

    # Stop loading and rerun to show stats
    st.session_state.loading = False
    st.experimental_rerun()


# -------------------------------
# STATISTICS / MAIN PAGE
# -------------------------------
def show_stats():
    st.title(f"Benvenuto, {st.session_state.nickname}!")

    df_scores, df_pairs, giocatori_to_keep = utilities.load_data()

    if "performance_summary" not in st.session_state:
        st.session_state.performance_summary = utilities.performance_plot(df_scores, giocatori_to_keep)

    tabs = st.tabs([f"Statistiche di {st.session_state.nickname}", "Statistiche Delirio"])
    with tabs[0]:
        st.text('Statistiche principali')
    with tabs[1]:
        st.text("Statistiche delirio")


# -------------------------------
# LOGIC SWITCH
# -------------------------------
if not st.session_state.logged_in:
    show_login()
elif st.session_state.loading:
    show_loading()
else:
    show_stats()
