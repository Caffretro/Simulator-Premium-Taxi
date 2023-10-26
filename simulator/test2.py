import osmnx as ox

G = ox.load_graphml('./input1/hongkong_updated.graphml')
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
lat_list = gdf_nodes['y'].tolist()
lng_list = gdf_nodes['x'].tolist()
node_id = gdf_nodes.index.tolist()
edge_id = gdf_edges.index.tolist()
print(edge_id)