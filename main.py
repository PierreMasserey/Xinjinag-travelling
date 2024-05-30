import networkx as nx
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, StringVar, Listbox, END, MULTIPLE, OptionMenu, Scale, HORIZONTAL
from database import G, routes_df, cities_data



# Définir le graphe
G = nx.Graph()

# Ajoutez les trajets au graphe avec l'attribut 'distance'
for index, row in routes_df.iterrows():
    G.add_edge(row['From'], row['To'], distance=row['km'], time=row['time'])


def dijkstra_shortest_path(graph, start, end):
    shortest_paths = nx.shortest_path(graph, source=start, weight='distance')
    shortest_path = shortest_paths[end]

    total_distance = sum(graph[shortest_path[i]][shortest_path[i+1]]['distance'] for i in range(len(shortest_path) - 1))

    return shortest_path, total_distance

def create_custom_route(graph, start, end, waypoints):
    total_path = []
    total_distance = 0

    # Initial starting point
    current_start = start

    for waypoint in waypoints:
        path_segment, distance_segment = dijkstra_shortest_path(graph, current_start, waypoint)
        total_path += path_segment[:-1]  # Add path segment, except the last node to avoid duplication
        total_distance += distance_segment
        current_start = waypoint

    # Final segment to the destination
    path_segment, distance_segment = dijkstra_shortest_path(graph, current_start, end)
    total_path += path_segment
    total_distance += distance_segment

    return total_path, total_distance

# Cette fonction draw_graph est également identique à celle que vous avez fournie.
def draw_graph(G, shortest_path, custom_path):
    plt.figure(figsize=(14, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=10, font_weight='bold')

    labels = {(u, v): f"{data['distance']}km\n{data['time']}min" for u, v, data in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Highlight the custom path in green first
    green_edges = list(zip(custom_path, custom_path[1:]))
    edge_colors = ['green' if edge in green_edges or (edge[1], edge[0]) in green_edges else 'black' for edge in G.edges()]
    nx.draw_networkx_edges(G, pos, edgelist=green_edges, edge_color='green', width=2)

    # Highlight the shortest path in red after the green path
    red_edges = list(zip(shortest_path, shortest_path[1:]))
    edge_colors = ['red' if edge in red_edges or (edge[1], edge[0]) in red_edges else edge_colors[i] for i, edge in enumerate(G.edges())]
    nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='red', width=2)

    plt.show()



def get_city_scores(city_name):
    city_index = cities_data['City'].index(city_name)
    natural_scenery_score = cities_data['Natural scenery'][city_index]
    city_sight_score = cities_data['City sight'][city_index]
    historical_spot_score = cities_data['Historical spot'][city_index]
    cultural_experience_score = cities_data['Cultural experience'][city_index]
    rest_score = cities_data['Rest'][city_index]
    return {
        'natural_scenery': natural_scenery_score,
        'city_sight': city_sight_score,
        'historical_spot': historical_spot_score,
        'cultural_experience': cultural_experience_score,
        'rest': rest_score
    }


# Cette fonction on_calculate est également identique à celle que vous avez fournie.
def on_calculate():
    start_node = start_var.get()
    end_node = end_var.get()
    waypoints = [waypoint_listbox.get(i) for i in waypoint_listbox.curselection()]

    # Get preferences from scales
    natural_scenery_pref = natural_scenery_scale.get()
    city_sight_pref = city_sight_scale.get()
    historical_spot_pref = historical_spot_scale.get()
    cultural_experience_pref = cultural_experience_scale.get()
    rest_pref = rest_scale.get()

    # Calculate score for each city based on preferences
    city_scores = {}
    for city in sorted(G.nodes()):
        scores = get_city_scores(city)
        score = (natural_scenery_pref * scores['natural_scenery'] +
                 city_sight_pref * scores['city_sight'] +
                 historical_spot_pref * scores['historical_spot'] +
                 cultural_experience_pref * scores['cultural_experience'] +
                 rest_pref * scores['rest'])
        city_scores[city] = score

    # Sélectionner les villes les mieux adaptées
    suitable_cities = sorted(city_scores.keys(), key=lambda x: city_scores[x], reverse=True)[:3]  # Sélectionnez les 5 meilleures villes

    # Calculer l'itinéraire avec les villes sélectionnées
    shortest_path, total_distance = dijkstra_shortest_path(G, start_node, end_node)
    custom_path, custom_distance = create_custom_route(G, start_node, end_node, waypoints + suitable_cities)

    # Afficher les résultats
    shortest_path_text.set(f"Shortest Path (Red): {' -> '.join(shortest_path)}\nTotal distance: {total_distance} km")
    custom_path_text.set(f"Custom Path (Green): {' -> '.join(custom_path)}\nTotal distance: {custom_distance} km")

    draw_graph(G, shortest_path, custom_path)


# Vous pouvez ajouter vos données de graphe ici.
# Par exemple:
# G.add_edges_from(edges)

# Configuration de l'interface utilisateur Tkinter
# Configuration de l'interface utilisateur Tkinter
# Configuration de l'interface utilisateur Tkinter
root = Tk()
root.title("Personnalised.Itinary")

window_width = 1200
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

Label(root, text="Starting Point:").grid(row=0, column=0, padx=10, pady=10)
start_var = StringVar()
start_menu = OptionMenu(root, start_var, *sorted(G.nodes()))
start_menu.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Arriving Point:").grid(row=1, column=0, padx=10, pady=10)
end_var = StringVar()
end_menu = OptionMenu(root, end_var, *sorted(G.nodes()))
end_menu.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Intermediary Points:").grid(row=2, column=0, padx=10, pady=10)
waypoint_listbox = Listbox(root, selectmode=MULTIPLE, height=10, width=30)
waypoint_listbox.grid(row=2, column=1, padx=10, pady=10)
for node in sorted(G.nodes()):
    waypoint_listbox.insert(END, node)

Label(root, text="Preferences:").grid(row=3, column=0, padx=10, pady=10)
natural_scenery_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL, label="Natural Scenery")
natural_scenery_scale.grid(row=3, column=1, padx=10, pady=5)

city_sight_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL, label="City Sight")
city_sight_scale.grid(row=4, column=1, padx=10, pady=5)

historical_spot_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL, label="Historical Spot")
historical_spot_scale.grid(row=5, column=1, padx=10, pady=5)

cultural_experience_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL, label="Cultural Experience")
cultural_experience_scale.grid(row=6, column=1, padx=10, pady=5)

rest_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL, label="Rest")
rest_scale.grid(row=7, column=1, padx=10, pady=5)


Button(root, text="Calculate Itinerary", command=on_calculate).grid(row=8, column=1, padx=10, pady=10)

shortest_path_text = StringVar()
custom_path_text = StringVar()

Label(root, textvariable=shortest_path_text, fg='red', wraplength=1000).grid(row=9, column=0, columnspan=2, sticky='w', padx=10, pady=10)
Label(root, textvariable=custom_path_text, fg='green', wraplength=1000).grid(row=10, column=0, columnspan=2, sticky='w', padx=10, pady=10)

root.mainloop()
