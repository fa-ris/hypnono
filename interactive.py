import os, subprocess, datetime
import pygame
import speech_recognition as sr
import re

'''
Check if string contains time value in it.
'''
def contains_time(in_str):
    print("---------")
    print(in_str)
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
def alarm_clock(time, type):
    time = time.split(":")
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
            print(in_text)
            if confidence < conf_threshold:
                continue
            if contains_snaur(in_text):
                if contains_word(in_text, alarm) == True:
                    if contains_word(in_text, morning) == True:
                        print("Setting alarm for the morning")
                        alarm_time = contains_time(in_text)
                        alarm_clock(alarm_time, 0)
                        break
                    elif contains_word(in_text, night) == True:
                        print("Setting alarm for the evening")
                        alarm_time = contains_time(in_text)
                        alarm_clock(alarm_time, 1)
                        break
            else:
                continue
        except sr.UnknownValueError:
            print("Could you repeat that?")
            pass
        except sr.RequestError as e:
            print("Sorry, could not request results from Google Speech Recognition service; {0}".format(e))
            pass