import streamlit as st
import utilities

def main():
    # If no one is logged in → show only the login page
    if "player_name" not in st.session_state or not st.session_state.player_name:
        pages = {
            "Login": [
                st.Page("login.py", title="Accedi"),
            ],
        }
    elif "loading" in st.session_state and st.session_state.loading:
        # Show only loading page
        pages = {
            "Loading": [st.Page("loading_delirio.py", title="Caricamento")],
        }
    else:
        # If logged in → show only the stats page
        pages = {
            "Statistiche": [
                st.Page("statistics_singole.py", title=f"Statistiche di {st.session_state.player_name}"),
                st.Page("statistics_gruppo.py", title=f"Statistiche di gruppo")
            ],
            "Account": [
                st.Page("logout.py", title="Logout"),
            ]
        }

    # Create the navigation bar
    pg = st.navigation(pages, position="top")
    pg.run()


if __name__ == "__main__":
    main()