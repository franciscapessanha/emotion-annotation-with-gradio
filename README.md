# 🎧 Audio Annotation Web App

A simple and interactive web application for **emotion annotation** of audio files using Python and Gradio.  
Perfect for annotating `.wav` and `.mp3` files with customizable emotions, with data persistence on Hugging Face Spaces or local setup. 

---

## 🚀 Features

- Load audio files from a directory for annotation  
- Choose emotions from a dropdown menu for each audio clip  
- Save annotations as CSV for easy export and analysis  
- Persistent storage integration allowing multiple annotators to perform annotations simultaneously (designed for Hugging Face Spaces `/data` folder)  
- Navigate through multiple audio files and re-annotate if needed

---

## ⚙️ Installation

Make sure you have Python 3.7+ installed.

📦 Requirements
- Python 3.7 or higher
- Gradio
- Pandas
- Mutagen
- Openpyxl (if Excel export is used)
- Huggingface Hub (optional)

Install the required Python libraries with:

```bash
pip install -r requirements.txt
```
Or install individually:

``` bash
pip install gradio pandas mutagen openpyxl huggingface_hub
```

## 📂 Folder Structure
``` bash
/data
  ├─ /files_to_annotate/    # Audio files for annotation
  ├─ /emotion_examples/             # Example audio files for each emotion
  └─ annotations.csv                # Saved annotations (auto-generated)
```
### Note:
If running locally, change the persistent_storage path in the code from /data to your local folder (e.g., ./data)
Ensure the audio files are placed inside the corresponding folders before starting the app.

## 🔧 Usage
1. Run the app:
```bash
python app_huggingface.py
```
2. The app opens in your browser.
3. Select emotions from the dropdown for each audio clip.
4. Click **Save** and **Next** to save annotations and move to the next file.
5. Use **Save Current Annotation** if you want to save without moving on.


## 🎯 Deployment in Hugging Face

Designed to work on Hugging Face Spaces with persistent storage at /data.
To deploy:
1. Upload your app code
2. Place audio files in /data/files_to_annotate/
S3. tart the space and annotate!

