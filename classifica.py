import streamlit as st
import utilities

# Redirect protection
if "player_name" not in st.session_state or not st.session_state.player_name:
    st.warning("⚠️ Effettua il log in prima.")
    st.rerun()

st.title(f"Benvenuto, {st.session_state.nickname}!")

df_scores, df_pairs, giocatori_to_keep = utilities.load_data()


