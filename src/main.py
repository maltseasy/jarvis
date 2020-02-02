# libs
import speech_recognition as sr
import subprocess as s
import os
import fnmatch

# dependencies
from rake_nltk import Rake
from win10toast import ToastNotifier
from sys import platform

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
            r.adjust_for_ambient_noise(source)
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
                        for k_word in keywords:
                            if k_word == "time":
                                print("The time right now is 11:43 pm")
                            elif k_word == "open":
                                # file search
                                s.call("D:\\osu\\osu!.exe")
                            elif k_word == "remind":
                                if platform == "linux" or platform == "linux2" or platform == "darwin":
                                    s.call(
                                        ["notify-send", "INSERT_MSG_HERE"])
                                elif platform == "win32":
                                    toaster = ToastNotifier()
                                    toaster.show_toast(
                                        "This is your reminder to: ", duration=10)
                                    while toaster.notification_active():
                                        time.sleep(0.1)
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
