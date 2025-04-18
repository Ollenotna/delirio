import streamlit as st
import utilities


def main():
    df_scores, df_pairs, giocatori_to_keep = utilities.load_data()

    st.title('Gigi')

    tabs = st.tabs(["TAB_1", "TAB_2"])
    with tabs[0]:
        # Get plot
        fig = utilities.performance_plot(df_scores, giocatori_to_keep)
        st.pyplot(fig=fig)
    with tabs[1]:
        st.text("VCIODUJVJ")



if __name__ == "__main__":
    main()