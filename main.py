import skfuzzy as fuzz
import skfuzzy.control as ctrl
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from database import routes_df, cities_df, G

# Définir les ensembles flous pour chaque type de préférence
natural_scenery = ctrl.Antecedent(np.arange(0, 101, 1), 'natural_scenery')
city_sight = ctrl.Antecedent(np.arange(0, 101, 1), 'city_sight')
historical_spot = ctrl.Antecedent(np.arange(0, 101, 1), 'historical_spot')
cultural_experience = ctrl.Antecedent(np.arange(0, 101, 1), 'cultural_experience')
rest = ctrl.Antecedent(np.arange(0, 101, 1), 'rest')

# Définir les fonctions d'appartenance floues
natural_scenery.automf(3)
city_sight.automf(3)
historical_spot.automf(3)
cultural_experience.automf(3)
rest.automf(3)

# Définir la variable de sortie
preference = ctrl.Consequent(np.arange(0, 101, 1), 'preference')
preference.automf(3)

# Règles floues pour déterminer les préférences
rule1 = ctrl.Rule(natural_scenery['good'] & city_sight['poor'] & historical_spot['average'] & cultural_experience['poor'] & rest['average'], preference['good'])
rule2 = ctrl.Rule(natural_scenery['average'] & city_sight['average'] & historical_spot['good'] & cultural_experience['good'] & rest['poor'], preference['average'])
rule3 = ctrl.Rule(natural_scenery['poor'] & city_sight['good'] & historical_spot['poor'] & cultural_experience['average'] & rest['good'], preference['poor'])

# Système de contrôle flou
preference_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
preference_sim = ctrl.ControlSystemSimulation(preference_ctrl)


# Ajouter les arêtes au graphe
for _, row in routes_df.iterrows():
    G.add_edge(row['From'], row['To'], weight=row['km'])



# Ajouter les attributs des villes au graphe
for _, row in cities_df.iterrows():
    G.nodes[row['City']].update({
        'natural_scenery': row['Natural scenery'],
        'city_sight': row['City sight'],
        'historical_spot': row['Historical spot'],
        'cultural_experience': row['Cultural experience'],
        'rest': row['Rest']
    })

# Calculer les scores flous pour chaque ville
city_scores = {}

for city in G.nodes():
    attrs = G.nodes[city]
    preference_sim.input['natural_scenery'] = attrs['natural_scenery']
    preference_sim.input['city_sight'] = attrs['city_sight']
    preference_sim.input['historical_spot'] = attrs['historical_spot']
    preference_sim.input['cultural_experience'] = attrs['cultural_experience']
    preference_sim.input['rest'] = attrs['rest']
    preference_sim.compute()
    city_scores[city] = preference_sim.output['preference']

# Trier les villes en fonction des scores"""
sorted_cities = sorted(city_scores.items(), key=lambda x: x[1], reverse=True)
print("Villes classées par score de préférence:", sorted_cities)

# Sélectionner les meilleures villes (par exemple, les 5 premières)
top_cities = [city for city, score in sorted_cities[:5]]
print("Meilleures villes à visiter:", top_cities)

# Trouver les meilleurs trajets entre les villes sélectionnées
def find_best_path(graph, cities):
    paths = []
    for i in range(len(cities) - 1):
        path = nx.shortest_path(graph, source=cities[i], target=cities[i + 1], weight='weight')
        paths.append(path)
    return paths

best_paths = find_best_path(G, top_cities)
print("Meilleurs trajets entre les villes sélectionnées:", best_paths)

# Visualiser le graphe et les trajets

# Dessiner le graphe
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')

# Mettre en évidence les meilleurs trajets
for path in best_paths:
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

plt.show()
