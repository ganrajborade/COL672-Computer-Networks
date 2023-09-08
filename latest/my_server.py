from socket import *
import threading
import time
lock = threading.Lock()
count = [0]
lst = ['']*1000
my_peeraddr = '10.194.55.66'
my_peerport = 12001


def other_client_process(client_connection_socket, addr):
  print("hello")
  while True:
    if(count[0]==1000):
      break
    message = client_connection_socket.recv(2048)
    
    if(not message) : 
      continue
    sentence = message.decode()
    if (sentence[0]=='-'):
      continue
    temp = sentence.split('\n',maxsplit = 1)
    index = int(temp[0])
    sentence = temp[1]
    if(lst[index] != ''):
      while(True):
        if(sentence[len(sentence)-1]=='\n'):
          break
        message = client_connection_socket.recv(2048)
        sentence = message.decode()
    else:
      lock.acquire()        
      count[0]+=1
      #print(count[0])
      #print(sentence,end='')
      while(True) :
        lst[index]+=sentence
        if(sentence[len(sentence)-1]=='\n'):
          break
        message = client_connection_socket.recv(2048)
        sentence = message.decode()
      lock.release()
  client_connection_socket.close()


def main():
  serverPort = 12002
  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.bind(('10.194.49.161', serverPort))
  serverSocket.listen(15)
  # test listen function
  while True:
    client_connection_socket, addr = serverSocket.accept()
    client = threading.Thread(target=other_client_process, args=(client_connection_socket,addr))
    client.start()
  
if __name__== "__main__":
  main()