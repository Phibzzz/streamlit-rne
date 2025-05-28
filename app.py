"""
Application principale Streamlit pour l'exploration du RNE
"""

import streamlit as st
from config.settings import APP_TITLE, APP_DESCRIPTION
from data.loader import load_data_by_type, load_coords_cache, filter_data, preprocess_data
from visualization.map import display_map
from visualization.ui import (
    setup_page, display_data_preview, download_button,
    display_stats, display_filters, display_about, display_elu_type_selector
)
from visualization.advanced import display_advanced_visualizations

def main():
    # Configuration de la page
    setup_page()
    st.title(APP_TITLE)
    st.markdown(APP_DESCRIPTION)
    
    # Sélecteur de type d'élu
    selected_elu_type = display_elu_type_selector()
    
    # Chargement des données selon le type sélectionné
    with st.spinner("Chargement des données..."):
        df = load_data_by_type(selected_elu_type)
        commune_cache = load_coords_cache("commune_coords_cache.json")
        dept_cache = load_coords_cache("dept_coords_cache.json")
        
        # Prétraitement des données
        df = preprocess_data(df, commune_cache, dept_cache)
    
    if df.empty:
        st.warning("Aucune donnée disponible. Veuillez vérifier la connexion à l'API.")
        return
    
    # Afficher les filtres et appliquer la sélection
    filters = display_filters(df)
    filtered_df = filter_data(df, filters)
    
    # Afficher les statistiques
    display_stats(filtered_df)
    
    # Création des onglets
    tab1, tab2, tab3, tab4 = st.tabs(["Carte", "Visualisations", "Tableau de données", "À propos"])
    
    with tab1:
        display_map(filtered_df)
    
    with tab2:
        st.header("Visualisations")
        display_advanced_visualizations(filtered_df)
    
    with tab3:
        st.header("Tableau de données")
        display_data_preview(filtered_df, df.columns.tolist())
        download_button(filtered_df)
    
    with tab4:
        display_about()

if __name__ == "__main__":
    main()