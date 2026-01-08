# simple AI assistant using Python
import datetime
import random

def respond(text):
    text = text.lower()
    if "time" in text:
        return f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}"
    elif "joke" in text:
        jokes = ["Why did the chicken cross the road? To get to the other side!",
                 "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.'"]
        return random.choice(jokes)
    elif "hello" in text or "hi" in text:
        return "Hello! How can I help you today?"
    else:
        return "Sorry, I don't understand that command."

# main loop
print("AI Assistant started. Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    print("AI:", respond(user_input))