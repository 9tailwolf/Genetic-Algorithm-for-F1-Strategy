import argparse

from classes.Genetic import Genetic
from classes.DataGenerator import data_writer

path = './data/Bahrain.csv'
def get_circuit(circuit):
    possible_circuit = set(['Bahrain','Montreal','Spielberg','Zandvoort'])
    path = './data/'+circuit+'.csv'
    laps = {'Bahrain':57,'Montreal':70,'Spielberg':71,'Zandvoort':72 }
    if circuit not in possible_circuit:
        raise Exception('No Circuit')
    return path, laps[circuit]




def get_argparse():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument('--change', default=False, type=bool, help='Type True if you want to change variables for regression')
    parser.add_argument('--circuit', default='Bahrain', type=str, help='Circuits : You can use Bahrain,Montreal,Spielberg,Zandvoort')
    parser.add_argument('--initial_population_size', default=100, type=int, help='Population size')
    parser.add_argument('--pit_time', default=60, type=int, help='Estimated pit time')
    parser.add_argument('--max_pitstop', default=4, type=int, help='Maximum pitstip size')
    parser.add_argument('--selection_size', default=20, type=int, help='Selection size')
    parser.add_argument('--crossover_size', default=40, type=int, help='Crossover size')
    parser.add_argument('--mutation_size', default=40, type=int, help='Mutation size')
    parser.add_argument('--iteration', default=100, type=int, help='Iteration size')
    parser.add_argument('--result_size', default=30, type=int, help='Strategies that you want to get')

    return parser

def main(args=None):
    if args.change == True:
        data_writer()
    else:
        path, lap = get_circuit(args.circuit)
        genetic = Genetic(path=path, initial_population_size=args.initial_population_size, lap=lap, pit_time=args.pit_time, max_pitstop=args.max_pitstop, selection_size=args.selection_size,
                          crossover_size=args.crossover_size, mutation_size=args.mutation_size, iteration=args.iteration)
        genetic.run(result_size=args.result_size)


if __name__ == '__main__':
    args = get_argparse().parse_args()
    main(args)
