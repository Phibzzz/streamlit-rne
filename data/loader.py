"""
Module de chargement et prétraitement des données
"""

import pandas as pd
import numpy as np
import json
import requests
from io import StringIO
import streamlit as st
from config.settings import ELUS_CONFIG, DEFAULT_ELU_TYPE, COLUMN_MAPPING, DEFAULT_DEPT_COORDS

@st.cache_data(ttl=3600)  # Cache pendant 1 heure
def load_data_by_type(elu_type: str = DEFAULT_ELU_TYPE) -> pd.DataFrame:
    """
    Charge les données selon le type d'élu sélectionné avec mise en cache Streamlit
    """
    if elu_type not in ELUS_CONFIG:
        st.error(f"Type d'élu non reconnu : {elu_type}")
        return pd.DataFrame()
    
    url = ELUS_CONFIG[elu_type]["url"]
    return load_data(url)

def load_data(url: str = None) -> pd.DataFrame:
    """
    Charge les données depuis l'URL avec mise en cache Streamlit
    """
    if url is None:
        url = ELUS_CONFIG[DEFAULT_ELU_TYPE]["url"]
        
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lever une exception en cas d'erreur HTTP
        
        # Lire le contenu CSV avec l'encodage approprié
        content = response.content.decode('utf-8', errors='replace')
        df = pd.read_csv(StringIO(content), sep=";", low_memory=False)
        
        # Renommer les colonnes en utilisant le mapping
        df = df.rename(columns=COLUMN_MAPPING)
        
        # Calculer l'âge si la date de naissance est disponible
        if 'Date de naissance' in df.columns:
            df['Age'] = pd.to_datetime('today').year - pd.to_datetime(df['Date de naissance'], format='%d/%m/%Y', errors='coerce').dt.year
        
        return df
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=86400)  # Cache pendant 24 heures
def load_coords_cache(cache_file: str) -> dict:
    """
    Charge les coordonnées depuis le fichier de cache avec mise en cache Streamlit
    """
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"Erreur lors du chargement du cache {cache_file} : {str(e)}")
        if 'dept' in cache_file.lower():
            return DEFAULT_DEPT_COORDS
        return {}

