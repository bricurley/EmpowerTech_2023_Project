# Mental Health Simulation
# Created by Briana Curley and Ahmad Qureshi

# Imports all used widgets and constants from Tkinter, the GUI package
from tkinter import Label, Button, DISABLED, Tk, CENTER, mainloop, ACTIVE

# Imports randomization functions for shuffling an array and 
# getting a random thing from a dictionatry
from random import sample, shuffle

# Imports options from the defined options.py file
#from options import GOOD_OPTIONS, BAD_OPTIONS, ALL_OPTIONS

GOOD_OPTIONS = {'Walk Outside': {
        'Mental Health': 2,
        'Physical Health': 5,
        'Social Standing': 5,
        'Description': 'You go on a walk to ease your stress, get some exercise, and make new friends'
    },
    'Solid Sleep': {
        'Mental Health': 5,
        'Physical Health': 5,
        'Description': 'You get a good night\'s rest to recharge both your mental and physical health'
    }, 
    'Make Friends': {
        'Social Standing': 10,
        'Mental Health': 5,
        'Description': 'You are able to find people to open up to and connect with'
    },
    'Journal Entry': {
        'Mental Health': 5,
        'Description': 'You write in your journal to destress from the comfort of your bedroom desk'
    }
}

BAD_OPTIONS = {'Alcohol': {
        'Mental Health': -5,
        'Drug Independency': -5,
        'Money': -50,
        'Description': 'You turn to alcohol as a way to cope. But it is expensive and only a temporary solution'
    },
    'Burn Bridges': {
        'Mental Health': -5,
        'Social Standing': -10,
        'Description': 'You refuse to accept help and support from close friends'
    },
    'The Bar': {
        'Mental Health': -5,
        'Drug Independency': -5,
        'Physical Health': -5,
        'Social Standing': 5,
        'Money': -35,
        'Description': 'You go to the bar to loosen up and feel cool, but spend money and the alcohol affects your health'
    },
    'No Exercise': {
        'Mental Health': -5,
        'Physical Health': -10,
        'Description': 'You skip exercising, leaving you feeling drained and out of energy'
    },
    'All Nighter Studying': {
        'Mental Health': -10,
        'Physical Health': -10,
        'Description': 'You are stressed for an exam and study too much, and perform poorly due to lack of sleep'
    }
}

MIXED_OPTIONS = {'Therapy': {
        'Money': -100,
        'Mental Health': 10,
        'Social Standing': -5,
        'Drug Independency': 5,
        'Description': 'You open up through therapy and find help other than drugs.\nUnfortunately, there are costs and social stigma as well'
    },
    'Medication': {
        'Money': -35,
        'Mental Health': 10,
        'Drug Independency': -5,
        'Social Standing': -5,
        'Description': 'Medication helps, but can be expensive, increase drug dependency, and have social stigma\nassociated with it'
    },
    'Social Media': {
        'Mental Health': -5,
        'Social Standing': 5,
        'Description': 'You doomscroll tiktok, leaving you drained but found a friend doing the same'
    },
    'Work Extra Hours': {
        'Social Standing': 5,
        'Money': 100,
        'Mental Health': -5,
        'Description': 'You skip family time to work, leaving you feeling drained and alone with more money'
    },
    'Mental Health Day': {
        'Mental Health': 5,
        'Social Standing': -5,
        'Money': -100,
        'Description': 'You skip work to recharge, you couldn\'t work and people look down on you but you feel great'
    },
    'Self Care Day': {
        'Mental Health': 10,
        'Money': -35,
        'Description': 'You take a day off you get your favorite ice cream but you spend money.'
    },
    'Healthy Boundaries': {
        'Social Standing': -10,
        'Mental Health': 10,
        'Description': 'You need to take care of yourself but people are upset you aren\'t there for them as much'
    },
    'No Boundaries': {
        'Social Standing': 10,
        'Mental Health': -10,
        'Description': 'You become a people pleaser, which makes you more popular but lets people take advantage of you'
    }
}

ALL_OPTIONS = GOOD_OPTIONS | BAD_OPTIONS | MIXED_OPTIONS

'''CONSTANTS'''
# Max values of stats. Everything but money is represented as a percentage (starting at 100). Money starts at $1000
MAX_VALS = {"Mental Health": 100,
            "Drug Independency": 100,
            "Physical Health": 100,
            "Social Standing": 100,
            "Money": 1000}

'''INTERNAL'''
# Function to control colors from rgb function
def _from_rgb(rgb):
    # translates an rgb tuple of int to a tkinter friendly color code
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

