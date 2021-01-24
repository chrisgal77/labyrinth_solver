import cv2
import numpy as np
import imutils
import os 
from copy import copy, deepcopy
from random import randint, choice
import time

class PointsSearcher:
    def __init__(self):
        pass

    def init(self, image_name='image.png'):
        
        if os.path.isfile(os.path.dirname(__file__) + '/' + image_name):
            self.image = cv2.imread(os.path.dirname(__file__) + '/' + image_name)
        else:
            raise IOError("No such file")

    def set_starting_point(self, point):
        self.starting_point = point

    def get_path(self, step=20):
        
        print("Processing...")

        self.distances = {
            'right' : step,
            'left' : -step,
            'up' : -step,
            'down' : step
        }

        self.opposite = {
            'right' : 'left',
            'left' : 'right',
            'up' : 'down',
            'down' : 'up'
        }

        def is_move_possibility():
            for point in self.checkpoints:
                if point[1]:
                    return True
            if self.current[1]:
                return True
            return False

        def in_collection(collection, item):
            for element in collection:
                if item[0] == element[0]:
                    return True
            return False

        def search_point_with_move_possibility(collection, priority=None):
            for i, point in enumerate(collection):
                if point[1]:
                    return collection[i]
            raise RuntimeError('No such point')

        def exchange(collection, item):
            for i, element in enumerate(collection):
                if item[0] == element[0]:
                    collection[i] = item
                    break

        def set_point(direct):
            if direct == 'up' or direct == 'down':
                point = (self.current[0][0], self.current[0][1] + self.distances[direct])
                return [point, set_possibilities(point, self.opposite[direct])]
            elif direct == 'left' or direct == 'right':
                point = (self.current[0][0] + self.distances[direct], self.current[0][1])
                return [point, set_possibilities(point, self.opposite[direct])]

        def set_possibilities(point, exclude=None):
            
            directions = []
            photo = copy(self.image)
            hsv_frame = cv2.cvtColor(photo, cv2.COLOR_BGR2HSV)
            lower = np.array((0,0,0), dtype = "uint8")
            upper = np.array((16,16,16), dtype = "uint8")
            mask = cv2.inRange(hsv_frame, lower, upper)
            mask = cv2.threshold(mask,200,255,cv2.THRESH_BINARY)[1]

            for way in ['right','left']:
                if point[0] + self.distances[way] < len(self.image[0]) and point[0] + self.distances[way] > 0:
                    frameBoolean = np.zeros((len(self.image),len(self.image[0]),3),dtype = "uint8")
                    frameBoolean = cv2.circle(copy(frameBoolean),(point[0] + self.distances[way], point[1]), 4,(255,255,255),-1)
                    thresh = cv2.threshold(copy(frameBoolean),200,255,cv2.THRESH_BINARY)[1]
                    thresh = cv2.bitwise_and(thresh,thresh,mask=mask)
                    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
                    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)

                    if not len(cnts)==1:
                        directions.append(way)

            for way in ['up','down']:
                if point[1] + self.distances[way] > 0 and point[1] + self.distances[way] < len(self.image):
                    frameBoolean = np.zeros((len(self.image),len(self.image[0]),3),dtype = "uint8")
                    frameBoolean = cv2.circle(copy(frameBoolean),(point[0], point[1] + self.distances[way]),4,(255,255,255),-1)
                    thresh = cv2.threshold(copy(frameBoolean),200,255,cv2.THRESH_BINARY)[1]
                    thresh = cv2.bitwise_and(thresh,thresh,mask=mask)
                    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
                    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)

                    if not len(cnts)==1:
                        directions.append(way)
            try:
                directions.remove(exclude)
            except ValueError:
                pass

            return directions

        self.connections = []

        self.current = [self.starting_point, set_possibilities(self.starting_point)]
        self.checkpoints = []
        checkpoint = deepcopy(self.current)
        
        direction = 'left'
        checkpoint[1].remove(direction)
        self.checkpoints.append(checkpoint)
        #TO_OPTIMIZE
        while is_move_possibility():
            
            if not self.current[1]:
                self.connections.append([checkpoint[0], self.current[0]])
                try:
                    self.current = search_point_with_move_possibility(self.checkpoints)
                except RuntimeError:
                    break
                checkpoint = self.current
                
            elif len(self.current[1]) == 1 and direction in self.current[1]:
                self.current = set_point(direction)
                
                
            elif len(self.current[1]) == 1 and direction not in self.current[1]:
                self.connections.append([checkpoint[0], self.current[0]])
                checkpoint = deepcopy(self.current)
                direction = choice(checkpoint[1])
                try:
                    checkpoint[1].remove(direction)
                except ValueError:
                    pass
                if not in_collection(self.checkpoints, checkpoint):
                    self.checkpoints.append(checkpoint)
                else:
                    exchange(self.checkpoints, checkpoint)
                
                self.current = set_point(direction)
            
            elif len(self.current[1]) > 1 and direction in self.current[1]:
                self.connections.append([checkpoint[0], self.current[0]])
                checkpoint = deepcopy(self.current)
                try:
                    checkpoint[1].remove(direction)
                except ValueError:
                    pass
                if not in_collection(self.checkpoints, checkpoint):
                    self.checkpoints.append(checkpoint)
                else:
                    exchange(self.checkpoints, checkpoint)
                self.current = set_point(direction)
                
            else:
                self.connections.append([checkpoint[0], self.current[0]])
                checkpoint = deepcopy(self.current)
                direction = choice(checkpoint[1])
                try:
                    checkpoint[1].remove(direction)
                except ValueError:
                    pass
                if not in_collection(self.checkpoints, checkpoint):
                    self.checkpoints.append(checkpoint)
                else:
                    exchange(self.checkpoints, checkpoint)
                self.current = set_point(direction)

        to_del = []
        for i, connection in enumerate(self.connections):
            if connection[0] == connection[1]:
                to_del.append(i)

        for i in reversed(to_del):
            self.connections.pop(i)

        print("Path taken.")

        return self.connections

if __debug__ and __name__ == "__main__":

    pts = PointsSearcher()
    pts.init('lab1.png')
    pts.set_starting_point((980,480))
    print(pts.get_path())
        
