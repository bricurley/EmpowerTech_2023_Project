# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *


GOOD_OPTIONS = {}
BAD_OPTIONS = {}



# Update stats values based on user's decision
def update_stats(stats, stat_change_val, stat_labels):
    # go through value in current_stats dict and update accordingly
    for key in stat_change_val.keys():
        stats[key] += stat_change_val[key]
        stat_labels[key]['text'] = f"{key}: {stats[key]}"
    
def dummy():
    pass

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
        "Dependency Level": 100,
        "Kidney Health": 100,
        "Lung Health": 100,
        "Liver Health": 100,
        "Money": 1000
    }
    
    stat_labels = {}
    
    # sets the geometry of
    # main root window
    window.geometry("1024x600")
    
    
    label = Label(window, text ="This is the main window")
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
            text=f"{key}: {current_stats[key]}", 
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
    event="This is the event that happened to the user"
    event_label = Label(window,
                        text=event,
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
                                                  {'Money':-500}, 
                                                  stat_labels))
    
    option_2 = Button(window, 
                      text="Option 2", 
                      command=lambda:update_stats(current_stats, 
                                                  {"Liver Health": 100, "Money": 1000},
                                                  stat_labels))
    
    option_3 = Button(window, 
                      text="Option 3", 
                      command=dummy)
    
    # Place option buttons 
    option_1.place(x=340,
                   y=400)
    option_2.place(x=570, y=400)
    option_3.place(x=800, y=400)
    #FIXME add button border
    #button_border = Label(window, width=70, border=2, borderwidth=2, relief='solid', foreground='transparent')
    #button_border.place(x=300, y=400)
    
    # Following line will bind click event
    # On any click left / right button
    # of mouse a new window will be opened
    
    
    
    # mainloop, runs infinitely
    mainloop()

if __name__ == "__main__":
    main()
