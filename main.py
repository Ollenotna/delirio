import streamlit as st
import utilities

def main():
    # Initialize session state
    if "nickname" not in st.session_state:
        st.session_state.nickname = None
    if "loading" not in st.session_state:
        st.session_state.loading = False

    # --- Page selection logic ---
    if st.session_state.nickname is None:
        # User not logged in → show login page
        st.title("🎮 Login")
        show_login_page()
    elif st.session_state.loading:
        # Show loading page
        show_loading_page()
    else:
        # Logged in → show statistics / classifica
        show_stats_pages()

# --- Login page ---
def show_login_page():
    df_players = utilities.load_players()

    selected_nickname = st.selectbox(
        "Seleziona il tuo nome:",
        ["-- Nessun selezionato --"] + df_players['nickname'].to_list()
    )

    if selected_nickname != "-- Nessun selezionato --":
        if st.button("Login"):
            selected_player = df_players[df_players['nickname'] == selected_nickname]['player'].values[0]
            st.session_state.nickname = selected_nickname
            st.session_state.player_name = selected_player
            st.session_state.loading = True
            st.experimental_rerun()

# --- Loading page ---
def show_loading_page():
    st.markdown("<h3 style='text-align:center;'>Caricamento...</h3>", unsafe_allow_html=True)
    my_bar = st.progress(0)

    # Simulate loading
    for i in range(100):
        my_bar.progress(i + 1)
    my_bar.empty()

    # Stop loading and go to stats
    st.session_state.loading = False
    st.experimental_rerun()

# --- Stats / Classifica pages ---
def show_stats_pages():
    st.title(f"Benvenuto, {st.session_state.nickname}!")

    tabs = st.tabs(["Statistiche", "Classifica", "Logout"])

    with tabs[0]:
        try:
            import statistics
            statistics.run()  # Wrap your statistics page logic in run()
        except Exception as e:
            st.error(f"Errore nel caricamento delle statistiche: {e}")

    with tabs[1]:
        try:
            import classifica
            classifica.run()  # Wrap your classifica logic in run()
        except Exception as e:
            st.error(f"Errore nel caricamento della classifica: {e}")

    with tabs[2]:
        if st.button("Logout"):
            st.session_state.nickname = None
            st.session_state.player_name = None
            st.experimental_rerun()


if __name__ == "__main__":
    main()
