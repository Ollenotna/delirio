import streamlit as st
import utilities

if "nickname" not in st.session_state:
    st.session_state.nickname = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "loading" not in st.session_state:
    st.session_state.loading = False

def main():
    print(f"DEBUG: nickname in session_state: {'nickname' in st.session_state}")
    print(f"DEBUG: nickname value: {st.session_state.get('nickname', 'NOT SET')}")
    
    # If no one is logged in → show only the login page
    if "nickname" not in st.session_state or not st.session_state.nickname:
        pages = {
            "Login": [
                st.Page("login_delirio.py", title="Accedi"),
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
            "Risultati": [
                st.Page("statistics_delirio.py", title=f"Statistiche"),
                st.Page("classifica.py", title=f"Classifica")
            ],
            "Account": [
                st.Page("logout_delirio.py", title="Logout"),
            ]
        }

    # Create the navigation bar
    pg = st.navigation(pages, position="top")
    pg.run()


if __name__ == "__main__":
    main()