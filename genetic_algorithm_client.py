import socket, re
from os import system
import bot_scan
import numpy as np
from random import choice
import json


population_count = 20
max_point = 50
min_point = -50
mutation_rate = 0.01
crossover_rate = 0.3
population = []
for i in range(population_count):
    population.append((max_point-min_point) * np.random.random_sample((8, 8)) + min_point)



match_count = 1






def crossover(chronoA,chronoB,crossover_rate):
    chronoC = np.copy(chronoA)
    chronoD = np.copy(chronoB)
    for i,k in enumerate(chronoA):
        if np.random.random_sample() < crossover_rate:
            chronoC[i] = chronoB[i]
            chronoD[i] = chronoA[i]
    return chronoC,chronoD

def mutate(chronoA,mutation_rate):
    chronoB = np.copy(chronoA)
    for i,k in enumerate(chronoB):
        if np.random.random_sample() < mutation_rate:
            chronoB[i] = (max_point-min_point) * np.random.random_sample() + min_point
    return chronoB





def main():
    global population
    HOST, PORT = socket.gethostname(), 14003
    PORT =  14003
    HOST = input("enter host: ")
    winrate = list()
    gen = 0
    while True:
        for i in population:
            rate = start_match(HOST, PORT, i)
            winrate.append(rate)
            print(rate)

        if  gen == 200:
            break
        
        _,population = (list(t) for t in zip(*sorted(zip(winrate,population),key=lambda e: e[0])))
        
        best_5 = population[:10]
        new_gen = []
        for i in best_5:
            chronoA,chronoB = crossover(i,choice(population), crossover_rate)
            chronoA = mutate(chronoA, mutation_rate)
            chronoB = mutate(chronoB, mutation_rate)
            new_gen.append(chronoA)
            new_gen.append(chronoB)
        population = new_gen
        print(population)
        gen+=1
        
        with open('data.json', 'w') as outfile:
            data = [x.tolist() for x in population]
            json.dump(data, outfile)
    

def start_match(HOST,PORT,chromosome):
    white_win = 0
    white_lose = 0
    black_win = 0
    black_lose = 0
    for i in range(match_count):
        color = None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            while True:
                ret = str(sock.recv(1024), "ASCII")
                if re.match("^victory_cell", ret) is None:
                    print(ret)
                    if ret.split("\n")[-2] == color:
                        if color == "BLACK":
                            black_win += 1
                        else:
                            white_win +=1
                    else:
                        if color == "BLACK":
                            black_lose += 1
                        else:
                            white_lose +=1
                    sock.close()
                    break
                else:
                    if color is None:
                        color = ret.split('\n')[-2]
                    #system("cls")
                    print("Match Number: "+ str(i))
                    print(ret)
                    sock.sendall(bytes(bot_scan.callBot(ret,chromosome), "ASCII"))
    total = white_win+white_lose+black_lose+black_win
    return (white_win+black_win)/total




    # print("Total matches: " + str(total))        
    # print("White wins: " + str(white_win))        
    # print("White Loses: " + str(white_lose)) 
    # print('')
    # print("Black wins: " + str(black_win))        
    # print("Black loses: " + str(black_lose)) 
    # print("\nWinrate: " + str((black_win+white_win)*100/total)+"%")

main()