import os
import glob
import subprocess
import sys
from music21 import converter

# Find any image file uploaded to the repository
image_extensions = ('*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG')
image_files = []
for ext in image_extensions:
    image_files.extend(glob.glob(ext))

if not image_files:
    print("❌ Error: No sheet music image file found in the repository folder!")
    exit(1)

image_file = image_files[0]
print(f"🎵 Found sheet music file: {image_file}")

print("Step 1: AI is visually scanning your sheet music... (Muting download spam, please wait)")

# Run oemer but intercept the output to filter out the progress bar spam
process = subprocess.Popen(
    ["oemer", image_file], 
    stdout=subprocess.PIPE, 
    stderr=subprocess.STDOUT, 
    text=True
)

# Read the logs line by line as they happen
for line in process.stdout:
    # 🛑 IF THE LINE CONTAINS A PERCENTAGE SIGN, DO NOT PRINT IT!
    if "%" in line or "Downloading" in line:
        continue
    # Print the clean status updates only
    sys.stdout.write(line)
    sys.stdout.flush()

process.wait()

if process.returncode != 0:
    print(f"❌ AI scanning failed with exit code {process.returncode}")
    exit(process.returncode)

xml_filename = image_file.rsplit('.', 1)[0] + ".musicxml"

print("Step 2: Parsing musical tracks...")
score = converter.parse(xml_filename)

right_hand_part = score.parts[0]
left_hand_part = score.parts[1] if len(score.parts) > 1 else score.parts[0]

def get_semitone(n):
    note_mapping = {'C':3, 'C#':4, 'D-':4, 'D':5, 'D#':6, 'E-':6, 'E':7, 
                    'F':8, 'F#':9, 'G-':9, 'G':10, 'G#':11, 'A-':11, 'A':12, 'A#':13, 'B-':13, 'B':14}
    if n.isRest: return -100
    elif n.isNote: return note_mapping[n.pitch.step] + (n.pitch.octave - 4) * 12
    elif n.isChord:
        top_note = n.sortAscending().notes[-1]
        return note_mapping[top_note.pitch.step] + (top_note.pitch.octave - 4) * 12
    return -100

right_notes = [get_semitone(n) for n in right_hand_part.flatten().notesAndRests]
left_notes = [get_semitone(n) for n in left_hand_part.flatten().notesAndRests]

max_len = max(len(right_notes), len(left_notes))
right_notes += [-100] * (max_len - len(right_notes))
left_notes += [-100] * (max_len - len(left_notes))

print("\n🎉 SUCCESS! COPY THESE DIRECTLY INTO DESMOS:")
print(f"R = {right_notes}")
print(f"L = {left_notes}")
print(f"TOTAL NOTES: {max_len}")
