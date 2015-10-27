from pyfirmata import Arduino, util
from time import sleep
board=Arduino('/dev/ttyS0')

from socket import *      #import the socket library


##let's set up some constants
HOST = ''    #we are the host
PORT = 29876    #arbitrary port not currently in use
ADDR = (HOST,PORT)    #we need a tuple for the address
BUFSIZE = 256    #reasonably sized buffer for data


response = "HTTP/1.1 200 OK\n\rConnection: close\n\r\n\r"

led=board.digital[13];

EN1=board.get_pin('d:9:p');
IN1=board.digital[2];
IN2=board.digital[3];

EN2=board.get_pin('d:10:p');
IN3=board.digital[5];
IN4=board.digital[7];

GAIN=25.0;

def catch(recievedata):
  button=0;
  angle=0;
  num=0;
  num = recievedata.find(',');
  button=int(recievedata[0:num]);
  angle=int(recievedata[num+1:len(recievedata)]);
  #print 'button'
  #print button
  #print ' angle'
  #print angle

  #print "get:",
  #print receivedata
  L_control=0;
  R_control=0;
  if angle>=0:
    L_control=(100-angle*GAIN)/100.0;
    R_control=1;
  elif angle<0:
    L_control=1;
    R_control=(100+angle*GAIN)/100.0;


  if L_control<0:
    L_control=0;
  elif L_control>1:
    L_control=1;
  if R_control<0:
    R_control=0;
  elif R_control>1:
    R_control=1;

  print 'L'
  print L_control
  print 'R'
  print R_control

  if button==0:
    led.write(0);

    EN1.write(0);
    IN1.write(0);
    IN2.write(0);

    EN2.write(0);
    IN3.write(0);
    IN4.write(0);
    #pass
  if button==1:
    led.write(1);
    EN1.write(L_control);
    IN1.write(0);
    IN2.write(1);

    EN2.write(R_control);
    IN3.write(0);
    IN4.write(1);
    #pass
  if button==2:
    EN1.write(L_control);
    IN1.write(1);
    IN2.write(0);

    EN2.write(R_control);
    IN3.write(1);
    IN4.write(0);
    #pass
  pass

# print response
serv = socket( AF_INET,SOCK_STREAM)
serv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

receivedata = ""

dataget=0
counter=0
##bind our socket to the address
serv.bind(ADDR)    #the double parens are to create a tuple with one element
serv.listen(1)    #5 is the maximum number of queued connections we'll allow
print 'listening...'
while 1:
  conn,addr = serv.accept() #accept the connection
  #print '...connected!'
  connected = 1

  while connected:
    data = conn.recv(BUFSIZE)

    for char in data:
     #print char
     if(dataget):
        receivedata += char

        if(char=="\n"):
          print receivedata
          catch(receivedata)
          connected = 0
          flag = 0
          dataget=0
          receivedata = ""
          conn.sendall(response)
          conn.close()

     if(char=="\n"):
       counter=counter+1;
       if(counter==3):
         #print "entering dataget"
         dataget=1;
     elif(char=="\r" and counter==1):
       counter=2
       #print "get space"
     else:
       counter=0;
serv.close()
