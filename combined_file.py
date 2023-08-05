# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *
from random import sample, shuffle

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
    'Healthy Boundaries': {
        'Social Standing': 10,
        'Mental Health': 10,
        'Description': 'Your friends know you are there for them but also that you need to take care of yourself'
    },
    'Journal Entry': {
        'Mental Health': 10,
        'Description': 'You write in your journal to destress'
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
        'Description': 'You open up through therapy and find help other than drugs. Unfortunately, there are costs and social stigma as well'
    },
    'Medication': {
        'Money': -35,
        'Mental Health': 10,
        'Drug Independency': -5,
        'Social Standing': -5,
        'Description': 'Medication helps, but can be expensive, increase drug dependency, and have social stigma associated with it'
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
    'Stop Setting Boundaries': {
        'Social Standing': 10,
        'Mental Health': -10,
        'Description': 'You become a people pleaser, which makes you more popular but lets people take advantage of you'
    }
}

ALL_OPTIONS = GOOD_OPTIONS | BAD_OPTIONS | MIXED_OPTIONS

MAX_VALS = {"Mental Health": 100,
            "Drug Independency": 100,
            "Physical Health": 100,
            "Social Standing": 100,
            "Money": 1000}

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


# Update stats values based on user's decision
def update_stats(stats, button_clicked, stat_labels, buttons, event_label, prev_event, window):
    stat_change_val = ALL_OPTIONS[button_clicked['text']]
    event_text = ALL_OPTIONS[button_clicked['text']]['Description']
    global num_choices_made
    event_label['text'] = event_text
    # go through value in current_stats dict and update accordingly
    for key in stat_change_val.keys():
        if key != 'Description':
            if stats[key] + stat_change_val[key] <= MAX_VALS[key] and stat_change_val[key] + stats[key] >= 0:
                stats[key] += stat_change_val[key]
                if key == 'Money':
                    stat_labels[key]['text'] = f"{key}: ${stats[key]}"
                else:
                    stat_labels[key]['text'] = f"{key}: {stats[key]}%"
                stat_labels[key]['foreground'] = _from_rgb(((int)(255-255/MAX_VALS[key]*stats[key]), (int)(255/MAX_VALS[key]*stats[key]), 0))
    set_options(buttons)
    if num_choices_made < 30:
        num_choices_made += 1
    else:
        finish_game(buttons, event_label, prev_event, window, stats, stat_labels)
    
def reset_stats(stats, stat_labels):
    for key in MAX_VALS.keys():
        stats[key] = MAX_VALS[key]
        if key == 'Money':
            stat_labels[key]['text'] = f"{key}: ${stats[key]}"
        else:
            stat_labels[key]['text'] = f"{key}: {stats[key]}%"
        stat_labels[key]['foreground'] = _from_rgb((0, 255, 0))
    

def set_button(button, option_list):
    random_option = sample(option_list.items(), 1)
    button['text'] = random_option[0][0]

def finish_game(buttons, event_label, prev_event, window, stats, stat_labels):
    for button in buttons:
        button['state'] = DISABLED
    event_label['text'] = 'You completed the game, your stats are to the left.'
    prev_event['text'] = ''
    reset_button_reference = []
    reset_button = Button(window, text='Reset Simulation')
    reset_button_reference.append(reset_button)
    reset_button['command'] = lambda: reset_game(reset_button_reference, buttons, stats, stat_labels)
    reset_button.place(x=510, y=210)

def reset_game(reset_button_reference, buttons, stats, stat_labels):
    reset_button = reset_button_reference.pop()
    reset_button.destroy()
    for button in buttons:
        button['state'] = ACTIVE
    global num_choices_made
    num_choices_made = -1
    reset_stats(stats, stat_labels)
    

# 
def set_options(option_buttons):
    shuffle(option_buttons)
    set_button(option_buttons[0], GOOD_OPTIONS)
    set_button(option_buttons[1], BAD_OPTIONS)
    set_button(option_buttons[2], ALL_OPTIONS)

# Prepares Labels and buttons displayed on first code execution
def initialize_window():
    master = Tk()
    return master

def main():
    # creates a Tk() object
    window = Tk()
    
    # Initialize stat values for beginning of simulation
    current_stats = MAX_VALS
    
    stat_labels = {}
    
    # sets the geometry of
    # main root window
    window.geometry("1024x600")
    window.title("Mental Health Simulation")
    window.configure(bg=_from_rgb((0, 0, 128)))
    
    heading = Label(window, text ="This is a mental health simulation focused on understanding the impact of actions", width=102)
    heading.place(x=10,
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
    
    for key in current_stats.keys():
        if key != 'Money':
            value_recorder = Label(
                window, 
                text=f"{key}: {current_stats[key]}%", 
                border=2, 
                borderwidth=2, 
                relief='solid', 
                foreground='green', 
                anchor='center', 
                width=20)
        else:
            value_recorder = Label(
                window, 
                text=f"{key}: ${current_stats[key]}", 
                border=2, 
                borderwidth=2, 
                relief='solid', 
                foreground='green', 
                anchor='center', 
                width=20)
        value_recorder.place(x=27, 
                            y=top_y_position)
        top_y_position+=50
        stat_labels[key] = value_recorder
    
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

    # Event prompting the user to select a button
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

    # Initialize buttons/options user can select in simulation
    option_1 = Button(window, 
                      text="Option 1", 
                      command=lambda:update_stats(current_stats, 
                                                  option_1, 
                                                  stat_labels,
                                                  option_buttons,
                                                  prev_event,
                                                  event_label,
                                                  window))
    
    option_2 = Button(window, 
                      text="Option 2", 
                      command=lambda:update_stats(current_stats, 
                                                  option_2,
                                                  stat_labels,
                                                  option_buttons,
                                                  prev_event,
                                                  event_label,
                                                  window))
    
    option_3 = Button(window, 
                      text="Option 3",
                      command=lambda:update_stats(current_stats,
                                                  option_3,
                                                  stat_labels,
                                                  option_buttons,
                                                  prev_event,
                                                  event_label, 
                                                  window)
                      )
    

    option_buttons = [option_1, option_2, option_3]
    set_options(option_buttons)
    # Place option buttons 
    option_1.place(x=330,
                   y=400)
    option_2.place(x=500, y=400)
    option_3.place(x=670, y=400)

    # mainloop, runs until the user presses 'X'
    mainloop()

if __name__ == "__main__":
    main()
