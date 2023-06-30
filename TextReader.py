from PyPDF2 import PdfReader
import signal
import pyttsx3
from tkinter import *
from tkinter import filedialog as fd
import speech_recognition as sr
import keyboard

#NUMBER IN FORM OF WORD TO NUMBER IN FORM OF TEXT:
def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

# Initialize text-to-speech engine
TextToSpeech = pyttsx3.init()
TextToSpeech.setProperty("rate", 160)  # Slows down the speed of the reader

# Open file dialog to select PDF
TextToSpeech.say("Welcome to text dictator!")
TextToSpeech.runAndWait()
TextToSpeech.say("Select PDF")
TextToSpeech.runAndWait()

AskPath = Tk()
AskPath.withdraw()
file_path = fd.askopenfilename(
    title="SELECT PDF",
    filetypes=(("PDF files", "*.pdf"),)
    )


# Read the PDF file
reader = PdfReader(file_path)

# Initialize speech recognizer
r = sr.Recognizer()

# Variable initialization
stop = False
dictionary = {}
i = 0
reread = ''
text = ''
lines = ''

# Signal handler to stop the code
def stopTheCode(signal, frame):
    global stop
    stop = True

signal.signal(signal.SIGINT, stopTheCode)

# Function to repeat lines
def repeat():
    global reread
    global stoploop
    stoploop = True
    while stoploop:
        TextToSpeech.setProperty("rate", 160)
        TextToSpeech.say("Which line do you want me to repeat?")
        TextToSpeech.runAndWait()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source)

        try:
            reread = r.recognize_google(audio)
            reread = reread.lower()

            if reread in ['none', 'no', 'stop']:
                print("You said, " + reread)
                stoploop = False
            else:
                TextToSpeech.setProperty("rate", 130)
                readon = 'yes'
                for number, sentence in list(dictionary.items()):
                    if reread.lower() in sentence.lower() and readon == 'yes':

                        try:
                            print("You said, " + reread)
                            TextToSpeech.say("I'll repeat." + "\n" + dictionary[number] + dictionary[number + 1])
                            TextToSpeech.runAndWait()

                            TextToSpeech.say("Do you want me to read further?")
                            TextToSpeech.runAndWait()

                            with sr.Microphone() as source:
                                r.adjust_for_ambient_noise(source)
                                print("Listening...")
                                audio = r.listen(source)

                            readon = r.recognize_google(audio)

                            if readon == "yes":
                                print("You said, yes")
                                TextToSpeech.say("I'll repeat." + "\n" + dictionary[number + 2] + dictionary[number + 3])
                                TextToSpeech.runAndWait()
                                readon = "no"

                            elif readon == "no":
                                print("You said, no")
                                TextToSpeech.say("Ok")
                                TextToSpeech.runAndWait()

                            else:
                                print("You said, " + readon)
                                TextToSpeech.say("Please reply in yes or no")
                                TextToSpeech.runAndWait()

                        except:
                            TextToSpeech.say("I'll repeat." + "\n" + dictionary[number])
                            TextToSpeech.runAndWait()

        except sr.UnknownValueError:
            TextToSpeech.say("Sorry, can you please repeat")
            TextToSpeech.runAndWait()

# Main loop
global readpages
readpages = True
while readpages:
    global gotpage
    gotpage = 'notgot'

    while gotpage == 'notgot':
        TextToSpeech.say("Speak the page number you want me to read")
        TextToSpeech.runAndWait()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source)
            try:
                heard = r.recognize_google(audio)
                try:
                    heard = heard.lower()
                except:
                    pass

                if heard in ['none', 'no', 'stop','nun']:
                    readpages = False
                    print('You said:', heard)
                    break

                else:
                    if heard.lower() in ['tu', 'do']:
                        heard = 2
                        print('You said:', heard)
                    elif heard in ['free', 'tree']:
                        heard = 3
                        print('You said:', heard)
                    else:
                        try:
                            heard = int(heard)
                            print('You said:', heard)
                        except:
                            heard = text2int(heard)
                            print('You said:', heard)
                            
                    page_num = int(heard) - 1
                    if 0 <= page_num < len(reader.pages):
                        page = reader.pages[page_num]
                        text = page.extract_text()
                        gotpage = 'got'

                    else:
                        TextToSpeech.say("Looks like you said a page that does not exist in the PDF.")
                        TextToSpeech.runAndWait()
                        print('You said:', heard)
                        gotpage = 'notgot'

            except sr.UnknownValueError:
                TextToSpeech.say("Sorry, can you please repeat")
                TextToSpeech.runAndWait()


    if readpages:
        TextToSpeech.setProperty("rate", 160)
        TextToSpeech.say("Do you want me to repeat a pair of words twice?")
        TextToSpeech.runAndWait()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source)

        try:
            heard = r.recognize_google(audio)
            if heard == "yes":
                print("You said, yes")
                splitted_words = text.split()
                if len(splitted_words) % 2 == 1:
                    splitted_words.append(' ')
                word_pairs = {}
                p = 0
                list_pairs = []
                for word in splitted_words:
                    p += 1
                    if p % 2 == 1:
                        list_pairs.append(word)
                    else:
                        list_pairs.append(word)
                        word_pairs[p // 2] = list_pairs
                        list_pairs = []

                def repeatwice(dictionary):
                    for number, pair in dictionary.items():
                        TextToSpeech.say(pair[0])
                        TextToSpeech.runAndWait()
                        TextToSpeech.say(pair[1])
                        TextToSpeech.runAndWait()
                        TextToSpeech.say(pair[0])
                        TextToSpeech.runAndWait()
                        TextToSpeech.say(pair[1])
                        TextToSpeech.runAndWait()
                        if stop:
                            break

                TextToSpeech.setProperty("rate", 200)
                repeatwice(word_pairs)

            else:
                print("You said, no")
                lines = text.split("\n")
                for line in lines:
                    TextToSpeech.setProperty("rate", 130)
                    TextToSpeech.say(line)
                    TextToSpeech.runAndWait()
                    if stop:
                        break

            TextToSpeech.setProperty("rate", 160)
            TextToSpeech.say("Do you want me to repeat?")
            TextToSpeech.runAndWait()

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = r.listen(source)

            try:
                repet = r.recognize_google(audio).lower()
                if repet == "yes":
                    print("You said, " + repet)
                    for num in lines:
                        i += 1
                        dictionary[i] = num
                    print(dictionary)
                    repeat()

                elif repet == "no":
                    print("You said, " + repet)
                    TextToSpeech.say("Ok")
                    TextToSpeech.runAndWait()

                else:
                    print("You said, " + repet)
                    TextToSpeech.say("Please reply in yes or no")
                    TextToSpeech.runAndWait()

            except sr.UnknownValueError:
                TextToSpeech.say("Sorry, can you please repeat")
                TextToSpeech.runAndWait()

        except sr.UnknownValueError:
            TextToSpeech.say("Sorry, can you please repeat")
            TextToSpeech.runAndWait()
    TextToSpeech.say("Ok")
    TextToSpeech.runAndWait()

TextToSpeech.say("No Problem. Thank You for using Text Dictator")
TextToSpeech.runAndWait()
