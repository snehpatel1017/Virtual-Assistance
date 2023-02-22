import random
import json
import numpy as np
import pickle
import speech_recognition
import pyttsx3 as tts
import sys
import time
import webbrowser

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
