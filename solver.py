from graph import Graph
from graph import Node
from point_searcher import PointsSearcher
from numpy import sqrt

class LabyrinthSolver:
    def __init__(self):
        pass

    def take_labyrinth(self, filename, point):

        self.pts = PointsSearcher()
        self.pts.init(filename)
        self.pts.set_starting_point(point)
        
    def find_closest(self, aim):
        closest = [None, 100000] # point, distance
        for connection in self.path:
            for point in connection:
                distance = sqrt((point[0] - aim[0]) ** 2 + (point[1] - aim[1]) ** 2)
                if distance <= closest[1]:
                    closest = [point, distance]
        return closest[0]

    def solve(self, start, aim):

        self.path = self.pts.get_path()
        end = self.find_closest(aim)
        start = self.find_closest(start)
        g = Graph.create_from_connections(self.path, distances=True)
        a = g.A_algorithm(start, end)
        return a

if __debug__ and __name__ == "__main__":
    
    slr = LabyrinthSolver()
    slr.take_labyrinth('image.png', (980,380))
    slr.solve((980,380),(40,40))
