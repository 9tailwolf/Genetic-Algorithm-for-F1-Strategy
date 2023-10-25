from tqdm import tqdm
import time

from classes.DataGenerator import DataGenerator

class Regression():
    def __init__(self,lr:int,lt:int,path:str,compound:str):
        self.lr = lr
        self.lt = lt
        self.path = path
        self.compound = compound

        self.Y = None
        self.X1 = None
        self.X2 = None
        self.ideal_lap = -1
        self.estim_laps = -1
        self.mean_fuel_usage = -1

        self.ideal_laptime = -1

    def is_setup(self):
        return self.Y

    def getdata(self):
        dataGenerator = DataGenerator(self.path)
        self.Y,self.X1,self.X2,self.ideal_lap,self.estim_laps,self.mean_fuel_usage = dataGenerator.data_generator(self.compound)
        self.ideal_laptime = dataGenerator.ideal

    def regression(self):
        minimum_fuel_usage = self.mean_fuel_usage * 0.9
        a = (92 - self.ideal_lap) / self.estim_laps ** 3
        b = -3 * a * self.estim_laps * 0.5
        c = 3 * a * self.estim_laps ** 2 * 0.5
        d = self.ideal_lap
        e = 1  # Unknown
        for _ in tqdm(range(self.lt),desc=self.compound + ' Compound Regression'):
            y = a * self.X1 ** 3 + b * self.X1 ** 2 + c * self.X1 + d + e * (self.X2 - minimum_fuel_usage)
            a_grad = sum((self.X1 ** 3) * (y - self.Y)) / len(self.X1)
            b_grad = sum((self.X1 ** 2) * (y - self.Y)) / len(self.X2)
            c_grad = sum((self.X1) * (y - self.Y)) / len(self.X1)
            d_grad = sum((y - self.Y)) / len(self.X1)
            e_grad = sum(self.X2 - minimum_fuel_usage) / len(self.X2)

            a = a - self.lr * a_grad
            b = b - self.lr * b_grad
            c = c - self.lr * c_grad
            d = d - self.lr * d_grad
            e = e - self.lr * e_grad

            time.sleep(0.0001)

        return a, b, c, d, e

    def getCoefficient(self):
        self.getdata()
        return self.regression()

    def get_ideal(self):
        return self.ideal_laptime

    def get_mean_fuel_usage(self):
        return self.mean_fuel_usage