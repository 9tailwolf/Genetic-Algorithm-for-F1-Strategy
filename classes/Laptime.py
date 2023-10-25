from classes.Regression import Regression

class Laptime:
    def __init__(self,path:str,compound:str):
        self.compound = compound
        self.path = path

        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None

        self.reg = None

        self.ideal = -1
        self.minimum_fuel = -1

    def setCoefficient(self):
        self.reg = Regression(lr = 10**-11, lt = 20000, path = self.path, compound = self.compound)

        self.minimum_fuel = self.reg.get_mean_fuel_usage()

        self.a,self.b,self.c,self.d,self.e = self.reg.getCoefficient()
        self.ideal = self.reg.get_ideal()

    def getlaptime_tire(self,age,fuel_usage):
        return self.a * age**3 + self.b * age**2 + self.c * age + self.d + self.e * (fuel_usage-self.minimum_fuel)

    def getlaptime_fuel(self,fuel,time_per_fuel = 30):
        return fuel * time_per_fuel

    def getlaptime(self,age,fuel,fuel_usage):
        if self.a:
            time = round(int(self.ideal * 100 / self.getlaptime_tire(age,fuel_usage) + self.getlaptime_fuel(fuel))/1000,3)
            if time>1000 or time<0:
                return 1000000
            return time
        return None

class LaptimeCalculator:
    def __init__(self, path:str):
        self.calculator = [Laptime(path,i) for i in ['Soft','Medium','Hard']]
        for i in self.calculator:
            i.setCoefficient()

    def calculation(self,strategy,pitstop,pit_time):
        laptimes = 0
        for s in strategy:
            tire,age,fuel,fuel_usage = s
            t = self.calculator[tire].getlaptime(age,fuel,fuel_usage)
            #print(s,t)
            laptimes += t
        #print(laptimes + pit_time * pitstop,end='\n')
        return laptimes + pit_time * pitstop