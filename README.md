# Genetic-Algorithm-for-F1-Strategy
I apply basic genetic algorithm in formula1 to optimize the race strategy with practice session datas.

When you type below code on your terminal, then the code will be executed.

```bash
python main.py
```

If you want to change condition for find strategy, you should type below.

```bash
python main.py --circuit='Bahrain' --initial_population_size=100 --pit_time=60 --max_pitstop=4 --selection_size=20 --crossover_size=40 --mutation_size=40 --iteration=100 --result_size=30
```

You can edit regression setup by

```bash
python main.py --change=True
```

Below is a option of setup.
- Laptime loss per fuel
- Correction of wear in regression
- Correction of ideal tire in regression
- Tire wear limitation
- Tire performance when limitation


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


I refered [This Paper](https://dl.acm.org/doi/10.1145/3583133.3596349)

For more Information, [Visit HERE](https://9tailwolf.github.io/playground/f1/genetic/)
