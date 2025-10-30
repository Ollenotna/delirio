import streamlit as st

# Clear session state
st.session_state.nickname = None
st.success("Hai effettuato il log out!")


# Optionally, rerun main
st.rerun()