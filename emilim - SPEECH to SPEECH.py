import speech_recognition as sr
from time import sleep
import keyboard
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import json
from tkinter import *
from tkinter.filedialog import asksaveasfile

with open('credential.json') as f:
   data = json.load(f)
api_key = data['api_key']
url = data['url']

root = Tk()
root.resizable(False, False)
root.geometry("800x500")
root.configure(bg='ghost white')
root.title("emilim - SPEECH to SPEECH")

Label(root, text = "TEXT_TO_SPEECH", font = "arial 20 bold", bg='white smoke').pack()
Label(text ="emilim", font = 'arial 15 bold', bg ='white smoke' , width = '20').pack(side = 'bottom')
Label(root,text ="Enter Text", font = 'arial 15 bold', bg ='white smoke').place(x=20,y=60)
entry_field = Text(root, height='20', width='70')
entry_field.place(x=20, y=100)

def GetText():
    mic = sr.Microphone(device_index=1)
    r = sr.Recognizer()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Please say something: ")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("you said: ", text)
            entry_field.insert(INSERT, text)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

def Convert():
    authenticator = IAMAuthenticator(api_key)
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )
    text_to_speech.set_service_url(url)
    files = [('WAV Files', '*.wav')]
    file = asksaveasfile(filetypes = files, defaultextension = files)

    with open(file.name, 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                entry_field.get('1.0', 'end-1c'),
                voice='en-US_KevinV3Voice',
                accept='audio/wav'        
            ).get_result().content)

def Exit():
    root.destroy()

def Reset():
    entry_field.delete('1.0', 'end-1c')

Button(root, text="GET MIC", font='arial 15 bold' , command=GetText, width = '7').place(x=600,y=97)
Button(root, text = "CONVERT", font = 'arial 15 bold' , command = Convert ,width = '9').place(x=25,y=440)
Button(root, font = 'arial 15 bold',text = 'EXIT', width = '4' , command = Exit, bg = 'OrangeRed1').place(x=155 , y = 440)
Button(root, font = 'arial 15 bold',text = 'RESET', width = '6' , command = Reset).place(x=220 , y = 440)

root.mainloop()
