import random
import matplotlib.pyplot as plt

NUM_ROUNDS = int(input("Enter number of rounds: "))
scale = float(input("Enter scale: "))

Game = [[0, 1], [2, 3]]
w = 3
y = 4
x = 1
maximum = 0
topScores = []

Payoffs = [(6,6), (0, 5),
           (5, 0), (1, 1)]


def Play(p1Move, p2Move):
    return Payoffs[Game[p1Move][p2Move]]


class Player:
    def __init__(self, strategy, opponentMove, numoppmoves):
        self.opponentMove = opponentMove
        self.oppmoves = []
        self.numoppmoves = numoppmoves
        self.strategy = strategy
        if self.strategy[0] > 1:
            self.strategy[0] = 1
        if self.strategy[1] > 1:
            self.strategy[1] = 1
        if self.strategy[0] < 0:
            self.strategy[0] = 0
        if self.strategy[1] < 0:
            self.strategy[1] = 0
        self.score = 0
        self.strcalc = [1]

    def setoppmove(self, oppmove):
        self.oppmoves.insert(0, oppmove)
        if self.numoppmoves < len(self.oppmoves):
            while (len(self.oppmoves) > self.numoppmoves):
                self.oppmoves.pop(self.numoppmoves)
        else:
            if self.numoppmoves > len(self.oppmoves):
                for i in range(len(self.oppmoves), self.numoppmoves):
                    self.oppmoves.append(0)

        if len(self.strcalc) < self.numoppmoves:
            for i in range(len(self.strcalc), self.numoppmoves):
                self.strcalc.append(1)
        else:
            while (len(self.strcalc) > self.numoppmoves):
                self.strcalc.pop(self.numoppmoves)

        p = [self.oppmoves[i] * self.strcalc[i] for i in range(0, self.numoppmoves)]
        # print("P = ", p)
        opponentMove = sum(p)
        if random.uniform(0, 1) >= opponentMove:
            self.opponentMove = 0
        else:
            self.opponentMove = 1

    def executestr(self):
        if random.uniform(0, 1) >= self.strategy[self.opponentMove]:
            return 0
        else:
            return 1

    def setStrat(self, str1, str2, err):
        self.strategy[0] += str1
        if self.strategy[0] < 0:
            self.strategy[0] = 0
        else:
            if self.strategy[0] > 1:
                self.strategy[0] = 1
        self.strategy[1] += str2
        if self.strategy[1] < 0:
            self.strategy[1] = 0
        else:
            if self.strategy[1] > 1:
                self.strategy[1] = 1

        for i in range(0, len(self.strcalc)):
            self.strcalc[i] += random.uniform(-err, err)
            if self.strcalc[i] < 0:
                self.strcalc[i] = 0
            if self.strcalc[i] > 1:
                self.strcalc[i] = 1
        if self.numoppmoves < 1:
            self.numoppmoves = 1
        if self.strategy[0] > 1:
            self.strategy[0] = 1
        if self.strategy[1] > 1:
            self.strategy[1] = 1
        if self.strategy[0] < 0:
            self.strategy[0] = 0
        if self.strategy[1] < 0:
            self.strategy[1] = 0

    def setPayoff(self, payoff):
        self.payoff = payoff


Players = []
e1 = 0
e2 = 0
n = 10
numPlayers = int(input("Enter number of players (multiple of 10): "))
for i in range(0, int(numPlayers/5)):
    P = Player([0 + e1, 0 + e2], 0, n)
    Players.append([P, 0, 0, i])

    P2 = Player([0 + e1, 1 + e2], 0, n)
    Players.append([P2, 0, 0, i+100])

    P3 = Player([1 + e1, 0 + e2], 0, n)
    Players.append([P3, 0, 0, i+200])

    P4 = Player([1 + e1, 1 + e2], 0, n)
    Players.append([P4, 0, 0, i+300])

    P5 = Player([.5 + e1, .5 + e2], 0, n)
    Players.append([P5, 0, 0, i+400])


def Sort(pl, num):
    return sorted(pl, key=lambda x: x[num], reverse=True)


zero0 = 0
zero0pl = []
zero1 = 0
zero1pl = []
zerozero1 = 0
one0 = 0
one0pl = []
one1 = 0
one1pl = []
other = 0
otherpl = []

