import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLib
import requests
import time
from gtts import gTTS
import pygame
import os


recognizer = sr.Recognizer()
engine = pyttsx3.init()
apikey = "f75d30c9dbb84207a62039b3f2a98624"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    filename = "temp.mp3"

    # Stop and unload if already in use
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    except:
        pass

    # Try to delete previous mp3
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except Exception as e:
            print("Failed to delete previous temp.mp3:", e)
            return

    # Create new mp3
    gtts = gTTS(text)
    gtts.save(filename)

    # Play mp3
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Cleanup
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        os.remove(filename)
    except Exception as e:
        print("Failed to delete after playing:", e)


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLib.music[song]
        webbrowser.open(link)
    elif 'news' in c.lower() or 'headlines' in c.lower():
        speak("Fetching the latest headlines from India")
        try:
            response=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={apikey}")
            response.raise_for_status()
            data=response.json()
            articles=data.get('articles',[])

            if not articles:
                speak("Sorry, I couldn't find any news.")
            else:
                speak("Here are the top five headlines")
                for i,article in enumerate(articles[:5],1):
                    title = article.get('title','No title found')
                    print(f"{i}. {title}")
                    speak(f"Headline {i}: {title}")
        except Exception as e:
            speak("Sorry, I couldn't fetch the news due to an error.")
            print("Error fetching news:", e)


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r = sr.Recognizer()

        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=3, phrase_time_limit=2)

            word = r.recognize_google(audio)
            print("Heard: ", word)
            if word.lower() == "jarvis":

                with sr.Microphone() as source:
                    speak("Yeah, I'm listening")
                    time.sleep(0.8)
                    print("Jarvis Active...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                    command = r.recognize_google(audio)

                    processCommand(command)
                    print("Detected word:", word)

        except Exception as e:
            print("Speak clearly....; {0}".format(e))