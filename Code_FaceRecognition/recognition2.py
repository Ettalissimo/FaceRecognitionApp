import threading
import cv2
import numpy as np
import pickle
import face_recognition as fr
import tkinter as tk
from PIL import ImageTk, Image
import socket, pickle,struct
import winsound
import os


# Open the file "ref_name.pkl" in binary mode for reading
f = open("ref_name.pkl", "rb")
ref_dict = pickle.load(f)           # Load the pickled data from the file and assign it to the variable ref_dict
f.close()           # Close the file

# Open the file "ref_embed.pkl" in binary mode for reading
f = open("ref_embed.pkl", "rb")
embed_dict = pickle.load(f)
f.close()

# Create empty lists to store face IDs and face encodings
known_face_ids = []
known_face_encodings = []

# Iterate over the items in embed_dict, which contains reference IDs and corresponding embedding lists
for ref_id, embed_list in embed_dict.items():
    # Iterate over the embedding list for each reference ID
    for my_embed in embed_list:
        # Append the embedding to the known_face_encodings list
        known_face_encodings += [my_embed]
        # Append the reference ID to the known_face_ids list
        known_face_ids += [ref_id]

isRecognized_val = False

# Returns wether the face is Recognized or not
def prog(window,x,y):
    global isRecognized_val
    

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
    isRec_list = list()
    
    while True:
        global isRecognized_val
        ret, frame = cap.read()
        if not ret:
                break

        # Resize the frame to fit the window
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the frame to RGB format
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
                    isRecognized_val =True
                    i=i+1
                    isRec_list.append(isRecognized_val)
                    print(isRecognized_val)
                else:
                    i=i+1 
                    isRecognized_val= False


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
        
        key = cv2.waitKey(1)

        if cv2.waitKey(1) & key == ord('q'): break

        if ((True not in isRec_list) and i==10):
            print(False)
            isRecognized_val= False
            return isRecognized_val
        else:
            if isRecognized_val == True :
                cap.release()
                cv2.destroyAllWindows()
                return isRecognized_val                

    cap.release()
    cv2.destroyAllWindows()
    return isRecognized_val

# To send in Real time the webcam feed to the Owner
def Server(window,x,y):
    global video_label

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


    face_locations = []
    face_encodings = []
    face_ids = []
    process_this_frame = True

    #start webcam
    cap = cv2.VideoCapture(0)

    # Create a label to display the video feed
    video_label = tk.Label(window)
    video_label.place(x=x, y=y)  # Use place method to position the label


    # Socket Accept
    while True:
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)
        if client_socket:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Failed to open the camera.")
                break

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                        break

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
                            isRecognized_val = True

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

                # Serialization
                a = pickle.dumps(frame_resized)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)

                # Convert the frame to ImageTk format
                img = Image.fromarray(frame_resized)
                img_tk = ImageTk.PhotoImage(image=img)

                # Update the image in the Tkinter label
                video_label.config(image=img_tk)
                video_label.image = img_tk
                
                
                if cv2.waitKey(1) & 0xFF == ord('q'): break

            cap.release()
            cv2.destroyAllWindows()

# To Receive in Real time the webcam feed from the Visitor
def Client(window,x,y):
 
    # Create a label to display the video feed
    video_label = tk.Label(window)
    video_label.place(x=x, y=y)  # Use place method to position the label
    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '192.168.56.1'  # replace with the actual server IP address
    port = 9999
    client_socket.connect((host_ip, port))  # a tuple

    data = b""
    payload_size = struct.calcsize("Q")


    # This section is related with the file that was created to check if Visitor.py was executed
    # the path of the file want to delete
    file_path = 'py1_executed.marker'

    try:
        # Delete the file
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except OSError as e:
        print(f"Error occurred while deleting file: {e}")


    # Define the address and port to receive the message
    HOST = host_ip
    PORT = 12345

    # Receiving wether the password is correct or not
    def receive_message():
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Bind the socket to the address and port
            s.bind((HOST, PORT))
            # Listen for incoming connections
            s.listen(1)
            # Accept a connection from the sender
            conn, addr = s.accept()
            # Receive the message
            data = conn.recv(1024)

        message_received = data.decode()

        message_label = tk.Label(window,font=("Arial",15),bg="white",fg="black", text="")
        message_label.place(x=138,y=530)

        # "1" :: True and "0" :: False
        if message_received == "1" :
            print("Received message:", message_received)
            message_label.config(text="Password Correct")       # Update the text of message_label to "Password Correct"
        elif message_received=="0" :
            print("Received message:", message_received)
            message_label.config(text="Password not Correct")       # Update the text of message_label to "Password not Correct"
            #ALARM
            winsound.PlaySound("Alarm_Sound_Effect",winsound.SND_FILENAME)      # Play an alarm sound effect


    thread_msg = threading.Thread(target=receive_message)
    thread_msg.start()

    # Receiving the webcam feed 
    while True:
        # Receive and reconstruct the frame data

        # Receive and assemble data packets until the length reaches the expected payload size
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # Receive packets of size 4K (4 * 1024 bytes)
            if not packet:
                break
            data += packet

        # Extract the packed message size from the received data
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        # Receive and assemble data packets until the length reaches the expected message size
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)

        # Extract the frame data from the received data and deserialize it
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

        frame_resized = cv2.resize(frame, (400, 300))

        # Convert the frame to ImageTk format
        img = Image.fromarray(frame_resized)
        img_tk = ImageTk.PhotoImage(image=img)

        # Update the image in the Tkinter label
        video_label.config(image=img_tk)
        video_label.image = img_tk
        cv2.waitKey(1)  # Update the video window

        # Check for termination condition
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    client_socket.close()


	
            
    
    

