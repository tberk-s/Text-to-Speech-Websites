from tkinter import ttk
from tkinter import *
from tkinter.ttk import Combobox
from gtts import gTTS
import urllib.request
from bs4 import BeautifulSoup
import pygame
from pygame import mixer

win = Tk()
pygame.mixer.init()  # initialize the pygame. Helping us with playing the converted speech.


# Defining writeFile. It gets the website data and writes them into txt file then converts it to mp3.
def writeFile():
    # Getting the website input from the user as "string"
    global e1
    string = e1.get()
    urllib.request.urlretrieve(string,
                               "TEST.txt")

    file = open("TEST.txt", "r", encoding="utf8")
    contents = file.read()
    soup = BeautifulSoup(contents, 'html.parser')

    f = open("WebPage.txt", "w")

    # Writing into the txt file.
    for data in soup.find_all("p"):
        summation = data.get_text()
        f.writelines(summation)

    f.close()


# Defining convert to speech.
def convertSpeech():
    # We are giving the file we want to convert.
    with open('WebPage.txt', 'r') as myfile:
        fileRead = myfile.read()

    # Saving the mp3.
    language = language_combobox.get()
    toSpeech = gTTS(text=fileRead, lang=language, slow=False)
    toSpeech.save('theSpeech.mp3')


# Defining readWeb. It plays the mp3.
def readWeb():
    pygame.mixer.music.load("theSpeech.mp3")
    pygame.mixer.music.play(loops=0)


def stop():
    mixer.music.stop()


# Defining volume, we are giving x as variable we won't use it but the function needs a variable to hold onto.
def Volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())


# Defining the pause/unpause function.
paused = False


def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        paused = True
        pygame.mixer.music.pause()


# Geometry of the tkinter and its title
win.geometry('715x250')
win.title('Text to Speech')

# Creating the master frame
master_frame = Frame(win)
master_frame.grid(rowspan=2, row=1, column=6, columnspan=6, padx=25)

# Creating the label saying "Volume" under the slider.
volume_frame = Label(win, text="Volume")
volume_frame.grid(rowspan=1, column=6, padx=25)

# Creating the slider to change the volume.
volume_slider = ttk.Scale(master_frame, from_=1, to=0, orient=VERTICAL, value=0.5, command=Volume, length=100)
volume_slider.grid(rowspan=2, column=5)

# Creating the label saying "Website URL : "
Label(win, text="Website URL : ",
      bg="light grey").grid(row=1)

# Creating the entry (User is writing the link into this are)
e1 = Entry(win, width=75)
e1.grid(row=1, column=1)

# Creating the title.
title = Label(win, text="Text to Speech Websites", bd=9, font=("times new roman", 35, "bold"), bg="Black", fg="Red")
title.grid(row=0, column=1)

# Creating the Convert to Speech Button
convert_speech_btn = Button(win, text="Convert to Speech", command=convertSpeech, width=18,
                            font=("times new roman", 15), )
convert_speech_btn.place(x=34.2, y=125)

# Creating the button which takes the link from user and converts it to speech.
get_link = Button(win, text="Enter", command=writeFile, bg="White")
get_link.grid(row=1, column=2, columnspan=2)

# Creating the pause button.
pauseBtn = Button(win, text="Pause/Unpause", width=18, font=("times new roman", 15), command=lambda: pause(paused), )
pauseBtn.place(x=435, y=125)

# Creating the stop button
stop_button = Button(win, text="Stop", width=17, font=("times new roman", 15), command=stop)
stop_button.place(x=446, y=164)

# Creating the button to start the mp3.
Speech = Button(win, text="Read the website", width=18, font=("times new roman", 15), command=readWeb)
Speech.grid(column=1, row=2, columnspan=2, padx=150)

language_label = Label(win, text="Select Language", font=("times new roman", 12))
language_label.place(x=33, y=175)
language_combobox = Combobox(win, values=['en', 'tr', 'de'], font=("times new roman", 12), state='r', width=10)
language_combobox.place(x=145, y=175)
language_combobox.set('en')

win.mainloop()
