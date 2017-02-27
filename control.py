import curses
import wiringpi2
import time
import serial
#importing necessary libraries

wiringpi2.wiringPiSetupSys() # For /sys/class/gpio with GPIO pin numbering - THE USED ONE
# OR
#wiringpi2.wiringPiSetup() # For sequential pin numbering, one of these MUST be called before using IO functions
# OR
#wiringpi2.wiringPiSetupGpio() # For GPIO pin numbering


# important MX-28 constants
AX_WRITE_DATA = 3
AX_READ_DATA = 4

s = serial.Serial()               # create a serial port object
s.baudrate = 1000000              # baud rate, in bits/second
s.port = "/dev/ttySAC0"           # this is whatever port your are using
s.open()

#function which takes input from keyboard without the need to press ENTER
def input_char(message):
    try:
        win = curses.initscr()
        win.addstr(0, 0, message)
        while (True): 
            ch = win.getch()
            if ch in range(32, 127): break
            time.sleep(10)
    except: raise
    finally:
        curses.endwin()
    ch=chr(ch)
    if(ch=='+'):
        ch=3
    elif(ch=='-'):
        ch=-3
    else:
        ch=int(ch)
    return ch


#defining all pins as outputs
wiringpi2.pinMode(21,1)
wiringpi2.pinMode(18,1)
wiringpi2.pinMode(22,1)
wiringpi2.pinMode(19,1)
wiringpi2.pinMode(30,1)
wiringpi2.pinMode(28,1)

# set register values for MX-28
def setReg(ID,reg,values):
    length = 3 + len(values)
    checksum = 255-((ID+length+AX_WRITE_DATA+reg+sum(values))%256)          
    s.write(chr(0xFF)+chr(0xFF)+chr(ID)+chr(length)+chr(AX_WRITE_DATA)+chr(reg))
    for val in values:
        s.write(chr(val))
    s.write(chr(checksum))

#defining MX-28 positions
a=b=c=d=e=f=0
direction=0
x=250
position=2000
setReg(19,30,((position%256),(position>>8)))
#last line sets wrist in middle position

while True:
    #control wrist
    direction=input_char('UPRAVLJANJE: \n+ i - za zglob\n1 i 2 za sve prste\n4 i 7, 5 i 8, 6 i 9  za zasebno upravljanje prstima\n')
    if(direction==3 and position<3095-x):
        position=position+x
    elif(direction==-3 and position>=x+1000):
        position=position-x
    setReg(19,30,((position%256),(position>>8)))


    #control fingers:
    if(direction==1):
        b=d=f=0
        a=c=e=1
    elif(direction==2):
        b=d=f=1
        a=c=e=0
    elif(direction==0):
        a=b=c=d=e=f=0
    elif(direction==4):
        b=1
        a=c=d=e=f=0
    elif(direction==7):
        a=1
        b=c=d=e=f=0
    elif(direction==5):
        d=1
        a=b=c=e=f=0
    elif(direction==8):
        c=1
        a=b=d=e=f=0
    elif(direction==6):
        f=1
        a=b=c=d=e=0
    elif(direction==9):
        e=1
        a=b=c=d=f=0

    wiringpi2.digitalWrite(21,a)
    wiringpi2.digitalWrite(18,b)
    wiringpi2.digitalWrite(22,c)
    wiringpi2.digitalWrite(19,d)
    wiringpi2.digitalWrite(30,e)
    wiringpi2.digitalWrite(28,f)

    time.sleep(0.0075)