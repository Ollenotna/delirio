import streamlit as st
import utilities

players = utilities.load_players()

if "player_name" not in st.session_state:
    st.session_state.player_name = None

if "loading" not in st.session_state:
    st.session_state.loading = False

st.title("🎮 Login")

selected_player = st.selectbox("Seleziona il tuo nome:", ["-- Nessun selezionato --"] + players)

# Use a container for the button
button_placeholder = st.empty()

# Show the button only if not clicked yet
if not st.session_state.loading:
    if selected_player != "-- Nessun selezionato --":
        if button_placeholder.button("Login"):
            # Immediately remove button
            button_placeholder.empty()

            # Set session state
            st.session_state.player_name = selected_player
            st.session_state.loading = True

            # Redirect to loading page
            st.rerun()