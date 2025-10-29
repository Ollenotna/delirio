import streamlit as st
import utilities

# Redirect protection
if "player_name" not in st.session_state or not st.session_state.player_name:
    st.warning("⚠️ Effettua il log in prima.")
    st.rerun()

st.title(f"Benvenuto, {st.session_state.player_name}!")

df_scores, df_pairs, giocatori_to_keep = utilities.load_data()

tabs = st.tabs(["TAB_1", "TAB_2"])
with tabs[0]:
    fig = utilities.performance_plot(df_scores, giocatori_to_keep)
    st.pyplot(fig)
with tabs[1]:
    st.text("Miao")

