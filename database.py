import pandas as pd
import networkx as nx

# Données sur les trajets
routes_data = {
    'From': ['Minfeng', 'Minfeng', 'Yutian', 'Yutian', 'Minfeng', 'Minfeng', 'Luntai', 'Luntai', 'Kuqa', 'Kuqa', 'Aksu', 'Aksu', 'Atushi / Atux', 'Atushi / Atux', 'Kashgar', 'Kashgar', 'Kashgar', 'Taxkorgan', 'Yarkand', 'Yarkand', 'Yarkand', 'Yarkand', 'Hotan', 'Hotan', 'Qiao mo/Qiemo', 'Qiao mo/Qiemo', 'Ruoqiang', 'Ruoqiang', 'Kuqa', 'Korler/Korla', 'Korler/Korla', 'Xinyuan', 'Xinyuan', 'Xinyuan', 'Xinyuan', 'Xinyuan', 'Xinyuan', 'Korler/Korla', 'Korler/Korla', 'Kuitun / Kuytun', 'Kuitun / Kuytun', 'Karamay', 'Karamay', 'Korler/Korla', 'Korler/Korla', 'Korler/Korla', 'Turpan', 'Hotan', 'Alaer', 'Alaer', 'Kuqa', 'Kuqa', 'Yili/Yining', 'Yili/Yining'],
    'To': ['Qiao mo/Qiemo', 'Qiao mo/Qiemo', 'Minfeng', 'Minfeng', 'Luntai', 'Luntai', 'Korler/Korla', 'Korler/Korla', 'Luntai', 'Luntai', 'Kuqa', 'Kuqa', 
'Aksu', 'Aksu', 'Atushi / Atux', 'Atushi / Atux', 'Atushi / Atux', 'Kashgar', 'Hotan', 'Kashgar', 'Kashgar', 'Kashgar', 'Yutian', 'Yutian', 'Ruoqiang', 'Ruoqiang', 'Korler/Korla', 'Korler/Korla', 'Xinyuan', 'Kuitun / Kuytun', 'Kuitun / Kuytun', 'Kuitun / Kuytun', 'Kuitun / Kuytun', 'Kuitun / Kuytun', 'Urumqi', 'Urumqi', 'Urumqi', 'Urumqi', 'Urumqi', 'Urumqi', 'Karamay', 'Urumqi', 'Urumqi', 'Turpan', 'Turpan', 'Turpan', 'Urumqi', 'Alaer', 'Kuqa', 'Kuqa', 'Yili/Yining', 'Yili/Yining', 'Xinyuan', 'Xinyuan'],
    'km': [300, 311, 110, 114, 575, 733, 176, 222, 115, 123, 290, 250, 426, 487, 45, 45, 45, 290, 315, 190, 237, 
192, 201, 217, 280, 280, 415, 430, 505, 700, 760, 290, 634, 419, 518, 871, 695, 482, 524, 240, 154, 316, 358, 415, 377, 427, 210, 438, 230, 313, 590, 900, 184, 184],
    'time': [180,
240,
105,
85,
490,
540,
150,
210,
75,
135,
240,
180,
270,
340,
50,
50,
90,
285,
225,
150,
165,
225,
220,
170,
180,
210,
240,
300,
360,
480,
630,
225,
435,
440,
360,
570,
680,
360,
480,
135,
105,
210,
280,
310,
310,
430,
165,
330,
240,
220,
360,
800,
120,
180,
]

,
}

# Vérifiez les longueurs des listes pour les trajets
print("Vérification des longueurs des listes pour les trajets:")
for key, value in routes_data.items():
    print(f'Length of {key}: {len(value)}')

# Données sur les villes
cities_data = {
    'City': ['Minfeng', 'Qiao mo/Qiemo', 'Yutian', 'Luntai', 'Korler/Korla', 'Kuqa', 'Aksu', 'Atushi / Atux', 'Kashgar', 
             'Taxkorgan', 'Yarkand', 'Hotan', 'Ruoqiang', 'Xinyuan', 'Kuitun / Kuytun', 'Urumqi', 'Karamay', 
             'Turpan', 'Alaer', 'Yili/Yining'],
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
    routes_df = pd.DataFrame(routes_data)
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
    G.add_edge(row['From'], row['To'], weight=row['km'], time=row['time'])

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
