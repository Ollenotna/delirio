import streamlit as st
import time

# If somehow no player selected, redirect back to login
if "player_name" not in st.session_state or not st.session_state.player_name:
    st.warning("No player selected. Redirecting to login...")
    st.session_state.loading = False
    st.rerun()

st.markdown("<h3 style='text-align:center;'>Caricamento...</h3>", unsafe_allow_html=True)
my_bar = st.progress(0)

# Fill progress bar
for percent_complete in range(100):
    time.sleep(0.00001)  # adjust speed
    my_bar.progress(percent_complete + 1)

# Optional small pause
time.sleep(0.2)
my_bar.empty()

# Stop showing loading page and redirect to stats page
st.session_state.loading = False
st.rerun()
