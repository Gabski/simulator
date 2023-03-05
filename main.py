from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from kivy.clock import Clock
from  SimulationController import SimulationController
from SimulationState import SimulationState, ObstaclesManager
import numpy as np
from Car import Car
import csv  

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

class Goal(Widget):
    pass
class SensorPoint1(Widget):
    color = (1,1,0,1)
class SensorPoint2(Widget):
    color = (1,1,0,1)
class SensorPoint3(Widget):
    color = (1,1,0,1)
class SensorPoint4(Widget):
    color = (1,1,0,1)
class SensorPoint5(Widget):
    color = (1,1,0,1)


class SimulatorApp(App):

    def addTool(self, label, column, row, bind):
        elementSize = (200, 30)
        element = Button(text = label, pos = ((column - 1)* elementSize[0], (row - 1)* elementSize[1]), size = elementSize)
        element.bind(on_release = bind)
        self.ss.add_widget(element)
        return element  
    
    def addLabel(self, label, column, row):
        elementSize = (200, 30)
        element = Label(text = label, pos = ((column - 1)* elementSize[0], (row - 1)* elementSize[1]), size = elementSize)
        self.ss.add_widget(element)
        return element
    
    def restartSimulation(self):
        self.time = 0
        self.ss.loadScenario(self.sc.rounds, self.sc.goals, self.sc.scenario)
        self.ss.prepareCar()


    def saveResults(self):
        outputFile = "output.csv"
        with open(outputFile,'a') as fd:
            writer = csv.writer(fd)
            writer.writerow([self.sc.simulation, self.sc.rounds, self.time, self.sc.scenarioName()])
            fd.close()
                

    def build(self):
        self.sc = SimulationController("scenario.yaml")
        self.ss = SimulationState()
        self.restartSimulation()
        self.ss.drawGoals()
        self.om = ObstaclesManager()

        self.addTool('Wczytaj przeszkody', 1, 2,  self.load)
        self.addTool('Usuń przeszkody', 1, 1, self.clear)
        self.addTool('Zakończ symulacje', 3, 1, self.exit)
        self.addLabel('Czas scenariusza:', 4, 2)
        self.timerPlaceholder = self.addLabel('---', 4, 1)
        self.scenarioPlaceholder = self.addLabel(self.sc.scenarioName(), 5, 2)
        self.awardsPlaceholder = self.addLabel(self.sc.showAwards(), 5, 1)
        self.ss.add_widget(self.om)

        Clock.schedule_interval(self.ss.update, 1.0/60.0)
        Clock.schedule_interval(self.timer, 0.05)
        Clock.schedule_interval(self.simulationLoop, 0.01)

        return self.ss


    def simulationLoop(self, dt):

        limit = 60*10
        if(self.ss.isSymulationFinished() or limit < self.time):
            print(str(self.sc.scenarioName()) + " w czasie: " + str(self.time) + 's')
            self.saveResults()
            self.sc.nextSimulation()
            self.restartSimulation()
            self.scenarioPlaceholder.text = self.sc.scenarioName()
            self.awardsPlaceholder.text = self.sc.showAwards()

    def timer(self, dt):
        self.timerPlaceholder.text = str(self.time)
        self.time+=dt
        self.time = round(self.time, 2)

    def load(self, obj):
        self.om.loadObstacles() 

    def clear(self, obj):
        self.om.clearAllObstacles()

    def exit(self, obj):
        print("Zamykanie aplikacji")   
        self.stop() 
        
if __name__ == '__main__':
   SimulatorApp().run()
