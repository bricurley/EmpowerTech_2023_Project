# Manages sleep functions for switching between threads
import time

# Allows for scanning nearby sphero robots for use in the script
from spherov2 import scanner

# Allows for commands to be sent to the Robot
from spherov2.sphero_edu import SpheroEduAPI

# Allows for changing colors to manage and perceive robot interaction TO BE IMPLEMENTED 
from spherov2.types import Color

# Allows for listening to commands and drawing to the screen to happen simultaneously
import threading

# Used for further control of the console
import sys

# Important for drawing circles
import math

# Used to prevent spam to the console
import os

# Used for click interactions with the user and for the main interface
import pygame

# Used for various pygame screen and side elements
from pygame.locals import *

# Used as a separate input to get text input from the user
import tkinter as tk

# Used to manage and send commands to mosquitto
import paho.mqtt.client as paho

# Creates a global variable that continually tries to connnect to the robot and prints the status should it fail
toy = None
while(toy == None):
    try:
        toy = scanner.find_RVR()
        time.sleep(1)
        
    except:
        print("connect failed")


# Manages messages sent from the phone server
def onMessage(client, userdata, msg):
    # Grabs access to a global various connected to the robot
    global gdroid
    message = (msg.payload.decode())
    print(message)

    # Splits rotation commands based on axis (x, y, and z)
    tokens = message.split(',\"')
    print(f'{tokens[2]} to {tokens[2][0:1]} {float(tokens[2][4:9])}')
    for i in range(2,5):
        currToken = tokens[i][0:1] 
        currVal = (float(tokens[i][4:9]))
        print(tokens[i])

        # Changes robot movement based on x and y rotation (buggy, TO BE FIXED)
        print(f'CurrToken is {currToken} and currVal is {currVal}')
        if(currToken == 'x'):
            print(f"setting Speed to {gdroid.get_speed() + 10*currVal}" )
            gdroid.set_speed(gdroid.get_speed() + int(10*currVal))
        elif(currToken == 'y'):
            print(f'Setting heading to {gdroid.get_heading() + int(10*currVal)}')
            gdroid.set_heading(gdroid.get_heading() + int(10*currVal))

# Manages messages from the speech client and translates to commands for the robot
def onSpeechMessage(client, userdata, msg):
    global gdroid
    message = (msg.payload.decode())
    print(f"Executing function {message}")
    if "turning" in message:
        if "North" in message:
            gdroid.set_heading(0)
        if "East" in message:
            gdroid.set_heading(90)
        if "South" in message:
            gdroid.set_heading(180)
        if "West" in message:
            gdroid.set_heading(270)
    elif "setting speed to a higher value" in message:
        gdroid.set_speed(gdroid.get_speed() + 20)
    elif "setting speed to a lower value" in message:
        gdroid.set_speed(math.floor(0, gdroid.get_speed() - 20))
    elif "stopping!" in message:
        gdroid.set_speed(0)


# Runs on pressing the circle button and has the robot draw a circle
def spinCircle(droid, speed, radius):
    radius *= 1.5
    tempHeading = droid.get_heading()
    circumference = 2 * math.pi * radius
    time = circumference / float(speed)
    speed = circumference / float(time)
    droid.set_speed(int(speed))
    droid.spin(360, int(time))
    droid.set_speed(0)
    droid.set_heading(tempHeading)

# Runs on pressing the square button and draws a square by rotating 90 degrees and going a fixed distance repeatedly
def square(droid, dimesion, speed, screen, background):
    tempHeading = droid.get_heading()
    droid.set_heading(droid.get_heading())
    go_dist_in_centimeters(droid, dimesion, speed, screen, background)
    time.sleep(0.5)
    droid.set_heading(droid.get_heading() + 90)
    go_dist_in_centimeters(droid, dimesion, speed, screen, background)
    time.sleep(0.5)
    droid.set_heading(droid.get_heading() + 90)
    go_dist_in_centimeters(droid, dimesion, speed, screen, background)
    time.sleep(0.5)
    droid.set_heading(droid.get_heading() + 90)
    go_dist_in_centimeters(droid, dimesion, speed, screen, background)
    droid.set_speed(0)
    droid.set_heading(tempHeading)

