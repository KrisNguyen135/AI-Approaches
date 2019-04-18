import random#; random.seed(0)
import networkx as nx
import matplotlib.pyplot as plt


class Game:
    def __init__(self, n_cities, dis_matrix=None, dis_limit=1000):
        self.num_cities = n_cities
        self.dis_matrix = dis_matrix
        self.dis_limit = dis_limit

        # Generate the distance matrix if not specified
        if self.dis_matrix is None:
            self.dis_matrix = self.generate_dis_matrix(
                self.num_cities, self.dis_limit)

        # Network representation of cities
        self.net = nx.Graph()
        self.net.add_nodes_from(list(range(self.num_cities)))
        for row in range(self.num_cities):
            for col in range(row, self.num_cities):
                self.net.add_edge(row, col, weight=self.dis_matrix[row][col])

        self.net_layout = nx.spring_layout(self.net)

    def visualize_solution(self, sol):
        # Check whether the solution is valid
        if len(sol) != self.num_cities + 1:
            return False
        for city in sol:
            if not (isinstance(city, int) and 0 <= city < self.num_cities):
                return False
        if sol[0] != sol[-1]:
            return False

        # Calculate total distance
        running_dis = 0
        for i in range(len(sol) - 1):
            running_dis += self.dis_matrix[sol[i]][sol[i + 1]]
        plt.title(f'Total distance: {running_dis}')

        # Draw the general network
        nx.draw(
            self.net,
            with_labels=True,
            font_weight='bold',
            pos=self.net_layout
        )

        # Highlight the path specified by the solution
        nx.draw_networkx_edges(
            self.net,
            self.net_layout,
            edgelist=[(sol[i], sol[i + 1]) for i in range(len(sol) - 1)],
            edge_color='r'
        )

        # Customize edge labels
        edge_labels = nx.get_edge_attributes(self.net, 'weight')
        nx.draw_networkx_edge_labels(
            self.net,
            pos=self.net_layout,
            edge_labels=edge_labels
        )

        plt.show()

    @staticmethod
    def generate_dis_matrix(size, limit):
        dis_matrix = [[0 for _ in range(size)] for __ in range(size)]

        for row in range(size):
            for col in range(row, size):
                if row == col:
                    dis_matrix[row][col] = 0
                else:
                    dis_matrix[row][col] = dis_matrix[col][row] \
                        = random.randint(0, limit)

        return dis_matrix
