import tkinter as tk
import threading
import time
from recognition2 import Client

# Create a frame whare we display the time, day and date
def create_Frame_date(fenetre,height_val,width_val):
    frame1 = tk.Frame(fenetre, height=height_val, width=width_val, bg="black",bd=1, relief="flat")
    frame1.place(x=0,y=0)

# Same as date_time_vis in Visitor 
def date_time_owner(fen_):
    def update_():
        timeString = time.strftime("%I:%M:%S")
        timeLabel.config(text=timeString)

        dateString = time.strftime("%B%d,%Y")
        dateLabel.config(text=dateString)
 
        dayString = time.strftime("%A")
        dayLabel.config(text=dayString)
        fen_.after(1000,update_)

    fen_.update()

    timeLabel = tk.Label(fen_,font=("Arial",15),bg="black",fg="white")
    timeLabel.place(x=350,y=15)

    dateLabel = tk.Label(fen_,font=("Arial",12),bg="black",fg="white")
    dateLabel.place(x=165,y=30)

    dayLabel = tk.Label(fen_,font=("Arial",12),bg="black",fg="white")
    dayLabel.place(x=181,y=8)

    update_()

def create_window_owner():

    # Create a Tkinter window
    window = tk.Tk()

    window.geometry("443x650")      # Set the dimensions of the window 
    window.config(background="white")       # Set the background color of the window to white
    window.title("Recognition App - Owner")         # Set the title of the window to "Recognition App - Owner"
    create_Frame_date(window,70,443)
    date_time_owner(window)
    import os
    import time

    # Checking if the Visitor.py is executed or not
    while not os.path.exists('py1_executed.marker'):
        # Code to execute in py2 until py1.py is executed
        print("Waiting for Visitor.py to be executed...")
 
        time.sleep(1)  # Delay for 1 second

  
    # Code to execute after py1.py is executed
    print("Visitor.py has been executed!")
    # Add any other code you want to execute after py1.py is executed

    # to execute the client code imported from recognition2 where the Owner receive the webcam feed and wether the password is correct or not from the Visitor
    thread_client=threading.Thread(target=Client,args=(window,18,100))
    thread_client.start()
    window.mainloop()

    #thread_client.join()


#Main
create_window_owner()


