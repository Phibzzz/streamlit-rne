"""
Module pour les composants de l'interface utilisateur
"""

import streamlit as st
import pandas as pd
from config.settings import APP_TITLE, APP_DESCRIPTION, APP_ICON, APP_LAYOUT, APP_INITIAL_SIDEBAR_STATE, ELUS_CONFIG, DEFAULT_ELU_TYPE

def setup_page(title: str = APP_TITLE, description: str = APP_DESCRIPTION):
    """Configure la page Streamlit"""
    st.set_page_config(
        page_title=title,
        page_icon=APP_ICON,
        layout=APP_LAYOUT,
        initial_sidebar_state=APP_INITIAL_SIDEBAR_STATE
    )

def display_elu_type_selector() -> str:
    """
    Affiche un sélecteur élégant pour choisir le type d'élu
    Retourne le type d'élu sélectionné
    """
    st.markdown("### 🗳️ Choisissez le type d'élu à explorer")
    
    # Créer des colonnes pour un affichage élégant
    cols = st.columns(3)
    
    # Organiser les options en groupes
    options_display = []
    for key, config in ELUS_CONFIG.items():
        option_text = f"{config['icon']} **{config['name']}**\n\n*{config['description']}*"
        options_display.append((key, option_text, config['name']))
    
    # Utiliser un selectbox avec des options formatées
    selected_key = st.selectbox(
        "Type d'élu",
        options=[opt[0] for opt in options_display],
        format_func=lambda x: next(opt[2] for opt in options_display if opt[0] == x),
        index=list(ELUS_CONFIG.keys()).index(DEFAULT_ELU_TYPE),
        help="Sélectionnez le type d'élu que vous souhaitez explorer"
    )
    
    # Afficher les détails de la sélection
    if selected_key in ELUS_CONFIG:
        config = ELUS_CONFIG[selected_key]
        st.info(f"{config['icon']} **{config['name']}** - {config['description']} (Niveau: {config['level']})")
    
    return selected_key

def display_data_preview(df: pd.DataFrame, colonnes: list):
    """Affiche un aperçu des données"""
    with st.expander("Informations sur les données"):
        st.write("Colonnes disponibles dans le jeu de données:")
        st.write(df.columns.tolist())
        st.write("Aperçu des premières lignes:")
        st.dataframe(df[colonnes].head(3))

def download_button(df: pd.DataFrame):
    """Ajoute un bouton de téléchargement pour les données"""
    csv = df.to_csv(index=False)
    st.download_button(
        label="Télécharger les données complètes (CSV)",
        data=csv,
        file_name="repertoire_des_elus_filtré.csv",
        mime="text/csv"
    )

def display_stats(df: pd.DataFrame):
    """Affiche les statistiques dans la barre latérale"""
    st.sidebar.header("Statistiques")
    st.sidebar.metric("Nombre total d'élus", len(df))
    
    if 'Code sexe' in df.columns:
        gender_ratio = df['Code sexe'].value_counts(normalize=True).to_dict()
        male_pct = gender_ratio.get('M', 0) * 100
        female_pct = gender_ratio.get('F', 0) * 100
        st.sidebar.metric("Pourcentage d'hommes", f"{male_pct:.1f}%")
        st.sidebar.metric("Pourcentage de femmes", f"{female_pct:.1f}%")

