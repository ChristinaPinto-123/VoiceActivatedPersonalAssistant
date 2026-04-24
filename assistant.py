import speech_recognition as sr
import pyttsx3
import requests
import datetime
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from scipy.io.wavfile import write
import feedparser
import os

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    fs = 44100  
    seconds = 4 
    
    try:
        print("Listening...")
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait() 
        
        write('temp_audio.wav', fs, myrecording)
        
        with sr.AudioFile('temp_audio.wav') as source:
            audio = recognizer.record(source)
            
        os.remove('temp_audio.wav')
        
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}\n")
        return query.lower()
        
    except Exception as e:
        print(f"Error: {e}")
        return "none"


def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        response = requests.get(url)
        if response.status_code == 200:
            report = response.text
            speak(f"The weather in {city} is {report}.")
        else:
            speak("I couldn't find weather for that location.")
    except Exception:
        speak("I'm having trouble connecting to the weather service.")

def get_news():
    try:
        feed_url = "http://feeds.bbci.co.uk/news/world/rss.xml"
        news_feed = feedparser.parse(feed_url)
        
        speak("Here are the top three stories from BBC News.")
        for i in range(3):
            story = news_feed.entries[i].title
            speak(f"Story number {i+1}: {story}")
    except Exception:
        speak("I couldn't fetch the news right now.")

def run_assistant():
    speak("Hello! How can I help you today?")
    while True:
        command = listen()

        if 'weather' in command:
            speak("Which city?")
            city = listen()
            get_weather(city)

        elif 'time' in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {time}")

        elif 'news' in command:
            get_news()
            
        elif 'stop' in command or 'exit' in command:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    run_assistant()