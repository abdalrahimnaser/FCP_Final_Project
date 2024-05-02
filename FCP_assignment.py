import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse

#task 3:

class Node:

    def __init__(self, value, number, connections=None):

        self.index = number
        self.connections = connections
        self.value = value

class Network: 

    def __init__(self, nodes=None):
        if nodes is None:
            self.nodes = []
        else:
            self.nodes = nodes 

    def get_mean_degree(self):

        # iteration over each node in the network while summing up it's connections to find its degree
        NodeDegree = [sum(node.connections) for node in self.nodes]

        return sum(NodeDegree) / len(NodeDegree)

    def get_mean_clustering(self):

        # empty list
        clustering_coefficients = []

        for node in self.nodes:

            # iteration through connections of each node to find neighbours
            # if a connection exists, ==1
            Number_of_neighbours = [self.nodes[i] for i, connection in enumerate(node.connections) if
                                    connection == 1]

            # less than 2 neighnours, the clustering coefficient is undefined
            if len(Number_of_neighbours) < 2:
                clustering_coefficients.append(0)

                continue
            # to count number of connections between neighbours:
            node_connections = 0

            # iterate over all pairs of neighbours
            for i, neighbor1 in enumerate(Number_of_neighbours):
                for j, neighbor2 in enumerate(Number_of_neighbours):

                    # to avoid counting connections twice
                    if i < j and neighbor1.connections[neighbor2.index] == 1:
                        node_connections += 1

            # Formula given:
            possible_connections = len(Number_of_neighbours) * (len(Number_of_neighbours) - 1) / 2

            # To append the results
            clustering_coefficients.append(node_connections / possible_connections)

        return sum(clustering_coefficients) / len(clustering_coefficients)

    def shortest_path_length(self, start_node):

        # to track if a node has been visited:
        is_visited = [False] * len(self.nodes)

        Distance = [0] * len(self.nodes)
        queue = [start_node]
        is_visited[start_node.index] = True
        Total_Distance = 0
        node_count = 0

        # To loop through nodes until every node has been processed:
        while queue:

            # To remove and return the first node from the queue for processing
            current_node = queue.pop(0)

            # If a node has been visited:
            node_count += 1

            Total_Distance += Distance[current_node.index]

            # Iteration over the neighbours (connections) of the current node
            for i, connection in enumerate(current_node.connections):

                if connection == 1 and not is_visited[i]:
                    # To mark a node as visited:
                    is_visited[i] = True

                    # To update the distance:
                    Distance[i] = Distance[current_node.index] + 1

                    queue.append(self.nodes[i])

        if node_count == 1:
            # When the only connection is to itself

            return 0

            # subtract the starting node
        return Total_Distance / (node_count - 1)

    def get_mean_path_length(self):

        # To store the shortest path length from each node:
        path_lengths_list = []

        # To iterate through each node and append the shortest path length to a list:
        for start_node in self.nodes:
            path_lengths_list.append(self.shortest_path_length(start_node))

        # Mean calculation:
        return sum(path_lengths_list) / len(self.nodes)

    def make_random_network(self, N, connection_probability=0.5):

        self.nodes = []

        for node_number in range(N):
            value = np.random.random()
            connections = [0 for _ in range(N)]
            self.nodes.append(Node(value, node_number, connections))

        for (index, node) in enumerate(self.nodes):

            for neighbour_index in range(index + 1, N):

                if np.random.random() < connection_probability:
                    node.connections[neighbour_index] = 1
                    self.nodes[neighbour_index].connections[index] = 1

    # to plot a network of size N with fixed probability of 0,5:
    def plot_network(self):

        for node in self.nodes:

            for i, connection in enumerate(node.connections):

                if connection == 1:
                    plt.plot([node.index, i], [node.value, self.nodes[i].value], 'k-', linewidth=0.8)
        plt.scatter([node.index for node in self.nodes], [node.value for node in self.nodes], color='g')
        plt.xlabel('Node Number')
        plt.title('Random Size Network')
        plt.show()


