# Step 1: Setting Up the Environment

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment

load_dotenv()

BASE_DIR = Path(__file__).parent
AUDIO_DIR = BASE_DIR / "audio"
CHUNKS_DIR = BASE_DIR / "chunks"
OUTPUTS_DIR = BASE_DIR / "outputs"

for folder in [AUDIO_DIR, CHUNKS_DIR, OUTPUTS_DIR]:
    folder.mkdir(exist_ok=True)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY wurde nicht gefunden. Prüfe deine .env Datei.")

client = OpenAI(api_key=api_key)

# Check1 - Messages only print w/o error before

print("OpenAI Client initialized successfully.")
print("Project folders checked:")
print(AUDIO_DIR)
print(CHUNKS_DIR)
print(OUTPUTS_DIR)
print("pydub imported successfully.")

#Step 2: Downloading Sample Meeting Audio

from pathlib import Path
from pydub import AudioSegment

BASE_DIR = Path(__file__).parent
AUDIO_DIR = BASE_DIR / "audio"

audio_file = AUDIO_DIR / "Arthur.mp3"

if not audio_file.exists():
    raise FileNotFoundError(f"Audio file not found: {audio_file}")

audio = AudioSegment.from_file(audio_file)

duration_seconds = len(audio) / 1000
duration_minutes = duration_seconds / 60

# Check2 - Messages only print w/o error before

print("Audio file validation successful.")
print(f"File: {audio_file.name}")
print(f"Duration: {duration_seconds:.2f} seconds")
print(f"Duration: {duration_minutes:.2f} minutes")
print(f"Channels: {audio.channels}")
print(f"Frame rate: {audio.frame_rate} Hz")
print(f"Sample width: {audio.sample_width} bytes")