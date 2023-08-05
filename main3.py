# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *
 
# Update stats values based on user's decision
def update_stats(stats, stat_change_val):
    # go through value in current_stats dict and update accordingly
    for key in stat_change_val.keys():
        stats[key] += stat_change_val[key]

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
    
    stats_labels = {}
    
    # sets the geometry of
    # main root window
    window.geometry("1024x600")
    
    
    label = Label(window, text ="This is the main window")
    label.pack(side = TOP, pady = 10)

    top_y_position = 150

    stats_border = Label(window, border=2, borderwidth=2, width=100, relief='solid')
    stats_border.place(x=10, y=top_y_position-45, width=200, height=335)
    stats_title = Label(window, text='Your Stats', relief='solid', borderwidth=2, border=2)
    stats_title.place(x=67, y=top_y_position-30)
    
    for key in current_stats.keys():
        value_recorder = Label(window, text=f"{key}: {current_stats[key]}", border=2, borderwidth=2, relief='solid', foreground='green', justify='center', width=20)
        value_recorder.place(x=20, y=top_y_position)
        top_y_position+=50
        stats_labels[key] = value_recorder
    

    # Event prompting the user to select a button
    event="This is the event that happened to the user"
    event_label = Label(window, text=event, width=70, border=2, borderwidth=2, relief='solid', foreground='black')
    event_label.place(x=300, y=370)
    
    # Initialize buttons/options user can select in simulation
    option_1 = Button(window, text="Option 1")
    option_2 = Button(window, text="Option 2")
    option_3 = Button(window, text="Option 3")
    
    # Place option buttons
    option_1.place(x=300, y=400)
    option_2.place(x=570, y=400)
    option_3.place(x=840, y=400)
    #FIXME add button border
    
    # Following line will bind click event
    # On any click left / right button
    # of mouse a new window will be opened
    
    
    
    # mainloop, runs infinitely
    mainloop()

if __name__ == "__main__":
    main()
