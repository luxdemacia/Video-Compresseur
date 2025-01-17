import os
import tkinter as tk
from tkinter import filedialog
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import subprocess

def compress_video(input_path, output_path, resolution=(1920, 1080), audio_quality="high"):
    try:
        # Define the ffmpeg command for video compression
        ffmpeg_command = [
            'ffmpeg',
            '-i', input_path,          # Input file
            '-vcodec', 'libx264',       # Video codec (H.264)
            '-acodec', 'aac',           # Audio codec (AAC)
            '-b:a', '192k',             # Audio bitrate
            '-preset', 'fast',          # Compression preset (speed/quality balance)
            '-crf', '23',               # Constant Rate Factor (affects quality, lower = better)
            '-s', f'{resolution[0]}x{resolution[1]}',  # Set resolution
            '-y',                       # Overwrite output file if it exists
            output_path
        ]

        # Execute the command
        subprocess.run(ffmpeg_command, check=True)
        
        print(f"Compression successful for {input_path}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error compressing {input_path}: {str(e)}")

def compress_folder(original_folder, compress_folder):
    # Ensure the compress folder exists
    if not os.path.exists(compress_folder):
        os.makedirs(compress_folder)

    # Iterate over all files in the original folder
    for filename in os.listdir(original_folder):
        if filename.endswith(".mp4"):
            input_path = os.path.join(original_folder, filename)
            output_path = os.path.join(compress_folder, filename)
            compress_video(input_path, output_path)

def choose_folder(prompt):
    """Open a folder dialog and let the user choose a folder."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title=prompt)
    return folder_selected

if __name__ == "__main__":
    # Ask the user for the folder containing the videos to compress
    original_folder = choose_folder("Select the folder with videos to compress")
    if not original_folder:
        print("No folder selected. Exiting...")
        exit()

    # Ask the user where to save the compressed videos
    compress_folder_path = choose_folder("Select the folder to save compressed videos")
    if not compress_folder_path:
        print("No folder selected for compressed videos. Exiting...")
        exit()

    # Compress videos in the original folder and save to the compress folder
    compress_folder(original_folder, compress_folder_path)
