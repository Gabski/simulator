import yaml

class SimulationController(object):
    
    def __init__(self, file):
        with open(file) as f:
            self.data = yaml.load(f)

        if (self.data['version'][:2] != '1.'):
            print("Nie poprawna wersja pliku scenariusza")
            raise SystemExit(2)
        
        self.simulation = 0
        self.scenario = self.data['scenarios'][self.simulation]
        self.goals = self.data['goals']
        self.rounds = self.data['rounds']

    def nextSimulation(self):
        self.simulation += 1
        if(self.simulation>=len(self.data['scenarios'])):
                self.simulation = 0

        print(self.scenarioName())
        return self.simulation
    
    def scenarioName(self):
         return self.data['scenarios'][self.simulation]['name']
    
    def showAwards(self):
         return '[' + str(self.data['scenarios'][self.simulation]['awards']['from_target']) +  '; ' + str(self.data['scenarios'][self.simulation]['awards']['to_target']) + '; ' + str(self.data['scenarios'][self.simulation]['awards']['obstacle']) + ']'
