import streamlit as st
import utilities

# Redirect protection
if "nickname" not in st.session_state or not st.session_state.nickname:
    st.warning("⚠️ Effettua il log in prima. class")
    st.rerun()

st.title(f"Benvenuto, {st.session_state.nickname}!")


