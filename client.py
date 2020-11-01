import socket
import multiprocessing
import hashlib
import threading
import time

IP = '127.0.0.1'
Port = 5000

stop_event = threading.Event()

class listening(threading.Thread):

    def __init__(self, client_socket):
       threading.Thread.__init__(self)
       self.client = client_socket

    def run(self):
        data = self.client.recv(1024).decode()
        if(data == 'close the client'):
            self.client.send("not found".encode())
            print("work has stopped, another client found the password")
            stop_event.set()
        else:
            stop_event.set()


class Client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((IP, Port))
        self.client.send((str(multiprocessing.cpu_count())).encode())
        self.lst_of_params = []

    def Recieve_ranges(self):
        data = self.client.recv(1024).decode()
        self.lst_of_params = data.split(" ")
        return


    def run(self):
        start = int(self.lst_of_params[0])
        end = int(self.lst_of_params[1])
        hash = self.lst_of_params[2]
        m = hashlib.md5()
        while(not stop_event.isSet() and start<end):
            string = str(start)
            print(string)
            m.update(string.encode())
            if (hash == m.hexdigest()):
                print("this is the right number: " + string)
                print("sending the Aanswer to server")
                self.client.send(string.encode())
                return
            m = hashlib.md5()
            start+=1
            time.sleep(0.000001)





c = Client()
c.Recieve_ranges()
t = listening(c.client)
t.start()
c.start()


input()