#task 4
    
    def make_random_network(self, N, connection_probability=0.5):
        '''
        This function makes a *random* network of size N.
        Each node is connected to each other node with probability p
        '''

        self.nodes = []
        for node_number in range(N):
            value = np.random.random()
            connections = [0 for _ in range(N)]
            self.nodes.append(Node(value, node_number, connections))

        for (index, node) in enumerate(self.nodes):
            for neighbour_index in range(index+1, N):
                if np.random.random() < connection_probability:
                    node.connections[neighbour_index] = 1
                    self.nodes[neighbour_index].connections[index] = 1


#making a ring network by adopting the concept of likelyhood but with a range of 1
#the ring network does not achieve higher cluster coefficient and can be rewired
    def make_ring_network(self,N,re_wire_prob=0.2):
        self.nodes = []
        for number in range(N):
            value = np.random.random()
            connections = [0 for _ in range(N)]
            self.nodes.append(Node(value, number, connections))

            #implementing the one to one connection implicitly
        for number,node in enumerate(self.nodes):
            for element in range(number-1,number+2):
                neighbour_index = element % N
                if neighbour_index!=number:
                    node.connections[neighbour_index]=1

#this concept was used to design small world but it is not significant while making ring network
#this part is optional however but it helped come up with the small world
        for number, node in enumerate(self.nodes):
            for neighbour_index, connection in enumerate(node.connections):
                if connection==1 and np.random.random()<re_wire_prob:
                    new_neighbour = np.random.choice(self.nodes)
                    while(new_neighbour == node or new_neighbour.connections[node.index]== 1):
                        new_neighbour=np.random.choice(self.nodes)
                    node.connections[neighbour_index]=0
                    node.connections[new_neighbour.index] = 1
    def make_small_world_network(self,N,re_wire_prob=0.2):
        self.nodes=[]
        #designing the network based on the value inputted by the user
        for number in range(N):
            value=np.random.random()
            connections =[0 for _ in range(N)]
            self.nodes.append(Node(value, number, connections))
#implementing network connection beyonf a range of 1 unlike for ring network
        for number, node in enumerate(self.nodes):
            for element in range(number-2,number+3):
                neighbour_index = element % N
                if neighbour_index != number:
                    node.connections[neighbour_index]=1
#introducing the concept of likelyhood with a re_wiring probability
        for number, node in enumerate(self.nodes):
            for neighbour_index, connection in enumerate(node.connections):
                if connection == 1 and np.random.random() < re_wire_prob:
                    new_neighbour = np.random.choice(self.nodes)
                    while (new_neighbour == node or new_neighbour.connections[node.index]):
                        new_neighbour = np.random.choice(self.nodes)
                    node.connections[neighbour_index] = 0
                    node.connections[new_neighbour.index] =1

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_axis_off()
        
        num_nodes = len(self.nodes)
        network_radius = num_nodes * 10
        ax.set_xlim([-1.1*network_radius, 1.1*network_radius])
        ax.set_ylim([-1.1*network_radius, 1.1*network_radius])
        #this dictionary will store nodes positions
        positions={}
        #ensuring that all nodes are accounted for
        for (i, node) in enumerate(self.nodes):
            node_angle = i * 2 * np.pi / num_nodes
            node_x = network_radius * np.cos(node_angle)
            node_y = network_radius * np.sin(node_angle)
            positions[node.index]=(node_x,node_y)
            
            circle = plt.Circle((node_x, node_y), 0.9*num_nodes, color=cm.hot(node.value))
            ax.add_patch(circle)
            
            for neighbour_index in range(i+1, num_nodes):
                if node.connections[neighbour_index]:
                    neighbour_angle = neighbour_index * 2 * np.pi / num_nodes
                    neighbour_x = network_radius * np.cos(neighbour_angle)
                    neighbour_y = network_radius * np.sin(neighbour_angle)
                    width=node.connections[neighbour_index]*2
                    
                    ax.plot((node_x, neighbour_x), (node_y, neighbour_y), color='black',linewidth=width)
        for node in self.nodes:
            node_x, node_y = positions[node.index]
            ax.text(node_x, node_y, str(node.index), ha="center", va="center")
        plt.show()


