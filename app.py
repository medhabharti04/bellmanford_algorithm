from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def bellman_ford(graph, source):
    distance = {vertex: float('infinity') for vertex in graph}
    distance[source] = 0

    for _ in range(len(graph) - 1):
        for vertex in graph:
            for neighbor, weight in graph[vertex].items():
                if distance[vertex] + weight < distance[neighbor]:
                    distance[neighbor] = distance[vertex] + weight

    return distance

def generate_graph_image(graph):
    """Generate a graph visualization and save it as an image."""
    G = nx.DiGraph()

    # Add edges to the graph
    for u in graph:
        for v, w in graph[u].items():
            G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G)  # Layout for the graph

    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', font_weight='bold', node_size=2000)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Ensure the static directory exists
    if not os.path.exists('static'):
        os.makedirs('static')

    # Save the graph as an image
    image_path = 'static/graph.png'
    plt.savefig(image_path)
    plt.close()

    return image_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        edges = request.form['edges']
        source = request.form['source']

        graph = {}
        try:
            edges_list = edges.strip().splitlines()
            for edge in edges_list:
                edge = edge.strip()
                if edge:
                    u, v, w = edge.split()
                    w = int(w)
                    if u not in graph:
                        graph[u] = {}
                    if v not in graph:
                        graph[v] = {}
                    graph[u][v] = w

            if source not in graph:
                return render_template('index.html', error=f"Source vertex '{source}' not found in the graph.")

            distances = bellman_ford(graph, source)

            # Generate and save the graph visualization
            image_path = generate_graph_image(graph)

            return render_template('result.html', distances=distances, source=source, image_path=image_path)

        except ValueError:
            return render_template('index.html', error="Invalid input. Please enter edges in the format: u v w.")
        except Exception as e:
            return render_template('index.html', error=f"An error occurred: {str(e)}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

