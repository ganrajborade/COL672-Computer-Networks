from socket import *
import time
serverName = 'vayu.iitd.ac.in'
serverPort = 9801
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
masterSocket = socket(AF_INET, SOCK_STREAM)
masterSocket.connect(('localhost',12001))

lst = [False]*1000
sendLine = "SENDLINE\n"
i=1
try:
  while (True):
    #print(i)
    response1 = ""
    clientSocket.send(sendLine.encode())
    message = clientSocket.recv(2048)
    sentence = message.decode()
    if (sentence[0]=='-'):
      continue
    temp = sentence.split(maxsplit=1)
    #print("before")
    #print(sentence)
    index = int(temp[0])
    
    response1+=temp[1]
    #print(response1)
    # if(lst[index]== True):
    #   while(True) :
    #     #print("received")
    #     if(sentence[len(sentence)-1]=='\n'):
    #       break
    #     message = clientSocket.recv(1024)
    #     sentence = message.decode()
    if(lst[index]== False):
      lst[index] = True
      if(response1.find('\n')!=-1) :
        print(response1)
      else :
        while(True) :
          message = clientSocket.recv(2048)
          sentence = message.decode()
          response1+=sentence
          if(response1.find('\n')!=-1) : 
              break 
          print(response1)
        #masterSocket.send(response1.encode())
      
except Exception as e:
  print(e)
  masterSocket.close()
  clientSocket.close()

