import streamlit as st
from streamlit_mic_recorder import mic_recorder
from llm_agent import get_ai_response
from voice_output import speak
from memory_store import MemoryStore
import tempfile
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile

# ================================================
# 🏡 Streamlit Page Configuration
# ================================================
st.set_page_config(page_title="Riverwood Voice Assistant", page_icon="🏡", layout="centered")

# =======================
# 🪶 Custom Chat UI Style
# =======================
st.markdown("""
    <style>
        .chat-container {
            max-width: 700px;
            margin: auto;
            padding: 20px;
            background-color: #1E1E1E;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .user-bubble {
            background-color: #0078FF;
            color: white;
            padding: 10px 15px;
            border-radius: 20px 20px 0px 20px;
            margin: 8px 0;
            text-align: right;
            width: fit-content;
            max-width: 80%;
            margin-left: auto;
            font-size: 16px;
        }
        .ai-bubble {
            background-color: #F4D03F;
            color: #222;
            padding: 10px 15px;
            border-radius: 20px 20px 20px 0px;
            margin: 8px 0;
            width: fit-content;
            max-width: 80%;
            text-align: left;
            margin-right: auto;
            font-size: 16px;
        }
        .voice-mode-hint {
            text-align: center;
            color: #AAA;
            font-size: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# ================================================
# 🧠 Initialize Session State
# ================================================
if "memory" not in st.session_state:
    st.session_state.memory = MemoryStore()
if "history" not in st.session_state:
    st.session_state.history = []
if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False
if "greeted" not in st.session_state:
    st.session_state.greeted = False

# ================================================
# 🧠 Helper Functions
# ================================================
def record_voice(duration=5, fs=16000):
    """Record voice for a few seconds"""
    st.write("🎤 Listening... Speak now")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    filepath = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    wavfile.write(filepath, fs, audio)
    return filepath

def handle_conversation(user_input):
    """Process user input and generate AI response"""
    context = st.session_state.memory.get_context()
    ai_reply = get_ai_response(user_input, context)
    st.session_state.memory.update(user_input, ai_reply)
    st.session_state.history.append(("🧑‍💼 You", user_input))
    st.session_state.history.append(("🤖 Riverwood AI", ai_reply))
    speak(ai_reply, save_demo=True)

def greet_user():
    """Speak greeting once per session"""
    if not st.session_state.greeted:
        greeting = "Namaste Sir, chai pee li? Main Riverwood AI Voice Agent hoon. Kaise hain aap?"
        st.session_state.history.append(("🤖 Riverwood AI", greeting))
        speak(greeting, save_demo=True)
        st.session_state.greeted = True

# ================================================
# 🎤 Mode Selection
# ================================================
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.title("🏡 Riverwood Voice Assistant")
st.caption("Namaste Sir! Main Riverwood AI Voice Agent hoon — chai pee li? ☕")

col1, col2 = st.columns(2)
with col1:
    if st.button("🎤 Voice Mode ON" if not st.session_state.voice_mode else "🛑 Voice Mode OFF"):
        st.session_state.voice_mode = not st.session_state.voice_mode
        st.session_state.greeted = False

with col2:
    st.info(f"Mode: {'🎙️ Voice' if st.session_state.voice_mode else '⌨️ Text'}")

st.divider()

# ================================================
# 🎤 Voice Mode
# ================================================
if st.session_state.voice_mode:
    greet_user()
    st.markdown("<div class='voice-mode-hint'>🎧 Voice mode active — speak freely (no text displayed)</div>", unsafe_allow_html=True)
    audio_file = mic_recorder(start_prompt="🎙️ Speak", stop_prompt="🛑 Stop", key="recorder")
    if audio_file:
        # Demo placeholder; replace with speech-to-text later
        user_input = "Maine kal site visit kiya tha."
        handle_conversation(user_input)
else:
    # ============================================
    # 💬 Text Mode (Chat UI)
    # ============================================
    if not st.session_state.greeted:
        greet_user()

    user_input = st.text_input("💬 Type your message here:")
    if st.button("Send") and user_input.strip():
        handle_conversation(user_input)

# ================================================
# 💬 Chat Bubble Display
# ================================================
if not st.session_state.voice_mode:
    for speaker, msg in st.session_state.history:
        if "You" in speaker:
            st.markdown(f"<div class='user-bubble'>{msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-bubble'>{msg}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Developed by Satyam Kumar | Riverwood Projects LLP | Powered by Gemini + gTTS + Streamlit")
