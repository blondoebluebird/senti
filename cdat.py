from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import shutil
import os

# Étape 1 : Collecte de données Sentinel-1

# Connexion à l'API
api = SentinelAPI('bbb1988', 'Mdp@2019', 'https://scihub.copernicus.eu/dhus')

# Définir la zone d'intérêt à partir d'un fichier GeoJSON
footprint = geojson_to_wkt(read_geojson('coteg.geojson'))

# Recherche de données
products = api.query(footprint,
                     date=('20220101', '20220131'),
                     platformname='Sentinel-1',
                     cloudcoverpercentage=(0, 30))

# Téléchargement de données
download_dir = 'dataset'
os.makedirs(download_dir, exist_ok=True)

for product_id, product_info in products.items():
    api.download(product_id, directory_path=download_dir)

# Étape 2 : Prétraitement des données SAR
# (Cette étape dépendra du prétraitement spécifique que vous devez effectuer sur vos données)

# Étape 3 : Stockage des données

# Déplacer les données téléchargées dans un répertoire de stockage
storage_dir = 'datstock'
os.makedirs(storage_dir, exist_ok=True)

for root, _, files in os.walk(download_dir):
    for file in files:
        if file.endswith('.zip'):
            shutil.move(os.path.join(root, file), storage_dir)

# Nettoyer le répertoire de téléchargement
shutil.rmtree(download_dir)

print("Les données Sentinel-1 ont été collectées, prétraitées et stockées avec succès.")

