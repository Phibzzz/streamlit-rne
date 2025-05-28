# Explorateur du Répertoire National des Élus

Une application Streamlit interactive pour explorer et visualiser les données du Répertoire National des Élus (RNE) de France.

## 🚀 Nouvelles fonctionnalités

### Types d'élus supportés

L'application permet maintenant d'explorer **6 types d'élus différents** :

- 🏛️ **Conseillers municipaux** (488k élus) - Élus des conseils municipaux
- 🏢 **Conseillers départementaux** (4k élus) - Élus des conseils départementaux  
- 🌍 **Conseillers régionaux** - Élus des conseils régionaux
- 👨‍💼 **Maires** (35k élus) - Maires des communes françaises
- 🏛️ **Députés** - Députés de l'Assemblée nationale
- 🏛️ **Sénateurs** - Sénateurs du Sénat

### Sélecteur intelligent

- **Interface élégante** : Sélecteur avec icônes et descriptions pour chaque type d'élu
- **Chargement dynamique** : Les données se chargent automatiquement selon le type sélectionné
- **Filtres adaptatifs** : Les filtres s'ajustent selon les colonnes disponibles pour chaque type

## ✨ Fonctionnalités

### Filtrage intelligent
- **Départements** : Filtrage par département (disponible pour tous les types)
- **Genre** : Répartition homme/femme (disponible pour tous les types)
- **Communes** : Filtrage par commune (conseillers municipaux, maires)
- **Cantons** : Filtrage par canton (conseillers départementaux)
- **Fonctions** : Filtrage par fonction spécifique (selon disponibilité)
- **Recherche textuelle** : Recherche dans noms, prénoms, communes, cantons

### Visualisations
- **Carte interactive** : Localisation géographique des élus avec PyDeck
- **Graphiques de répartition** : Analyse par genre, département, etc.
- **Statistiques en temps réel** : Métriques dynamiques selon les filtres
- **Tableau interactif** : Exploration détaillée des données

### Interface utilisateur
- **Design moderne** : Interface claire et intuitive
- **Responsive** : Adaptation automatique à différentes tailles d'écran
- **Performance optimisée** : Mise en cache des données pour une navigation fluide

## 🛠️ Installation

1. Clonez le repository :
```bash
git clone <repository-url>
cd streamlit-rne-explorer
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancez l'application :
```bash
streamlit run app.py
```

## 📊 Sources de données

Les données proviennent du site officiel [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus-1/) :

- **Conseillers municipaux** : ~488k enregistrements
- **Conseillers départementaux** : ~4k enregistrements  
- **Maires** : ~35k enregistrements
- **Conseillers régionaux** : Données régionales
- **Députés** : Assemblée nationale
- **Sénateurs** : Sénat

## 🏗️ Architecture

```
├── app.py                 # Application principale
├── config/
│   └── settings.py       # Configuration des types d'élus et URLs
├── data/
│   └── loader.py         # Chargement et filtrage des données
├── visualization/
│   ├── ui.py            # Composants d'interface utilisateur
│   ├── map.py           # Carte interactive
│   └── advanced.py      # Visualisations avancées
└── utils/               # Utilitaires
```

## 🔧 Technologies utilisées

- **[Streamlit](https://streamlit.io/)** - Framework d'application web
- **[Pandas](https://pandas.pydata.org/)** - Manipulation de données
- **[Plotly](https://plotly.com/)** - Visualisations interactives
- **[PyDeck](https://deckgl.readthedocs.io/)** - Cartographie 3D
- **[Requests](https://requests.readthedocs.io/)** - Chargement de données

## 📈 Améliorations futures

- [ ] Ajout de visualisations temporelles (évolution des mandats)
- [ ] Comparaisons inter-départementales avancées
- [ ] Export de rapports personnalisés
- [ ] Intégration d'analyses prédictives
- [ ] Mode hors-ligne avec cache local

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Optimiser les performances

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.