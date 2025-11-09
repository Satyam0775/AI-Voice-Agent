import os
from pydub import AudioSegment

def merge_to_mp3():
    folder = os.path.join(os.getcwd(), "demo_recording")
    files = sorted([f for f in os.listdir(folder) if f.endswith(".mp3")])
    combined = AudioSegment.empty()
    for f in files:
        combined += AudioSegment.from_file(os.path.join(folder, f), format="mp3")
    output = os.path.join(folder, "demo.mp3")
    combined.export(output, format="mp3")
    print(f"✅ Demo saved at {output}")

if __name__ == "__main__":
    merge_to_mp3()
