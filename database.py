import pandas as pd
import networkx as nx
import skfuzzy as fuzz
import numpy as np

# Données sur les trajets
data = {
    'From': ['Minfeng', 'Minfeng', 'Yutian', 'Yutian', 'Minfeng', 'Minfeng', 'Luntai', 'Luntai', 'Kuqa', 'Kuqa', 'Aksu', 'Aksu', 'Atushi / Atux', 'Atushi / Atux', 'Kashgar / Kashi', 'Kashgar / Kashi', 'Kashgar / Kashi', 'Taxkorgan', 'Yarkand', 'Yarkand', 'Yarkand', 'Yarkand', 'Hotan', 'Hotan', 'Qiao mo/Qiemo', 'Qiao mo/Qiemo', 'Ruoqiang', 'Ruoqiang', 'Kuqa', 'Korler/Korla', 'Korler/Korla', 'Xinyuan', 'Xinyuan', 'Xinyuan', 'Xinyuan', 'Xinyuan', 'Xinyuan', 'Korler/Korla', 'Korler/Korla', 'Kuitun / Kuytun', 'Kuitun / Kuytun', 'Karamay', 'Karamay', 'Korler/Korla', 'Korler/Korla', 'Korler/Korla', 'Turpan', 'Hotan', 'Alaer', 'Alaer', 'Kuqa', 'Kuqa', 'Yili/Yining', 'Yili/Yining'],
    'To': ['Qiao mo/Qiemo', 'Qiao mo/Qiemo', 'Minfeng', 'Minfeng', 'Luntai', 'Luntai', 'Korler/Korla', 'Korler/Korla', 'Luntai', 'Luntai', 'Kuqa', 'Kuqa', 
'Aksu', 'Aksu', 'Atushi / Atux', 'Atushi / Atux', 'Atushi / Atux', 'Kashi', 'Hotan', 'Kashgar', 'Kashgar', 'Kashgar', 'Yutian', 'Yutian', 'Ruoqiang', 'Ruoqiang', 'Korler/Korla', 'Korler/Korla', 'Xinyuan', 'Kuitun / Kuytun', 'Kuitun / Kuytun', 'Kuitun / Kuytun', 'Kuitun / Kuytun', 'Kuitun / Kuytun', 'Urumqi', 'Urumqi', 'Urumqi', 'Urumqi', 'Urumqi', 'Urumqi', 'Karamay', 'Urumqi', 'Urumqi', 'Turpan', 'Turpan', 'Turpan', 'Urumqi', 'Alaer/Aral', 'Kuqa', 'Kuqa', 'Yili/Yining', 'Yili/Yining', 'Xinyuan', 'Xinyuan'],
    'km': ['300', '311', '110', '114', '575', '733', '176', '222', '115', '123', '290', '250', '426', '487', '45', '45', '45', '290', '315', '190', '237', 
'192', '201', '217', '280', '280', '415', '430', '505', '700', '760', '290', '634', '419', '518', '871', '695', '482', '524', '240', '154', '316', '358', '415', '377', '427', '210', '438', '230', '313', '590', '900', '184', '184'],
    'time': ['3h00', '4h', '1h45', '1h25', '8h10', '9h', '2h30', '3h30', '1h15', '2h15', '4h', '3h', '4h30', '5h40', '0h50', '0h50', '1h30', '4h45', '3h45', 
'2h30', '2h45', '3h45', '3h40', '2h50', '3h00', '3h30', '4h', '5h', '6h00', '8h', '10h30', '3h45', '7h15', '7h20', '6h00', '9h30', '11h20', '6h', '8h', '2h15', '1h45', '3h30', '4h40', '5h10', '5h10', '7h10', '2h45', '5h30', '4h', '3h40', '6h', '13h20', '2h', '3h'],
    'Type of road': ['Highway', 'Highway+freeway', 'Freeway', 'Highway', 'Desert road', 'Highway+freeway', 'Highway', 'Highway+Desert road+freeway', 'Highway', 'Freeway', 'Freeway', 'Highway', 'Highway', 'Highway+freeway', 'Highway', 'Highway+freeway', 'Freeway', 'Freeway', 'Highway', 'Highway+freeway', 'Highway', 'Freeway', 'Freeway', 'Highway', 'Highway', 'Highway+freeway', 'Highway', 'Highway+freeway', '', 'Highway', 'Highway+freeway', 'Road closure', 'Highway', 'Freeway', 'Road closure', 'Highway', 'Highway+freeway', 'Highway', 'Highway+freeway', 'Highway', 'Highway', 'Highway', 'Highway+freeway', 'Highway', 'Highway+freeway', 'Freeway', 'Highway', 'Freeway', 'Freeway', 'Highway+freeway', 'Road closure', 'Highway+freeway', 'Highway', 'Highway+freeway']
}

# Vérifiez les longueurs des listes pour les trajets
print("Vérification des longueurs des listes pour les trajets:")
for key, value in data.items():
    print(f'Length of {key}: {len(value)}')

# Données sur les villes
cities_data = {
    'City': ['Minfeng', 'Qiemo', 'Yutian', 'Luntai', 'Korler', 'Kuqa', 'Aksu', 'Atushi', 'Kashi', 
             'Taxkorgan', 'Yarkand', 'Hotan', 'Ruoqiang', 'Xinyuan', 'Kuitun', 'Urumqi', 'Karamay', 
             'Turpan', 'Alaer', 'Yili'],
    'Natural scenery': [80, 20, 50, 80, 50, 50, 70, 20, 20, 100, 20, 10, 45, 100, 0, 25, 85, 28, 40, 20],
    'City sight': [0, 20, 0, 0, 0, 0, 0, 0, 20, 0, 0, 10, 0, 0, 0, 25, 0, 0, 0, 20],
    'Historical spot': [20, 20, 20, 20, 25, 30, 20, 0, 30, 0, 40, 50, 40, 0, 0, 25, 15, 44, 0, 20],
    'Cultural experience': [0, 0, 0, 0, 25, 20, 10, 0, 20, 0, 40, 30, 15, 0, 0, 25, 0, 28, 0, 20],
    'Rest': [0, 40, 30, 0, 25, 0, 0, 80, 0, 0, 0, 30, 0, 0, 100, 25, 0, 0, 60, 20]
}

# Vérifiez les longueurs des listes pour les villes
print("Vérification des longueurs des listes pour les villes:")
for key, value in cities_data.items():
    print(f'Length of {key}: {len(value)}')

# Créez les DataFrames après avoir corrigé les longueurs
try:
    routes_df = pd.DataFrame(data)
    cities_df = pd.DataFrame(cities_data)
    print("DataFrames créés avec succès.")
except ValueError as e:
    print(f"Erreur lors de la création des DataFrames: {e}")

print(routes_df)
print(cities_df)

# Créez le graphe pondéré
G = nx.Graph()

# Ajoutez les trajets au graphe
for index, row in routes_df.iterrows():
    G.add_edge(row['From'], row['To'], weight=row['km'], time=row['time'], road_type=row['Type of road'])

# Ajoutez les attributs des villes au graphe
for index, row in cities_df.iterrows():
    G.add_node(row['City'], 
               natural_scenery=row['Natural scenery'], 
               city_sight=row['City sight'], 
               historical_spot=row['Historical spot'], 
               cultural_experience=row['Cultural experience'], 
               rest=row['Rest'])

print("Graph nodes with attributes:", G.nodes(data=True))
print("Graph edges with attributes:", G.edges(data=True))
