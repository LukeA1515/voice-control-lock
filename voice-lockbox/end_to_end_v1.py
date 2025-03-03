import speech_recognition as sr
import time
import json

WIT_AI_KEY = ""  # Wit.ai keys are 32-character uppercase alphanumeric strings

task = input("What would you like to do: ")

if task == "register":
    name = input("What is your name: ")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        password = r.recognize_wit(audio, key=WIT_AI_KEY)
        print("Wit.ai thinks you said/password " + password)
        with open("data.json", 'r') as f:
            data = json.load(f)

        data[name] = password
        with open("data.json", 'w') as f:
            json.dump(data,f)
            
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))

if task == "open":
    name = input("name: ")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        password = r.recognize_wit(audio, key=WIT_AI_KEY)
        print("Wit.ai thinks you said/password " + password)
        with open('data.json', "r") as json_file:
            data = json.load(json_file)
        print(type(data))
        temp = data[name]
        if password == temp:
            print("ACCESS GRANTEd")
        else:
            print("PASSWORD DENIED")
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))

