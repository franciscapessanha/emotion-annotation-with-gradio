# 🎧 Audio Annotation Web App

A simple and interactive web application for **emotion annotation** of audio files using Python and Gradio.  
Perfect for annotating `.wav` and `.mp3` files with customizable emotion labels, with data persistence on Hugging Face Spaces or a local setup.  

---

## 🚀 Features

- Load audio files from a selected directory for annotation.  
- Define different annotation groups with common files to annotate.  
- Choose an emotion label and assign a confidence score for each audio clip.  
- Add comments or notes in a dedicated section.  
- Save all annotations in a CSV file for easy export and analysis.  
- Navigate through multiple audio files and re-annotate as needed.  

**For Hugging Face:** Persistent storage integration allows multiple annotators to perform annotations simultaneously (designed for the Hugging Face Spaces `/data` folder).  

---

## ⚙️ Installation

Make sure you have **Python 3.7+** installed.

### 📦 Requirements
- Python 3.7 or higher  
- Gradio  
- Pandas  
- Mutagen  
- Openpyxl (if Excel export is used)  
- Hugging Face Hub (optional)  

Install the required Python libraries with:

```bash
pip install -r requirements.txt
```

Or install them individually:

```bash
pip install gradio pandas mutagen openpyxl huggingface_hub
```

---

## 📂 Folder Structure

```bash
/data
  ├─ /files_to_annotate/             # Audio files for annotation
  │    ├─ {sample_id}/               # ID for the interview in question (sentences are divided by interview — e.g., Interview 10; you can define other structures as needed)
  │    │    └─ {sample_id}_instance.wav   # All examples belonging to that interview  
  ├─ /emotion_examples/              # Example audio files for each emotion
  ├─ /temp/                          # Temporary folder
  │    └─ {annotator_id}_annotations_{timestamp}.csv   # Saved annotations (auto-generated)
  ├─ {annotator_id}_annotations.csv  # Saved annotations (auto-generated)
  └─ group_{group_id}.csv            # List of files to be annotated by {group_id}. 
                                     # The CSV file should contain the following columns: 
                                     # sample_id, participant, start, end, sentence. 
                                     # The 'start' and 'end' values correspond to the section of the audio to be highlighted. 
                                     # Check the example files provided under /examples/. 
                                     # This structure is easily customizable depending on your annotation task.
```

### Note:
- If running locally, set the variable `HUGGINGFACE` (under `utils.py`) to `False`.  
- Ensure that the audio files are placed inside their corresponding folders before starting the app.  
- If running on Hugging Face, define the `password` under the **"Access Files"** tab in **Settings → Variables and Secrets**.  
  This allows you to securely access the files in the `/data` folder outside of development mode without exposing your password in the code.  

---

## 🔧 Usage locally

1. Run the app:  
   ```bash
   python app_huggingface.py
   ```
2. The app will open in your browser.  
3. Select emotions from the dropdown for each audio clip.  
4. Click **Save** and **Next** to save annotations and move to the next file.  
5. Use **Save Current Annotation** if you want to save without moving to the next file.  

---

## 🎯 Deployment on Hugging Face

This app is designed to work on **Hugging Face Spaces** with persistent storage at `/data`.  

To deploy:
1. Upload your app code.  
2. Place audio files in `/data/files_to_annotate/`.  
3. Start the Space and begin annotating!  
