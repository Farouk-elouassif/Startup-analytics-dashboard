# Guide d'Installation - Startup Insights Dashboard

## 1. Installation de Python
- Téléchargez et installez Python 3.8 ou plus récent depuis [python.org](https://www.python.org/downloads/)
- Cochez la case "Add Python to PATH" lors de l'installation

## 2. Installation des bibliothèques requises
Ouvrez un terminal et exécutez les commandes suivantes :

pip install customtkinter
pip install pandas
pip install folium
pip install matplotlib
pip install seaborn
pip install numpy
pip install tkinterhtml
```

## 3. Préparation des données
- Placez le fichier `startups_with_coordinates.csv` dans le même dossier que le script principal
- Assurez-vous que le fichier CSV contient les colonnes : Company Name, Valuation ($B), Country, City, Industry, Select Investors, Latitude, Longitude

## 4. Lancement de l'application
- Double-cliquez sur `interface222.py`
- Ou ouvrez un terminal et exécutez :
```bash
python interface222.py
```

## En cas de problème
- Vérifiez que Python est bien installé : `python --version`
- Vérifiez que toutes les bibliothèques sont installées : `pip list`
- Assurez-vous que le fichier CSV est présent et bien formaté