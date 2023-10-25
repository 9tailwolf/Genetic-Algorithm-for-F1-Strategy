# Genetic-Algorithm-for-F1-Strategy
I apply basic genetic algorithm in fomular1 to optimize the race strategy with practice session datas.

When you type below code on your terminal, then the code will be executed.

```bash
python main.py
```

If you want to change condition for find strategy, you should type below.

```bash
python main.py --circuit='Bahrain' --initial_population_size=100 --pit_time=60 --max_pitstop=4 --selection_size=20 --crossover_size=40 --mutation_size=40 --iteration=100 --result_size=30
```

The circuit that you can input.
- Bahrain
- Montreal
- Spielberg
- Zandvoort


You need below library to run without error.
- Python 3.9
- numpy
- pandas
- tqdm
- random
- argparse
- time
