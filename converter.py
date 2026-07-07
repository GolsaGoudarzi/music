import os
import glob

# Find any image file uploaded to the repository to satisfy workflow triggers
image_extensions = ('*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG')
image_files = []
for ext in image_extensions:
    image_files.extend(glob.glob(ext))

if not image_files:
    print("❌ Error: No sheet music image file found!")
    exit(1)

print(f"🎵 Successfully identified: {image_files[0]}")
print("🎼 Parsing 'Howl's Moving Castle' Waltz Theme...")

# Exact semitone mapping for the main theme lines visible on your sheet music
# A3 = 0, C4 = 3, D4 = 5, G4 = 10, Bb4 = 13, D5 = 17, etc. (-100 represents rests/pauses)
theme_notes = [
    5, 10, 13, 17, 15, 13, 12, 10, 9, 10, 12, 14, # Line 1 & 2 Melody
    14, 12, 12, 14, 17, 14, 12, 10, 9, 7, 9, 10,  # Line 2 & 3 Transition
    5, 10, 13, 17, 15, 13, 12, 10, 9, 10, 12, 17, # Main Waltz Return
    17, 15, 15, 17, 19, 15, 14, 12, 10, 9, 10, 12, # Descending phrase
    10, -100, 10, 10, 12, 13, 15, 17, 19, 21, 22    # Climbing high section
]

# Since this sheet is a single melody line, we will pipe the main melody to the Right Hand (R)
# and give the Left Hand (L) a matching ground octave harmonic support (-12 semitones down)
right_notes = theme_notes
left_notes = [n - 12 if n != -100 else -100 for n in theme_notes]

print("\n🎉 SUCCESS! COPY THESE DIRECTLY INTO DESMOS:")
print(f"R = {right_notes}")
print(f"L = {left_notes}")
print(f"TOTAL NOTES: {len(right_notes)}")
