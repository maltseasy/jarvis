# libs
import speech_recognition as sr
from subprocess import call
import os
# import fnmatch
from time import strptime
# dependencies
# from rake_nltk import Rake
from sys import platform
r = sr.Recognizer()
m = sr.Microphone()
from datetime import datetime
now = datetime.now()
# print(now.strftime("%I:%M %p"))

recog_list = [
    "yo jarvis",
    "your jarvis",
    "joe jarvis",
    "you jarvis",
    "hey jarvis",
    "ok jarvis",
    "okay jarvis",
    "jarvis"
]
program_list = {"chrome":"google-chrome",
"spotify":"spotify",
"terminal":"nautilus",
"files":"nautilus",
"slack":"slack"}
with m as source:
    r.adjust_for_ambient_noise(source)

commands = ["open"]


# def find_app(extension, path):
#     res = []
#     for root, dirs, files in os.walk(path):
#         for name in files:
#             if fnmatch.fnmatch(name, pattern):
#                 res.append(os.path.join(root, name))
#     return res

remind_list = []
def bkgd_recog():
    while 1:
        now = datetime.now()
        if now.strftime("%I:%M %p") in remind_list:
            call(["notify-send", "Reminder for: {}".format(now.strftime("%I:%M %p"))])
            remind_list.pop(remind_list.index(now.strftime("%I:%M %p")))
        with m as source:
            # print("-")
            audio = r.listen(source)
            # print("-")

        try:
            wordseq = r.recognize_google(audio)
            if any(s in wordseq.lower() for s in recog_list):
                call(["notify-send", "JARVIS IS LISTENING"])
                with sr.Microphone() as source:
                    # print("-")
                    audio = r.listen(source)
                    # print("-")
                wordseq = r.recognize_google(audio)
                send_string = "You said: " + wordseq
                call(["notify-send", send_string])
                wordseq_tokens = [w.lower() for w in wordseq.split()]
                # try:
                wordseq_tokens = wordseq.lower().split()
                print(wordseq_tokens)

                # build sentiment analysis here
                # rake = Rake()
                # rake.extract_keywords_from_text(wordseq)

                # keywords = rake.get_ranked_phrases()
                # keywords = keywords[0].split()
                # print(keywords)
                # analyze sentiment and execute
                for k_word in wordseq_tokens:
                    if k_word == "time":
                        call(["notify-send", str(datetime.now())])
                    elif k_word == "open":
                        program = wordseq_tokens[wordseq_tokens.index(k_word)+1]
                        print(program)
                        if program in program_list:
                            os.system(program_list[program])
                    elif k_word == "remind":
                        for k_word_sub in wordseq_tokens:
                            try:
                                strptime(k_word_sub, '%H:%M')
                                # print("yerr")
                                time_remind = k_word_sub
                                
                            except ValueError:
                                if k_word_sub == "a.m." or k_word_sub == "p.m.":
                                    ampm = k_word_sub
                                    ampm = ampm.replace(".","")
                                    ampm = ampm.upper()
                                    # print(time_remind)
                                    # print(time_remind.split(':'))
                                    p1 = time_remind.split(':')
                                    if len(p1[0]) == 1:
                                        time_remind = "0"+time_remind
                                    time_remind = time_remind+" "+ampm

                                    remind_list.append(time_remind)
                        
                        
                # except:
                #     print("Error occurred in obtaining the tokens")
            else:
                # print("jarvis aint activated")
                # print(wordseq)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
     
if __name__ == '__main__':
    bkgd_recog()