import streamlit as st

# Clear session state
st.session_state.player_name = None
st.success("Hai effettuato il log out!")


# Optionally, rerun main
st.rerun()