import streamlit as st
import utilities

col1, col2 = st.columns([0.3, 0.7], border=False)
with col1:
    st.image("images/logo_delirio.png")

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



# Cache the function
@st.cache_data(show_spinner=False)
def load_data_cached():
    return utilities.load_data()

# Load data
df_scores, df_pairs, giocatori_to_keep = load_data_cached()

# Cache the performance summary in session state
if "performance_summary" not in st.session_state:
    st.session_state.performance_summary = utilities.performance_plot(df_scores, giocatori_to_keep)

tabs = st.tabs([f"Statistiche di {st.session_state.nickname}", "Statistiche Delirio"])
with tabs[0]:
    sel_tappa = st.select_slider(
    "Seleziona tappa",
    options = df_scores['Tappa'].unique(),
    value = df_scores['Tappa'].unique()[-1]
    )

    sel_match = utilities.df_sel_match(df_scores, sel_tappa)

    col1, col2, col3, col4 = st.columns(4, border=False)

    with col1:
        st.markdown(
            f"""
            <style>
                @media (max-width: 768px) {{
                    .responsive-container {{
                        padding: 8% !important;
                    }}
                    .label-text {{
                        font-size: 3.5vw !important;
                    }}
                    .value-text {{
                        font-size: 5.5vw !important;
                    }}
                }}
            </style>
            <div class="responsive-container" style="
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100%;
                width: 100%;
                padding: 5%;
                text-align: center;
                box-sizing: border-box;
            ">
                <div class="label-text" style="font-size: 1.8vh; color: gray; margin-bottom: 1vh;">Data</div>
                <div class="value-text" style="font-size: 3vh; font-weight: bold; margin-bottom: 1.5vh;">{sel_match['Data'].iloc[0].strftime('%d/%m/%Y')}</div>
                <div class="label-text" style="font-size: 1.8vh; color: gray; margin-bottom: 1vh;">Tappa</div>
                <div class="value-text" style="font-size: 3vh; font-weight: bold;">{sel_tappa}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        df_sel_tappa = df_pairs[df_pairs['Tappa'] == sel_tappa]
        row = df_sel_tappa[(df_sel_tappa['Player 1'] == st.session_state.player_name) | 
                        (df_sel_tappa['Player 2'] == st.session_state.player_name)]
        
        if not row.empty:
            teammate = row.iloc[0]['Player 2'] if row.iloc[0]['Player 1'] == st.session_state.player_name else row.iloc[0]['Player 1']
        else:
            teammate = 'NA'
        
        st.markdown(
            f"""
            <style>
                @media (max-width: 768px) {{
                    .responsive-container {{
                        padding: 8% !important;
                    }}
                    .label-text {{
                        font-size: 3.5vw !important;
                    }}
                    .value-text {{
                        font-size: 5.5vw !important;
                    }}
                }}
            </style>
            <div class="responsive-container" style="
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100%;
                width: 100%;
                padding: 5%;
                text-align: center;
                box-sizing: border-box;
            ">
                <div class="label-text" style="font-size: 1.8vh; color: gray; margin-bottom: 1vh;">Compagno</div>
                <div class="value-text" style="font-size: 3vh; font-weight: bold; word-break: break-word; max-width: 100%;">{teammate}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        row = sel_match[sel_match['Giocatore'] == st.session_state.player_name]
        
        if not row.empty and row['Presenza'].values[0] == 1:
            sel_posizione = row['Posizione'].values[0].astype(int)
            sel_punti = row['Punteggio'].values[0].astype(int)
            sel_posizione_string = f"{sel_posizione}° / {sel_match['Coppie'].iloc[0]}"
            sel_punti_string = f"+ {sel_punti}"
        else:
            sel_posizione_string = 'NA'
            sel_punti_string = 'NA'
        
        st.markdown(
            f"""
            <style>
                @media (max-width: 768px) {{
                    .responsive-container {{
                        padding: 8% !important;
                    }}
                    .label-text {{
                        font-size: 3.5vw !important;
                    }}
                    .value-text {{
                        font-size: 5.5vw !important;
                    }}
                }}
            </style>
            <div class="responsive-container" style="
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100%;
                width: 100%;
                padding: 5%;
                text-align: center;
                box-sizing: border-box;
            ">
                <div class="label-text" style="font-size: 1.8vh; color: gray; margin-bottom: 1vh;">Piazzamento</div>
                <div class="value-text" style="font-size: 3vh; font-weight: bold; margin-bottom: 1.5vh;">{sel_posizione_string}</div>
                <div class="label-text" style="font-size: 1.8vh; color: gray; margin-bottom: 1vh;">Punteggio</div>
                <div class="value-text" style="font-size: 3vh; font-weight: bold;">{sel_punti_string}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        if not row.empty and row['Presenza'].values[0] == 1:
            sel_pt_braciole = row['Punto Braciola'].values[0].astype(int)
            sel_pt_cocktail = row['Punto Cocktail'].values[0].astype(int)
            sel_pt_bonus_malus = row['Penalità/Bonus'].values[0].astype(int)
            sel_pt_bonus = sel_pt_bonus_malus if sel_pt_bonus_malus > 0 else 0
            sel_pt_malus = sel_pt_bonus_malus if sel_pt_bonus_malus < 0 else 0
        else:
            sel_pt_braciole = 'NA'
            sel_pt_cocktail = 'NA'
            sel_pt_bonus = 'NA'
            sel_pt_malus = 'NA'
        
        st.markdown(
            f"""
            <style>
                @media (max-width: 768px) {{
                    .responsive-container {{
                        padding: 8% !important;
                    }}
                    .label-text {{
                        font-size: 3.5vw !important;
                    }}
                    .value-text {{
                        font-size: 5.5vw !important;
                    }}
                    .bonus-line {{
                        border-left-width: 0.8vw !important;
                    }}
                    .malus-line {{
                        border-left-width: 0.8vw !important;
                    }}
                }}
            </style>
            <div class="responsive-container" style="
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100%;
                width: 100%;
                padding: 5%;
                text-align: center;
                box-sizing: border-box;
            ">
                <div class="label-text" style="font-size: 1.8vh; color: gray; margin-bottom: 1.5vh;">Bonus/Malus</div>
                <div style="display: flex; align-items: stretch; justify-content: center; margin-bottom: 1vh; width: 100%;">
                    <div class="bonus-line" style="border-left: 0.4vw solid #4CAF50; margin-right: 1vw; height: 12vh;"></div>
                    <div class="value-text" style="display: flex; flex-direction: column; gap: 0.5vh; font-size: 2.5vh;">
                        <div style="display: flex; justify-content: space-between; min-width: 80px;">
                            <span>🥩</span>
                            <span style="text-align: right; margin-left: 10px;">{sel_pt_braciole}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; min-width: 80px;">
                            <span>🍸</span>
                            <span style="text-align: right; margin-left: 10px;">{sel_pt_cocktail}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; min-width: 80px;">
                            <span>💎</span>
                            <span style="text-align: right; margin-left: 10px;">{sel_pt_bonus}</span>
                        </div>
                    </div>
                </div>
                <div style="display: flex; align-items: stretch; justify-content: center; width: 100%;">
                    <div class="malus-line" style="border-left: 0.4vw solid #f44336; margin-right: 1vw; height: 4vh;"></div>
                    <div class="value-text" style="display: flex; justify-content: space-between; min-width: 80px; font-size: 2.5vh;">
                        <span>💔</span>
                        <span style="text-align: right; margin-left: 10px;">{sel_pt_malus}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Display vertical performance bar in a container
    col1, col2, col3 = st.columns(3, border=True)

    # Column 1: Performance bar
    with col1:
        fig = utilities.performance_bar(st.session_state.player_name)
        if fig:
            st.pyplot(fig, use_container_width=False, bbox_inches='tight', transparent=True)

    with col2:
        delta_list, curr_delta, curr_position = utilities.delta_plot(df_scores, st.session_state.player_name)
        st.metric("📈 Andamento classifica", f"{curr_position}°", f"{curr_delta} pos", chart_data=delta_list, chart_type="area", border=False)

    with col3:
        pt_braciole, pt_cocktail, pt_bonus, pt_malus = utilities.stats_bonus_malus(
            df_scores, giocatori_to_keep, st.session_state.player_name
        )
        st.markdown(
        f"""
        <b>🎯 Bonus e penalità</b><br><br>

        <div style="display:flex; align-items:center; font-size:18px;">
            <!-- Left line for positives -->
            <div style="border-left:4px solid #4CAF50; margin-right:10px; height:85px;"></div>
            <div style="display:flex; flex-direction:column; gap:4px;">
                <div style="display:flex; justify-content:space-between; width:150px;">
                    <span>🥩 <b>Braciola</b></span>
                    <span style="text-align:right;">{pt_braciole}</span>
                </div>
                <div style="display:flex; justify-content:space-between; width:150px;">
                    <span>🍸 <b>Cocktail</b></span>
                    <span style="text-align:right;">{pt_cocktail}</span>
                </div>
                <div style="display:flex; justify-content:space-between; width:150px;">
                    <span>💎 <b>Bonus</b></span>
                    <span style="text-align:right;">{pt_bonus}</span>
                </div>
            </div>
        </div>

        <br>

        <div style="display:flex; align-items:center; font-size:18px;">
            <!-- Left line for malus -->
            <div style="border-left:4px solid #f44336; margin-right:10px; height:25px;"></div>
            <div style="display:flex; justify-content:space-between; width:150px;">
                <span>💔 <b>Malus</b></span>
                <span style="text-align:right;">{pt_malus}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    n_first, n_second, n_third, n_last = utilities.stats_podio_ultimi(df_scores, giocatori_to_keep, st.session_state.player_name)
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(
        f"<div style='border:3px solid gold; padding:10px; border-radius:10px; text-align:center; font-size:20px;'>🥇 <b>{n_first}</b></div>",
        unsafe_allow_html=True,
    )
    col2.markdown(
        f"<div style='border:3px solid silver; padding:10px; border-radius:10px; text-align:center; font-size:20px;'>🥈 <b>{n_second}</b></div>",
        unsafe_allow_html=True,
    )
    col3.markdown(
        f"<div style='border:3px solid darkgoldenrod; padding:10px; border-radius:10px; text-align:center; font-size:20px;'>🥉 <b>{n_third}</b></div>",
        unsafe_allow_html=True,
    )
    col4.markdown(
        f"<div style='border:3px solid #ff4d4d; padding:10px; border-radius:10px; text-align:center; font-size:20px;'>💀 <b>{n_last}</b></div>",
        unsafe_allow_html=True,
    )
with tabs[1]:
    st.text("Miao")