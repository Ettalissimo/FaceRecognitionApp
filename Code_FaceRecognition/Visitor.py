
import tkinter as tk
import threading, time, recognition2, winsound
import socket

# To send to the Owner whether the password is wrong or not
def send_password_state(message):
    PORT = 12345
    # iP adress of the host (Visitor)
    host_ip='192.168.56.1'
    #   To send a message
    def send_message(message):
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # Connect to the Owner 
            s.connect((host_ip, PORT))

            # Send the message
            s.sendall(message.encode())

    thread_msg = threading.Thread(target=send_message,args=(message,))
    thread_msg.start()

def password_section(_fen):
    def command_test():
        global isPasswordCorrect
        password = entry.get()          # Get the value entered in the 'entry' widget and store it in the 'password' variable
        isPasswordCorrect = (password == "password")    

        # If the password is correct:
        if  isPasswordCorrect :
                # door unlocks
                # send message to owner
                send_password_state("1")
                # Update the message in the Visitor GUI 
                message_label_mdp.config(text=" Welcome! The Door\n is Open")
                submit_button.config(state="disabled")          # Disable the submit button to prevent further input

        # If the password is incorrect:
        else:
                #send message to owner
                send_password_state("0")
                message_label_mdp.config(text=" Wrong Password!!!")

                # Alarm
                winsound.PlaySound("Alarm_Sound_Effect",winsound.SND_FILENAME)      

    # Creates an entry widget for user input, with a black background, white text, and obscured characters (*).
    entry=tk.Entry(_fen,font=("Arial",20),bg="black",fg="white",show="*")
    entry.place(x=70,y=430)

    # Creates a button widget labeled "SUBMIT" with specified font, size, and color, and associates it with a command called "command_test".
    submit_button= tk.Button(_fen,text="SUBMIT",font=("Arial",13), width=10, height=2,bg="black",fg="white",command=command_test)
    submit_button.place(x=173,y=490)

    # Creates a label widget for displaying a message, with specified font, background color, text color, and an empty initial text.
    message_label_mdp = tk.Label(_fen,font=("Arial",13),bg="white",fg="black", text="")
    message_label_mdp.place(x=138,y=555)

# to display the day date time 
def date_time_vis(fen_):
    def update_():
        # Get the current time and format it as HH:MM:SS
        timeString = time.strftime("%I:%M:%S")
        timeLabel.config(text=timeString)  # Update the text of the timeLabel widget with the current time

        # Get the current date and format it as Month DD, YYYY
        dateString = time.strftime("%B %d, %Y")
        dateLabel.config(text=dateString)  # Update the text of the dateLabel widget with the current date

        # Get the current day of the week
        dayString = time.strftime("%A")
        dayLabel.config(text=dayString)  # Update the text of the dayLabel widget with the current day of the week

        fen_.after(1000, update_)  # Schedule the next update after 1000 milliseconds (1 second)

    # Create a label widget to display the time
    timeLabel = tk.Label(fen_, font=("Arial", 15), bg="black", fg="white")
    timeLabel.place(x=350, y=15)

    # Create a label widget to display the date
    dateLabel = tk.Label(fen_, font=("Arial", 12), bg="black", fg="white")
    dateLabel.place(x=165, y=30)

    # Create a label widget to display the day of the week
    dayLabel = tk.Label(fen_, font=("Arial", 12), bg="black", fg="white")
    dayLabel.place(x=181, y=8)

    update_()  # Call the update function to start displaying the current time, date, and day

# the main function where we create the main window
def create_window_visitor():
    isRecognized_val = False

    window = tk.Tk()# Create the main window for the GUI

    window.geometry("443x650")  # Set the dimensions of the window 
    window.config(background="white")   # Set the background color of the window to white
    window.title("Recognition App - Visitor")     # Set the title of the window to "Recognition App - Visitor"

    x=18
    y=100

    def window_components():
        global startButton

        # Function called when the "START" button is clicked
        def command_start(isRecognized_val):
            print("start!")
            startButton.config(state="disabled")

            print(isRecognized_val)

            b_value = isRecognized_val
            if b_value:        
                message_label.config(text="Face recognised!")
                button_next_2.config(state="active")
            else:       
                message_label.config(text="Face not recognised!")

        # Function for the first tab of the interface
        def tab1():
            global button_next_2

            # Function called when the "NEXT" button is clicked
            def tab2():
                message_label.destroy()
                startButton.destroy()
                password_section(window)

            #create next button (it executes the tab2 function)
            button_next_2 = tk.Button(window,text="NEXT",font=("Arial",15),bg="black",fg="white",command=tab2)
            button_next_2.place(x=190,y=600)            
            button_next_2.config(state="disabled")
       
        #create Start button (it executes the command_start function)
        startButton = tk.Button(window,font=("Arial",13),text="START", width=10, height=2,bg="black",fg="white",command=lambda :command_start(isRecognized_val))
        startButton.place(x=175, y=450)
        

        message_label = tk.Label(window,font=("Arial",15),bg="white",fg="black", text="")
        message_label.place(x=138,y=530)

        # create a Frame where we display the date, time and day
        frame1 = tk.Frame(window, height=70, width=443, bg="black",bd=1, relief="flat")
        frame1.place(x=0,y=0)

        date_time_vis(window)        # Display the date, time and day in the GUI
        tab1()      # Set up the first tab of the interface

    # execution of theface recognition code imported from the recognition2 file
    def execution_recognition2():
            nonlocal isRecognized_val  
            isRecognized_val = recognition2.prog(window,x,y)
            return isRecognized_val 
        
    window.after(0,window_components)
    window.after(100,execution_recognition2)

    # to execute the Server code imported from recognition2 where the Visitor send the webcam feed to the Owner
    thread_server=threading.Thread(target=recognition2.Server,args=(window,x,y)) 
    thread_server.start()

    window.mainloop()

    thread_server.join()


#MAIN

# Create a marker file to indicate that Visitor.py has been executed
with open('py1_executed.marker', 'w') as marker_file:
    marker_file.write('Executed')

create_window_visitor()







