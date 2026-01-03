# DecompMaster - Maître de la Décomposition LU

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Status](https://img.shields.io/badge/status-stable-green.svg)

**DecompMaster** est une application Python haute performance conçue pour effectuer des analyses matricielles avancées via la **Décomposition LU** (algorithme de Doolittle avec pivot partiel). Elle offre une interface graphique moderne (GUI) ainsi qu'une interface en ligne de commande (CLI) pour s'adapter à tous les besoins des ingénieurs et étudiants.

## 🚀 Fonctionnalités Clés

- **Décomposition LU Robuste** : Implémentation de PA = LU pour une stabilité numérique optimale.
- **Résolution de Systèmes** : Calcul efficace de déterminants et d'inverses matriciels.
- **Double Interface** :
  - 🖥️ **GUI (Tkinter)** : Interface intuitive avec onglets pour visualiser L, U, P et l'inverse.
  - ⌨️ **CLI** : Interface rapide pour les terminaux et scripts.
- **Entrée Flexible** : Accepte les matrices sous forme de texte copié/collé (espaces, virgules) ou syntaxe de liste Python.
- **Précision** : Utilise `numpy` pour le stockage et les calculs flottants double précision.
- **Vérification** : Comparaison automatique de la trace $Trace(A \cdot A^{-1})$ pour valider l'inversion.

## 🛠️ Installation

### Prérequis
- Python 3.8 ou supérieur.
- Pip (gestionnaire de paquets).

### Étapes

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-user/DecompMaster.git
   cd DecompMaster
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Utilisation

### Interface Graphique (GUI)
Pour une expérience visuelle interactive :
```bash
python gui_app.py
```
1. Collez votre matrice dans la zone de texte.
2. Cliquez sur **Calculer Décomposition**.
3. Naviguez entre les onglets pour voir les résultats détaillés.

### Ligne de Commande (CLI)
Pour une utilisation rapide ou via SSH :
```bash
python main.py
```
Suivez les instructions à l'écran pour saisir votre matrice ligne par ligne ou via un bloc de texte.

## 📂 Structure du Projet

```
DecompMaster/
├── src/
│   ├── numerics.py   # Cœur mathématique (LU, solveurs, déterminant)
│   └── utils.py      # Utilitaires de parsing et formatage
├── tests/
│   └── test_numerics.py # Tests unitaires et vérification automatique
├── gui_app.py        # Point d'entrée de l'interface graphique
├── main.py           # Point d'entrée de l'interface ligne de commande
├── requirements.txt  # Liste des dépendances
└── README.md         # Documentation
```

## 🧪 Tests

Pour vérifier la fiabilité des calculs sur votre machine, lancez la suite de tests incluse :
```bash
python tests/test_numerics.py
```
Cela testera l'algorithme sur des matrices aléatoires de différentes tailles (5x5, 10x10, 50x50) et des matrices singulières.

## 🧮 Exemple Mathématique

Pour une matrice $A$ donnée, le programme trouve $P$, $L$, et $U$ tels que :
$$ P \cdot A = L \cdot U $$

Où :
- $P$ est une matrice de permutation.
- $L$ est triangulaire inférieure (diagonale unitaire).
- $U$ est triangulaire supérieure.

## 🤝 Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une *issue* ou une *pull request* pour des améliorations ou des corrections.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
