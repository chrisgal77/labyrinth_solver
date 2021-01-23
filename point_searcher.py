import cv2
import numpy as np
import imutils
import os 
from copy import copy
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
            for point in self.points:
                if point[1] != 0:
                    return True
            return False

        def search_point_with_move_possibility(priority=None):
            for i, point in enumerate(self.points):
                if point[1]:
                    return self.points[i]
            raise RuntimeError('No such point')

        def set_point(direct):
            if direct == 'up' or direct == 'down':
                point = (current[0][0], current[0][1] + self.distances[direct])
                return [point, set_possibilities(point, self.opposite[direct])]
            elif direct == 'left' or direct == 'right':
                point = (current[0][0] + self.distances[direct], current[0][1])
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

        self.points = [[self.starting_point, set_possibilities(self.starting_point)]]
        self.connections = []

        current = self.points[0]
        checkpoint = self.points[0]
        direction = 'left'
        #TO_OPTIMIZE
        while is_move_possibility():
            
            if not current[1]:
                self.connections.append([checkpoint[0], current[0]])
                current = checkpoint
                
            elif len(current[1]) == 1 and direction in current[1]:
                current = set_point(direction)
                
                
            elif len(current[1]) == 1 and direction not in current[1]:
                self.connections.append([checkpoint[0], current[0]])
                checkpoint = current
                try:
                    checkpoint[1].remove(direction)
                except ValueError:
                    pass
                direction = choice(checkpoint[1])
                current = set_point(direction)
            
            elif len(current[1]) > 1 and direction in current[1]:
                self.connections.append([checkpoint[0], current[0]])
                checkpoint = current
                try:
                    checkpoint[1].remove(direction)
                except ValueError:
                    pass
                current = set_point(direction)
                
            else:
                self.connections.append([checkpoint[0], current[0]])
                checkpoint = current
                try:
                    checkpoint[1].remove(direction)
                except ValueError:
                    pass
                direction = choice(checkpoint[1])
                current = set_point(direction)
            time.sleep(0.5)
            print(current[0])
                
                    
            
            
            
            # try:
            #     current = search_point_with_move_possibility()
            # except RuntimeError:
            #     break
            # for i, direct in enumerate(current[1]):
            #     point = ()
            #     if direct == 'up' or direct == 'down':
            #         point = (current[0][0], current[0][1] + self.distances[direct])
            #         self.points.append([point, set_possibilities(point, self.opposite[direct])])
            #         print(self.points[len(self.points)-1])
            #     elif direct == 'left' or direct == 'right':
            #         point = (current[0][0] + self.distances[direct], current[0][1])
            #         self.points.append([point, set_possibilities(point, self.opposite[direct])])
            #         print(self.points[len(self.points)-1])
            #     current[1].pop(i)
            #     self.connections.append([current[0], point])

        return self.connections

if __debug__ and __name__ == "__main__":

    pts = PointsSearcher()
    pts.init('lab.png')
    pts.set_starting_point((980,480))
    print(pts.get_path())

        
