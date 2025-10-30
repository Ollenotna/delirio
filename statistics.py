import streamlit as st
import utilities

# Redirect protection
if "nickname" not in st.session_state or not st.session_state.nickname:
    st.warning("⚠️ Effettua il log in prima. stats")
    st.rerun()


col1, col2 = st.columns([0.3, 0.7], border=False)
with col1:
    st.title('miao')

with col2:
    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px 0;  /* vertical padding instead of fixed height */
        ">
            <h1 style="margin:0; text-align:center; font-size:2rem;">
                Benvenuto, {st.session_state.nickname}!
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )



# Load data
df_scores, df_pairs, giocatori_to_keep = utilities.load_data()

# Cache the performance summary in session state
if "performance_summary" not in st.session_state:
    st.session_state.performance_summary = utilities.performance_plot(df_scores, giocatori_to_keep)

tabs = st.tabs([f"Statistiche di {st.session_state.nickname}", "Statistiche Delirio"])
with tabs[0]:
    st.text('miao')
with tabs[1]:
    st.text("Miao")