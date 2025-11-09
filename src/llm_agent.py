import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

# ------------------------------------------------------
# 1️⃣  Load Environment Variables
# ------------------------------------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Default Model
MODEL = os.getenv("MODEL", "gemini-2.0-flash")

# ------------------------------------------------------
# 2️⃣  Detect Language (Hindi / Hinglish / English)
# ------------------------------------------------------
def detect_language(text: str) -> str:
    """
    Detects whether the user input is in Hindi (or Hinglish) or English.
    - Returns 'hi' for Hindi/Hinglish
    - Returns 'en' for English
    """

    # Detect Hindi characters (Devanagari)
    if re.search(r'[\u0900-\u097F]', text):
        return "hi"

    text_lower = text.lower()

    # Common Hinglish clues
    hinglish_keywords = [
        "hai", "kya", "acha", "nahi", "haan", "kaam", "ghar",
        "aap", "ji", "kal", "bataiye", "theek", "visit", "mujhe"
    ]

    # English clues
    english_words = [
        "the", "is", "are", "was", "were", "i", "you", "we",
        "they", "today", "yesterday", "construction", "project",
        "update", "how", "what", "when", "where", "my", "your"
    ]

    # Count both types
    hinglish_hits = sum(word in text_lower for word in hinglish_keywords)
    english_hits = sum(word in text_lower for word in english_words)

    # Decide based on dominant language
    if hinglish_hits > english_hits:
        return "hi"
    return "en"

# ------------------------------------------------------
# 3️⃣  Generate Contextual AI Response
# ------------------------------------------------------
def get_ai_response(user_input: str, memory: str = "") -> str:
    """
    Generates a context-aware response from Gemini in the same language
    as the user input. Keeps tone friendly and business-like.
    """
    try:
        lang = detect_language(user_input)
        model = genai.GenerativeModel(MODEL)

        # ------------------ HINDI MODE ------------------
        if lang == "hi":
            system_prompt = (
                "User is speaking in Hindi or Hinglish. "
                "Reply completely in Hindi (Hinglish allowed but no English sentences). "
                "You are 'Miss Riverwood', a friendly but professional AI voice assistant "
                "for Riverwood Projects LLP. "
                "Keep your replies short, warm, and business-like. "
                "Focus on project updates, construction progress, site visits, "
                "and customer engagement. "
                "Avoid emojis and maintain a polite tone."
            )

        # ------------------ ENGLISH MODE ------------------
        else:
            system_prompt = (
                "User is speaking in English. "
                "Reply strictly in English — do NOT use Hindi or Hinglish words. "
                "You are 'Miss Riverwood', a polite and professional AI assistant "
                "representing Riverwood Projects LLP. "
                "Keep your responses concise, conversational, and business-focused. "
                "Talk naturally about real estate updates, project progress, "
                "customer queries, and visit scheduling. "
                "Avoid emojis and use clear, polite English."
            )

        # Full prompt with conversational memory
        prompt = (
            f"{system_prompt}\n\n"
            f"Previous conversation:\n{memory}\n"
            f"User: {user_input}\n"
            "Assistant reply (no 'AI:' prefix):"
        )

        # Generate reply using Gemini
        response = model.generate_content(prompt)

        # Extract text safely
        if hasattr(response, "text") and response.text:
            text = response.text.strip()
        else:
            text = "Sorry Sir, I didn’t catch that clearly."

        return text

    except Exception as e:
        return f"Error: {e}"
