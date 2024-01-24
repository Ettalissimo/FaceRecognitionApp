






########################################################################################################""""

########################################################################################################""""

########################################################################################################""""

########################################################################################################""""
import struct,imutils
import socket
import face_recognition as fr
import pickle
import tkinter as tk
import cv2
from PIL import ImageTk, Image
import threading
import time
from tkinter import ttk
import queue
import recognition2
import numpy as np

def display_webcam(window, x, y):
 
    # Function to continuously read frames from the webcam
    def execution_recognition2():
        recognition2.prog_after(window,x,y)

    thread = threading.Thread(target=execution_recognition2)
    thread.start()


def create_window_visitor():
    from recognition2 import prog
    isRecognized_val = False

    def command_display_message(b_value):
        if b_value:        
            message_label.config(text="Face recognised!")
        else:       
            message_label.config(text="Face not recognised!")
            #code that sends warnings to the owner
     
        # Function to continuously read frames from the webcam

    #create a Start Button 
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
            #code that sends warnings to the owner

    def tab1():
            global button_next_2
            def tab2():
                message_label.destroy()
                startButton.destroy()
                password_section(window)

            button_next_2 = tk.Button(window,text="NEXT",font=("Arial",15),bg="black",fg="white",command=tab2)
            button_next_2.pack(side='bottom')
            button_next_2.config(state="disabled")

    def execution_recognition2():
            global isRecognized_val     
            #window.after(0, prog, window, x, y)
            isRecognized_val = recognition2.prog(window,x,y)

            isRecognized_val = recognition2.isRecognized_val

            return isRecognized_val 

    window = tk.Tk()
    window.geometry("443x650")
    window.config(background="white")

    x=15
    y=100

    #create Start button (it executes the command_start function)
    startButton = tk.Button(window,text="START",command=lambda :command_start(isRecognized_val))
    startButton.place(x=200, y=450)

        
    message_label = tk.Label(window,font=("Arial",15),bg="black",fg="white", text="")
    message_label.place(x=138,y=550)


    frame1 = tk.Frame(window, height=70, width=443, bg="black",bd=1, relief="flat")
    frame1.place(x=0,y=0)





    #create_Frame_date(window,70,443)
    date_time_vis(window)
    tab1()
    isRecognized_val = execution_recognition2() 
    display_webcam(window,15,100)
    window.mainloop()





def create_window_owner():
    def on_resize(event):
    # Retrieve the new size of the window
        new_width = event.width
        new_height = event.height

    # Update any elements or perform actions based on the new size

    # Create a Tkinter window
    window = tk.Tk()

    # Set the title of the window
    window.title("Resizable Window")

    # Configure the window to allow resizing
    window.resizable(True, True)

    # Bind the on_resize function to the window's resize event
    window.bind("<Configure>", on_resize)

    window.update()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = 70
    y = 190
    display_webcam(window,x,y)
    
    ##
    create_Frame_date(window,70,screen_width)
    date_time_owner(window)

    # Start the Tkinter event loop
    window.mainloop()


    # Specify the desired x and y coordinates for the webcam feed label


def password_section(_fen):
    def command_test():
        password = entry.get()
        b_val = True
        i=3
        while(b_val and i>0 ):
            contenu=""
            if  (password == "password"):
                #door unlocks
                #send message to owner
                message_label_mdp.config(text=" Welcome!         ")
                b_val = False
            else:
                #send message to owner
                contenu=" Wrong Password!!!\nTry again"
                message_label_mdp.config(text=contenu)
                i-=1
                if (i>0):
                    try_again_button= tk.Button(_fen,text="try again",command=try_again)
                    try_again_button.place(x=318,y=455)        
    
    def try_again():
        message_label_mdp.destroy()
        password_section(_fen)

    entry=tk.Entry(_fen,font=("Arial",20),bg="black",fg="white",show="*")
    entry.place(x=70,y=450)

    submit_button= tk.Button(_fen,text="submit",command=command_test)
    submit_button.place(x=197,y=500)

    message_label_mdp = tk.Label(_fen,font=("Arial",13),bg="black",fg="white", text="")
    message_label_mdp.place(x=138,y=535)

