import face_recognition
import cv2
import os
import datetime
import pyttsx3
import speech_recognition as sr
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,timeout=3,phrase_time_limit=5)

    try:
        print("Recognising")
        query = r.recognize_google(audio,language = 'en-in')
        

    except Exception as e:
        
        print("pls say again")
        return "None"
    
    return query

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)

cred = credentials.Certificate("facialattendance-e144f-firebase-adminsdk-w0m7n-78c1b87e16.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

count = 0
files = os.listdir("Faces")
for i in files:
    i = "Faces/" + i
    files[count] = i
    count += 1

cap = cv2.VideoCapture(0)
j = 0
state = False
while(cap.isOpened()):
    testimg = face_recognition.load_image_file(files[j]) #iterate overall
    testimg = cv2.cvtColor(testimg,cv2.COLOR_BGR2RGB)
    testencodings = face_recognition.face_encodings(testimg)[0]
    _,img = cap.read()
    img = cv2.resize(img,(0,0),None,0.25,0.25)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    imgencodings = face_recognition.face_encodings(img)
    facecount = 0
    for i in imgencodings:
        facecount = facecount+1
    if(facecount == 1):
        if(face_recognition.face_distance(testencodings,imgencodings) < 0.5):
          name = str(files[j])
          name = name.replace('.jpg','')
          name = name.replace('Faces/','')
          now = str(datetime.datetime.now())
          doc_ref = db.collection("users").document(name)
          doc_ref.set({"entry":now})
          cv2.putText(img,'DONE',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1,cv2.LINE_AA)
          state = True
        else:
            state = False

          
    cv2.imshow('img',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    j = j+1
    
    if(j == count) & (state == False) & (facecount == 1):
        #print("unknown")
        speak("you are unknown to the system!")
        speak("please tell your name")
        query = takeCommand().lower()
        if(query == "None"):
            break
        print(query)
        files.append(query +".jpg")
        cv2.imwrite("Faces/" + query + ".jpg",img)
        files[j] = "Faces/" + files[j]
        print(files)
        count = count + 1
        j = j+1
    
    #print(j)
    #print(state)

    if(j == count):
        j = 0
    
    
    

cap.release()
cv2.destroyAllWindows()