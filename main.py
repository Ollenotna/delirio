import streamlit as st
import utilities

def main():
    # Check login state
    if "player_name" not in st.session_state or st.session_state.player_name is None:
        st.switch_page("pages/login.py")

    # If logged in, show main content
    st.title(f"Welcome {st.session_state.player_name}!")
    st.write("Here are your stats...")

    if st.button("Logout"):
        st.session_state.player_name = None
        st.switch_page("pages/login.py")


    #df_scores, df_pairs, giocatori_to_keep = utilities.load_data()

    st.title('Gigi')

    tabs = st.tabs(["TAB_1", "TAB_2"])
    with tabs[0]:
        # Get plot
        st.text("miao 1")
        #fig = utilities.performance_plot(df_scores, giocatori_to_keep)
        #st.pyplot(fig=fig)
    with tabs[1]:
        st.text("miao")



if __name__ == "__main__":
    main()