from tkinter import *
import tkinter.messagebox
import RPi.GPIO as GPIO
import time
import pygame
import pygame.mixer
from pygame.mixer import Sound
#Camera
import sys
import pygame.camera
pygame.init()
pygame.camera.init()

#create fullscreen display 640x480
screen = pygame.display.set_mode((640,480),0)
#find, open and start low-res camera
cam_list = pygame.camera.list_cameras()
webcam = pygame.camera.Camera(cam_list[0])
webcam.start()

root = Tk()
root.title("Inteligent calling Bell")
pygame.init()
pygame.mixer.init()

opendoor=Sound("audio/open-the-door.wav")
house_empty=Sound("audio/house_empty.wav")
siren=Sound("audio/old-phone-ringing.wav")

GPIO.setmode(GPIO.BOARD)

IR_PIN=7
LIGHT_PIN=11
flag=1
IR_PIN2=13
LIGHT_PIN2=22

GPIO.setup (LIGHT_PIN,GPIO.OUT)
GPIO.setup (LIGHT_PIN2,GPIO.OUT)
GPIO.output(LIGHT_PIN,False)
GPIO.output(LIGHT_PIN2,False)
    
running = True
cameraflag = True
count=0
statusmsg="Turn On the device to view the status "
     
def readIR():
    GPIO.setup (IR_PIN,GPIO.OUT)
    GPIO.output(IR_PIN,False)
    GPIO.setup (IR_PIN2,GPIO.OUT)
    GPIO.output(IR_PIN2,False)
    if flag:
        #Outside Sensor
        GPIO.setup(IR_PIN,GPIO.IN)
        i=GPIO.input(IR_PIN)
        if(i==False):
            global statusmsg
            #statusmsg="STATUS : "+str (i)
            print("Outside Sensor :status :",i)
            GPIO.output(LIGHT_PIN,False)
            opendoor.stop()
        elif(i==True):
            global statusmsg
            #statusmsg="STATUS : "+str (i)
            print("Outside Sensor :status :",i)
            GPIO.output(LIGHT_PIN,True)
            opendoor.play()
        
    else:
        #Outside Sensor 
        GPIO.setup(IR_PIN,GPIO.IN)
        i=GPIO.input(IR_PIN)
        if(i==False):
            print("Outside Sensor :status :",i)
            GPIO.output(LIGHT_PIN,False)
            house_empty.stop()
        elif(i==True):
            print("Outside Sensor :status :",i)
            GPIO.output(LIGHT_PIN,True)
            house_empty.play()
        #Inside Sensor
        GPIO.setup(IR_PIN2,GPIO.IN)
        i=GPIO.input(IR_PIN2)
        if(i==False):
            print("Inside Sensor :status :",i)
            GPIO.output(LIGHT_PIN2,False)
            siren.stop()
        elif(i==True):
            print("Inside Sensor :status :",i)
            GPIO.output(LIGHT_PIN2,True)
            siren.play()
 
        
def scanning():
    if running:
        try:
            readIR()
           # time.sleep(0.5)
        except KeyboardInterrupt:
            GPIO.Cleanup()
            exit()
    
    root.after(1000, scanning)

def PowerOn():
    global running
    running = True
    global statusmsg
    statusmsg="Device is turned ON"
    scanning()
    
def PowerOff():
    print("Power off Code")
    global statusmsg
    statusmsg="Device is turned OFF"
    global running
    running = False
    turnoffsensor()

def turnoffsensor():
    GPIO.setup (IR_PIN,GPIO.OUT)
    GPIO.output(IR_PIN,False)
    GPIO.setup (LIGHT_PIN,GPIO.OUT)
    GPIO.output(LIGHT_PIN,False)
    opendoor.stop()
    
def quitcall():
  answer = tkinter.messagebox.askquestion('Inteligent Calling Bell','Do you want to exit ?')
  if answer=='yes':
      root.destroy()
      turnoffsensor()
      webcam.stop()
      pygame.quit()
      
def House_Empty():
    print("House_Empty Code")
    global flag
    global statusmsg
    if(flag): 
        flag = 0
        statusmsg ="STATUS : Not At Home"
    else:
        flag = 1
        statusmsg ="STATUS : At Home"
    
def Baby_Inside():
    print("Baby_Inside Code")
    
def Camera_On():
    print("Camera Code")
    global cameraflag
    cameraflag = True
    camerascanning()
    
def Camera_Off():
    print("Camera Code")
    #webcam.stop()
    #pygame.quit()
    global cameraflag
    cameraflag = False
 
def camerascanning():
        if cameraflag:
             procam()
        root.after(100, camerascanning)
def procam():
    #grab image, scale and blit to screen
    imagen = webcam.get_image()
    imagen = pygame.transform.scale(imagen,(640,480))
    screen.blit(imagen,(0,0))

    #draw all updates to display
    pygame.display.update()


    # check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            webcam.stop()
            pygame.quit()
            sys.exit()

toppic = Frame(root)
toppic.pack()
photo = PhotoImage(file="images/h1.gif")

lb = Label(toppic,image=photo)
lb.pack()


middle = Frame(root)
middle.pack()
on = Button(middle,text="ON",command=PowerOn)
io_LEDRedOn=PhotoImage(file="images/power-button-on.gif")
io_LEDRedOn = io_LEDRedOn.zoom(2) 
io_LEDRedOn = io_LEDRedOn.subsample(32)
on.config(image=io_LEDRedOn)
on.pack(side=LEFT,padx=10,pady=10)


quit1 = Button(middle,text="QUIT",command= quitcall)
quitbtn=PhotoImage(file="images/quit.gif")
quitbtn = quitbtn.zoom(2) 
quitbtn = quitbtn.subsample(32)
quit1.config(image=quitbtn)
quit1.pack(side=LEFT,padx=10,pady=10)


off = Button(middle,text="OFF",command=PowerOff)
io_LEDRedOff=PhotoImage(file="images/power-button-off.gif")
io_LEDRedOff = io_LEDRedOff.zoom(2) 
io_LEDRedOff = io_LEDRedOff.subsample(32)
off.config(image=io_LEDRedOff)
off.pack(side=LEFT,padx=10,pady=10)


status = Label(root, bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM,fill=X)

bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)

cameraon = Button(bottomframe,text="Camera On",command=Camera_On)
cimg =PhotoImage(file="images/on.gif")
cimg = cimg.zoom(2) 
cimg = cimg.subsample(32)
cameraon.config(image=cimg)
cameraon.pack(side=LEFT,padx=10,pady=10)

house = Button(bottomframe,text="HOUSE_EMPTY",command=House_Empty)
houseimg =PhotoImage(file="images/home.gif")
houseimg = houseimg.zoom(2) 
houseimg = houseimg.subsample(32)
house.config(image=houseimg)
house.pack(side=LEFT,padx=10,pady=10)

cameraoff = Button(bottomframe,text="Camera Off",command=Camera_Off)
cimg2 =PhotoImage(file="images/off.gif")
cimg2 = cimg2.zoom(2) 
cimg2 = cimg2.subsample(32)
cameraoff.config(image=cimg2)
cameraoff.pack(side=LEFT,padx=10,pady=10)

def update_label():
    status.config(text=statusmsg)
    status.after(100, update_label)

status.after(100, update_label)

root.mainloop()
