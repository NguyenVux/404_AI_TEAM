import socket, re
from bot import callBot, validSteps
HOST, PORT = socket.gethostname(), 14003


# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    while True:
        ret = str(sock.recv(1024), "ASCII")
        print(ret)
        if re.match("^victory_cell", ret) is None:
            break
        else:
            print('Valid steps:')
            print(validSteps(ret))
            yourStep = input("Your Step: ")
            sock.sendall(bytes(yourStep, "ASCII"))