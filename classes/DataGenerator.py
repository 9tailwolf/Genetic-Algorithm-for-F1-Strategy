import pandas as pd
import numpy as np

class DataGenerator:
    def __init__(self,path:str):
        self.initial_data = pd.read_csv(path)
        self.ideal = None

    def data_processing(self):
        practice = self.initial_data
        data = {'Soft': [], 'Medium': [], 'Hard': [], 'Inter': [], 'Wet': []}
        for i in range(len(practice)):
            lap = practice.loc[i]
            d = {'Lap': lap['Lap'], 'LapTime': lap['LapTime'], 'Fuel': lap['Fuel'],
                 'Wear': max([lap['FLWear'], lap['FRWear'], lap['RLWear'], lap['RRWear']])}
            data[str(lap['Compound'])].append(d)

        for i in data.keys():
            if len(data[i]) != 0:
                data[i] = self.data_processing_fuel(data[i])
        return data


    def data_processing_fuel(self, lap_data):
        for i in range(len(lap_data) - 1):
            lap_data[i]['FuelUsage'] = round(
                (lap_data[i]['Fuel'] - lap_data[i + 1]['Fuel']) / (lap_data[i + 1]['Lap'] - lap_data[i]['Lap']), 5)
        lap_data[-1]['FuelUsage'] = round(
            sum([lap_data[i]['FuelUsage'] for i in range(len(lap_data) - 1)]) / (len(lap_data) - 1), 5)
        return lap_data

    def get_ideal(self, lap_data, time_per_fuel=30):
        return int(min([i['LapTime'] - time_per_fuel * i['Fuel'] for i in lap_data]))

    def data_for_regression(self, soft_ideal_lapime, lap_data, time_per_fuel=30, correction_wear=3, correction_ideal=5,
                            wear_limit=40, wear_limit_performance=92):
        Y = np.array([soft_ideal_lapime * 100 / (i['LapTime'] - time_per_fuel * i['Fuel']) for i in lap_data])
        ideal_lap = max(Y)
        Y = np.array(
            [soft_ideal_lapime * 100 / (i['LapTime'] - time_per_fuel * i['Fuel']) for i in lap_data] + [ideal_lap for _
                                                                                                        in range(
                    correction_ideal)] + [wear_limit_performance for _ in range(correction_wear)])

        estim_laps = wear_limit / (
                    sum([lap_data[i]['Wear'] - lap_data[i - 1]['Wear'] for i in range(1, len(lap_data))]) / (
                        len(lap_data) - 1))
        X1 = np.array([i['Lap'] for i in lap_data] + [1 for i in range(correction_ideal)] + [estim_laps for i in
                                                                                             range(correction_wear)])

        X2 = np.array([i['FuelUsage'] for i in lap_data])
        mean_fuel_usage = max(X2)
        X2 = np.array(
            [i['FuelUsage'] for i in lap_data] + [mean_fuel_usage for _ in range(correction_ideal + correction_wear)])

        return Y, X1, X2, ideal_lap, estim_laps, mean_fuel_usage

    def data_generator(self,compound):
        data = self.data_processing()
        self.ideal = self.get_ideal(data['Soft'])
        return self.data_for_regression(self.ideal, data[compound],time_per_fuel=30, correction_wear=3, correction_ideal=5,
                            wear_limit=40, wear_limit_performance=92)