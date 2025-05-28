"""
Script de test pour vérifier le bon fonctionnement de l'application avec tous les types d'élus
"""

import pandas as pd
from data.loader import load_data_by_type, preprocess_data, load_coords_cache
from config.settings import ELUS_CONFIG

def test_elu_type(elu_type):
    """Test le chargement et le prétraitement pour un type d'élu"""
    print(f"\n=== Test {elu_type.upper()} ===")
    
    try:
        # Chargement des données
        df = load_data_by_type(elu_type)
        print(f"✅ Chargement réussi: {len(df)} lignes, {len(df.columns)} colonnes")
        
        # Affichage des colonnes
        print("Colonnes disponibles:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        # Test du prétraitement
        commune_cache = load_coords_cache("commune_coords_cache.json")
        dept_cache = load_coords_cache("dept_coords_cache.json")
        
        df_processed = preprocess_data(df, commune_cache, dept_cache)
        print(f"✅ Prétraitement réussi: {len(df_processed)} lignes")
        
        # Vérification des coordonnées
        has_commune_coords = 'Latitude_Commune' in df_processed.columns and df_processed['Latitude_Commune'].notna().any()
        has_dept_coords = 'Latitude_Dept' in df_processed.columns and df_processed['Latitude_Dept'].notna().any()
        
        print(f"Coordonnées communes: {'✅' if has_commune_coords else '❌'}")
        print(f"Coordonnées départements: {'✅' if has_dept_coords else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Test tous les types d'élus"""
    print("🧪 Test de l'application multi-élus")
    print("=" * 50)
    
    results = {}
    for elu_type in ELUS_CONFIG.keys():
        results[elu_type] = test_elu_type(elu_type)
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    for elu_type, success in results.items():
        status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        name = ELUS_CONFIG[elu_type]["name"]
        print(f"{status} - {name}")
    
    total_success = sum(results.values())
    total_tests = len(results)
    print(f"\nRésultat global: {total_success}/{total_tests} tests réussis")
    
    if total_success == total_tests:
        print("🎉 Tous les tests sont passés avec succès !")
    else:
        print("⚠️ Certains tests ont échoué.")

if __name__ == "__main__":
    main() 