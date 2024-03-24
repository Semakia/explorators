import pandas as pd 

#On répoartit la donnée en deux parties principales : Les noeuds amonts(début de parcours) et les noeuds aval(fin de parcours)
def prepare_data(df) :
	starting_nodes = list(df[df['type_aretes'] == 'depart'].noeud_amont)
	ending_nodes = list(df[df['type_aretes'] == 'arrivee'].noeud_aval)
	return starting_nodes , ending_nodes
    

def create_upstream_downstream_dict(df):
    return {row["noeud_amont"]: (row["noeud_aval"], row['distance']) for _, row in df.iterrows()}

# Fonction permettant de retrouver le chemin le plus court 
def get_shortest_explorator_path(starting_nodes, ending_nodes, dict_upstream_downstream):
    min_distance = float("inf")
    shortest_path = None
	#chaque itération représente le parcours de chaque utilisateur .
    for starting_node in starting_nodes:
        explorator_path = [starting_node]
        distance = 0

        while explorator_path[-1] not in ending_nodes:
            downstream_node, edge_distance = dict_upstream_downstream[explorator_path[-1]]
            distance += edge_distance
            explorator_path.append(downstream_node)
        
        if distance < min_distance:
            shortest_path = explorator_path
            min_distance = distance

    return shortest_path


# Fonction permettant de retrouver le chemin le plus long 
def get_longest_explorator_path(starting_nodes, ending_nodes, dict_upstream_downstream):
    max_distance = 0
    longest_path = None

    for starting_node in starting_nodes:
        explorator_path = [starting_node]
        distance = 0

        while explorator_path[-1] not in ending_nodes:
            downstream_node, edge_distance = dict_upstream_downstream[explorator_path[-1]]
            distance += edge_distance
            explorator_path.append(downstream_node)
        
        if distance > max_distance:
            longest_path = explorator_path
            max_distance = distance

    return longest_path



if __name__ == "__main__":
    edges_df = pd.read_csv("./parcours_explorateurs.csv")
    starting_nodes , ending_nodes = prepare_data(edges_df)
    dict_upstream_downstream = create_upstream_downstream_dict(edges_df)

    shortest_path = get_shortest_explorator_path(starting_nodes, ending_nodes, dict_upstream_downstream)
    longest_path = get_longest_explorator_path(starting_nodes, ending_nodes, dict_upstream_downstream)

    print("Chemin le plus court:", shortest_path)
    print("Chemin le plus long:", longest_path)
