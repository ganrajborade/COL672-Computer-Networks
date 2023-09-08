from socket import *
import threading
import time
lock = threading.Lock()
count = [0]
lst = ['']*1000
sock1addr = '10.184.42.213'
sock1port = 12001

def client_process(connectionSocket, addr):
  print("hello")
  while True:
    if(count[0]==1000):
      break
    message = connectionSocket.recv(2048)
    if(not message):
      break
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
        message = connectionSocket.recv(2048)
        sentence = message.decode()
    else:
      lock.acquire()        
      count[0]+=1
      # print(count[0])
      #print(sentence,end='')
      while(True) :
        lst[index]+=sentence
        if(sentence[len(sentence)-1]=='\n'):
          break
        message = connectionSocket.recv(2048)
        sentence = message.decode()
      lock.release()
  connectionSocket.close()


def my_client():
  start = time.time() 
  serverName = 'vayu.iitd.ac.in'
  serverPort = 9801
  sock1 = socket(AF_INET,SOCK_STREAM)
  while True:
    try:
      sock1.connect((sock1addr,sock1port))
      break
    except:
      {}

  clientSocket = socket(AF_INET, SOCK_STREAM)
  clientSocket.connect((serverName, serverPort))
  sendLine = "SENDLINE\n"
  while True:
    if(count[0]==1000):
      break
    clientSocket.send(sendLine.encode())
    message = clientSocket.recv(2048)
    sentence = message.decode()
    if (sentence[0]=='-'):
      continue
    temp = sentence.split('\n',maxsplit = 1)
    index = int(temp[0])
    senstr = sentence
    sentence = temp[1]
    if(lst[index] != ''):
      while(True):
        if(sentence[len(sentence)-1]=='\n'):
          break
        message = clientSocket.recv(2048)
        sentence = message.decode()
    else:
      lock.acquire()        
      count[0]+=1
      print(count[0])
      while True :
        lst[index]+=sentence
        try:
          sock1.send(senstr.encode())
        except:
          print(end='')
        if(sentence[len(sentence)-1]=='\n'):
          break
        message = clientSocket.recv(2048)
        sentence = message.decode()
        senstr = sentence
      lock.release()
  
  end = time.time() 
  print(end - start)

  submit = "SUBMIT\n"
  team = "2023MCS2488@dags\n"
  clientSocket.send(submit.encode())
  clientSocket.send(team.encode())
  clientSocket.send('1000\n'.encode())

  for i in range(1000):
    if(lst[i]==''):
      continue
    s = str(i)
    s +='\n'
    s+=lst[i]
    clientSocket.send(s.encode())
    try:
      sock1.send(s.encode())
    except:
      print(end='')
  message = clientSocket.recv(2048)
  sentence = message.decode()
  print(sentence)
  clientSocket.close()
  sock1.close()



def main():
  threading.Thread(target=my_client).start()
  serverPort = 12003
  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.bind(('10.184.50.108', serverPort))
  serverSocket.listen(15)
  while True:
    connectionSocket, addr = serverSocket.accept()
    client = threading.Thread(target=client_process, args=(connectionSocket,addr))
    client.start()
  
if __name__== "__main__":
  main()