import datetime
import math
import random
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Speak the text out loud"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user input via microphone"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
        return ""
    except sr.RequestError:
        print("Speech service unavailable.")
        return ""

# ---------------- MATH FUNCTIONS ----------------

def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)

def permutation(n, k):
    return factorial(n) // factorial(n - k)

def combination(n, k):
    return permutation(n, k) // factorial(k)

def quadratic_roots(a, b, c):
    if a == 0:
        return [-c/b] if b != 0 else []
    d = b**2 - 4*a*c
    if d > 0:
        sqrt_d = math.sqrt(d)
        return [(-b + sqrt_d)/(2*a), (-b - sqrt_d)/(2*a)]
    elif d == 0:
        return [-b/(2*a)]
    else:
        sqrt_d = math.sqrt(-d)
        return [f"{-b/(2*a)} + {sqrt_d/(2*a)}i", f"{-b/(2*a)} - {sqrt_d/(2*a)}i"]

# ---------------- PREDEFINED RESPONSES ----------------

jokes = [
    "Why did the computer go to the doctor? It caught a virus!",
    "Why did the chicken cross the road? To get to the other side!",
]

def process_command(text):
    text = text.lower()
    
    # Greetings
    if "hello" in text or "hi" in text:
        return "Hello! How can I help you today?"
    
    # Time
    elif "time" in text:
        return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}"
    
    # Joke
    elif "joke" in text:
        return random.choice(jokes)
    
    # Factorial
    elif "factorial" in text:
        try:
            n = int(text.split()[-1])
            return f"{n}! = {factorial(n)}"
        except:
            return "Please provide a number for factorial."
    
    # Permutation
    elif "permutation" in text:
        try:
            numbers = [int(s) for s in text.split() if s.isdigit()]
            return f"P({numbers[0]},{numbers[1]}) = {permutation(numbers[0], numbers[1])}"
        except:
            return "Please provide n and k for permutation."
    
    # Combination
    elif "combination" in text:
        try:
            numbers = [int(s) for s in text.split() if s.isdigit()]
            return f"C({numbers[0]},{numbers[1]}) = {combination(numbers[0], numbers[1])}"
        except:
            return "Please provide n and k for combination."
    
    # Quadratic roots
    elif "quadratic" in text:
        try:
            numbers = [float(s) for s in text.split() if s.replace('.','',1).isdigit()]
            roots = quadratic_roots(numbers[0], numbers[1], numbers[2])
            return f"Roots: {roots}"
        except:
            return "Please provide coefficients a, b, c for quadratic."
    
    # Unknown
    else:
        return "Sorry, I don't understand that command yet."

# ---------------- MAIN LOOP ----------------

print("AI Assistant started. Say 'exit' to quit.")
speak("Hello! I am your assistant. How can I help you today?")

while True:
    # You can toggle between text input or speech input
    # user_input = input("You: ")
    user_input = listen()
    
    if "exit" in user_input.lower():
        speak("Goodbye!")
        print("Goodbye!")
        break
    
    response = process_command(user_input)
    print("AI:", response)
    speak(response)