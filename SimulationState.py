from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.vector import Vector
import numpy as np
from Ai import Ai
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle


firstUpdate = True
lastReward = 0

def init():
    global firstUpdate
    global obstacles
    obstacles = np.zeros((canvasWidth,canvasHeight))
    firstUpdate = False

class ObstaclesManager(Widget):

    def on_touch_down(self, touch):
        global length, nPoints, lastX, lastY, obstacles
        with self.canvas:
            Color(1,0.5,0)
            d=10.
            touch.ud['line'] = Line(points = (touch.x, touch.y), width = 1)
            lastX = int(touch.x)
            lastY = int(touch.y)
            nPoints = 0
            length = 0
            obstacles[int(touch.x),int(touch.y)] = 1

    def on_touch_move(self, touch):
        global length, nPoints, lastX, lastY, obstacles
        if touch.button=='left':
            touch.ud['line'].points += [touch.x, touch.y]
            x = int(touch.x)
            y = int(touch.y)
            length += np.sqrt(max((x - lastX)**2 + (y - lastY)**2, 2))
            lastX = x
            lastY = y
            nPoints += 1.
            touch.ud['line'].width = int(5)
            obstacles[int(touch.x) - 5 : int(touch.x) + 5, int(touch.y) - 5 : int(touch.y) + 5] = 1
          
    def clearAllObstacles(self):
        print("Usunięcie wszystkich przeszkód")
        global obstacles
        self.canvas.clear()
        obstacles = np.zeros((canvasWidth,canvasHeight))    

    def saveObstacles(self):
        print("Zapisanie stworzonych przeszkód do pliku")
        global obstacles
        with open('obstacles.npy', 'wb') as f:
            np.save(f, obstacles)

    def loadObstacles(self):
        print("Wczytanie zapisanych przeszkód")
        global obstacles
        with open('obstacles.npy', 'rb') as f:
            obstacles = np.load(f)
        
        for x in range(0,canvasWidth,4):
            for y in range(0,canvasHeight,4):
                if obstacles[x,y] == 1:
                    with self.canvas:
                        Color(1., 0, 0)
                        Rectangle(pos=(x, y), size=(1, 1))

     

class SimulationState(Widget):
    scores = []
    car = ObjectProperty(None)
    sensorPoint1 = ObjectProperty(None)
    sensorPoint2 = ObjectProperty(None)
    sensorPoint3 = ObjectProperty(None)
    sensorPoint4 = ObjectProperty(None)
    sensorPoint5 = ObjectProperty(None)
    goal = ObjectProperty(None)
    scenario = []
    goals = []
    actualGoal = 0
    round = 0
    goalX = ObjectProperty(None)
    goalY = ObjectProperty(None)
    lastDistance = 0
    
    endSymulation = False
    brain = Ai(6,3,0.9)
    
    def drawGoals(self):    
        for goal in self.goals:
            with self.canvas:
                Color(1., 0, 1.)
                Rectangle(pos=(goal['x'], goal['y']), size=(2, 2))


    def loadScenario(self, rounds, goals, scenario):
        self.round = 0
        self.scenario = scenario
        self.rounds = rounds
        self.goals = goals
        self.endSymulation = False


    def updateGoal(self):
        self.goalX = self.goals[self.actualGoal]['x']
        self.goalY = self.goals[self.actualGoal]['y']

    def prepareCar(self):
        self.car.center = self.center
        self.brain = Ai(6,3,0.9)
        
    def update(self, dt):
        global lastReward
        global canvasWidth
        global canvasHeight

        canvasWidth = self.width
        canvasHeight = self.height

        if firstUpdate:
            init()

        self.updateGoal()
        self.goal.pos =  Vector(self.goalX, self.goalY); 

        self.sensorPoint1.pos = self.car.sensor1
        self.sensorPoint2.pos = self.car.sensor2
        self.sensorPoint3.pos = self.car.sensor3
        self.sensorPoint4.pos = self.car.sensor4
        self.sensorPoint5.pos = self.car.sensor5
        helperxx = self.goalX - self.car.x
        helperyy = self.goalY - self.car.y
        orientation = Vector(*self.car.velocity).angle((helperxx,helperyy))/180.
        lastSignal = [self.car.signal1, self.car.signal2, self.car.signal3, self.car.signal4, self.car.signal5, orientation]

        action = self.brain.update(lastReward, lastSignal)
        actionrotation = [0,10,-10]
        rotation = actionrotation[action]

        self.scores.append(self.brain.score())
        speed = Vector(self.scenario['speed'], 0)
        self.car.update(speed, rotation, obstacles)

        distance = np.sqrt((self.car.x - self.goalX)**2 + (self.car.y - self.goalY)**2)
        lastReward = self.scenario['awards']['from_target']
       
        if distance < self.lastDistance:
            lastReward = self.scenario['awards']['to_target'] 
            
        signals = (self.car.signal1 + self.car.signal2 + self.car.signal3 + self.car.signal4 + self.car.signal5)

        if(signals > 0):
            lastReward = self.scenario['awards']['obstacle'] 

        if distance < 50:
            self.actualGoal += 1

            if(self.actualGoal >= len(self.goals)):
                self.actualGoal = 0
                self.round = self.round + 1
                if(self.rounds <= self.round):
                    self.endSymulation = True

            self.updateGoal()

        
        self.lastDistance = distance
    
    def save(self):
        self.brain.save()


    def load(self):
        self.brain.load()

    def isSymulationFinished(self):
        return self.endSymulation
