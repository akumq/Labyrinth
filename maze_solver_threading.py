import threading
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
    
    def distance(self, point):
        return math.sqrt((self.x+point.x)**2, (self.y+point.y)**2)
    
    def checkColor(self,image):
        b, g, r = image[self.y,self.x]
        return b,g,r

    def __hash__(self):
        return hash((self.x,self.y))
    
    def setColor(self,image,color=(0,255,255)):
        if(image.shape[0] >= self.y) and (image.shape[1] >= self.x):
            image[self.y,self.x] = color
    
    def __str__(self):
        return str(self.x)+"," + str(self.y)
    
class MazeSolver:
    
    def __init__(self,image):
        self.image = image
        self.points = []
        self.color = [(0,0,255),(0,255,0)]
        
        self.gradient_start_color = (0, 255, 255)
        self.gradient_end_color = (255, 0, 255) 
        self.gradient_steps = 750000
        # cv2.imshow('Image Base', self.image)
    
    
    def getNeighboor(self, point):
        result = []
       
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        for move in moves:
            new_x = point.x + move[0]
            new_y = point.y + move[1]
            
            if 0 <= new_x < self.image.shape[1] and 0 <= new_y < self.image.shape[0] and self.image[new_y, new_x].any() != 0:
                result.append(Point(new_x, new_y))
                
        return result
    
    def BFS(self):
        depart = self.points[0]
        arrive = self.points[1]
        
        queue = deque()
        visited = set()
        parent = {}
        
        queue.append(depart)
        visited.add(depart)

        gradient_colors = self.generate_gradient(self.gradient_start_color, self.gradient_end_color, self.gradient_steps)
        gradient_index = 0
        
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
                    neighbor.setColor(self.image, gradient_colors[gradient_index])
                    parent[neighbor] = current
                    gradient_index = (gradient_index + 1) % len(gradient_colors)
        
        if found:
            path = []
            while current != depart:
                path.append(current)
                current = parent[current]
            path.append(depart)
            

            for p in path:
                cv2.circle(self.image,(p.x,p.y),2,(255,255,255),-1)
                # p.setColor(self.image, (255, 0, 0)) 
        else:
            print("No path found")

    
    def mouseEvent(self,event,x,y,flags,params):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            # print("test")
            if(len(self.points) < 2):
                cv2.circle(self.image,(x,y),5,self.color[len(self.points)-1],-1)
                self.points.append(Point(x,y))
            # else:
            #     self.BFS()

            # cv2.imshow('Image Base', self.image)
            
    def display(self):
        print("displaying ...")
        cv2.imshow('out',self.image)
        cv2.setMouseCallback('out',self.mouseEvent)
        while True:
            cv2.imshow('out',self.image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite("./Resultat/BFS_out.png",self.image)
                break
    
    def generate_gradient(self, start_color, end_color, steps):
        gradient_colors = []
        for i in range(steps):
            r = int(start_color[0] + (end_color[0] - start_color[0]) * i / steps)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * i / steps)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * i / steps)
            gradient_colors.append((b, g, r))  
        return gradient_colors


image = cv2.imread("theseus.png")


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_,thresh = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
thresh = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)

maze = MazeSolver(thresh)

t= threading.Thread(target=maze.display,args=())
# t.daemon = True
t.start()

while len(maze.points) < 2:
    pass

maze.BFS()

# cv2.imshow('Image Base', image)
# cv2.imshow('Image Thresh', thresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()