import Testing_model as tm
import speech_recognition
import pyttsx3 as tts
import sys
import time
import webbrowser
import datetime
import numpy as np


recongnizer = speech_recognition.Recognizer()
speaker = tts.init('sapi5')
voices = speaker.getProperty('voices')
rate = speaker.getProperty('rate')
speaker.setProperty('voice', voices[1].id)
speaker.setProperty('rate', 140)
capablities = ["I can assist you in your daily small work like i can notify you about current time, make files for you , open up some sites like youtube for you excetra. i can only do some small amout of task since i am train on only small data set"]
identity = ["My name is veronika , i am a virtual assistance made by my owner sneh patel",
            "I am Veronika a virtual assistance to assist you in your work , My owner sneh patel created me"]


def speak(text):
    speaker.say(text)
    speaker.runAndWait()


def takecommand():

    recongnizer = speech_recognition.Recognizer()

    done = False
    while not done:
        with speech_recognition.Microphone() as mic:
            print("Listening...")
            audio = recongnizer.listen(mic)
            print('Recognizing....')
            try:
                statement = recongnizer.recognize_google(
                    audio, language='en-in')
                print(f"user said:{statement}\n")
                return statement
            except Exception as e:
                speak("Pardon me, please say that again")


def getfilename(note):
    global recongnizer

    speak("What file name do you want to give it")

    filename = takecommand()
    filename.lower()
    with open(filename, "w") as file:
        file.write(note)
    str = 'I have successfully created the {} file'.format(
        filename)
    speak(str)


def make_file():
    global recongnizer

    speak('What do you want to write on to your note')

    note = takecommand()
    note.lower()
    print('calling function')
    getfilename(note)


def greeting():
    speak('Hello how can i help you')


def quit():
    speak("good bye")
    sys.exit(0)


def identify():
    i = np.random.randint(0, len(identity)-1)
    speak(identity[i])


def capablity():
    # i = np.random.randint(0, len(capablities)-1)
    speak(capablities[0])


todolist = []


def add_todo():
    global recongnizer

    speaker.say('What do you want to add')
    speaker.runAndWait()
    item = takecommand()
    item.lower()
    todolist.append(item)
    str = item + 'successfully added into todo list'
    speaker.say(str)


def show_todo():
    if len(todolist) == 0:
        speak("You have nothing in your to do list")
        return

    speaker.say("Your todo list items are")
    for item in todolist:
        speaker.say(item)
    speaker.runAndWait()


def open_youtube():
    webbrowser.open_new_tab("https://www.youtube.com")
    speak("youtube is open now")
    time.sleep(5)


def current_time():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"the time is {strTime}")


mapping = {"greetings": greeting, "quit": quit, "make_file": make_file,
           "add_todo": add_todo, "show_todo": show_todo, "open_you_tube": open_youtube,
           "current_time": current_time,
           "identity": identify,
           "capability": capablity}

while True:

    question = takecommand()
    question.lower()
    tag = tm.predict(question)
    if tag == '-1':
        str = "sorry it may seen that what you have ask is not in my data set so i didn't know above it , i am a small assistance,  i am only capable of doing small task , since i am not trained on laege dataset"
        speak(str)
    print(tag)
    mapping[tag]()
