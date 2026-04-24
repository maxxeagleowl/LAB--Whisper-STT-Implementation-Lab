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

# Step 3: Basic Transcription Without Chunking

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = Path(__file__).parent
AUDIO_DIR = BASE_DIR / "audio"
OUTPUTS_DIR = BASE_DIR / "outputs"

audio_file = AUDIO_DIR / "Arthur.mp3"

# Error Step Missing File

if not audio_file.exists():
    raise FileNotFoundError(f"Audio file not found: {audio_file}")

# Transcribtion

print("Transcribing audio with Whisper")

with open(audio_file, "rb") as file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=file
    )

print("\nTranscription:")
print("-" * 40)
print(transcript.text)

output_file = OUTPUTS_DIR / "arthur_basic_transcription.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(transcript.text)

print(f"\nTranscription saved to: {output_file}")

# Step 4: Transcription with Prompts Guided Approach

print("Transcribing audio with Whisper using prompt")

with open(audio_file, "rb") as file:
    prompted_transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=file,
        prompt = "Arthur, Aunt Helen, Nelly, pine rafters, joists, barn,scouts, stone house, elm tree, coarsely, undaunted, snug"
    )

print("\nPrompted Transcription:")
print("-" * 40)
print(prompted_transcript.text)

prompted_output_file = OUTPUTS_DIR / "arthur_prompted_transcription.txt"

with open(prompted_output_file, "w", encoding="utf-8") as f:
    f.write(prompted_transcript.text)

print(f"\nPrompted transcription saved to: {prompted_output_file}")

# Step 5: Compare Prompted and Unprompted Transcriptions

basic_output_file = OUTPUTS_DIR / "arthur_basic_transcription.txt"
prompted_output_file = OUTPUTS_DIR / "arthur_prompted_transcription.txt"
comparison_output_file = OUTPUTS_DIR / "arthur_comparison.txt"

#if not basic_output_file.exists():
#    raise FileNotFoundError(f"Basic transcription file not found: {basic_output_file}")

#if not prompted_output_file.exists():
#    raise FileNotFoundError(f"Prompted transcription file not found: {prompted_output_file}")

with open(basic_output_file, "r", encoding="utf-8") as f:
    basic_text = f.read()

with open(prompted_output_file, "r", encoding="utf-8") as f:
    prompted_text = f.read()

print("\nComparison: Prompted vs. Unprompted")
print("-" * 40)

print("\nUnprompted transcription:")
print(basic_text)

print("\nPrompted transcription:")
print(prompted_text)

comparison_text = f"""
Comparison: Prompted vs. Unprompted Transcription

Unprompted Transcription:
{basic_text}

Prompted Transcription:
{prompted_text}

"""

with open(comparison_output_file, "w", encoding="utf-8") as f:
    f.write(comparison_text)

print(f"\nComparison saved to: {comparison_output_file}")

# Step 5b: Show Exact Text Differences

import difflib

print("\nExact Differences:")
print("-" * 40)

diff = difflib.ndiff(
    basic_text.split(),
    prompted_text.split()
)

difference_lines = []

for line in diff:
    if line.startswith("- ") or line.startswith("+ "):
        print(line)
        difference_lines.append(line)

difference_output_file = OUTPUTS_DIR / "arthur_differences.txt"

with open(difference_output_file, "w", encoding="utf-8") as f:
    f.write("Exact Differences: Prompted vs. Unprompted\n")
    f.write("-" * 40 + "\n")

    for line in difference_lines:
        f.write(line + "\n")

print(f"\nDifferences saved to: {difference_output_file}")


# Step 6: Implementing Audio Chunking

chunk_length_minutes = 1 #chunk_duration * sample_rate
chunk_length_ms = chunk_length_minutes * 60 * 1000

print(f"\n 🔪 Splitting audio into chunks")
print("-" * 40)

audio = AudioSegment.from_file(audio_file)

total_duration_ms = len(audio)
total_duration_seconds = total_duration_ms / 1000

chunks = []

