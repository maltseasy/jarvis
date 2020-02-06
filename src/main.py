# libs
import speech_recognition as sr
import subprocess as s
import os
import fnmatch
from datetime import datetime 
import webbrowser

# dependencies
from rake_nltk import Rake
from win10toast import ToastNotifier
from sys import platform
import spotipy
from spotipy.oauth2 import SpotifyClientCredientials 

r = sr.Recognizer()
recog_list = [
    "yo jarvis",
    "your jarvis",
    "joe jarvis",
    "you jarvis",
    "hey jarvis",
    "ok jarvis",
    "okay jarvis"
]

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
              'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']

commands = ["open"]


def find_app(extension, path):
    res = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                res.append(os.path.join(root, name))
    return res


def mic_test():
    while 1:
        with sr.Microphone() as source:
            print("-")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            print("-")

        try:
            wordseq = r.recognize_google(audio)
            if any(s in wordseq.lower() for s in recog_list):
                print("JARVIS ACTIVATED")
                with sr.Microphone() as source:
                    print("-")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    print("-")
                    wordseq = r.recognize_google(audio)
                    print(wordseq)

                    try:
                        wordseq_tokens = wordseq.lower().split()
                        print(wordseq_tokens)

                        # build sentiment analysis here
                        rake = Rake()
                        rake.extract_keywords_from_text(wordseq)

                        keywords = rake.get_ranked_phrases()
                        print(keywords)

                        # analyze sentiment and execute
                        if "time" in keywords:
                            print("The time right now is %s" % datetime.now().strftime("%H:%M"))
                        elif "open" in keywords:
                            # file search
                            """
                                Assuming extraction contains 2 words
                                ex. ["open", "PROGRAM_TO_OPEN"] 
                            """
                            reg_ex = r.search("open (.+)", wordseq)
                            if reg_ex:
                                domain = reg_ex.group(1)
                                url = "https://www." + domain + ".com"
                                webbrowser.open(url)
                                print("Website has been loaded")
                            else:
                                pass
                        elif "remind" in keywords:
                            if platform == "linux" or platform == "linux2" or platform == "darwin":
                                s.call(
                                    ["notify-send", wordseq])
                            elif platform == "win32":
                                toaster = ToastNotifier()
                                toaster.show_toast(
                                    "This is your reminder to: ", duration=10)
                                while toaster.notification_active():
                                    time.sleep(0.1)
                        elif "launch" in keywords:
                            reg_ex = r.search("launch (.+)", wordseq)
                            if reg_ex:
                                app = reg_ex.group(1)
                                app_ext = app+".app"
                                s.Popen(["open", "-n", "/Applications/" + app_ext], stdout=s.PIPE)
                                print("Desktop application launched")
                        elif "play" in keywords:

                    except:
                        print("Error occurred in obtaining the tokens")
            else:
                print("Please activate Jarvis")

        except sr.UnknownValueError:
            print("Jarvis deactivated, please call on it to reactive it")

        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))


if __name__ == '__main__':
    mic_test()
