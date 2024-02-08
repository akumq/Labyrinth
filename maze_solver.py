import colorsys
import cv2
import math
import numpy as np
from collections import deque 

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)
    
    def __eq__(self, point):
        return (self.x == point.x) and ( self.y == point.y)
    
    def checkColor(self,image):
        b, g, r = image[self.y,self.x]
        return b,g,r

    def __hash__(self):
        return hash((self.x,self.y))
    
    def setColor(self,image,color=(0,255,255)):
        image[self.y,self.x] = color
    
    def __str__(self):
        return str(self.x)+"," + str(self.y)
    
class MazeSolver:
    
    def __init__(self,image):
        self.image = image
        self.points = []
        self.color = [(0,0,255),(0,255,0)]
        cv2.namedWindow('Image Base')
        cv2.setMouseCallback('Image Base',self.mouseEvent)
        cv2.imshow('Image Base', self.image)
    
    
    def getNeighboor(self,point):
        result = []
        temp = []
        temp.append(Point(point.x+ 1,point.y))
        temp.append(Point(point.x- 1,point.y))
        temp.append(Point(point.x,point.y+1))
        temp.append(Point(point.x,point.y-1))
        
        for p in temp:
            if p.checkColor(self.image) != (0,0,0):
                result.append(p)
            
        return result
    
    def BFS(self):
        depart = self.points[0]
        arrive = self.points[1]
        
        queue = deque()
        visited = set()
        parent = {}
        
        queue.append(depart)
        visited.add(depart)
        
        found = False
        while queue:
            current = queue.popleft()
            if current == arrive:
                found = True
                break
            
            for neighbor in self.getNeighboor(current):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    neighbor.setColor(self.image)
                    parent[neighbor] = current
        
        if found:
            path = []
            while current != depart:
                path.append(current)
                current = parent[current]
            path.append(depart)
            

            for p in path:
                cv2.circle(self.image,(p.x,p.y),2,(255,255,255),-1)
                # p.setColor(self.image, (255, 0, 0)) 
            cv2.imshow('Image Base', self.image)
        else:
            print("No path found")

    
    def mouseEvent(self,event,x,y,flags,params):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            # print("test")
            if(len(self.points) < 2):
                cv2.circle(self.image,(x,y),3,self.color[len(self.points)-1],-1)
                self.points.append(Point(x,y))
            else:
                self.BFS()
              
            cv2.imshow('Image Base', self.image)
            
            


image = cv2.imread("theseus.png")


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_,thresh = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
thresh = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)


maze = MazeSolver(thresh)

# cv2.imshow('Image Base', image)
# cv2.imshow('Image Thresh', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()