for i, start_ms in enumerate(range(0, total_duration_ms, chunk_length_ms)):
    end_ms = min(start_ms + chunk_length_ms, total_duration_ms)
    chunk = audio[start_ms:end_ms]

    chunk_filename = f"arthur_chunk_{i + 1}.mp3"
    chunk_path = CHUNKS_DIR / chunk_filename

    chunk.export(chunk_path, format="mp3")

    chunk_info = {
        "chunk_number": i + 1,
        "file": str(chunk_path),
        "start_seconds": start_ms / 1000,
        "end_seconds": end_ms / 1000,
        "duration_seconds": (end_ms - start_ms) / 1000
    }

    chunks.append(chunk_info)

    print(
        f"Chunk {i + 1} created: "
        f"{chunk_filename} "
        f"[{chunk_info['start_seconds']:.2f}s - {chunk_info['end_seconds']:.2f}s]"
    )

print(f"\nTotal audio duration: {total_duration_seconds:.2f} seconds")
print(f"Total chunks created: {len(chunks)}")


# Step 7: Transcribing Chunks with Timestamps

print("\nTranscribing chunks with timestamps")
print("-" * 40)

all_segments = []
full_chunked_text = ""

for chunk_info in chunks:
    chunk_number = chunk_info["chunk_number"]
    chunk_path = Path(chunk_info["file"])
    chunk_offset = chunk_info["start_seconds"]

    print(f"\nTranscribing chunk {chunk_number}/{len(chunks)}")
    print(f"File: {chunk_path.name}")
    print(f"Offset: {chunk_offset:.2f}s")

    with open(chunk_path, "rb") as file:
        chunk_transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )

    full_chunked_text += chunk_transcript.text + " "

    if hasattr(chunk_transcript, "segments") and chunk_transcript.segments:
        for segment in chunk_transcript.segments:
            adjusted_segment = {
                "chunk_number": chunk_number,
                "start": segment.start + chunk_offset,
                "end": segment.end + chunk_offset,
                "text": segment.text.strip()
            }

            all_segments.append(adjusted_segment)

            print(
                f"[{adjusted_segment['start']:.2f}s - "
                f"{adjusted_segment['end']:.2f}s] "
                f"{adjusted_segment['text']}"
            )

chunked_output_file = OUTPUTS_DIR / "arthur_chunked_transcription_with_timestamps.txt"

with open(chunked_output_file, "w", encoding="utf-8") as f:
    for segment in all_segments:
        f.write(
            f"[{segment['start']:.2f}s - {segment['end']:.2f}s] "
            f"{segment['text']}\n"
        )

print(f"\nChunked transcription with timestamps saved to: {chunked_output_file}")
print(f"Total timestamped segments: {len(all_segments)}")


# Step 8: Exporting with Timestamps

import json

print("\nExporting transcriptions with timestamps")
print("-" * 40)

# Helper function for SRT time format
def format_srt_time(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    total_seconds = int(seconds)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


# 1. TXT export
txt_export_file = OUTPUTS_DIR / "arthur_final_transcription.txt"

with open(txt_export_file, "w", encoding="utf-8") as f:
    for segment in all_segments:
        f.write(
            f"[{segment['start']:.2f}s - {segment['end']:.2f}s] "
            f"{segment['text']}\n"
        )

print(f"TXT export saved to: {txt_export_file}")


# 2. SRT export
srt_export_file = OUTPUTS_DIR / "arthur_final_transcription.srt"

with open(srt_export_file, "w", encoding="utf-8") as f:
    for index, segment in enumerate(all_segments, start=1):
        start_time = format_srt_time(segment["start"])
        end_time = format_srt_time(segment["end"])

        f.write(f"{index}\n")
        f.write(f"{start_time} --> {end_time}\n")
        f.write(f"{segment['text']}\n\n")

print(f"SRT export saved to: {srt_export_file}")


# 3. JSON export
json_export_file = OUTPUTS_DIR / "arthur_final_transcription.json"

export_data = {
    "audio_file": audio_file.name,
    "total_segments": len(all_segments),
    "segments": all_segments
}

with open(json_export_file, "w", encoding="utf-8") as f:
    json.dump(export_data, f, indent=4, ensure_ascii=False)

print(f"JSON export saved to: {json_export_file}")

print("\nExport completed successfully.")