def test_networks():

    #Ring network
    nodes = []
    num_nodes = 10
    for node_number in range(num_nodes):
        connections = [0 for val in range(num_nodes)]
        connections[(node_number-1)%num_nodes] = 1
        connections[(node_number+1)%num_nodes] = 1
        new_node = Node(0, node_number, connections=connections)
        nodes.append(new_node)
    network = Network(nodes)

    print("Testing ring network")
    assert(network.get_mean_degree()==2), network.get_mean_degree()
    assert(network.get_clustering()==0), network.get_clustering()
    assert(network.get_path_length()==2.777777777777778), network.get_path_length()

    nodes = []
    num_nodes = 10
    for node_number in range(num_nodes):
        connections = [0 for val in range(num_nodes)]
        connections[(node_number+1)%num_nodes] = 1
        new_node = Node(0, node_number, connections=connections)
        nodes.append(new_node)
    network = Network(nodes)

    print("Testing one-sided network")
    assert(network.get_mean_degree()==1), network.get_mean_degree()
    assert(network.get_clustering()==0),  network.get_clustering()
    assert(network.get_path_length()==5), network.get_path_length()

    nodes = []
    num_nodes = 10
    for node_number in range(num_nodes):
        connections = [1 for val in range(num_nodes)]
        connections[node_number] = 0
        new_node = Node(0, node_number, connections=connections)
        nodes.append(new_node)
    network = Network(nodes)

    print("Testing fully connected network")
    assert(network.get_mean_degree()==num_nodes-1), network.get_mean_degree()
    assert(network.get_clustering()==1),  network.get_clustering()
    assert(network.get_path_length()==1), network.get_path_length()

    print("All tests passed")

'''
==============================================================================================================
This section contains code for the Ising Model - task 1 in the assignment
==============================================================================================================
'''
def calculate_agreement(population, row, col, external=0.0):

    n_rows, n_cols = population.shape
    current_opinion = population[row, col]
    total_agreement = 0.0

    # Calculate agreement with horizontal neighbors
    left_neighbor = population[row, (col - 1) % n_cols]
    right_neighbor = population[row, (col + 1) % n_cols]

    # Calculate agreement with vertical neighbors
    top_neighbor = population[(row - 1) % n_rows, col]
    bottom_neighbor = population[(row + 1) % n_rows, col]

    total_agreement = current_opinion * (left_neighbor + right_neighbor + top_neighbor + bottom_neighbor) + external * current_opinion

    # Calculate change in agreement if the cell flips its value
    change_in_agreement = -2 * total_agreement

    return total_agreement


def ising_step(population, external=0.0,alpha=1.0):

    n_rows, n_cols = population.shape
    row = np.random.randint(0, n_rows)
    col = np.random.randint(0, n_cols)

    total_agreement = calculate_agreement(population, row, col, external)

    if total_agreement <= 0:
        population[row, col] *= -1

    elif total_agreement > 0 and alpha is not None and alpha != 0:
        if np.random.rand() < np.exp(-total_agreement/ alpha):
            population[row, col] *= -1

def plot_ising(im, population):
    new_im = np.array([[255 if val == -1 else 1 for val in rows] for rows in population], dtype=np.int8)
    im.set_data(new_im)
    plt.pause(0.1)

