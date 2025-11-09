from gtts import gTTS
import pygame
import os
import time
from datetime import datetime

def speak(text: str, save_demo: bool = False):
    """
    Convert text to speech, play using pygame, and optionally
    save audio clips in /demo_recording for the final demo.

    - Works reliably on Windows (Python 3.13)
    - Avoids blocking or leftover temporary files
    - Handles both playback and safe saving
    """

    try:
        # === 1️⃣  Temporary Audio Setup ===
        temp_dir = os.path.join(os.getcwd(), "temp_audio")
        os.makedirs(temp_dir, exist_ok=True)
        filename = f"voice_{int(time.time())}.mp3"
        filepath = os.path.join(temp_dir, filename)

        # === 2️⃣  Generate Voice File ===
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(filepath)

        # === 3️⃣  Play Using pygame ===
        pygame.mixer.init()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.stop()
        pygame.mixer.quit()

        # === 4️⃣  Save Clip for Demo (Optional) ===
        if save_demo:
            demo_dir = os.path.join(os.getcwd(), "demo_recording")
            os.makedirs(demo_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            demo_path = os.path.join(demo_dir, f"ai_output_{timestamp}.mp3")

            os.replace(filepath, demo_path)  # Move file safely
            print(f"[🎧 Saved for demo: {demo_path}]")
        else:
            os.remove(filepath)

        # === 5️⃣  Cleanup Temporary Folder ===
        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)

    except Exception as e:
        print("⚠️ Audio playback failed:", e)
