# -*- coding: utf-8 -*-
IP = '127.0.0.1'
PORT = 5000
import socket
import threading
import math
clients = []
cores_and_clients = []
threadss = []
total_cores = 0
low = 0
st = "3d2172418ce305c7d16d4b05597c6a59"
class listening(threading.Thread):

    def __init__(self, client_socket):
       threading.Thread.__init__(self)
       self.client = client_socket


    def run(self):
        global clients
        data = self.client.recv(1024).decode()
        if(data == 'not found'):
            pass
        else:
            print("the password is: " + data)
            for c in clients:
                if (c != self.client):
                    c.send("close the client".encode())
                else:
                    c.send("ack".encode())


class getCores(threading.Thread):

    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client = client_socket

    def run(self):
        global cores_and_clients
        num = int(self.client.recv(1024).decode())
        cores_and_clients.append((self.client, num))

class Server(object):
    def __init__(self):
        self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mysocket.bind((IP, PORT))
        self.mysocket.listen(5)
        self.mysocket.settimeout(10)

    def get_clients(self):
        global clients
        while True:
            try:
                client_socket, client_adress = self.mysocket.accept()
                print(client_adress)
                clients.append(client_socket)
            except:
                print("client accepting process is done")
                break
        
    def send_ranges(self, start, end, client):
        start_and_end = str(start) + " " + str(end)+ " " + st
        client.send(start_and_end.encode())







       

def main():
    """
    Add Documentation here
    """
    global clients
    global threadss
    global total_cores
    global cores_and_clients
    s = Server()

    s.get_clients()
    for c in clients:
        t = getCores(c)
        threadss.append((t, c))
        t.start()
        t.join()

    for i in cores_and_clients:
        total_cores += i[1]

    num_to_core = math.ceil(89999.0 / total_cores)

    starting_num = 10000
    for i in cores_and_clients:
        s.send_ranges(starting_num, starting_num+num_to_core*i[1], i[0])
        starting_num += num_to_core*i[1]

    for t in threadss:
        t1 = listening(t[1])
        t1.start()




if __name__ == '__main__':
    main()
