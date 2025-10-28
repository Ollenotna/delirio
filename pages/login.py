import streamlit as st

# Simulated player list
players = ["Alice", "Bob", "Charlie", "Diana"]

# Initialize session state
if "player_name" not in st.session_state:
    st.session_state.player_name = None

st.title("🎮 Player Login")

selected_player = st.selectbox("Select your name:", ["-- Choose your name --"] + players)

if selected_player != "-- Choose your name --":
    if st.button("Login"):
        st.session_state.player_name = selected_player
        st.switch_page("pages/main.py")