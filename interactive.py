import os, time
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: {}".format(text))
            # Check if the user said the trigger phrase
            if "Hey Siri" in text:
                print("Trigger phrase detected!")
                break
        except sr.UnknownValueError:
            print("Sorry, I didn't understand what you said.")
            pass
        except sr.RequestError as e:
            print("Sorry, could not request results from Google Speech Recognition service; {0}".format(e))
            pass