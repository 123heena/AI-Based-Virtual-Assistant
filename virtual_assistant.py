import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import wolframalpha
import requests
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # Speed of speech
engine.setProperty("volume", 1)  # Volume (0.0 to 1.0)

# Initialize WolframAlpha API (Replace 'YOUR_APP_ID' with your WolframAlpha API key)
wolfram_api = "PJH2AJ-3L49JHW46K"  # Get API key from https://developer.wolframalpha.com/

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input from the microphone and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"🗣️ You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand. Please repeat.")
            return None
        except sr.RequestError:
            speak("Network error. Please check your connection.")
            return None
        except Exception as e:
            speak(f"Error: {str(e)}")
            return None

def get_time():
    """Tell the current time."""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

def get_date():
    """Tell the current date."""
    today = datetime.date.today().strftime("%B %d, %Y")
    speak(f"Today's date is {today}")

def search_wikipedia(query):
    """Search Wikipedia and return a summary."""
    if not query:
        speak("I didn't hear the topic. Please say it again.")
        return

    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"There are multiple results for {query}. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find anything on Wikipedia for that topic.")
    except Exception as e:
        speak(f"An error occurred: {str(e)}")

def open_website(url):
    """Open a website in the browser."""
    speak(f"Opening {url}")
    webbrowser.open(url)

def get_weather(city):
    """Fetch weather data from OpenWeatherMap API."""
    api_key = "c946a4819adead8ce78434639f8ce7be"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url).json()
    
    if response["cod"] == 200:
        temp = response["main"]["temp"]
        weather_desc = response["weather"][0]["description"]
        speak(f"The current temperature in {city} is {temp} degrees Celsius with {weather_desc}.")
    else:
        speak("City not found.")

def solve_math(query):
    """Solve mathematical or general knowledge queries using WolframAlpha."""
    if not query:
        speak("I didn't hear the question. Please say it again.")
        return

    try:
        client = wolframalpha.Client(wolfram_api)
        res = client.query(query)
        answer = next(res.results).text
        speak(f"The answer is {answer}")
    except Exception as e:
        speak("I couldn't solve that. Please check your API key or try a different question.")

def virtual_assistant():
    """Main function that continuously listens and processes voice commands."""
    speak("Hello! I am your virtual assistant. How can I help you?")
    
    while True:
        command = listen()
        if command:
            if "time" in command:
                get_time()
            elif "date" in command:
                get_date()
            elif "wikipedia" in command:
                speak("What should I search on Wikipedia?")
                topic = listen()
                if topic:
                    search_wikipedia(topic)
                else:
                    speak("I couldn't hear the topic. Please try again.")
            elif "open youtube" in command:
                open_website("https://www.youtube.com")
            elif "open google" in command:
                open_website("https://www.google.com")
            elif "weather" in command:
                speak("Which city?")
                city = listen()
                if city:
                    get_weather(city)
            elif "solve" in command:
                speak("What should I solve?")
                question = listen()
                if question:
                    solve_math(question)
                else:
                    speak("I couldn't hear the question. Please try again.")
            elif "exit" in command or "bye" in command:
                speak("Goodbye! Have a great day.")
                break
            else:
                speak("I'm sorry, I didn't understand that command.")

if __name__ == "__main__":
    virtual_assistant()
