from llm_agent import get_ai_response
from voice_input import listen
from voice_output import speak
from memory_store import MemoryStore
import random

# --------------------------------------
# Random construction updates
# --------------------------------------
def random_update():
    updates = [
        "Aapke ghar ka slab ka kaam complete ho gaya hai.",
        "Boundary wall ka paint finish kar diya gaya hai.",
        "Garden area ke tiles lag rahe hain.",
        "Clubhouse ke construction ka 70 percent kaam complete ho gaya hai.",
        "Electric wiring ka kaam bhi lagbhag khatam ho gaya hai.",
        "Roadside plantation ka kaam bhi shuru ho gaya hai.",
        "Main hall ke flooring ka kaam complete ho gaya hai, Sir."
    ]
    return random.choice(updates)

# --------------------------------------
# Initial greeting
# --------------------------------------
def greet():
    msg = "Namaste Sir, chai pee li? Main Riverwood AI Voice Agent hoon. Kaise hain aap?"
    print(msg)
    speak(msg, save_demo=True)

# --------------------------------------
# Main conversational loop
# --------------------------------------
def run():
    memory = MemoryStore()
    greet()

    while True:
        print("\n--- Waiting for your reply ---")
        user_input = listen()
        if not user_input:
            continue

        context = memory.get_context()
        ai_reply = get_ai_response(user_input, context)

        # Add a construction update naturally
        if any(keyword in user_input.lower() for keyword in ["site", "ghar", "visit", "update", "clubhouse", "project"]):
            ai_reply += " " + random_update()

        print(ai_reply)
        speak(ai_reply, save_demo=True)
        memory.update(user_input, ai_reply)

        # Exit condition
        if any(x in user_input.lower() for x in ["bye", "goodbye", "exit", "stop"]):
            closing = "Thik hai Sir, fir milte hain! Have a wonderful day ahead!"
            print(closing)
            speak(closing, save_demo=True)
            break


if __name__ == "__main__":
    run()
