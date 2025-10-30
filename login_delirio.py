import streamlit as st
import utilities

df_players = utilities.load_players()

if "nickname" not in st.session_state:
    st.session_state.nickname = None

if "loading" not in st.session_state:
    st.session_state.loading = False

st.markdown("""
    <style>
    .title-container {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 80px;
        padding: 1rem 0;
    }
    .title-container h1 {
        margin: 0;
        font-size: clamp(1.5rem, 5vw, 2.5rem);
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([0.7, 0.3], border=False)

with col1:
    st.markdown('<div class="title-container"><h1>🎮 Login</h1></div>', unsafe_allow_html=True)

with col2:
    st.image("images/logo_delirio.png", use_container_width=True)

selected_nickname = st.selectbox("Seleziona il tuo nome:", ["-- Nessun selezionato --"] + sorted(df_players['nickname'].to_list()))

# Use a container for the button
button_placeholder = st.empty()

# Show the button only if not clicked yet
if not st.session_state.loading:
    if selected_nickname != "-- Nessun selezionato --":
        if button_placeholder.button("Login"):
            # Immediately remove button
            button_placeholder.empty()

            # Set session state
            selected_player = df_players[df_players['nickname']==selected_nickname]['player'].values[0]
            st.session_state.player_name = selected_player
            st.session_state.nickname = selected_nickname
            st.session_state.loading = True

            # Redirect to loading page
            st.rerun()