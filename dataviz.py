import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Chargement des données
df = pd.read_csv("resultats_reviews.csv")
 
# Titre du dashboard
st.title("Analyse des Avis des Joueurs - FIFA 24")
 
# Section 1 : Histogramme de la distribution des notes
st.header("Distribution des Notes")
fig_notes = px.histogram(
    df,
    x="notes",
    nbins=20,
    title="Distribution des Notes des Joueurs",
    labels={"notes": "Notes", "count": "Nombre de joueurs"},
    color_discrete_sequence=["#636EFA"]
)
fig_notes.update_layout(bargap=0.2)
st.plotly_chart(fig_notes)
 
# Section 2 : Vérification et traitement des dates
# Conversion des dates




try:
    df['dates'] = pd.to_datetime(df['dates'], errors='coerce')  # Forcer la conversion
    df['dates'] = df['dates'].dt.date  # Garder uniquement la partie date
except Exception as e:
    st.error(f"Erreur lors de la conversion des dates : {e}")
    st.stop()  # Arrête l'exécution si les dates ne peuvent pas être traitées



# Suppression des lignes avec des dates invalides
df = df.dropna(subset=['dates'])

# Ajout d'une colonne "année" pour le filtrage
df['année'] = pd.to_datetime(df['dates']).dt.year  # On convertit en datetime temporairement pour extraire l'année

# Filtrer uniquement les données des années 2023 et 2024
df = df[df['année'].isin([2023, 2024])]

# Vérifier si des données existent pour ces années
if df.empty:
    st.warning("Aucune donnée disponible pour les années 2023 et 2024.")
else:
    # Widget pour sélectionner l'année (limité à 2023 et 2024)
    selected_year = st.selectbox(
        "Sélectionnez une année", 
        [2023, 2024], 
        key="année_select"
    )  # Ajout d'une clé unique

    # Filtrer les données selon l'année sélectionnée
    filtered_df = df[df['année'] == selected_year]

    # Supprimer la colonne 'cleanned_review' avant l'affichage
    df_without_cleaned_review = filtered_df.drop(columns=['cleanned_review'])

    # Afficher le dataframe sans la colonne 'cleanned_review'
    st.write(df_without_cleaned_review)

    # Afficher les résultats filtrés
    st.write(f"Résultats pour l'année {selected_year} :")
    #st.write(filtered_df)

    # Exemple de visualisation : histogramme des notes avec un code couleur
    if not filtered_df.empty:
        # Ajout d'une colonne catégorielle pour les couleurs (exemple basé sur les notes)
        filtered_df['catégories'] = pd.cut(
            filtered_df['notes'], 
            bins=[0, 2, 4, 6, 8, 10], 
            labels=["Très mauvais", "Mauvais", "Moyen", "Bon", "Excellent"]
        )

        # Graphique avec couleur
        fig = px.histogram(
            filtered_df, 
            x="notes", 
            color="catégories",  # Couleur basée sur les catégories
            nbins=20, 
            title=f"Distribution des notes pour l'année {selected_year}",
            color_discrete_map={
                "Très mauvais": "red",
                "Mauvais": "orange",
                "Moyen": "yellow",
                "Bon": "lightgreen",
                "Excellent": "green",
            },
            labels={"catégories": "Catégories de notes"}
        )

        st.plotly_chart(fig)
    

 
 
# Section 3 : Relation entre la note et l'accord sur les avis
st.header("Relation entre Notes et Accord sur les Avis")
fig_note_accord = px.scatter(
    df,
    x="notes",
    y="accords_avis",
    color="classification",
    title="Relation entre Note et Accord",
    labels={"notes": "Note", "accords_avis": "Accords (J'aime)"},
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig_note_accord)
 
# Section 4 : Analyse des sentiments
st.header("Analyse des Sentiments")
 


print( df['cleanned_review'])
# Calcul des polarités
df['polarité'] = df['cleanned_review'].apply(lambda x: TextBlob(x).sentiment.polarity)
 
# Distribution des polarités
fig_polarity = px.histogram(
    df,
    x="polarité",
    nbins=20,
    title="Distribution de la Polarité des Sentiments",
    labels={"polarité": "Polarité", "count": "Nombre de commentaires"},
    color_discrete_sequence=["#00CC96"]
)
st.plotly_chart(fig_polarity)
 
# Polarité moyenne
polarité_moyenne = df['polarité'].mean()
st.write(f"**Polarité moyenne : {polarité_moyenne:.2f}**")
 
# Nuages de mots pour sentiments positifs et négatifs
commentaires_négatifs = " ".join(df[df['polarité'] < 0]['cleanned_review'])
 
# Nuages de mots
wordcloud_négatif = WordCloud(width=800, height=400, background_color="white").generate(commentaires_négatifs)
 
st.subheader("Nuage de Mots - Avis Négatifs")
st.image(wordcloud_négatif.to_array())


 
# Polarité moyenne par classification
st.header("Polarité Moyenne par Classification")
polarité_moyenne_classification = df.groupby("classification")["polarité"].mean().reset_index()
fig_classification = px.bar(
    polarité_moyenne_classification,
    x="classification",
    y="polarité",
    title="Polarité Moyenne par Classification",
    labels={"classification": "Classification", "polarité": "Polarité Moyenne"},
    color_discrete_sequence=["#AB63FA"]
)
st.plotly_chart(fig_classification)


# Section 5 : Pourcentage des classifications
df['polarité'] = df['polarité'].apply(lambda x: (x + 1) if x < 0 else x)
st.header("Répartition des Classifications")
classification_counts = df['classification'].value_counts(normalize=True) * 100
fig_classification_pie = px.pie(
    names=classification_counts.index,
    values=classification_counts.values,
    title="Répartition des Classifications en Pourcentage",
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(fig_classification_pie)