def test_ising():
    print("Testing ising model calculations")
    population = -np.ones((3, 3))
    assert (calculate_agreement(population, 1, 1) == 4), "Test 1"

    population[1, 1] = 1.
    assert (calculate_agreement(population, 1, 1) == -4), "Test 2"

    population[0, 1] = 1.
    assert (calculate_agreement(population, 1, 1) == -2), "Test 3"

    population[1, 0] = 1.
    assert (calculate_agreement(population, 1, 1) == 0), "Test 4"

    population[2, 1] = 1.
    assert (calculate_agreement(population, 1, 1) == 2), "Test 5"

    population[1, 2] = 1.
    assert (calculate_agreement(population, 1, 1) == 4), "Test 6"

    "Testing external pull"
    population = -np.ones((3, 3))
    assert (calculate_agreement(population, 1, 1, 1) == 3), "Test 7"
    assert (calculate_agreement(population, 1, 1, -1) == 5), "Test 8"
    assert (calculate_agreement(population, 1, 1, 10) == -6), "Test 9"
    assert (calculate_agreement(population, 1, 1, -10) == 14), "Test 10"

    print("Tests passed")

def ising_main(population, alpha=1.0, external=0.0):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    im = ax.imshow(population, interpolation='none', cmap='RdPu')

    # Iterating an update 100 times
    for frame in range(100):
        # Iterating single steps 1000 times to form an update
        for step in range(1000):
            ising_step(population, external,alpha)
        print('Step:', frame, end='\r')
        plot_ising(im, population)

'''
==============================================================================================================
This section contains code for the Defuant Model - task 2 in the assignment
==============================================================================================================
'''
# helper function 1
def defuant_update(opinions, beta, threshold, is_network=False):
    """
    Perform a single update according to the Deffuant model.

    Args:
        opinions (numpy.ndarray): Array representing opinions of individuals.
        beta (float): Coupling parameter.
        threshold (float): Threshold parameter.

    Returns:
        None
    """
    
    if is_network:
        person = np.random.choice(opinions.nodes)

        # Find indices where value is 1
        indices_ones = np.where(np.array(person.connections) == 1)[0]

        #print(indices_ones)

        t = indices_ones.shape[0]

        # skip update if the node has no neighbours
        if t == 0:
            return None

        
        # Choose a random index from the indices where value is 1
        neighbour_index = np.random.choice(indices_ones)
        neighbour = opinions.nodes[neighbour_index]

        peron_prev = person.value
        neighbour_prev = neighbour.value

        if abs(peron_prev - neighbour_prev) < threshold:
                person.value += beta * (neighbour_prev - peron_prev)
                neighbour.value += beta * (peron_prev - neighbour_prev)

    else:
        population = opinions.shape[0]

        # skip update if no. opinions <= 1 
        if population <= 1:
            return None
        
        else:
            # Randomly select direction (left or right)
            neighbour_dir = np.random.choice([1, -1])

            # Randomly selecting a person's index and calculating its corresponding neighbour's index
            person_idx = np.random.choice(population)
            neighbour_idx = person_idx + neighbour_dir

            # Ensure neighbour index stays within bounds
            if person_idx == 0:
                neighbour_idx = 1
            elif person_idx == population - 1:
                neighbour_idx = population - 2

            # Get opinions of the two individuals
            person = opinions[person_idx]
            neighbour = opinions[neighbour_idx]

            # Update opinions if difference is below threshold
            if abs(person - neighbour) < threshold:
                opinions[person_idx] += beta * (neighbour - person)
                opinions[neighbour_idx] += beta * (person - neighbour)

        return True


# helper function 2
def defuant_plot(iteration_data, beta, threshold):
    """
    Plot the evolution of opinions over iterations and a histogram of final opinions.

    Args:
        iteration_data (numpy.ndarray): Array containing opinions at each iteration.
        beta (float): Coupling parameter.
        threshold (float): Threshold parameter.

    Returns:
        None
    """

    # Create an array of indices for plotting
    indices = np.arange(iteration_data.shape[0]).reshape(-1, 1)
    duplicated_indices = np.tile(indices, (1, iteration_data.shape[1]))

    # Plotting
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    ax[0].hist(iteration_data[-1])
    ax[0].set_xlim([0, 1])
    ax[0].set_xlabel("Opinion")

    ax[1].scatter(duplicated_indices, iteration_data, color='r', s=5)
    ax[1].set_ylim([0, 1])
    ax[1].set_ylabel("Opinion")

    fig.suptitle(f"Coupling: {beta}, Threshold: {threshold}")

    plt.show()