def date_time_owner(fen_):
    def update_():
        timeString = time.strftime("%I:%M:%S %p")
        timeLabel.config(text=timeString)

        dateString = time.strftime("%B%d,%Y")
        dateLabel.config(text=dateString)
 
        dayString = time.strftime("%A")
        dayLabel.config(text=dayString)
        fen_.after(1000,update_)

    fen_.update()
    window_width = fen_.winfo_width()
    window_height = fen_.winfo_height()
    screen_width = fen_.winfo_screenwidth()
    screen_height = fen_.winfo_screenheight()

    timeLabel = tk.Label(fen_,font=("Arial",15),bg="black",fg="white")
    timeLabel.place(x=screen_width-170 ,y=14)

    dateLabel = tk.Label(fen_,font=("Arial",12),bg="black",fg="white")
    x_val=(screen_width//2)-40
    dateLabel.place(x=x_val ,y=30)

    dayLabel = tk.Label(fen_,font=("Arial",12),bg="black",fg="white")
    dayLabel.place(x=x_val ,y=8)

    update_()


def date_time_vis(fen_):
    def update_():
        timeString = time.strftime("%I:%M:%S %p")
        timeLabel.config(text=timeString)

        dateString = time.strftime("%B%d,%Y")
        dateLabel.config(text=dateString)
 
        dayString = time.strftime("%A")
        dayLabel.config(text=dayString)
        fen_.after(1000,update_)

    timeLabel = tk.Label(fen_,font=("Arial",15),bg="black",fg="white")
    timeLabel.place(x=320,y=14)

    dateLabel = tk.Label(fen_,font=("Arial",12),bg="black",fg="white")
    dateLabel.place(x=150,y=30)

    dayLabel = tk.Label(fen_,font=("Arial",12),bg="black",fg="white")
    dayLabel.place(x=159,y=8)

    update_()

def create_Frame_date(fenetre,height_val,width_val):
    frame1 = tk.Frame(fenetre, height=height_val, width=width_val, bg="black",bd=1, relief="flat")
    frame1.place(x=0,y=0)

def display_message(fent,b_value):
    def command_display_message(b_value):
        if b_value:        
            message_label.config(text="Face recognised!")
        else:       
            message_label.config(text="Face not recognised!")
            #code that sends warnings to the owner

    button = tk.Button(fent, text="display message", command=command_display_message)
    button.place(x=170,y=500)

    message_label = tk.Label(fent,font=("Arial",15),bg="black",fg="white", text="")
    message_label.place(x=143,y=600)

def Start_Button(fen):
        def command_start():
            # recognition phase!!!!!!
            print("start!")
            startButton.config(state="disabled")
            #waiting for yaya code
            b_value=False
            command_display_message(b_value)

        def command_display_message(b_value):
            if b_value:        
                message_label.config(text="Face recognised!")
            else:       
                message_label.config(text="Face not recognised!")
                #code that sends warnings to the owner


        startButton = tk.Button(fen,text="START",command=command_start)
        startButton.place(x=200, y=450)

        message_label = tk.Label(fen,font=("Arial",15),bg="black",fg="white", text="")
        message_label.place(x=143,y=600)




#MAIN
create_window_visitor()
#test
#password_section(wind)
#create_window_owner()
# Function to continuously read frames from the webcam

def read_frames(video_label,cap):

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize the frame to fit the window
            frame_resized = cv2.resize(frame_rgb, (400, 300))

            # Convert the frame to ImageTk format
            img = Image.fromarray(frame_resized)
            img_tk = ImageTk.PhotoImage(image=img)

            # Update the image in the Tkinter label
            video_label.config(image=img_tk)
            video_label.image = img_tk

def prog_after(window,x,y):
    #import name, ids, encodings and ids
    f = open("ref_name.pkl", "rb")
    ref_dict = pickle.load(f)
    f.close()

    f = open("ref_embed.pkl", "rb")
    embed_dict = pickle.load(f)
    f.close()

    known_face_ids = []
    known_face_encodings = []

    for ref_id, embed_list in embed_dict.items():
        for my_embed in embed_list:
            known_face_encodings += [my_embed]
            known_face_ids += [ref_id]
        global video_label    

    face_locations = []
    face_encodings = []
    face_ids = []
    process_this_frame = True

    #start webcam
    cap = cv2.VideoCapture(0)

    # Create a label to display the video feed
    video_label = tk.Label(window)
    video_label.place(x=x, y=y)  # Use place method to position the label


    i=0
    while True:
        ret, frame = cap.read()
        if not ret:
                break

        # Convert the frame to RGB format
        # Resize the frame to fit the window
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame  = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        if process_this_frame:
            face_locations = fr.face_locations(rgb_small_frame)
            face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

            face_ids = []

            for face_encoding in face_encodings:
                matches = fr.compare_faces(known_face_encodings, face_encoding)
                id = "Unknown"

                face_distances = fr.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)


                if matches[best_match_index]:
                    id = known_face_ids[best_match_index]
                    face_ids.append(id)



        process_this_frame = not process_this_frame

        for (top_s, right, bottom, left), f_id in zip(face_locations, face_ids):
            top_s *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top_s), (right, bottom), (0, 255, 0), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, ref_dict[f_id], (left+6, bottom-6), font, 1.0, (255, 255, 255), 1)

        font = cv2.FONT_HERSHEY_DUPLEX
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize the frame to fit the window
        frame_resized = cv2.resize(frame_rgb, (400, 300))
        
        #cv2.imshow("Video", frame)

        # Convert the frame to ImageTk format
        img = Image.fromarray(frame_resized)
        img_tk = ImageTk.PhotoImage(image=img)

        # Update the image in the Tkinter label
        video_label.config(image=img_tk)
        video_label.image = img_tk

        if cv2.waitKey(1) & 0xFF == ord('q'): break

    
    cap.release()
    cv2.destroyAllWindows()

def Server():
    # Socket Create
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('HOST IP:', host_ip)
    port = 9999
    socket_address = (host_ip, port)

    # Socket Bind
    server_socket.bind(socket_address)

    # Socket Listen
    server_socket.listen(5)
    print("LISTENING AT:", socket_address)

    # Socket Accept
    while True:
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)
        if client_socket:
            vid = cv2.VideoCapture(0)
            if not vid.isOpened():
                print("Failed to open the camera.")
                break

            while vid.isOpened():
                # Video Capture
                _, frame = vid.read()
                frame = imutils.resize(frame, width=320)

                # Serialization
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)

                # Display Frame
                cv2.imshow('TRANSMITTING VIDEO', frame)
                cv2.waitKey(1)  # Update display window

                # Control and Exit
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()
                    break

    server_socket.close()