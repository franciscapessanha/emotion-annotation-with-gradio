import gradio as gr
import pandas as pd
import os
import gradio as gr
from pathlib import Path
from huggingface_hub import login
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import json
from text_explanations import *
from utils import *

persistent_storage = Path('/data')
password_files = os.getenv("password_files")


def get_audio_duration(file_path):
    if file_path.lower().endswith('.mp3'):
        audio = MP3(file_path)
    elif file_path.lower().endswith(('.wav', '.wave')):
        audio = WAVE(file_path)
    else:
        raise ValueError("Unsupported file format")
    
    return audio.info.length  # Duration in seconds

def get_storage(password):
    # Check if the password is correct
    if password == password_files:
        # Get the list of file paths and calculate the total usage
        files = [
            file for file in persistent_storage.glob("**/*.csv") if file.is_file()
        ]
        
        # Calculate total usage (in bytes)
        usage = sum([file.stat().st_size for file in files])
        
        # Convert file paths to strings for Gradio's File component
        file_paths = [str(file.resolve()) for file in files]
        
        # Return the file paths (as strings) and the total usage in GB
        return file_paths, f"{usage / (1024.0 ** 3):.3f}GB"
    
    else:
        return gr.Warning("Please provide the correct password"), None

def count_clicks(n_clicks):
    n_clicks = n_clicks + 1
    return n_clicks