import random
import json
import numpy as np
import pickle
import speech_recognition
import pyttsx3 as tts


import nltk


from datetime import datetime


from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

lemitizer = WordNetLemmatizer()

words = pickle.load(open('word.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')
intents = json.loads(open('data.JSON').read())


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemitizer.lemmatize(w.lower()) for w in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = []
    for w in words:
        if w in sentence_words:
            bag.append(1)
        else:
            bag.append(0)
    return np.array(bag)


def predict(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]), verbose=0)[0]
    result = [[i, r] for i, r in enumerate(res) if r >= 0.9]
    if (len(result) > 0):
        result.sort(key=lambda x: x[1], reverse=True)
        tag = classes[result[0][0]]
        return tag
    else:
        return "-1"


recongnizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)


def getfilename(note):
    global recongnizer

    speaker.say('What file name do you want to give it')
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                print('enter the file name')
                recongnizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recongnizer.listen(mic)
                print("listed well")
                filename = recongnizer.recognize_google(audio)
                filename.lower()
                with open(filename, "w") as file:
                    file.write(note)
                str = 'I have successfully created the {} file'.format(
                    filename)
                speaker.say(str)
                speaker.runAndWait()
                done = True
        except speech_recognition.UnknownValueError:
            speaker.say("I don't  understande what you have said try again")
            speaker.runAndWait()
            recongnizer = speech_recognition.Recognizer()


def create_note():
    global recongnizer

    speaker.say('What do you want to write on to your note')
    speaker.runAndWait()

    done = False

    while not done:

        try:
            with speech_recognition.Microphone() as mic:
                print('enter the note')
                recongnizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recongnizer.listen(mic)
                print('listed well')
                note = recongnizer.recognize_google(audio)
                note.lower()
                print('calling function')
                getfilename(note)
                done = True
        except speech_recognition.UnknownValueError:
            recongnizer = speech_recognition.Recognizer()
            speaker.say(
                "I don't understand what you have said please try again")
            speaker.runAndWait()


def greeting():
    speaker.say('Hello how can i help you')
    speaker.runAndWait()


def quit():
    speaker.say("Good Bye")
    speaker.runAndWait()


todolist = ['shopping']


def add_todo():
    global recongnizer

    speaker.say('What do you want to add')
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recongnizer.adjust_for_ambient_noise(mic, 0.2)
                audio = recongnizer.listen(mic)

                item = recongnizer.recognize_google(audio)

                todolist.append(item)
                str = item + 'successfully added into todo list'
                speaker.say(str)
                done = True
        except speech_recognition.UnknownValueError:
            recongnizer = speech_recognition.Recognizer()
            speaker.say(
                "I don't understand what you have said please try again")
            speaker.runAndWait()


def show_todo():
    speaker.say("Your todo list items are")
    for item in todolist:
        speaker.say(item)
    speaker.runAndWait()


print('ready')

while True:
    try:
        with speech_recognition.Microphone() as mic:
            print("speak---")
            recongnizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recongnizer.listen(mic)
            print('listened')
            question = recongnizer.recognize_google(audio)
            print('converted')
            tag = predict(question)
            print(tag)
            if tag == 'quit':
                quit()
                break

            if tag == 'create_note':
                create_note()

            if tag == 'greetings':
                greeting()
            if tag == 'add_todo':
                add_todo()
            if tag == 'show_todo':
                show_todo()
    except speech_recognition.UnknownValueError:
        recongnizer = speech_recognition.Recognizer()