# Runs on pressing the triangle button and draws a right triangle
def triangle(droid, dimesion, speed, screen, background):
    tempHeading = droid.get_heading()
    droid.set_heading(droid.get_heading())
    go_dist_in_centimeters(droid, dimesion, speed, screen, background)
    droid.set_heading(droid.get_heading() + 90)
    go_dist_in_centimeters(droid, dimesion, speed, screen, background)
    droid.set_heading(droid.get_heading() + 135)
    go_dist_in_centimeters(droid, math.sqrt(dimesion**2+dimesion**2), speed, screen, background)
    droid.set_speed(0)
    droid.set_heading(tempHeading)

# Function used by the triangle and square function, makes the robot go a specified distance
def go_dist_in_centimeters(droid, dist, speed, screen, background):
    startDist = droid.get_distance()
    while(((droid.get_distance() - startDist < dist) and not traveled)):
        droid.set_speed(speed)
        updateFrame(screen, droid, background)
        #print(droid.get_distance() - startDist)
    droid.set_speed(0)
    print("successfully went " + (str)(dist) + " centimeters")

# Draws the dot for the robot as it travels on the screen
def updateFrame(screen, droid, background):
    # Makes a 4x4 square
    droid_pos = Rect(screen.get_size()[0]/2 -2 + droid.get_location()['x'], screen.get_size()[1]/2 - 2 - droid.get_location()['y'], 4, 4)

    # Puts the square on the screen
    pygame.draw.rect(background, (255, 0, 0), droid_pos)

    # Updates the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

# Updates the speed value on both TKinter text input and Pygame sliders
def update_speed(screen, background, speed_slider, speed_slider_bar, speedInput, speedVal):
    temp_speed = speedVal
    # Manages updates from the button (Come as a string from the box)
    if(speedVal == -1):
        print('from button')
        try:
            temp_speed = (int(speedInput.get().strip()))
        except:
            return 0
    
    # Updates tkinter by deleting what's there and putting the speed
    speedInput.delete(0,tk.END)
    speedInput.insert(0, (str)(temp_speed))

    # Redraws entire slider to cover slider bar
    pygame.draw.rect(background, (0, 211, 211), speed_slider)

    # Draws slider bar on the screen on top of the slider
    speed_slider_bar = Rect(screen.get_size()[0]/2-800/2-50,(-1)*temp_speed*800/255 +screen.get_size()[1]/2 + 800/2 ,30, 14)
    global speed
    speed = temp_speed
    pygame.draw.rect(background, (0, 100, 100), speed_slider_bar)

    # Does not update screen as postion updating thread will
    return temp_speed

# Updates the shape size value on both Tkinter Text input and Pygame Sliders
def update_size(screen, background, shape_slider, shape_slider_bar, sizeInput, sizeVal):
    temp_size = sizeVal

    # Manages updates from the button which come in as a string
    if(sizeVal == -1):
        try:
            print('from button')
            temp_size = (int(sizeInput.get().strip()))
        except:
            return 0
        
    # Deletes what is in tkinter and replaces with the most current values
    sizeInput.delete(0,tk.END)
    sizeInput.insert(0, (str)(temp_size))

    # Redraws entire slider to cover slider bar
    pygame.draw.rect(background, (211, 0, 211), shape_slider)
    
    # Draws slider bar on the screen on top of the slider
    shape_slider_bar = Rect(screen.get_size()[0]/2-800/2-100,(-1)*temp_size*800/80 + screen.get_size()[1]/2 + 800/2,30, 14)
    pygame.draw.rect(background, (100, 0, 100), shape_slider_bar)
    global shape_size
    shape_size = temp_size

    # Does not update screen as postion updating thread will
    return temp_size
    
# Draws centered text on the screen (harvested from Ahmad's side project, not yet implemented)
def drawCenteredText(text, background, font, height, screen):
    tempText = font.render(text, 1, (180, 180, 180))
    tempTextRect = tempText.get_rect()
    tempTextPos = Rect(0, height, tempTextRect.w, tempTextRect.h)
    centerXPos = background.get_rect().centerx
    tempTextPos.centerx = centerXPos
    background.blit(tempText, tempTextPos)
    screen.blit(background, (0,0))
        