# main function - task 2
def defuant_main(is_network = False, population=25, iterations=1000, beta=0.2, threshold=0.2):
    """
    Run the Deffuant model simulation and visualize the results.

    Args:
        population (int): Number of individuals.
        iterations (int): Number of iterations.
        beta (float): Coupling parameter.
        threshold (float): Threshold parameter.

    Returns:
        None
    """

    if not is_network:
        
        # Generate initial 1D opinions
        initial_opinions = np.random.uniform(0, 1, size=population) 
        
        # Simulation loop
        data = []
        for _ in range(iterations):

            #appending current iteration opinions to the 2d array (data)
            data.append(initial_opinions.copy()) 

            # updating opinions
            defuant_update(initial_opinions, beta=beta, threshold=threshold)

        data = np.array(data)

        # Plot results
        defuant_plot(data, beta=beta, threshold=threshold)

    else: 
        network  =  Network()
        network.make_random_network(N = population)

        # Simulation loop
        data = []
        for _ in range(iterations):

            # appending current-iteration network opinions to the 2d array (data)
            data.append([node.value for node in network.nodes]) 

            # updating opinions
            defuant_update(network, beta=beta, threshold=threshold, is_network=True)

        data = np.array(data)

        # Plot results
        defuant_plot(data, beta=beta, threshold=threshold)



# test function - task 2
def test_defuant():
    '''
    This function will test the defuant_update function in the defuant model 
    '''
    
    print("Testing")

    test_opinions_c = np.random.uniform(0, 1, size=100)
    test_opinions_n = test_opinions_c.copy()

    # test 1: ensures only two neighbours get updated each iteration, or none 
    test_1 = True

    # test 2: ensures distant neighbours (distance > 1) not get updated 
    test_2 = True

    # test 3: ensures no update happens at threshold = 0
    test_3 = True

    # test 4: ensures system returns none at population == 1 or 0
    test_4 = True


    ## testing code (t1 & t2)
    for _ in range(1000):
        
        defuant_update(test_opinions_n, beta=0.2, threshold=0.2)
        eq_mask = (test_opinions_c == test_opinions_n)
        updated_idx = np.where(eq_mask == False)[0]
        if updated_idx.shape[0] == 2:
            p1_idx , p2_idx = updated_idx 
            distance = abs(p2_idx - p1_idx)
            if distance != 1:
                test_2 = False
        
        elif updated_idx.shape[0] == 0:
            pass
        
        else:
            test_1 = False

        test_opinions_c = test_opinions_n.copy()
    

    ## testing code (t3)
    test_opinions = np.random.uniform(0, 1, size=100)
    test_opinions_updated = test_opinions.copy()

    for _ in range(1000):
        defuant_update(test_opinions_updated,beta=0.2,threshold=0)
        eq_mask = (test_opinions == test_opinions_updated)
        if eq_mask.all() != True:
            test_3 = False
    
    ## testing code (t4)
    test_4 = False if not (defuant_update(np.array([]),beta=0.2,threshold=0.2) or
                      not defuant_update(np.random.uniform(0, 1,size=1),beta=0.2,threshold=0.2)) else True



    assert(test_1), "test 1"
    assert(test_2), "test 2"
    assert(test_3), "test 3"
    assert(test_4), "test 4"


    print("Tests passed")

'''
==============================================================================================================
This section contains code for the main function- you should write some code for handling flags here
==============================================================================================================
'''

