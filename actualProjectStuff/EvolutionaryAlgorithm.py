from Matrix import Matrix

class EvolutionaryAlgorithm:
    
    def __init__(self, population, students):
        self.population = population
        self.students = students
    
    def evaluate(self):
        for i in self.population:
            i.setScore(i.measure())
        
    
