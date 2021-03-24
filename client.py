import socket, re
from os import system
from Bot0 import callBot

#HOST, PORT = socket.gethostname(), 14003
PORT = 14003
HOST = input("enter host: ")
match = int(input("enter match count: "))

white_win = 0
white_lose = 0
black_win = 0
black_lose = 0
for i in range(match):
    color = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        while True:
            ret = str(sock.recv(1024), "ASCII")
            if re.match("^victory_cell", ret) is None:
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
                system("cls")
                print("Match Number: " + str(i))
                print(ret)
                sock.sendall(bytes(callBot(ret), "ASCII"))

total = white_win+white_lose+black_lose+black_win
print("Total matches: " + str(total))        
print("White wins: " + str(white_win))        
print("White Loses: " + str(white_lose)) 
print('')
print("Black wins: " + str(black_win))        
print("Black loses: " + str(black_lose)) 
print("\nWinrate: " + str((black_win+white_win)*100/total)+"%")