# Main
def main():
    # Starts mqtt
    phone_client = paho.Client()
    phone_client.on_message = onMessage

    if phone_client.connect("localhost", 1883, 15) != 0:
        print("Could not connect")
        sys.exit(-1)

    # Subscribes to MQTT network that streams phone data
    phone_client.subscribe("data")

    # Starts retrieval from speech input
    speech_client = paho.Client()
    speech_client.on_Message = onSpeechMessage
    if speech_client.connect("localhost", 1883, 15) != 0:
        print("Could not connect")
        sys.exit(-1)
    
    # Subscribes to MQTT network that streams speech data
    speech_client.subscribe("speech_data")


    # Creates a Tkinter window
    window = tk.Tk()
    greeting = tk.Label(text="Welcome to Sphero Controls!")
    greeting.pack()
    window.update()

    #Displays to the user to wait pending all sensors starting up
    label = tk.Label(text="Setting everything up!")
    label.pack()
    window.update()
    sizeInput = tk.Entry(bg="purple", fg = "yellow",  width=50)
    sizeInput.insert(0, '0')
    speedInput = tk.Entry(bg = "blue", fg = "yellow", width = 50)
    speedInput.insert(0, '0')

    # Prevents unessesaary errors from spamming the console, uncomment in final edition
    sys.stderr = open(os.devnull, "w")

    # Initialise screen and displays game name
    pygame.init()
    screen = pygame.display.set_mode((1200, 1000))
    pygame.display.set_caption('Sphero Control')
    
    # Fill background with plain color
    BACKGROUNDCOLOR = (30, 30, 30)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BACKGROUNDCOLOR)
    
    # Prepare board upon which position can be displayed
    BOARDSIZE = 800
    board = Rect(screen.get_size()[0]/2-BOARDSIZE/2, screen.get_size()[1]/2-BOARDSIZE/2, BOARDSIZE, BOARDSIZE)
    pygame.draw.rect(background, (200, 200, 200), board, 0, 3)

    #Prepare Images for Sliders, Buttons, etc.

    #note picture size is 32x32
   #screen 1200x1000
    try:
       #Buttons
       upArrow_but = pygame.image.load("Assets/upArrow.png").convert()
       downArrow_but = pygame.image.load("Assets/DownArrow.png").convert()
       leftArrow_but = pygame.image.load("Assets/LeftArrow.png").convert()
       rightArrow_but = pygame.image.load("Assets/RightArrow.png").convert()
       stop_but = pygame.image.load("Assets/StopSign.png").convert()

       #Functions
       circle_but = pygame.image.load("Assets/Circle.png").convert()
       square_but = pygame.image.load("Assets/Square.png").convert()
       triangle_but = pygame.image.load("Assets/Triangle.png").convert()
       phone_but = pygame.image.load("Assets/Phone.png").convert()

       #Waiting of artwork for Vocal Commands
       speak_but = pygame.image.load("Assets/Phone.png").convert()

       #Sliders
       #TODO Design implementation


       #prints assets to UI
       screen.blit(upArrow_but, (screen.get_size()[0]/2+BOARDSIZE/2+70,screen.get_size()[1]/2-BOARDSIZE/2+30))

    except:
        print("Assets unable to load, Check to Ensure File path is correct and images are in the Asset Folder")
        print("Drawing Default Art")
 
    # Prepare Slider for speed
    speed_slider = Rect(screen.get_size()[0]/2-BOARDSIZE/2-50, screen.get_size()[1]/2-BOARDSIZE/2, 30, BOARDSIZE)
    pygame.draw.rect(background, (0, 211, 211), speed_slider)

    # Prepare Bar to show on speed Slider
    speed_slider_bar = Rect(screen.get_size()[0]/2-BOARDSIZE/2-50,screen.get_size()[1]/2+BOARDSIZE/2-14,30, 14)
    pygame.draw.rect(background, (0, 100, 100), speed_slider_bar)

    # Prepare numbers on top (0) and bottom (255) of bar to represent values

    # Prepare Slider for size of shape
    shape_slider = Rect(screen.get_size()[0]/2-BOARDSIZE/2-100, screen.get_size()[1]/2-BOARDSIZE/2, 30, BOARDSIZE)
    pygame.draw.rect(background, (211, 0, 211), shape_slider)

    # Prepare Bar to show on shape Slider
    shape_slider_bar = Rect(screen.get_size()[0]/2-BOARDSIZE/2-100,screen.get_size()[1]/2+BOARDSIZE/2-14,30, 14)
    pygame.draw.rect(background, (100, 0, 100), shape_slider_bar)

    # Prepare numbers on top (80) and bottom (0) of bar to represent values


    # Prepare North button for click-control
    north_button = Rect(screen.get_size()[0]/2+BOARDSIZE/2+70,screen.get_size()[1]/2-BOARDSIZE/2+30,30, 30)
    pygame.draw.rect(background, (0, 255, 0), north_button)

    #Prepare East button for click-control
    east_button = Rect(Rect(screen.get_size()[0]/2+BOARDSIZE/2+120,screen.get_size()[1]/2-BOARDSIZE/2+80,30, 30))
    pygame.draw.rect(background, (0, 255, 0), east_button)

    #Prepare South button for click-control
    South_button = Rect(Rect(screen.get_size()[0]/2+BOARDSIZE/2+70,screen.get_size()[1]/2-BOARDSIZE/2+130,30, 30))
    pygame.draw.rect(background, (0, 255, 0), South_button)

    #Prepare West button for click-control
    west_button = Rect(Rect(screen.get_size()[0]/2+BOARDSIZE/2+20,screen.get_size()[1]/2-BOARDSIZE/2+80,30, 30))
    pygame.draw.rect(background, (0, 255, 0), west_button)

    #Prepare stop button for click-control
    stop_button = Rect(Rect(screen.get_size()[0]/2+BOARDSIZE/2+70,screen.get_size()[1]/2-BOARDSIZE/2+80,30, 30))
    pygame.draw.rect(background, (255, 0, 0), stop_button)

    #Prepare phone button to change into phone control
    speech_button = Rect(Rect(screen.get_size()[0]/2+BOARDSIZE/2+70,screen.get_size()[1]/2-BOARDSIZE/2+350,30, 30))
    pygame.draw.rect(background, (255, 255, 0), speech_button)

    #Prepare phone button to change into phone control
    phone_button = Rect(Rect(screen.get_size()[0]/2+BOARDSIZE/2+70,screen.get_size()[1]/2-BOARDSIZE/2+450,30, 30))
    pygame.draw.rect(background, (255, 192, 203), phone_button)

    #Prepare circle button 
    circle_button = Rect(Rect(screen.get_size()[0]/2+BOARDSIZE/2+70,screen.get_size()[1]/2-BOARDSIZE/2+550,30, 30))
    pygame.draw.rect(background, (255, 145, 30), circle_button)

    #Prepare square button
    square_button = Rect(Rect(screen.get_size()[0]/2+BOARDSIZE/2+70,screen.get_size()[1]/2-BOARDSIZE/2+650,30, 30))
    pygame.draw.rect(background, (145, 30, 255), square_button)

    #Prepare Triangle button
    triangle_button = Rect(Rect(screen.get_size()[0]/2+BOARDSIZE/2+70,screen.get_size()[1]/2-BOARDSIZE/2+750,30, 30))
    pygame.draw.rect(background, (30, 255, 145), triangle_button)

    # Prepare opening text
    font = pygame.font.Font(None, 36)

    # Display everything for the screen
    speed_button = tk.Button(text= "Set Speed", width=20, height=1, bg = "blue", fg = "yellow", command = lambda: update_speed(screen, background, speed_slider, speed_slider_bar, speedInput, -1))
    size_button = tk.Button(text="Set Size", width=20, height=1, bg="purple", fg="yellow", command = lambda: update_size(screen, background, shape_slider, shape_slider_bar, sizeInput, -1))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepares starting config and related variables
    opening = True
    with SpheroEduAPI(toy) as droid:
        global gdroid
        gdroid = droid
        global traveled
        global currX
        global currY
        traveled = False
        currX = 0
        currY = 0
        global speed 
        speed= 0
        oldTime = 0
        global shape_size 
        shape_size= 0
        global phone_button_going
        phone_button_going = False
        global speech_button_going
        speech_button_going = False
        while(droid.get_location() == None):
            print("initializing, please wait")
            time.sleep(0.1)
        
        while(True):
            if((oldTime != round(time.time() * 10))):
                #print(droid.get_location())
                oldTime = round(time.time() * 2)
                board = Rect(screen.get_size()[0]/2-BOARDSIZE/2, screen.get_size()[1]/2-BOARDSIZE/2, BOARDSIZE, BOARDSIZE)
                if (droid.get_location()['x'] > 400 or droid.get_location()['x'] < -400) or (droid.get_location()['y'] > 400 or droid.get_location()['y'] < -400):
                    droid.set_heading(droid.get_heading() + 180)
                    drawCenteredText("Out of Bounds", background, font, screen.get_size()[1]/2, screen)
                    time.sleep(1.5)
                    pygame.draw.rect(background, (200, 200, 200), board, 0, 3)
                    screen.blit(background, (0, 0))
                    pygame.display.flip()

                updateFrame(screen, droid, background)
            
            # Updates TKinter to tell the user that everything is set up
            label['text'] = "You're good to go!"
            label.pack()
            sizeInput.pack()
            speedInput.pack()
            size_button.pack(side=tk.LEFT)
            speed_button.pack(side=tk.LEFT)
            window.update()

            # Runs TKinter in a thread to run pygame and control software at the same time
            tkinter_thread = threading.Thread(target = window.mainloop)
            tkinter_thread.setDaemon(True)
            tkinter_thread.start()


            for event in pygame.event.get():
                # Ends execution upon the user closing the window
                if event.type == QUIT:
                    toy.wake()
                    try:
                        phone_client.disconnect()
                    except:
                        pass
                    try:
                        speech_client.disconnect()
                    except:
                        pass
                    return 1
                
                # Runs code based on where a user had pressed on the screen
                elif event.type == MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    print(mousePos)

                    # Handles speed slider, changing value based on position of mouse
                    if(mousePos[0] > screen.get_size()[0]/2-BOARDSIZE/2-50 and mousePos[0] < screen.get_size()[0]/2-BOARDSIZE/2-20 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2 and mousePos[1] < screen.get_size()[1]/2+BOARDSIZE/2):
                        print("speed to be set to " + (str)((int(round((screen.get_size()[1]-mousePos[1]-screen.get_size()[1]/2+BOARDSIZE/2)/800*255)))))
                        speed = update_speed(screen, background, speed_slider, speed_slider_bar, speedInput, (int(round((screen.get_size()[1]-mousePos[1]-screen.get_size()[1]/2+BOARDSIZE/2)/800*255))))
                    
                    # Handles shape size slider, changing values based on position of mouse
                    elif(mousePos[0] > screen.get_size()[0]/2-BOARDSIZE/2-100 and mousePos[0] < screen.get_size()[0]/2-BOARDSIZE/2-70 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2 and mousePos[1] < screen.get_size()[1]/2+BOARDSIZE/2):
                        print("Shape size to be set to " + (str)((int(round((screen.get_size()[1]-mousePos[1]-screen.get_size()[1]/2+BOARDSIZE/2)/800*80)))))
                        shape_size = update_size(screen, background, shape_slider, shape_slider_bar, sizeInput, (int(round((1000-mousePos[1]-screen.get_size()[1]/2+BOARDSIZE/2)/800*80))))
                    
                    # Resets the board, covering it all in white
                    elif(mousePos[0] > screen.get_size()[0]/2-BOARDSIZE/2 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2 and mousePos[1] < screen.get_size()[1]/2+BOARDSIZE/2):
                        droid.set_speed(0)
                        time.sleep(0.1)
                        pygame.draw.rect(background, (200, 200, 200), board, 0, 3)
                        screen.blit(background, (0, 0))
                        pygame.display.flip()

                    # Handles North button and sets the robot to North (+y)
                    elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+30 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+60):
                        droid.set_heading(0)
                        droid.set_speed(speed)
                    
                    # Handles East button and sets the robot to East (+x)
                    elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+120 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+150 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+80 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+110):
                        droid.set_heading(90)
                        droid.set_speed(speed)

                    # Handles West button and sets the robot to West (-x)
                    elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+20 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+50 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+80 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+110):
                        droid.set_heading(270)
                        droid.set_speed(speed)

                    # Handles South button and sets the robot to South (-y)
                    elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+130 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+160):
                        droid.set_heading(180)
                        droid.set_speed(speed)

                    # Handles stop button and sets the robots speed to zero despite any additional settings
                    elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+80 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+110):
                        droid.set_speed(0)

                    # Handles speech button and begins speech control mode
                    elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+350 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+380):
                        print("Speech Button")


                    # Handles phone button and begins phone control mode
                    elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+450 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+480):
                        print("Phone Button")
                        if(phone_button_going == True):
                            phone_button_going = False
                            phone_client.loop_stop()
                        else:
                            try:
                                phone_client.loop_start()
                                print("loop started")
                                phone_button_going = True
                            except: 
                                print("phone failed, try again")

                    

                    # Handles circle button
                    # Creates a thread to send robot controls and map to screen at the same time 
                    # Utilized speed and size slider values
                    elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+550 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+580):
                        circle_thread = threading.Thread(target=spinCircle, args=(droid, speed, shape_size))
                        circle_thread.setDaemon(True)
                        circle_thread.start()
                    
                    # Handles square button and sets robot to draw square 
                    # Uses speed and size values
                    elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+650 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+680):
                        square(droid, shape_size, speed, screen, background)

                    # Handles triangles button and sets robot to draw square 
                    # Uses speed and size values
                    elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+750 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+780):
                        triangle(droid, shape_size, speed, screen, background)

# runs main
while(main() != 1):
    pass
    

