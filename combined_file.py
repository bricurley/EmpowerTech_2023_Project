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
    }
    }

BAD_OPTIONS = {'Alcohol': {
        'Mental Health': -5,
        'Drug Dependency': 5,
        'Money': -50,
        'Description': 'You turn to alcohol as a way to cope. But it is expensive and only a temporary solution'
    },
    'Burn Bridges': {
        'Mental Health': 5,
        'Social Standing': -10,
        'Description': 'You refuse to accept help and support from close friends'
    },
    'The Bar': {
        'Mental Health': -5,
        'Drug Dependency': 5,
        'Physical Health': -5,
        'Social Standing': 5,
        'Money': -35,
        'Description': 'You go to the bar to loosen up and feel cool, but spend money and the alcohol affects your health'
    },
    'No Exercise': {
        'Mental Health': -5,
        'Physical Health': -10,
        'Description': 'You skip exercising, leaving you feeling drained and out of energy'
    }
}

MIXED_OPTIONS = {'Therapy': {
        'Money': -100,
        'Mental Health': 10,
        'Social Standing': -5,
        'Drug Dependency': -5,
        'Description': 'You open up through therapy and find help other than drugs. Unfortunately, there are costs and social stigma as well'
    },
    'Medication': {
        'Money': -35,
        'Mental Health': 10,
        'Drug Dependency': 5,
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
    }
}

ALL_OPTIONS = GOOD_OPTIONS | BAD_OPTIONS | MIXED_OPTIONS


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


# Update stats values based on user's decision
def update_stats(stats, button_clicked, stat_labels, buttons, event_label):
    stat_change_val = ALL_OPTIONS[button_clicked['text']]
    event_text = ALL_OPTIONS[button_clicked['text']]['Description']
    event_label['text'] = event_text
    # go through value in current_stats dict and update accordingly
    for key in stat_change_val.keys():
        if key == 'Description':
            pass
        else:
            if stats[key] + stat_change_val[key] < 100 and stat_change_val[key] + stats[key] > 0:
                stats[key] += stat_change_val[key]
                stat_labels[key]['text'] = f"{key}: {stats[key]}%"
                stat_labels[key]['foreground'] = _from_rgb(((int)(255-255/100*stats[key]), (int)(255/100*stats[key]), 0))
    set_options(buttons)
    
def set_button(button, option_list):
    random_option = sample(option_list.items(), 1)
    button['text'] = random_option[0][0]

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
    current_stats = {
        "Mental Health": 100,
        "Drug Dependency": 0,
        "Physical Health": 100,
        "Social Standing": 100,
        "Money": 1000
    }
    
    stat_labels = {}
    
    # sets the geometry of
    # main root window
    window.geometry("1024x600")
    window.configure(bg=_from_rgb((0, 0, 128)))
    
    
    label = Label(window, text ="This is a mental health simulation focused on understanding the impact of actions")
    label.pack(side = TOP, pady = 10)

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
        value_recorder = Label(
            window, 
            text=f"{key}: {current_stats[key]}%", 
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
    

    # Event prompting the user to select a button
    event_text='lemon'
    event_label = Label(window,
                        text=event_text,
                        width=70, border=2,
                        borderwidth=2, relief='solid',
                        foreground='black',
                        anchor='center')
    event_label.place(x=300, 
                      y=300, #DELETE LATER used tobe 370
                      height = 150)

    # Initialize buttons/options user can select in simulation
    option_1 = Button(window, 
                      text="Option 1", 
                      command=lambda:update_stats(current_stats, 
                                                  option_1, 
                                                  stat_labels,
                                                  option_buttons,
                                                  event_label))
    
    option_2 = Button(window, 
                      text="Option 2", 
                      command=lambda:update_stats(current_stats, 
                                                  option_2,
                                                  stat_labels,
                                                  option_buttons,
                                                  event_label))
    
    option_3 = Button(window, 
                      text="Option 3",
                      command=lambda:update_stats(current_stats,
                                                  option_3,
                                                  stat_labels,
                                                  option_buttons,
                                                  event_label)
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