def display_filters(df: pd.DataFrame):
    """Affiche les filtres dans la barre latérale adaptés au type de données"""
    st.sidebar.header("Filtres")
    
    # Filtre par département/section départementale (adaptatif)
    selected_departments = []
    dept_column = None
    dept_label = "Départements"
    
    # Détecter la colonne département appropriée
    if 'Libellé de la section départementale' in df.columns:
        dept_column = 'Libellé de la section départementale'
        dept_label = "Sections départementales"
    elif 'Libellé du département' in df.columns:
        dept_column = 'Libellé du département'
        dept_label = "Départements"
    
    if dept_column:
        departments = df[dept_column].dropna().astype(str).unique()
        all_departments = sorted(departments)
        selected_departments = st.sidebar.multiselect(
            dept_label,
            options=all_departments,
            default=[]
        )
    
    # Filtre par genre (toujours présent)
    selected_gender = "Tous"
    if 'Code sexe' in df.columns:
        genders = df['Code sexe'].dropna().unique()
        gender_options = ["Tous"] + sorted(genders.tolist())
        selected_gender = st.sidebar.radio(
            "Genre",
            options=gender_options
        )
    
    # Filtre par commune (si disponible)
    selected_communes = []
    if 'Libellé de la commune' in df.columns:
        communes = df['Libellé de la commune'].dropna().astype(str).unique()
        if len(communes) > 0:
            selected_communes = st.sidebar.multiselect(
                "Communes",
                options=sorted(communes),
                default=[],
                help="Filtrer par commune (optionnel)"
            )
    
    # Filtre par canton (si disponible - pour les conseillers départementaux)
    selected_cantons = []
    if 'Libellé du canton' in df.columns:
        cantons = df['Libellé du canton'].dropna().astype(str).unique()
        if len(cantons) > 0:
            selected_cantons = st.sidebar.multiselect(
                "Cantons",
                options=sorted(cantons),
                default=[],
                help="Filtrer par canton (optionnel)"
            )
    
    # Filtre par région (si disponible - pour les conseillers régionaux)
    selected_regions = []
    if 'Libellé de la région' in df.columns:
        regions = df['Libellé de la région'].dropna().astype(str).unique()
        if len(regions) > 0:
            selected_regions = st.sidebar.multiselect(
                "Régions",
                options=sorted(regions),
                default=[],
                help="Filtrer par région (optionnel)"
            )
    
    # Filtre par fonction (si disponible)
    selected_functions = []
    if 'Libellé de la fonction' in df.columns:
        functions = df['Libellé de la fonction'].dropna().astype(str).unique()
        if len(functions) > 0 and functions[0] != '':
            selected_functions = st.sidebar.multiselect(
                "Fonctions",
                options=sorted(functions),
                default=[],
                help="Filtrer par fonction (optionnel)"
            )
    
    # Filtre de recherche textuelle
    search_term = st.sidebar.text_input(
        "Rechercher un élu, une commune ou un canton",
        help="Recherche dans les noms, prénoms, communes et cantons"
    )
    
    return {
        'departments': selected_departments,
        'dept_column': dept_column,  # Ajouter la colonne utilisée pour le filtrage
        'gender': selected_gender,
        'communes': selected_communes,
        'cantons': selected_cantons,
        'regions': selected_regions,
        'functions': selected_functions,
        'search_term': search_term
    }

def display_about():
    """Affiche la section À propos"""
    st.markdown("""
    Cette application permet d'explorer le Répertoire National des Élus (RNE) - une base de données 
    des élus en France. Elle offre des fonctionnalités de filtrage, de visualisation et d'analyse
    de données.
    
    ### Source des données
    Les données proviennent du site [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus-1/),
    qui est la plateforme de données ouvertes du gouvernement français.
    
    ### Fonctionnalités
    - Filtrage par département, genre et recherche textuelle
    - Visualisation de la répartition par genre
    - Analyse du nombre d'élus par département
    - Carte interactive des élus
    - Tableau interactif des résultats filtrés
    
    ### Développé avec
    - [Streamlit](https://streamlit.io/) - Framework pour applications de données
    - [Pandas](https://pandas.pydata.org/) - Manipulation de données
    - [Plotly](https://plotly.com/) - Visualisations interactives
    - [PyDeck](https://deckgl.readthedocs.io/) - Cartographie interactive
    """)

def display_signature():
    """Affiche la signature du développeur en bas de page"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; padding: 20px; color: #666; font-size: 14px;'>
            Développé avec 🧠 par <a href='https://www.linkedin.com/in/philippehaag/' target='_blank' style='color: #0066cc; text-decoration: none;'>Philippe Haag</a>
        </div>
        """, 
        unsafe_allow_html=True
    ) 