import random

class Chromosome:
    def __init__(self, range_min, range_max):
        self.range_min = range_min
        self.range_max = range_max
        self.value = random.randint(range_min, range_max)

    def mutate(self):
        # Randomly reinitialize the chromosome's value within the defined range
        self.value = random.randint(self.range_min, self.range_max)

    def __str__(self):

        return f'{self.value}'

class Simulation:
    def __init__(self, steps, population_size, ranges, func, mutate_rate):
        self.steps = steps
        self.population_size = population_size
        self.chromosomes = [Chromosome(ranges[0], ranges[1]) for _ in range(population_size)]
        self.func = func
        self.ranges = ranges
        self.mutate_rate = mutate_rate

    def select(self, population, fitness):
        total_fitness = sum(fitness)
        selection_probs = [fit / total_fitness for fit in fitness]
        return random.choices(population, weights=selection_probs, k=2)

    def mutate(self, chromosome):
        if random.random() <= self.mutate_rate:
            chromosome.mutate()
        return chromosome

    def crossover(self, parent1, parent2):
        # Simple average crossover
        child_value = (parent1.value + parent2.value) // 2
        return Chromosome(self.ranges[0], self.ranges[1])  # Create a new Chromosome with the averaged value

    def run(self):
        for _ in range(self.steps):
            sorted_chromosome = sorted(self.chromosomes, key=lambda ch: ch.value)
            print([str(i) for i in sorted_chromosome])
            fitness = self.evaluate_population()
            new_population = []
            
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select(self.chromosomes, fitness)
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_population.append(child)

            self.chromosomes = new_population

        best_chromosome = max(self.chromosomes, key=lambda c: self.func(c.value))
        return best_chromosome.value, self.func(best_chromosome.value)

    def evaluate_population(self):
        return [self.func(x.value) for x in self.chromosomes]

# Run the simulation
sim = Simulation(steps=100, population_size=20, ranges=(0, 30), func=lambda x: -x ** 2 + 12 * x + 6, mutate_rate=0.02)
best_value, best_fitness = sim.run()
print(f"Best value: {best_value}, Best fitness (f(x)): {best_fitness}")

