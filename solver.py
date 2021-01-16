from graph import Graph
from point_searcher import PointsSearcher

class LabyrinthSolver:
    def __init__(self):
        pass

    def take_labyrinth(self, filename='image.png', starting_point=(0,0)):

        pts = PointsSearcher()
        pts.init(filename, starting_point=starting_point)
        self.path = pts.take_path()

    def solve(self):

        # points = []
        # for i, point in enumerate(self.path):
        #     if point[0] not in points:
        #         points.append(point[0])
        #     if i == len(self.path) - 1:
        #         points.append(point[1])

        # identity = {}
        # for i, point in enumerate(points):
        #     identity.update({(point[0], point[1]) : i})
        # for i, points in enumerate(self.path):
        #     for j, point in enumerate(points):
        #         to_change = (point[0], point[1])
        #         self.path[i][j] = identity[to_change]
        print(self.path)
        g = Graph.create_from_connections(self.path)
        print(g.dijkstra_algorithm(0,17)[0])

if __debug__ and __name__ == "__main__":
    
    slr = LabyrinthSolver()
    slr.take_labyrinth('image.png', (980,380))
    slr.solve()