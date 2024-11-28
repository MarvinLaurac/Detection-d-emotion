# Detection-d-emotion

# Analyse E-reputation du jeu EA FC 24 (FIFA24) avec Streamlit

Cette application Streamlit vise à visualiser et analyser les tendances de recherche et l'opinion publique sur le jeu vidéo EA FC 24 (FIFA24). Elle utilise des graphiques interactifs et des analyses de sentiment pour fournir une vue d'ensemble de la réputation en ligne du jeu.

## Application dans le cloud

**Lien** : 

## Fonctionnalités

L'application offre les fonctionnalités suivantes :

- **Analyse des avis utilisateurs** : Extraction et analyse des commentaires sur FIFA 24, collectés depuis Jeuxvideo.com.
- **Analyse des sentiments** : Évaluation des sentiments (joy, sad, anger, neutral) exprimés dans les avis utilisateurs, avec une répartition graphique et des détails textuels.
- **Répartition des notes** : Présentation des notes attribuées au jeu, visualisée sous forme de barres colorées.
- **Évolution temporelle** : Étude des tendances des sentiments et des notes au fil du temps.
- **Nuages de mots** : Visualisation des mots les plus fréquemment mentionnés dans les avis utilisateurs.

## Installation et exécution

Pour exécuter cette application, vous devez installer les dépendances suivantes :

```bash
pip install streamlit pandas selenium transformers tensorflow sentencepiece bs4
```

Pour lancer l'application, exécutez :

```bash
streamlit run dataviz.py
``` 

Remplacez `dataviz.py` par le nom de votre fichier script en cas de changement de nom.

## Structure du script

Le script est organisé en plusieurs sections principales :

- **Configuration de la page Streamlit** : Mise en place de l'interface utilisateur et navigation entre les onglets d'analyse.
- **Chargement et préparation des données** : Importation des données à partir de fichiers CSV et prétraitement pour l'analyse.
- **Création de visualisations** : Utilisation de Plotly et Matplotlib pour générer des graphiques interactifs.
- **Analyse de texte** : Utilisation de TextBlob et WordCloud pour l'analyse de sentiment et la génération de nuages de mots.
