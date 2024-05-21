import pyttsx3 as p
import speech_recognition as sr
import ollama

engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
r = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def listen():
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        print("\n\nYou : ",end='')
        
        try:
            audio = r.listen(source)
            text = str(r.recognize_google(audio))
            print(text)
        except sr.UnknownValueError:
            text="Sorry, I could not understand the audio."
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            text="Could not request results from Google Speech Recognition service; {e}"
            print(f"Could not request results from Google Speech Recognition service; {e}")
            
    return text