count = 0
rounds = int(input("Enter how many different players per round: "))
matches = int(input("Enter number of matches: "))
topPlayers = 10
stratErr = .12
while count < NUM_ROUNDS:
    count += 1
    used = []
    for i in range(0, numPlayers):
        p1 = i
        pl1 = Players[p1]
        for k in range(0, rounds):
            p2 = random.randrange(0, numPlayers)
            pl2 = Players[p2]
            for j in range(0, matches):
                str1 = pl1[0].executestr()
                str2 = pl2[0].executestr()
                final = Play(str1, str2)
                pl1[1] += final[0]
                pl1[2] += final[0]
                pl1[0].score += final[0]
                pl2[0].score += final[1]
                pl1[0].setoppmove(str2)
                pl2[0].setoppmove(str1)
            Players[p1] = pl1
            Players[p2] = pl2
    Players = Sort(Players, 1)
    errorRange = 0
    print("Round: ", count)
    for i in range(0, topPlayers):
        print("Player: ", Players[i][3], ": Strategy: ", Players[i][0].strategy, "Score: ", Players[i][0].score)
        print("Strcalc: ", Players[i][0].strcalc)
        print(Players[i][1])
    num = 0
    for i in Players:
        strat = i[0].strategy
        if strat[0] <= stratErr:
            strat[0] = 0
        else:
            if strat[0] >= 1-stratErr:
                strat[0] = 1
        if strat[1] <= stratErr:
            strat[1] = 0
        else:
            if strat[1] >= 1-stratErr:
                strat[1] = 1
        if num < numPlayers/2:
            if strat == [0, 0]:
                zero0 += 1
            else:
                if strat == [0, 1]:
                    if i[0].strcalc[0] > stratErr:
                        if i[0].strcalc[1] > stratErr:
                            zero1 += 1
                        else:
                            zero1 += 1
                    else:
                        if i[0].strcalc[1] > stratErr:
                            zero1 += 1
                        else:
                            zero1 += 1
                else:
                    if strat == [1, 0]:
                        if i[0].strcalc[1] > stratErr:
                            one0 += 1
                        else:
                            if i[0].strcalc[1] > stratErr:
                                one0 += 1
                            else:
                                one0 += 1
                    else:
                        if strat == [1, 1]:
                            one1 += 1
                        else:
                            other += 1
        err1 = random.uniform(-errorRange, errorRange)
        err2 = random.uniform(-errorRange, errorRange)
        i[0].setStrat(err1, err2, errorRange)
        num += 1
        errorRange = ((num / numPlayers) ** 4) / 4
        if errorRange < 0:
            errorRange = 0
    Players = Sort(Players, 1)
    print("Best so far:", Players[0][3])
    print("Strategy: ", Players[0][0].strategy, "Score: ", Players[0][0].score)
    print("Round score:", Players[0][1])
    if Players[0][1] > maximum:
        maximum = Players[0][1]
    topScores.append(Players[0][1])
    for i in Players:
        i[1] = i[1]*scale
    print("Total score: ", Players[0][2])
    print("Strcalc: ", Players[0][0].strcalc)
    total = zero0 + zero1 + one0 + one1 + other + zerozero1
    print("[0,0]", zero0, zero0 / total)
    zero0pl.append(zero0 / total)
    print("[0,1]", zero1, zero1 / total)
    zero1pl.append(zero1 / total)
    print("[1,0]", one0, one0 / total)
    one0pl.append(one0 / total)
    print("[1,1]", one1, one1 / total)
    one1pl.append(one1 / total)
    print("Other: ", other, other / total)
    otherpl.append(other / total)

topScores = [i / maximum for i in topScores]
graph = [i / NUM_ROUNDS for i in range(0, NUM_ROUNDS)]

#plt.plot(graph, zero0pl, graph, zero1pl, graph, one1pl, graph, otherpl, graph, one0pl)
plt.plot(graph, zero0pl, label='[0,0]')
plt.plot(graph, zero1pl, label='[0,1]')
plt.plot(graph, one1pl, label='[1,1]')
plt.plot(graph, one0pl, label='[1,0]')

plt.legend()
plt.axis([0, 1, 0, 1])
plt.show()
print(Play(0, 0), Play(0, 1))
print(Play(1, 0), Play(1, 1))
