import  graphviz
import os

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

    def __eq__(self, other):
        try:
            if self.value == other.value:
                return True
        except (TypeError, AttributeError):
            if self.value == other:
                return True
        return False

    def __repr__(self):
        return f'{self.value}'

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

        path = [current_node[0]]
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

            unvisited_set.remove(current_node)

            if addition:
                tentative_nodes.append(addition)
                current_node = find_min(tentative_nodes)
            else:
                current_node = find_min(tentative_nodes)

            if current_node[0] == None:
                current_node = find_min(unvisited_set)

            path.append(current_node[0])

        
        result = current_node[1]
        
        #TO_OPTIMIZE

        # new_list = [item for item in unvisited_set if item[1] < 10000000]
        # try:
        #     del new_list[len(new_list) - 1]

        #     path_correction = None
        #     for node in new_list:
        #         temp_path, temp_distance = self.dijkstra_algorithm(self.find(node[0]), aim)
        #         temp_distance += node[1]
        #         if temp_distance < result:
        #             result = temp_distance
        #             path_correction = temp_path
        #     try:
        #         path += path_correction
        #     except:
        #         pass
        # except IndexError:
        #     pass

        # shortest_path = [path[0]]
        # current_node = path[0]
        # while current_node != path[len(path)-1]:
        #     idx = []
        #     for to_compare in current_node.connections:
        #         if to_compare[0] in path:
        #             idx.append(path.index(to_compare[0]))
        #     current_node = path[max(idx)]
        #     shortest_path.append(current_node)
        
        return path, result

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
    def create_from_connections(cls, connections, default_value = 1):
        g = cls()
        
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

    assert in_collection(g.vertices, Node('1'))[0]
    assert g.dijkstra_algorithm(Node('1'), Node('6'))[1] == 12

    g.show('g')