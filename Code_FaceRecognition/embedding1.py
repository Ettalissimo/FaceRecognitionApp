import sys
import cv2
import face_recognition as fr
import pickle

print("Add a new user : ")
name = input("Enter your name : ")
ref_id = input("Enter your id : ")

try:
    f = open("ref_name.pkl", "rb")
    ref_dict = pickle.load(f)
    f.close()
except:
    ref_dict = {}

ref_dict[ref_id] = name

f = open("ref_name.pkl", "wb")
pickle.dump(ref_dict, f)
f.close()

try:
    f = open("ref_embed.pkl", "rb")
    embed_dict = pickle.load(f)
    f.close()
except:
    embed_dict = {}

for i in range(5):
    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    while True:
        check, frame = webcam.read()

        cv2.imshow("Capturing ...", frame)

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        #rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        key = cv2.waitKey(1)

        if key==ord('s'):
            face_locations = fr.face_locations(rgb_small_frame)

            if face_locations!=[]:
                face_encoding = fr.face_encodings(frame)[0]
                if ref_id in embed_dict:
                    embed_dict[ref_id] += [face_encoding]
                else:
                    embed_dict[ref_id] = [face_encoding]
                
                webcam.release()
                cv2.waitKey(1)
                cv2.destroyAllWindows()
                break
        elif key==ord('q'):
            print("Turning off camera ...")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

f = open("ref_embed.pkl", "wb")
pickle.dump(embed_dict, f)
f.close()