import random
class Strategy:
    def __init__(self, encoded_strategy:str, lap:int):
        self.encoded_strategy = encoded_strategy
        self.fuel = 0
        self.pitstop = 0
        self.lap = lap
        self.tire = []

        self.decoded_strategy = []
        self.laptime = -1


        self.decoding()

    def decoding(self):
        '''
        stop tire lap tire lap tire lap ... fuel
        soft : 0
        medium : 1
        hard : 2
        '''

        strategy = list(map(int,self.encoded_strategy.split()))

        self.pitstop = strategy[0]
        self.fuel = strategy[-1]
        self.fuel_per_lap = (self.fuel-1) / self.lap

        for i in range(1,3+self.pitstop * 2, 2):
            self.tire.append([strategy[i],strategy[i+1]])

        if self.lap != sum([i[1] for i in self.tire]):
            raise Exception('Strategy and Laps are different')

        remain_fuel = self.fuel
        for tire in self.tire:
            for age in range(1,tire[1]+1):
                self.decoded_strategy.append([tire[0], age, round(remain_fuel,5), round(self.fuel_per_lap,5)])
                remain_fuel -= self.fuel_per_lap

    def update_encoded_strategy(self):
        res = str(self.pitstop) + ' '
        for tire in self.tire:
            res += str(tire[0]) + ' ' + str(tire[1]) + ' '

        self.encoded_strategy = res + str(self.fuel)

    def __repr__(self):
        res = ''
        compound = ['Soft','Medium','Hard']
        for t in self.tire:
            res += compound[t[0]] + ' ' + str(t[1]) + ' lap / '

        return '{' + res + 'with ' + str(self.fuel) + 'kg fuel' + '}'

    def __add__(self, other):
        res = Strategy(self.encoded_strategy,self.lap)
        res.tire[random.randint(0,res.pitstop)][0] = other.tire[random.randint(0,other.pitstop)][0]
        res.fuel = other.fuel
        res.checking_overlapped()

        corr = random.randint(0,5)
        min_laps = 10**3
        max_laps = 0
        min_index = -1
        max_index = -1
        for i in range(len(res.tire)):
            if res.tire[i][1] < min_laps:
                min_laps = res.tire[i][1]
                min_index = i
            if res.tire[i][1] > max_laps:
                max_laps = res.tire[i][1]
                max_index = i
        res.tire[max_index][1]-= corr
        res.tire[min_index][1]+= corr


        res.update_encoded_strategy()

        return res

    def checking_overlapped(self):
        is_diff = 0
        compound = self.tire[0][0]
        for i in range(len(self.tire)):
            is_diff += abs(compound - self.tire[i][0])

        if is_diff == 0:
            temp = [0, 1, 2]
            temp.pop(compound)
            self.tire[random.randint(0, self.pitstop)][0] = temp[random.randint(0, 1)]

    def delete_pitstop(self):
        tire, age = self.tire.pop(random.randint(0, self.pitstop))
        self.pitstop -= 1

        replace = random.randint(0, self.pitstop)
        self.tire[replace][1] += age
        self.checking_overlapped()


        self.update_encoded_strategy()

    def add_pitstop(self):
        max_laps, max_index = 0, -1
        for i in range(len(self.tire)):
            if self.tire[i][1] > max_laps:
                max_laps = self.tire[i][1]
                max_index = i

        laps = random.randint(1,max_laps - 1)
        self.tire[max_index][1] -= laps
        self.pitstop += 1

        self.tire.append([random.randint(0,2),laps])


    def mutate(self, max_pitstop, fuel_range):
        if self.pitstop==max_pitstop:
            self.delete_pitstop()
        elif self.pitstop==1:
            self.add_pitstop()
        else:
            if random.randint(0,1):
                self.delete_pitstop()
            else:
                self.add_pitstop()

        self.fuel = random.randint(fuel_range[0],fuel_range[1])

        random.shuffle(self.tire)
        self.update_encoded_strategy()
        return Strategy(self.encoded_strategy,self.lap)

    def tire_encoding(self):
        encoded_tire = 0
        dec = 1
        for tire in self.tire:
            encoded_tire += dec*(tire[0]+1)
            dec = dec * 10

        return encoded_tire

def strategyGenerator(size:int, lap:int, max_pitstop:int, fuel_range:tuple):
    strategies = []
    laps = [i+1 for i in range(lap-1)]

    for i in range(size):
        pitstop = random.randint(1, max_pitstop)
        fuel = random.randint(fuel_range[0], fuel_range[1])
        time = [0] + sorted(random.sample(laps,pitstop) + [lap])

        compound = random.sample([0,1,2],2) + [random.randint(0,2) for _ in range(pitstop-1)]
        random.shuffle(compound)

        res = str(pitstop) + ' '
        for i in range(pitstop+1):
            res += str(compound[i]) + ' '
            res += str(time[i+1]-time[i]) + ' '

        res += str(fuel)

        strategies.append(Strategy(res,lap))

    return strategies

def find_possible_strategy(pitstop):
    stack = [1,2,3]
    strategies = set()
    while stack:
        el = stack.pop()
        if el not in strategies and el < 10**(pitstop+1):
            strategies.add(el)
            for i in range(1,4):
                if el*10 + i not in stack:
                    stack.append(el*10 + i)

    for i in range(1,4):
        el = i
        for _ in range(pitstop):
            strategies.discard(el)
            el = el * 10 + i
        strategies.discard(el)

    return strategies
