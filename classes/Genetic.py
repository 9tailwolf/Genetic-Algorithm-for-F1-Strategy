import random
from tqdm import tqdm
import time

from classes.Strategy import Strategy
from classes.Strategy import strategyGenerator
from classes.Laptime import LaptimeCalculator
from classes.Strategy import find_possible_strategy

def laptime_calculation(path:str,strategy,pitstop_time):
    calculator = LaptimeCalculator(path)
    return calculator.calculation(strategy.decoded_strategy,strategy.pitstop,pitstop_time)

class Genetic:
    def __init__(self, path:str, initial_population_size:int, lap:int, pit_time:int,max_pitstop:int, selection_size:int, crossover_size:int, mutation_size:int, iteration:int):
        self.initial_population_size = initial_population_size
        self.lap = lap
        self.pit_time = pit_time
        self.max_pitstop = max_pitstop
        self.fuel_range = (100,110)
        self.fitting_function = LaptimeCalculator(path)
        self.selection_size = selection_size
        self.crossover_size = crossover_size
        self.mutation_size = mutation_size
        self.iteration = iteration
        self.population = None

        self.best_performance = 10**5
        self.best_strategy = None

        self.possible_strategy = find_possible_strategy(self.max_pitstop)
        self.save_results = {i:None for i in self.possible_strategy}
        self.save_performance = {i:10**5 for i in self.possible_strategy}

    def initial_population(self, pitstop, fuel):
        return strategyGenerator(self.initial_population_size, self.lap, pitstop, fuel)  # initial

    def fitness(self,strategy):
        return self.fitting_function.calculation(strategy.decoded_strategy,strategy.pitstop,self.pit_time)

    def compute_performance(self):
        performance = []
        for i in self.population:
            performance.append((Strategy(i.encoded_strategy,self.lap), round(self.fitness(Strategy(i.encoded_strategy,self.lap)),4)))

        sorted_population = sorted(performance, key=lambda x: x[1])
        return sorted_population

    def selection(self, performance):
        better_strategies = performance[:self.selection_size]
        better_strategies = [i[0] for i in better_strategies]
        return better_strategies

    def crossover(self, sub_population):
        crossovered_popupation = []
        for _ in range(self.crossover_size):
            parent1,parent2 = random.randint(0,self.selection_size-1), random.randint(0,self.selection_size-1)
            crossovered_popupation.append(sub_population[parent1] + sub_population[parent2])

        return crossovered_popupation

    def mutation(self, population):
        mutation_population = random.sample(population, self.mutation_size)
        for i in range(self.mutation_size):
            mutation_population[i] = mutation_population[i].mutate(self.max_pitstop,self.fuel_range)

        return mutation_population
    def generation(self):
        performance = self.compute_performance()
        self.compare_performance(performance)
        selected_population = self.selection(performance)
        crossover_population = self.crossover(selected_population)
        new_generation = selected_population + crossover_population
        mutation_population = self.mutation(new_generation)
        population = new_generation + mutation_population
        self.population = population

    def run(self,result_size):
        self.population = self.initial_population(self.max_pitstop, self.fuel_range)  # initial
        for _ in tqdm(range(self.iteration),desc='Genetic Algorithm'):
            self.generation()
            time.sleep(0.002)
        res = [self.save_results[i] if self.save_results[i] else(None,10**5) for i in self.possible_strategy]
        res.sort(key=lambda x:x[1])
        self.print_result(res,result_size)


    def compare_performance(self,strategies):
        good_strategy = strategies[0]
        if self.best_performance > good_strategy[1]:
            self.best_performance = good_strategy[1]
            self.best_strategy = Strategy(good_strategy[0].encoded_strategy,self.lap)

        for i in strategies:
            if self.save_performance[i[0].tire_encoding()] > round(self.fitness(Strategy(i[0].encoded_strategy,self.lap)),4):
                self.save_performance[i[0].tire_encoding()] = round(self.fitness(Strategy(i[0].encoded_strategy,self.lap)),4)
                self.save_results[i[0].tire_encoding()] = (Strategy(i[0].encoded_strategy,self.lap), round(self.fitness(Strategy(i[0].encoded_strategy,self.lap)),4))

    def print_result(self,res,result_size):
        for i in range(1,result_size +1):
            print('Strategy ',i,' : ',res[i-1][0])