'''GAME LOGIC'''
def update_stat_label(stats, stat_labels, key):
    stat_labels[key]['text'] = make_stat_label_text(key, stats)
    stat_labels[key]['foreground'] = _from_rgb(((int)(255-255/MAX_VALS[key]*stats[key]), (int)(255/MAX_VALS[key]*stats[key]), 0))

# Update stats values based on user's decision
def update_stats(stats, button_clicked, stat_labels, buttons, event_label, prev_event, window):
    # Grabs the values that change by referencing the text from the button and the options dictionary
    event_stats = ALL_OPTIONS[button_clicked['text']]

    # Updates the event label text with the event description
    event_text = event_stats['Description']
    prev_event['text'] = event_text

    global num_choices_made
    # go through value in current_stats dict and add/subtract values from accordingly
    for key in event_stats.keys():
        if key != 'Description':
            if stats[key] + event_stats[key] <= MAX_VALS[key] and event_stats[key] + stats[key] >= 0:
                stats[key]+=event_stats[key]
                update_stat_label(stats, stat_labels, key)
            if stats[key] + event_stats[key] < 0:
                stats[key] += event_stats[key]
                update_stat_label(stats, stat_labels, key)
                lose_label = lose_from_stat(key, window)
                finish_game(buttons, event_label, prev_event, window, stats, stat_labels, lose_label)
    set_options(buttons)
    # Check if user has reached 30 turns/decisions
    if num_choices_made < 30:
        num_choices_made += 1
    # End game if max number of turns has been reached
    else:
        finish_game(buttons, event_label, prev_event, window, stats, stat_labels, None)

'''END OF GAME FUNCTIONS'''

def make_stat_label_text(key, stats):
    if key == 'Money':
        return f"{key}: ${stats[key]}"
    else:
        return f"{key}: {stats[key]}%"

# Reset user's stats if reset button has been clicked
def reset_stats(stats, stat_labels):
    # Iterate through stats, change all values back to max (original) values
    for key in MAX_VALS.keys():
        stats[key] = MAX_VALS[key]
        stat_labels[key]['text'] = make_stat_label_text(key, stats)
        # Reset color to green
        stat_labels[key]['foreground'] = _from_rgb((0, 255, 0))

# Creates label to display message to the user if one of their stats has reached 0 or lower
def lose_from_stat(stat, window):
    # Create label and tell user which stat dropped to 0
    lose_label = Label(master=window, 
                       text=f"Your {stat}\n      fell too low", 
                       foreground=_from_rgb((255,0,0)), 
                       anchor=CENTER)
    # Place label in stats box below stats
    lose_label.place(x=47, y=380)
    return lose_label

def finish_game(buttons, event_label, prev_event, window, stats, stat_labels, lose_label):
    # Prevent user from being able to use buttons to make more decisions
    for button in buttons:
        button['state'] = DISABLED
    # Display message to user 
    prev_event['text'] = '\n\nYou completed the game, your final stats are to the left.'
    reset_button_reference = []
    # Create option for user to reset the simulation
    reset_button = Button(window, text='Reset Simulation')
    reset_button_reference.append(reset_button)
    reset_button['command'] = lambda: reset_game(reset_button_reference, 
                                                 buttons, stats, 
                                                 stat_labels, 
                                                 prev_event, 
                                                 event_label, 
                                                 lose_label)
    # Place a reset button in box that displays explanations of how events impact health
    reset_button.place(x=510, y=210)

# Resets game - only appears if user loses or finished game
def reset_game(reset_button_reference, buttons, stats, stat_labels, event_label, prev_event, lose_label):
    # Get rid of reset option
    reset_button = reset_button_reference.pop()
    reset_button.destroy()
    # If user has option to rest game because they lost
    if lose_label != None:
        lose_label.destroy()
    # Reactivate option buttons
    for button in buttons:
        button['state'] = ACTIVE
    # Reset number of turns
    global num_choices_made
    num_choices_made = -1
    reset_stats(stats, stat_labels)
    # Display prompts for user to make a decision from option buttons
    prev_event['text'] = '\n\nWhat would you like to do next?'
    event_label['text'] = ''

'''GAME INITIALIZATION'''
# Updates text in option buttons
def set_button(button, option_list):
    random_option = sample(option_list.items(), 1)
    button['text'] = random_option[0][0]

# Changes the 3 buttons to allow for the user to have new options to choose from
def set_options(option_buttons):
    # Randomizes the order of the list of buttons
    shuffle(option_buttons)
    # Sets one of the three buttons to a good option
    set_button(option_buttons[0], GOOD_OPTIONS)
    # Sets one button to a bad option
    set_button(option_buttons[1], BAD_OPTIONS)
    # Sets one option to a completely random option
    set_button(option_buttons[2], ALL_OPTIONS)

