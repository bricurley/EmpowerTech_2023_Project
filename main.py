# Manages sleep functions for switching between threads
import time



# Important for drawing circles
import math



# Used for click interactions with the user and for the main interface
import pygame

# Used for various pygame screen and side elements
from pygame.locals import *




# Draws the dot for the robot as it travels on the screen
def updateFrame(screen, droid, background):
    # Puts the square on the screen
    pygame.draw.rect(background, (255, 0, 0), (100,100))

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

    pygame.display.flip()
    while True:
        updateFrame(screen, None, background)
        for event in pygame.event.get():
            # Runs code based on where a user had pressed on the screen
            if event.type == MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                print(mousePos)

                # Handles speed slider, changing value based on position of mouse
                if(mousePos[0] > screen.get_size()[0]/2-BOARDSIZE/2-50 and mousePos[0] < screen.get_size()[0]/2-BOARDSIZE/2-20 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2 and mousePos[1] < screen.get_size()[1]/2+BOARDSIZE/2):
                    print("speed to be set to " + (str)((int(round((screen.get_size()[1]-mousePos[1]-screen.get_size()[1]/2+BOARDSIZE/2)/800*255)))))
                    
                # Handles shape size slider, changing values based on position of mouse
                elif(mousePos[0] > screen.get_size()[0]/2-BOARDSIZE/2-100 and mousePos[0] < screen.get_size()[0]/2-BOARDSIZE/2-70 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2 and mousePos[1] < screen.get_size()[1]/2+BOARDSIZE/2):
                    print("Shape size to be set to " + (str)((int(round((screen.get_size()[1]-mousePos[1]-screen.get_size()[1]/2+BOARDSIZE/2)/800*80)))))
                    
                # Resets the board, covering it all in white
                elif(mousePos[0] > screen.get_size()[0]/2-BOARDSIZE/2 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2 and mousePos[1] < screen.get_size()[1]/2+BOARDSIZE/2):
                    #droid.set_speed(0)
                    time.sleep(0.1)
                    pygame.draw.rect(background, (200, 200, 200), board, 0, 3)
                    #screen.blit(background, (0, 0))
                    pygame.display.flip()

                # Handles North button and sets the robot to North (+y)
                elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+30 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+60):
                    print("North")
                    #droid.set_heading(0)
                    #droid.set_speed(speed)
                
                # Handles East button and sets the robot to East (+x)
                elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+120 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+150 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+80 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+110):
                    print("East")
                    #droid.set_heading(90)
                    #droid.set_speed(speed)

                # Handles West button and sets the robot to West (-x)
                elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+20 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+50 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+80 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+110):
                    print("West")
                    #droid.set_heading(270)
                    #droid.set_speed(speed)

                # Handles South button and sets the robot to South (-y)
                elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+130 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+160):
                    print("South")
                    #droid.set_heading(180)
                    #droid.set_speed(speed)

                # Handles stop button and sets the robots speed to zero despite any additional settings
                elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+80 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+110):
                    print("Stop")
                    #droid.set_speed(0)

                # Handles speech button and begins speech control mode
                elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+350 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+380):
                    print("Speech Button")

                

                # Handles circle button
                # Creates a thread to send robot controls and map to screen at the same time 
                # Utilized speed and size slider values
                elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+550 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+580):
                    print("circle")
                
                # Handles square button and sets robot to draw square 
                # Uses speed and size values
                elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+650 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+680):
                    print("square")

                # Handles triangles button and sets robot to draw square 
                # Uses speed and size values
                elif(mousePos[0] > screen.get_size()[0]/2+BOARDSIZE/2+70 and mousePos[0] < screen.get_size()[0]/2+BOARDSIZE/2+100 and mousePos[1] > screen.get_size()[1]/2-BOARDSIZE/2+750 and mousePos[1] < screen.get_size()[1]/2-BOARDSIZE/2+780):
                    print("Triangle")

# runs main
while(main() != 1):
    pass
    

