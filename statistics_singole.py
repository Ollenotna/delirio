import streamlit as st
import utilities

# Redirect protection
if "player_name" not in st.session_state or not st.session_state.player_name:
    st.warning("⚠️ Effettua il log in prima.")
    st.rerun()

st.title(f"Benvenuto, {st.session_state.player_name}!")

# Load data
df_scores, df_pairs, last_match, giocatori_to_keep = utilities.load_data()

# Cache the performance summary in session state
if "performance_summary" not in st.session_state:
    st.session_state.performance_summary = utilities.performance_plot(df_scores, giocatori_to_keep)

st.markdown(
    "<div style='font-size:24px; font-weight:bold; margin-bottom:-5px;'>Ultima tappa</div>",
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4, border=False)

with col1:
    st.markdown(
    f"""
    <div style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 188px;  /* same height for all columns */
            text-align: center;
        ">
        <div style="font-size:14px; color:gray;">Data</div>
        <div style="font-size:22px; font-weight:bold;">{last_match['Data'][0].strftime('%d/%m/%Y')}</div>
        <div style="height:8px;"></div> <!-- small spacing -->
        <div style="font-size:14px; color:gray;">Tappa</div>
        <div style="font-size:22px; font-weight:bold;">{last_match['Tappa'][0]}</div>
    </div>
    """,
    unsafe_allow_html=True
    )
        
with col2:    
    df_last_tappa = df_pairs[df_pairs['Tappa'] == last_match['Tappa'][0]]
    # Find the row where the player is either Player 1 or Player 2
    row = df_last_tappa[(df_last_tappa['Player 1'] == st.session_state.player_name) | 
                        (df_last_tappa['Player 2'] == st.session_state.player_name)]

    # Determine the teammate
    teammate = row.iloc[0]['Player 2'] if row.iloc[0]['Player 1'] == st.session_state.player_name else row.iloc[0]['Player 1']

    st.markdown(
    f"""
    <div style="
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 180px;  /* fixed height to center inside */
        text-align: center;
    ">
        <div style="font-size:14px; color:gray;">Compagno</div>
        <div style="font-size:22px; font-weight:bold;">{teammate}</div>
        
    </div>
    """,
    unsafe_allow_html=True
    )

with col3:    
    last_posizione = last_match[last_match['Giocatore']==st.session_state.player_name]['Posizione'].values[0]
    last_punti = last_match[last_match['Giocatore']==st.session_state.player_name]['Punteggio'].values[0]
    
    st.markdown(
    f"""
    <div style="
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 188px;  /* fixed height to center inside */
        text-align: center;
    ">
        <div style="font-size:14px; color:gray;">Piazzamento</div>
        <div style="font-size:22px; font-weight:bold;">{last_posizione}° / {last_match['Coppie'][0]} </div>
        <div style="height:8px;"></div> <!-- small spacing -->
        <div style="font-size:14px; color:gray;">Punteggio</div>
        <div style="font-size:22px; font-weight:bold;"> + {last_punti}</div>
    </div>
    """,
    unsafe_allow_html=True
    )

with col4:
    last_pt_braciole = last_match[last_match['Giocatore']==st.session_state.player_name]['Punto Braciola'].values[0].astype(int)
    last_pt_cocktail = last_match[last_match['Giocatore']==st.session_state.player_name]['Punto Cocktail'].values[0].astype(int)
    last_pt_bonus_malus = last_match[last_match['Giocatore']==st.session_state.player_name]['Penalità/Bonus'].values[0].astype(int)
    last_pt_bonus = last_pt_bonus_malus if last_pt_bonus_malus > 0 else 0
    last_pt_malus = last_pt_bonus_malus if last_pt_bonus_malus < 0 else 0

    st.markdown(
    f"""
        <div style="
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 180px;  /* fixed height to center inside */
        text-align: center;
    ">

    <div style="font-size:14px; color:gray;">Bonus/Malus</div>

    <div style="display:flex; align-items:center; font-size:22px;">
        <!-- Left line for positives -->
        <div style="border-left:4px solid #4CAF50; margin-right:10px; height:85px;"></div>
        <div style="display:flex; flex-direction:column; gap:4px;">
            <div style="display:flex; justify-content:space-between; width:80px;">
                <span>🥩 <b></b></span>
                <span style="text-align:right;">{last_pt_braciole}</span>
            </div>
            <div style="display:flex; justify-content:space-between; width:80px;">
                <span>🍸 <b></b></span>
                <span style="text-align:right;">{last_pt_cocktail}</span>
            </div>
            <div style="display:flex; justify-content:space-between; width:80px;">
                <span>💎 <b></b></span>
                <span style="text-align:right;">{last_pt_bonus}</span>
            </div>
        </div>
    </div>

    <div style="display:flex; align-items:center; font-size:22px;">
        <!-- Left line for malus -->
        <div style="border-left:4px solid #f44336; margin-right:10px; height:25px;"></div>
        <div style="display:flex; justify-content:space-between; width:80px;">
            <span>💔 <b></b></span>
            <span style="text-align:right;">{last_pt_malus}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
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
    <b>🎯 Punteggi Totali</b><br><br>

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