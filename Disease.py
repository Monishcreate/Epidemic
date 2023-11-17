import networkx as nx
import matplotlib.pyplot as plt
import random

def initialize_graph(num_nodes, initial_infected, edge_probability):
    graph = nx.erdos_renyi_graph(num_nodes, edge_probability)

    # Initialize nodes with 'state' and 'days_infected' attributes
    for node in graph.nodes:
        graph.nodes[node]['state'] = 'S'  # 'S' for susceptible
        graph.nodes[node]['days_infected'] = 0  # Initialize 'days_infected' attribute

    # Randomly select initial infected nodes
    infected_nodes = random.sample(range(num_nodes), initial_infected)
    for node in infected_nodes:
        graph.nodes[node]['state'] = 'I'  # 'I' for infected

    return graph
def visualize_graph(graph, step):
    pos = nx.spring_layout(graph)  # Layout for visualization

    colors = {'S': 'blue', 'I': 'red', 'R': 'green', 'V': 'purple', 'Immune': 'orange', 'Dead': 'black'}

 
    node_colors = [colors.get(graph.nodes[node]['state'], 'gray') for node in graph.nodes]

    labels = {node: f"{node}\n{graph.nodes[node]['state']}" for node in graph.nodes}

    plt.figure(figsize=(8, 8))
    plt.title(f'Epidemic Spread - Month {step} | People Alive: {count_people_alive(graph)}')

    
    for state, color in colors.items():
        plt.scatter([], [], color=color, label=state)

    dead_nodes = [node for node in graph.nodes if graph.nodes[node]['state'] == 'Dead']
    for node in dead_nodes:
        x, y = pos[node]
        plt.text(x, y, f"{node} died", color='white', fontsize=8, ha='center', va='center')

    nx.draw(graph, pos, with_labels=True, node_color=node_colors, labels=labels)

  
    plt.legend(bbox_to_anchor=(1.05, 0), loc='lower right', borderaxespad=0.)

    plt.show()

def print_graph_state(graph, step):
    print(f"Day {step} - Graph State:")
    for node in graph.nodes:
        print(f"Node {node}: {graph.nodes[node]['state']}")
    print("\n")

def simulate_epidemic(graph, transmission_rate, recovery_rate, vaccination_rate, death_rate, immune_chance, num_steps):
    for step in range(num_steps):
        nodes_to_remove = []  
        for node in graph.nodes:
            if graph.nodes[node]['state'] == 'I':
                # Transmission to susceptible neighbors
                for neighbor in graph.neighbors(node):
                    if graph.nodes[neighbor]['state'] == 'S' and random.random() < transmission_rate:
                        graph.nodes[neighbor]['state'] = 'I'
                
              
                graph.nodes[node]['days_infected'] += 1
                if random.random() < recovery_rate * graph.nodes[node]['days_infected']:
                    if random.random() < vaccination_rate:
                        graph.nodes[node]['state'] = 'Immune'  
                    else:
                        if random.random() < immune_chance:
                            graph.nodes[node]['state'] = 'Immune'  
                        else:
                            if random.random() < death_rate:
                                graph.nodes[node]['state'] = 'Dead'  
                                nodes_to_remove.append(node) 
                                print(f"Node {node} has died.")
                            else:
                                graph.nodes[node]['state'] = 'R'  

           
            elif graph.nodes[node]['state'] == 'S' and random.random() < vaccination_rate:
                graph.nodes[node]['state'] = 'Immune'  # Vaccinated individuals become immune
        
      
        for node in nodes_to_remove:
            graph.remove_node(node)

       
        state_counts = {state: sum(1 for node in graph.nodes if graph.nodes[node]['state'] == state) for state in ['S', 'I', 'R', 'V', 'Immune', 'Dead']}
        print(f"Day {step} - People Count: {state_counts}")

        print_graph_state(graph, step)
        visualize_graph(graph, step)


def count_people_alive(graph):
    return sum(1 for node in graph.nodes if graph.nodes[node]['state'] in ['S', 'I', 'R', 'V', 'Immune', 'Dead'])



num_nodes = 100
initial_infected = 1
edge_probability = 0.1
transmission_rate = 0.2
recovery_rate = 0.2
vaccination_rate = 0.01
death_rate = 0.1  # Adjust this value for the probability of death
immune_chance = 0  # Adjust this value for the chance of becoming immune after recovery
num_steps = 15

graph = initialize_graph(num_nodes, initial_infected, edge_probability)
print_graph_state(graph, 0)

visualize_graph(graph, 0)

simulate_epidemic(graph, transmission_rate, recovery_rate, vaccination_rate, death_rate, immune_chance, num_steps)