def main():

    parser = argparse.ArgumentParser(description='running tasks 1-5, fcp final project')

    ########################### Adding Parser Arguments ###########################

    #TASK 1 ARGS
    parser.add_argument('-ising_model', action='store_true', help='Run the Ising model')
    parser.add_argument("-external", type=float, default=0.0, help="external influence is zero")
    parser.add_argument("-alpha", type=float, default=1.0, help="temperature default is 1")
    parser.add_argument("-test_ising", action="store_true", help="running test for the ising model")

    # TASK 2 ARGS  
    parser.add_argument('--defuant', '-defuant', action='store_true', help='runs the defuant model')
    parser.add_argument("-beta",  type=float, default=0.2, help="beta parameter of the defuant model - default = 0.2")
    parser.add_argument("-threshold",  type=float, default=0.2, help="threshold parameter of the defuant model - default = 0.2")
    parser.add_argument('--test_defuant', '-test_defuant', action='store_true', help='runs the defuant model test function')

    # TASK 3 ARGS  
    parser.add_argument("-network", type=int, help= "runs the network, add an integer value to choose the size of the network")
    parser.add_argument("-test_network", action='store_true' , help= "prints the results required")

    # TASK 4 ARGS  
    parser.add_argument("-ring_network", type=int, help="enter a flag -ring_network and value")
    parser.add_argument("-small_world", type=int, help="enter a flag -small_network and value")
    parser.add_argument("-probability",type=float,default=0.00001,help="enter a flag -probability followed by a float between 0 and 1")
    parser.add_argument("-re_wire", type=float, default=0.2, help="enter a float within a range of 0 and 1")

    # TASK 5 ARGS  
    parser.add_argument("-use_network", type=int)

    ########################### End Adding Parser Arguments ###########################

    args = parser.parse_args()

    ########################### interpreting terminal flags ###########################
    
    # Task 1
    if args.ising_model:
        population = -np.random.choice([-1,1], size=(100, 100))
        ising_step(population,external=args.external)
        ising_main(population,alpha=args.alpha,external=args.external)

    if args.test_ising:
        test_ising()


    # Task 2
    beta = args.beta
    threshold = args.threshold
    is_defuant = args.defuant
    is_test_defuant = args.test_defuant

    if is_defuant and not args.use_network:
        defuant_main(beta = beta, threshold = threshold)
    
    if is_test_defuant:
        test_defuant()

    # Task 3 
    size = args.network

    if args.test_network:

        nodes = []
        num_nodes = 10
        for node_number in range(num_nodes):
            connections = [1 for val in range(num_nodes)]
            connections[node_number] = 0
            new_node = Node(0, node_number, connections=connections)
            nodes.append(new_node)
        network = Network(nodes)

        assert (network.get_mean_degree() == num_nodes - 1), network.get_mean_degree()
        assert (network.get_mean_clustering() == 1), network.get_mean_clustering()
        assert (network.get_mean_path_length() == 1), network.get_mean_path_length()
        print("correct")

    if args.network:
        network = Network()
        network.make_random_network(size)
        network.plot_network()
        mean_degree = network.get_mean_degree()
        mean_clustering = network.get_mean_clustering()
        mean_path_length = network.get_mean_path_length()

        print("Mean Degree:", mean_degree)
        print("Mean Clustering Coefficient:", mean_clustering)
        print("Mean Path Length:", mean_path_length)

        
    # Task 4 
    network = Network()

    if args.ring_network is not None:
        network.make_ring_network(args.ring_network, args.probability)
        network.plot()
    elif args.small_world is not None:
        network.make_small_world_network(args.small_world, args.re_wire)
        network.plot()

    # Task 5 
    if args.defuant and args.use_network:
        n = args.use_network
        defuant_main(is_network=True, population=n ,beta=args.beta, threshold=args.threshold)

    ########################### End interpreting terminal flags ###########################


if __name__=="__main__":
    main()