def filter_data(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Filtre les données selon les critères sélectionnés
    """
    filtered_df = df.copy()
    
    # Filtre par département/section départementale (adaptatif)
    if filters.get('departments') and filters.get('dept_column'):
        dept_column = filters['dept_column']
        if dept_column in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[dept_column].fillna('').astype(str).isin(filters['departments'])]
    
    # Filtre par genre
    if filters.get('gender') and filters['gender'] != "Tous" and 'Code sexe' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Code sexe'].fillna('').astype(str) == filters['gender']]
    
    # Filtre par commune
    if filters.get('communes') and 'Libellé de la commune' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Libellé de la commune'].fillna('').astype(str).isin(filters['communes'])]
    
    # Filtre par canton
    if filters.get('cantons') and 'Libellé du canton' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Libellé du canton'].fillna('').astype(str).isin(filters['cantons'])]
    
    # Filtre par région
    if filters.get('regions') and 'Libellé de la région' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Libellé de la région'].fillna('').astype(str).isin(filters['regions'])]
    
    # Filtre par fonction
    if filters.get('functions') and 'Libellé de la fonction' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Libellé de la fonction'].fillna('').astype(str).isin(filters['functions'])]
    
    # Filtre par terme de recherche
    search_term = filters.get('search_term', '')
    if search_term:
        search_conditions = []
        
        # Recherche dans les noms et prénoms
        if 'Nom de l\'élu' in filtered_df.columns:
            search_conditions.append(filtered_df['Nom de l\'élu'].fillna('').astype(str).str.contains(search_term, case=False, na=False))
        if 'Prénom de l\'élu' in filtered_df.columns:
            search_conditions.append(filtered_df['Prénom de l\'élu'].fillna('').astype(str).str.contains(search_term, case=False, na=False))
        
        # Recherche dans les communes
        if 'Libellé de la commune' in filtered_df.columns:
            search_conditions.append(filtered_df['Libellé de la commune'].fillna('').astype(str).str.contains(search_term, case=False, na=False))
        
        # Recherche dans les cantons
        if 'Libellé du canton' in filtered_df.columns:
            search_conditions.append(filtered_df['Libellé du canton'].fillna('').astype(str).str.contains(search_term, case=False, na=False))
        
        # Recherche dans les régions
        if 'Libellé de la région' in filtered_df.columns:
            search_conditions.append(filtered_df['Libellé de la région'].fillna('').astype(str).str.contains(search_term, case=False, na=False))
        
        # Recherche dans les sections départementales
        if 'Libellé de la section départementale' in filtered_df.columns:
            search_conditions.append(filtered_df['Libellé de la section départementale'].fillna('').astype(str).str.contains(search_term, case=False, na=False))
        
        if search_conditions:
            search_condition = search_conditions[0]
            for cond in search_conditions[1:]:
                search_condition = search_condition | cond
            filtered_df = filtered_df[search_condition]
    
    return filtered_df

@st.cache_data
def preprocess_data(data: pd.DataFrame, commune_cache: dict, dept_cache: dict) -> pd.DataFrame:
    """
    Prétraite les données avec mise en cache Streamlit
    """
    if data.empty:
        return data
    
    # Ajouter les coordonnées des communes (seulement si la colonne existe)
    if 'Libellé de la commune' in data.columns:
        data['Latitude_Commune'] = data['Libellé de la commune'].map(lambda x: commune_cache.get(str(x), (None, None))[0] if pd.notna(x) else None)
        data['Longitude_Commune'] = data['Libellé de la commune'].map(lambda x: commune_cache.get(str(x), (None, None))[1] if pd.notna(x) else None)
    else:
        # Si pas de communes, initialiser les colonnes avec des valeurs nulles
        data['Latitude_Commune'] = None
        data['Longitude_Commune'] = None
    
    # Ajouter les coordonnées des départements (adaptatif selon le type de données)
    dept_column = None
    if 'Libellé de la section départementale' in data.columns:
        dept_column = 'Libellé de la section départementale'
    elif 'Libellé du département' in data.columns:
        dept_column = 'Libellé du département'
    
    if dept_column:
        data['Latitude_Dept'] = data[dept_column].map(lambda x: dept_cache.get(x, (None, None))[0] if pd.notna(x) else None)
        data['Longitude_Dept'] = data[dept_column].map(lambda x: dept_cache.get(x, (None, None))[1] if pd.notna(x) else None)
    else:
        # Si pas de départements, initialiser les colonnes avec des valeurs nulles
        data['Latitude_Dept'] = None
        data['Longitude_Dept'] = None
    
    # Ajouter un décalage aléatoire pour les coordonnées (seulement si elles existent)
    if 'Latitude_Dept' in data.columns and 'Longitude_Dept' in data.columns:
        # Vérifier qu'il y a des valeurs non nulles avant d'ajouter le décalage
        mask_dept = data['Latitude_Dept'].notna() & data['Longitude_Dept'].notna()
        if mask_dept.any():
            data.loc[mask_dept, 'Latitude_Dept'] = data.loc[mask_dept, 'Latitude_Dept'] + np.random.normal(0, 0.05, size=mask_dept.sum())
            data.loc[mask_dept, 'Longitude_Dept'] = data.loc[mask_dept, 'Longitude_Dept'] + np.random.normal(0, 0.05, size=mask_dept.sum())
    
    if 'Latitude_Commune' in data.columns and 'Longitude_Commune' in data.columns:
        # Vérifier qu'il y a des valeurs non nulles avant d'ajouter le décalage
        mask_commune = data['Latitude_Commune'].notna() & data['Longitude_Commune'].notna()
        if mask_commune.any():
            data.loc[mask_commune, 'Latitude_Commune'] = data.loc[mask_commune, 'Latitude_Commune'] + np.random.normal(0, 0.001, size=mask_commune.sum())
            data.loc[mask_commune, 'Longitude_Commune'] = data.loc[mask_commune, 'Longitude_Commune'] + np.random.normal(0, 0.001, size=mask_commune.sum())
    
    # Remplacer les valeurs manquantes par 0 pour les coordonnées
    coord_cols = ['Latitude_Dept', 'Longitude_Dept', 'Latitude_Commune', 'Longitude_Commune']
    for col in coord_cols:
        if col in data.columns:
            data[col] = data[col].fillna(0)
    
    return data 