def add_buttons(window, current_stats, stat_labels, prev_event, event_label):
    # Prepares a list to refer to all buttons when necessary
    option_buttons = []
    # Creates button objects that update stats and are given a label when clicked
    # All buttons change all buttons when clicked, using the previous reference
    option_1 = Button(window, 
                      text="Option 1", 
                      command=lambda:update_stats(current_stats, 
                                                  option_1, 
                                                  stat_labels,
                                                  option_buttons,
                                                  event_label,
                                                  prev_event,
                                                  window))
    
    option_2 = Button(window, 
                      text="Option 2", 
                      command=lambda:update_stats(current_stats, 
                                                  option_2,
                                                  stat_labels,
                                                  option_buttons,
                                                  event_label,
                                                  prev_event,
                                                  window))
    
    option_3 = Button(window, 
                      text="Option 3",
                      command=lambda:update_stats(current_stats,
                                                  option_3,
                                                  stat_labels,
                                                  option_buttons,
                                                  event_label,
                                                  prev_event, 
                                                  window)
                      )
    option_buttons = [option_1, option_2, option_3]
    set_options(option_buttons)
    # Place option buttons 
    option_1.place(x=330,
                   y=400)
    option_2.place(x=500, 
                   y=400)
    option_3.place(x=670, 
                   y=400)
    option_buttons = [option_1, option_2, option_3]

# Prepares Labels and buttons displayed on first code execution
def initialize_window():
    # creates a Tk() object
    window = Tk()
    
    # Initialize stat values for beginning of simulation
    current_stats = MAX_VALS.copy()
    
    # Initializes a dictionary to store labels for values of each stat
    stat_labels = {}
    
    # Sets the size, title, and main color of the window
    window.geometry("880x480")
    window.title("Mental Health Simulation")
    window.configure(bg=_from_rgb((0, 0, 128)))
        
    # Displays message to user about the most recent choice they made. Start off empty
    event_text=''
    prev_event = Label(window,
                       text=event_text,
                       width=70, border=2,
                       relief='solid',
                       foreground='black',
                       anchor='center')
    
    prev_event.place(x=300,
                     y=100,
                     height=150)

    # Event prompting the user to select a button. Buttons are also placed within this label box
    event_label = Label(window,
                        text='\n\nWhat would you like to do next?',
                        width=70, border=2,
                        borderwidth=2, relief='solid',
                        foreground='black',
                        anchor='n')
    event_label.place(x=300, 
                      y=300,
                      height = 150)

    global num_choices_made
    num_choices_made = 0

    # Create stats bar
    init_stats(window, current_stats, stat_labels)

    # Initialize buttons/options user can select in simulation
    add_buttons(window, 
                current_stats, 
                stat_labels, 
                prev_event, 
                event_label)
    

# Create stats bar
def init_stats(window, current_stats, stat_labels):
    # Display information about the simulation at the top of the screen
    heading = Label(window, 
                    text ="This is a mental health simulation focused on understanding the impact of actions\nCreated by Briana Curley and Ahmad Qureshi", 
                    width=102)
    heading.place(x=28,
                  y=10)
    
    top_y_position = 150

    stats_border = Label(window, 
                         border=2, 
                         borderwidth=2, 
                         width=100, 
                         relief='solid')
    
    stats_border.place(x=10,
                       y=top_y_position-45, 
                       width=200, 
                       height=335)
    
    stats_title = Label(window, 
                        text='Your Stats', 
                        relief='solid', 
                        borderwidth = 2, 
                        border = 2)
    
    stats_title.place(x=70, 
                      y= top_y_position - 30,)
    
    # Create labels for each stat value
    for key in current_stats.keys():
        # Creates each button with standard sizes and text
        if key != 'Money':
            value_recorder = Label(
                window, 
                text=f"{key}: {current_stats[key]}%", 
                border=2, 
                borderwidth=2, 
                relief='solid', 
                foreground=_from_rgb((0, 255, 0)), 
                anchor='center', 
                width=20)
        else:
            value_recorder = Label(
                window, 
                text=f"{key}: ${current_stats[key]}", 
                border=2, 
                borderwidth=2, 
                relief='solid', 
                foreground=_from_rgb((0, 255, 0)), 
                anchor='center', 
                width=20)
        # Adds each label to the screen
        value_recorder.place(x=27, 
                            y=top_y_position)
        # Moves the next label to be 50 pixels lower
        top_y_position+=50
        # Adds the label to a dictionary for later reference
        stat_labels[key] = value_recorder

# Run game
def main():
    # Prepares the window
    initialize_window()
    # mainloop, runs until the user presses 'X'
    mainloop()

if __name__ == "__main__":
    main()
