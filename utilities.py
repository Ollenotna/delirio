import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from collections import Counter
import matplotlib.ticker as ticker

# Filter and suppress only the specific warning related to data validation
warnings.filterwarnings("ignore")

def _read_data(filepath: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    players = pd.read_excel(filepath, sheet_name=1, header=None)
    players = players.rename(columns={0: 'player', 1: 'score'})
    
    scores = pd.read_excel(filepath, sheet_name=0)

    df_scores = pd.DataFrame()
    df_pairs = pd.DataFrame()
    sheet_number = 3
    while True:
        try:
            last_info = pd.read_excel(filepath, sheet_name=sheet_number, nrows=3, header=None).rename(columns={0: 'Info_var', 1: 'Valore'})
            last_data = last_info.loc[last_info["Info_var"] == "Data", "Valore"].values[0]
            last_val_braciola = last_info.loc[last_info["Info_var"] == "Valore braciola", "Valore"].values[0]
            last_val_cocktail = last_info.loc[last_info["Info_var"] == "Valore cocktail", "Valore"].values[0]

            last_match = pd.read_excel(filepath, sheet_name=sheet_number, skiprows=4, usecols='A:C').dropna()
            last_match['Posizione'] = last_match['Posizione'].astype(int)

            last_braciola = pd.read_excel(filepath, sheet_name=sheet_number, skiprows=4, usecols='F').dropna().rename(columns={'Punti Braciola': 'Giocatore'})
            last_braciola['Punto Braciola'] = last_val_braciola
            last_cocktail = pd.read_excel(filepath, sheet_name=sheet_number, skiprows=4, usecols='G').dropna().rename(columns={'Punti Cocktail': 'Giocatore'})
            last_cocktail['Punto Cocktail'] = last_val_cocktail

            last_bonus_malus = pd.read_excel(filepath, sheet_name=sheet_number, skiprows=4, usecols='I:J').dropna()
            last_bonus_malus['Bonus/Malus'] = last_bonus_malus['Bonus/Malus'].astype(int)

            # Creating the pairs dataframe
            last_match['Tappa'] = sheet_number-2
            df_pairs = pd.concat([df_pairs, last_match])
            last_match.drop('Tappa', axis=1, inplace=True)

            last_match = last_match.melt(id_vars=["Posizione"], var_name="Player Type", value_name="Giocatore").drop(columns='Player Type')

            coppie = last_match['Posizione'].max()
            last_score_dict = scores[['Posizione', f"{coppie} coppie"]].dropna().astype(int).set_index("Posizione").to_dict()[f"{coppie} coppie"]

            last_match['Punteggio'] = last_match['Posizione'].map(last_score_dict)
            last_match = last_match.merge(last_braciola, on = 'Giocatore', how = 'outer').fillna(0)
            last_match = last_match.merge(last_cocktail, on = 'Giocatore', how = 'outer').fillna(0)
            last_match = last_match.merge(last_bonus_malus, on = 'Giocatore', how = 'outer').fillna(0).rename(columns={'Bonus/Malus' :'Penalità/Bonus'})
            last_match['Tappa'] = sheet_number-2
            last_match['Coppie'] = coppie
            last_match['Data'] = last_data

            df_scores = pd.concat([df_scores, last_match], ignore_index=True)
            
            sheet_number += 1

            duplicates_classifica = [name for name, count in Counter(last_match['Giocatore']).items() if count > 1]
            duplicates_braciola = [name for name, count in Counter(last_braciola['Giocatore']).items() if count > 1]
            duplicates_cocktail = [name for name, count in Counter(last_cocktail['Giocatore']).items() if count > 1]
            if (duplicates_cocktail or duplicates_classifica or duplicates_braciola):
                print("Data: ", last_data)
            if duplicates_classifica:
                print("Duplicati classifica:", ', '.join(duplicates_classifica))
            if duplicates_braciola:
                print("Duplicati braciola:", ', '.join(duplicates_braciola))
            if duplicates_cocktail:
                print("Duplicati cocktail:", ', '.join(duplicates_cocktail))

        except ValueError:
            # If there is no more sheet, stop the loop
            break

    df_pairs.drop(columns = 'Posizione', inplace = True)
    df_pairs.reset_index(inplace=True, drop=True)

    return df_scores, df_pairs

def _preprocess_scores(df_scores: pd.DataFrame) -> pd.DataFrame:
    # Calculating the rank and punti totali columns
    df_scores['Rank'] = 0
    df_scores['Punti totali'] = 0

    for curr_tappa in df_scores['Tappa'].unique():
        
        temp_rank = df_scores[df_scores['Tappa'] <= curr_tappa]
        curr_data = temp_rank['Data'].max()
        curr_coppie = temp_rank[temp_rank['Data'] == curr_data]['Coppie'].unique()[0]
        temp_rank = temp_rank.groupby('Giocatore')[['Punteggio', 'Punto Braciola', 'Punto Cocktail', 'Penalità/Bonus']].sum()
        temp_rank['Punti totali'] = temp_rank.sum(axis=1).astype(int)
        temp_rank['Rank'] = temp_rank['Punti totali'].rank(method='min', ascending=False).astype(int)
        temp_rank['Tappa'] = curr_tappa
        temp_rank['Data'] = curr_data
        temp_rank['Coppie'] = curr_coppie
        temp_rank.reset_index(inplace=True)

        df_scores = df_scores.merge(temp_rank[['Giocatore', 'Rank', 'Punti totali', 'Tappa', 'Coppie', 'Data']], on = ['Giocatore', 'Tappa', 'Coppie', 'Data'], how = 'outer')

        df_scores['Rank'] = df_scores.filter(like='Rank_').sum(axis=1)
        df_scores.drop(columns=df_scores.filter(like='Rank_').columns, inplace=True)
        df_scores['Punti totali'] = df_scores.filter(like='Punti totali_').sum(axis=1)
        df_scores.drop(columns=df_scores.filter(like='Punti totali_').columns, inplace=True)

    df_scores.fillna(0, inplace=True)

    # Extracting the delta rank for each player

    # Calculating the delta rank that will be displayed in the rank table
    df_scores = df_scores.sort_values(by=["Giocatore", "Tappa"])
    df_scores["Delta Rank"] = -df_scores.groupby("Giocatore")["Rank"].diff().fillna(0).astype(int)
    df_scores = df_scores.sort_values(by=["Tappa", "Rank"], ascending=True).reset_index(drop=True)

    return df_scores

def load_data(filepath: str = 'data/Punteggi.xlsx'):
    df_scores, df_pairs = _read_data(filepath)
    df_scores = _preprocess_scores(df_scores)
    giocatori_to_keep = _filter_players(df_scores)

    return df_scores, df_pairs, giocatori_to_keep

def _filter_players(df_scores: pd.DataFrame) -> list[str]:
    df_scores['Presenza'] = (df_scores['Posizione'] != 0).astype(int)
    df_presenze = df_scores.groupby('Giocatore')[['Presenza']].sum().sort_values(by='Presenza', ascending=False).reset_index()

    # giocatori_to_keep = df_presenze[df_presenze['Presenza'] >= 1]['Giocatore']
    giocatori_to_keep = list(df_scores[(df_scores['Tappa'] == max(df_scores['Tappa']))]['Giocatore'].head(20))
    giocatori_to_keep = giocatori_to_keep + list(df_presenze[df_presenze['Presenza'] >= 5]['Giocatore']) + ['Stefano Bianco']
    giocatori_to_keep = set(giocatori_to_keep)

    return sorted(giocatori_to_keep)

def performance_plot(df_scores, giocatori_to_keep):
    norm_value = 10

    fig, ax = plt.subplots(figsize = (8, 10))

    ## FAI PRIMI 20 + CHI HA GIOCATO ALMENO 5 VOLTE
    df_scores_filt = df_scores[df_scores['Giocatore'].isin(giocatori_to_keep)]
    df_piazzamento = df_scores_filt[['Posizione', 'Giocatore', 'Tappa', 'Coppie', 'Data', 'Rank']].copy()
    # Getting rid of people that didn't partecipate in each tappa
    df_piazzamento = df_piazzamento[df_piazzamento['Posizione'] != 0]
    # Normalizing the posizione to get a common number to measure the piazzamento by doing the scaling
    # Giving the first 5 and the last -5 score
    df_piazzamento['Norm_posizione'] = norm_value/2 - (df_piazzamento['Posizione'] - 1) / (df_piazzamento['Coppie'] - 1) * norm_value

    df_piazzamento_summ = df_piazzamento.groupby('Giocatore')[['Norm_posizione']].mean().sort_values(by='Norm_posizione', ascending=False).reset_index()
    df_piazzamento_summ

    #cmap = sns.diverging_palette(10, 133, as_cmap=True)
    cmap = sns.color_palette("RdYlGn", as_cmap=True)
    sns.scatterplot(df_piazzamento_summ, x = 'Norm_posizione', y='Giocatore', hue='Norm_posizione', palette=cmap, legend=False, s=75, edgecolor='black')

    plt.xlabel("")
    plt.ylabel("")
    plt.xlim(-5, 5)

    # Add color bar at the bottom
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=-5, vmax=5))
    cbar = fig.colorbar(sm, ax=ax, orientation="horizontal", pad=0)
    cbar.ax.set_xticks([])

    # Get color bar position for accurate text placement
    cbar_pos = cbar.ax.get_position()
    x_left = cbar_pos.x0   
    x_right = cbar_pos.x1
    y_pos = cbar_pos.y0 + 0.14  

    # Add labels for first and last positions
    fig.text(x_left, y_pos, "Ultimo posto", ha="left", fontsize=12, color="red", fontweight="bold")
    fig.text(x_right, y_pos, "Primo posto", ha="right", fontsize=12, color="green", fontweight="bold")

    # Adjust layout to fit color bar and labels properly
    plt.subplots_adjust(bottom=0.2)
    plt.grid(axis="y", alpha=0.2)

    plt.title('Performance', weight = 'bold')
    plt.rc("font", size=12)

    # plt.savefig('./Plots/Performance_giocatori.pdf', bbox_inches = 'tight')
    # plt.show()
    return fig