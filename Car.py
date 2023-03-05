from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
import numpy as np

class Car(Widget):
    
    velocityX = NumericProperty(0)
    velocityY = NumericProperty(0)
    velocity = ReferenceListProperty(velocityX, velocityY)
    rotation = NumericProperty(0)
    angle = NumericProperty(0)
    sensor1X = NumericProperty(0)
    sensor1Y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1X, sensor1Y)
    sensor2X = NumericProperty(0)
    sensor2Y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2X, sensor2Y)
    sensor3X = NumericProperty(0)
    sensor3Y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3X, sensor3Y)
    sensor4X = NumericProperty(0)
    sensor4Y = NumericProperty(0)
    sensor4 = ReferenceListProperty(sensor4X, sensor4Y)
    sensor5X = NumericProperty(0)
    sensor5Y = NumericProperty(0)
    sensor5 = ReferenceListProperty(sensor5X, sensor5Y)
    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)
    signal4 = NumericProperty(0)
    signal5 = NumericProperty(0)

    def update(self, speed, rotation, obstacles):
        self._moveCar(speed, rotation)
        self._moveSensors()
        self._detectSignalOfColision(obstacles)

    def _moveCar(self, speed, rotation):
        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation
        self.velocity = speed.rotate(self.angle)

    def _moveSensors(self):
        self.sensor1 = self._sensorPosition(35, 0)
        self.sensor2 = self._sensorPosition(30, 25)
        self.sensor3 = self._sensorPosition(30, -25)
        self.sensor4 = self._sensorPosition(25, 54)
        self.sensor5 = self._sensorPosition(25, -54)

    def _detectSignalOfColision(self, obstacles):
        self.signal1 = self._convertSignal(obstacles, self.sensor1X, self.sensor1Y)
        self.signal2 = self._convertSignal(obstacles, self.sensor2X, self.sensor2Y)
        self.signal3 = self._convertSignal(obstacles, self.sensor3X, self.sensor3Y)
        self.signal4 = self._convertSignal(obstacles, self.sensor4X, self.sensor4Y)
        self.signal5 = self._convertSignal(obstacles, self.sensor3X, self.sensor5Y)

    def _convertSignal(self, obstacles, sensorX, sensorY):
        return int(np.sum(obstacles[int(sensorX)-10:int(sensorX)+10, int(sensorY)-10:int(sensorY)+10]))/400

    def _sensorPosition(self, sensorPosition, sensorAngle):
        return Vector(sensorPosition,0).rotate((self.angle+sensorAngle)%360) + Vector(-2.5,-2.5) + self.center 

