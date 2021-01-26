import  graphviz
import os
from math import sqrt

def in_collection(collection, arg):
    for i, element in enumerate(collection):
        try:
            if element[0] == arg:
                return True, i
        except TypeError:
            if element.value == arg.value:
                return True, i
    return False, None

class Node:
    def __init__(self, value):
        self.value = value
        self.connections = []

    def edge(self, other, edge_value=0):
        self.connections.append([other,edge_value])
        other.connections.append([self,edge_value])

    def __eq__(self, other):
        try:
            if self.value == other.value:
                return True
        except (TypeError, AttributeError):
            if self.value == other:
                return True
        return False

    def __repr__(self):
        return f'Node {self.value}'

class Graph:
    def __init__(self):
        self.vertices = []

    def node(self, node):
        if not in_collection(self.vertices, node)[0]:
            self.vertices.append(node)

    def edge(self, first_node, second_node, edge_value=0):
        
        self.node(first_node)
        self.node(second_node)  
        self.find(first_node.value).edge(second_node, edge_value) 

    def find(self, wanted_value):
        for i, item in enumerate(self.vertices):
            if item.value == wanted_value:
                return self.vertices[i]
        raise ValueError("No such item in the collection")

    def dijkstra_algorithm(self, start_node=0, aim=None):
        try:
            start_node = self.find(start_node.value)
        except AttributeError:
            start_node = self.vertices[start_node]
        try:
            aim = self.find(aim.value)
        except AttributeError:
            aim = self.vertices[aim]

        unvisited_set = [node for node in self.vertices]
        try:
            current_node = unvisited_set[start_node]
        except TypeError:
            current_node = unvisited_set[unvisited_set.index(start_node)]

        for i, node in enumerate(unvisited_set):
            if node != current_node:
                unvisited_set[i] = [node, 10000000]
            else:
                unvisited_set[i] = [node, 0]

        current_node = [current_node, 0]
        path = []

        while current_node[0] != aim:
            tentative_nodes = []
            addition = None
            try:
                for connection in current_node[0].connections:
                    if in_collection(unvisited_set, connection[0])[0]:
                        if unvisited_set[in_collection(unvisited_set, connection[0])[1]][1] < current_node[1]:
                            temp = [connection[0], unvisited_set[in_collection(unvisited_set, connection[0])[1]][1]]
                            unvisited_set[in_collection(unvisited_set, connection[0])[1]] = temp
                            addition = temp
                        else:
                            temp = [connection[0], current_node[1] + connection[1]]
                            unvisited_set[in_collection(unvisited_set, connection[0])[1]] = temp
                            tentative_nodes.append(temp)
            except:
                pass

            def find_min(collection):
                min_ = [None, 10000001]
                for node, value in collection:
                    if min_[1] > value:
                        min_ = [node, value]
                return min_

            try:
                unvisited_set.remove(current_node)
                path.append(current_node)
            except:
                break

            if addition:
                tentative_nodes.append(addition)
                current_node = find_min(tentative_nodes)
            else:
                current_node = find_min(tentative_nodes)

            if current_node[0] == None:
                current_node = find_min(unvisited_set)
        
        return current_node[1]

    def DFS(self, start_node, aim):
        pass


    def A_algorithm(self, start_node, aim):

        try:
            self.start_node = self.find(start_node)
        except AttributeError:
            self.start_node = self.vertices[start_node]
        try:
            self.aim = self.find(aim)
        except AttributeError:
            self.aim = self.vertices[aim]
        
        self.to_evaluate = [[self.start_node, 0]]
        self.evaluated = []

        path = []

        while True:

            def lowest_f():
                lowest = [None, 1000000]
                for i, point in enumerate(self.to_evaluate):
                    if lowest[1] > point[1]:
                        lowest = [i, point[1]]
                return self.to_evaluate[lowest[0]]

            def in_collection(collection, arg):
                for item in collection:
                    if item[0] == arg:
                        return True
                return False

            def exchange_to_evaluate(point, item):
                for i, item in enumerate(self.to_evaluate):
                    if point == item[0]:
                        self.to_evaluate[i] = [point, item]
                raise RuntimeError('Ops!')

            def calculate_f(point):
                return distance_to_target(point) + sqrt((int(point[0]) - int(self.current[0].value[0])) ** 2 + (int(point[1]) - int(self.current[0].value[1])) ** 2)

            def distance_to_target(point):
                return sqrt((int(point[0]) - int(self.aim.value[0])) ** 2 + (int(point[1]) - int(self.aim.value[1])) ** 2)

            self.current = lowest_f()
            self.to_evaluate.remove(self.current)
            self.evaluated.append(self.current)
            if self.current[0] == aim:
                path.append(self.current[0])
                break

            for node in self.current[0].connections:
                if not in_collection(self.evaluated, node[0]):
                    if distance_to_target(self.current[0].value) > distance_to_target(node[0].value) or not in_collection(self.to_evaluate, node):
                        path.append(self.current[0])
                        if not in_collection(self.to_evaluate, node[0]):
                            self.to_evaluate.append([node[0], calculate_f(node[0].value)])
                        else:
                            exchange_to_evaluate(node[0], calculate_f(node))
            
        output = []
        for element in path:
            if element not in output:
                output.append(element)
        return output


    def show(self, filename='graph'):

        graph_view = graphviz.Graph('G', filename=filename)

        for node in self.vertices:
               for node_, value in node.connections:
                   graph_view.edge(f'{node.value}', f'{node_}', label=f'{value}')
           
        graph_view.view()

    def input_graph(self):
        while True:
            input_ = input("Vertex name or end(q):")
            if input_ == 'q':
                break
            if Node(input_) not in self.vertices:
                self.vertices.append(Node(input_))
            current_node = self.find(input_)
            while True:       
                input_ = input("Neighbour's name and value (example:A 7) or end(q):")
                if input_ == 'q':
                    break
                input_ = input_.split(' ')
                if Node(input_[0]) not in self.vertices:
                    self.vertices.append(Node(input_[0]))
                g.edge(current_node, self.find(input_[0]), int(input_[1]))

    @classmethod
    def create_from_connections(cls, connections, distances=False, default_value = 1):
        g = cls()
        if distances:
            for pair in connections:
                if Node(pair[0]) not in g.vertices:
                    g.vertices.append(Node(pair[0]))
                if Node(pair[1]) not in g.vertices:
                    g.vertices.append(Node(pair[1]))
                g.edge(g.find(pair[0]), g.find(pair[1]), sqrt((pair[0][0] - pair[1][0]) ** 2 + (pair[0][1] - pair[1][1]) ** 2))
        else:
            for pair in connections:
                if Node(pair[0]) not in g.vertices:
                    g.vertices.append(Node(pair[0]))
                if Node(pair[1]) not in g.vertices:
                    g.vertices.append(Node(pair[1]))
                g.edge(g.find(pair[0]), g.find(pair[1]), default_value)
        
        return g

if __debug__ and __name__ == "__main__":
    
    # ASSERTS

    g = Graph()
    g.edge(Node('1'), Node('2'), 2)
    g.edge(Node('1'), Node('3'), 3)
    g.edge(Node('3'), Node('4'), 4)
    g.edge(Node('2'), Node('5'), 5)
    g.edge(Node('5'), Node('6'), 5)
    g.edge(Node('4'), Node('6'), 6)

    # assert in_collection(g.vertices, Node('1'))[0]
    # assert g.dijkstra_algorithm(Node('1'), Node('6'))[1] == 12
    a = g.A_algorithm(Node('1'), Node('6'))
    g.show('g')