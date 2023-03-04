import os, subprocess, datetime, time
import pygame
import speech_recognition as sr
import re

'''
Check if string contains time value in it and return string of it if it does.
'''
def contains_time(in_str):
    if len(in_str) == 0:
        return False
    to_check = in_str.split()
    out_time = "-1"
    for i in range(len(to_check)):
        if ":" in to_check[i]:
            out_time = to_check[i]
    return out_time

'''
Check for string having words in a list of other words.
'''
def contains_word(in_str, words):
    if len(in_str) == 0:
        return False
    to_check = in_str.split()
    for w in to_check:
        if w in words:
            return True
    return False

'''
Check if String has only one digit.
'''
def contains_digit(in_str):
    if len(in_str) == 0:
        return False
    i = 0
    for c in in_str:
        if c.isdigit():
            return (True, i)
        i += 1
    return (False, -1)

'''
Checks if 'Hey SNAuR' exists in string
'''
alaurm_call = ["hey snore", "hey snaur", "hey snawr", "hey snort", "hey nor", "hey naur", "hey no", "hey snow",
               "he snore", "he snaur", "he snawr", "he snort", "he nor", "he naur", "he no", "he snow"]
def contains_snaur(in_str):
    if len(in_str) == 0:
        return False
    to_check = in_str.split()
    for i in range(len(to_check) - 1):
        to_to_check = to_check[i] + " " + to_check[i + 1]
        if to_to_check in alaurm_call:
            return True
    return False

'''
Alarm clock function.
0 = AM
1 = PM
'''
alarm_file = ""
def alarm_clock(in_time, type):
    pygame.init()
    pygame.mixer.init()
    now = datetime.datetime.now()
    s = (now.hour * 3600) + (now.minute * 60) + now.second
    in_time = in_time.split(":")
    new_time = [int(in_time[0]), int(in_time[1])]
    if type == 1:
        new_time[0] += 12
    a = (new_time[0] * 3600) + (new_time[1] * 60)
    ring_in = (a - s) if (a - s < 84600) else (s - a + 84600)
    for i in range(ring_in):
        time.sleep(1)
    alarm = pygame.mixer.Sound("StarWars3.wav")
    alarm.play()
    while pygame.mixer.get_busy():
        pygame.time.delay(100)
    return -1

'''
0 = White noise
1 = Song
2 = Story
'''
def sound_player(option):
    return -1

'''
Main speech recognition function.
'''
conf_threshold = 0.9
alarm = ["alarm", "wake me up", "go off at", "set an alarm"]
morning = ["a.m.", "am", "a.m", "in the morning", "tomorrow morning", ":"]
night = ["p.m.", "pm", "p.m", "in the evening", "tonight", ":"]

r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, show_all = True, language = "en-US")
            if len(text) == 0:
                continue
            confidence = text["alternative"][0]["confidence"]
            in_text = text["alternative"][0]["transcript"]
            if confidence < conf_threshold:
                print("Try again!")
                continue
            if contains_snaur(in_text):
                if contains_word(in_text, alarm) == True:
                    if contains_word(in_text, morning) == True:
                        alarm_time = contains_time(in_text)
                        alarm_clock(alarm_time, 0)
                        break
                    elif contains_word(in_text, night) == True:
                        alarm_time = contains_time(in_text)
                        alarm_clock(alarm_time, 1)
                        break
            else:
                print("I don't understand that format, could you say that again?")
                continue
        except sr.UnknownValueError:
            print("Could you repeat that?")
            pass
        except sr.RequestError as e:
            print("Sorry, could not request results from Google Speech Recognition service; {0}".format(e))
            pass