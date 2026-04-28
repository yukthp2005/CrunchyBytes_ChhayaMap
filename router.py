import networkx as nx

def calculate_cool_route(graph_data, start_node, end_node, k_factor=2.5):
    """
    graph_data: List of dicts [{'id': 1, 'u': A, 'v': B, 'length': 200, 'shade': 0.8}, ...]
    """
    G = nx.Graph()

    for edge in graph_data:
        # The 'Cool' Weighting Logic
        # More shade = Lower weight = Preferred path
        shade_factor = max(edge['shade'], 0.01) # Avoid 0
        thermal_weight = edge['length'] * (1 + (k_factor / shade_factor))
        
        G.add_edge(edge['u'], edge['v'], 
                   weight=thermal_weight, 
                   actual_dist=edge['length'],
                   shade=edge['shade'])

    try:
        # Compute the path that minimizes Thermal Weight
        optimal_path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
        
        # Calculate 'Heat Exposure Saved' for the Pitch
        total_dist = 0
        avg_shade = []
        for i in range(len(optimal_path)-1):
            data = G.get_edge_data(optimal_path[i], optimal_path[i+1])
            total_dist += data['actual_dist']
            avg_shade.append(data['shade'])
            
        return {
            "path": optimal_path,
            "distance": total_dist,
            "avg_shade": round(sum(avg_shade)/len(avg_shade)*100, 2)
        }
    except nx.NetworkXNoPath:
        return None