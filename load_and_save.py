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
from datetime import datetime

"""
possible_ids = {"annotator": "annotation_group"} for example:

possible_ids = {'Elephant-003': 1, 'Panther-004': 1,
                 'Zebra-005': 2, 'Wolf-006': 2,
                 'Koala-007': 3, 'Otter-008': 3,
                 'Leopard-009': 4, 'Panda-010': 4,
                 'Cheetah-011': 5, 'Gorilla-012': 5,
                 'Dolphin-013' : 6, 'Lynx-014': 6,
                 'Moose-015': 7, 'Raccoon-016': 7,
                 'Rabbit-017': 0, 'Eagle-018': 8, 'Jaguar-019': 8}
There should be an csv file named "group_#number.csv" under data with the columns: sample_id,participant,start,end,sentence
"""
possible_ids = {'Example-001': 0, 'Example-002': 0}



def load_first_example(annotations_df, file_list_df, id, completed, index):
    """ Loads and first example and updates index
    
    Parameters:
    * annotations_df: annotation file
    * file_list_df: files to annotate
    * id: participant ID
    * completed: number of examples annotated
    * index: current index (in the files to annotate list)

    return:
    * annotations_df: dataframe with current annotations
    * load_example: current example to annotate
    * completed: updated number of completed annotations
    * index: updated current index

    """
    path_ann = f'{storage}/{id}_annotations.csv'

    if os.path.exists(path_ann):
        annotations_df = pd.read_csv(path_ann, keep_default_na=False)
        index = min(len(file_list_df) - 1, len(annotations_df))
        completed = len(annotations_df) # update how many examples were completed

    else: 
        # Initialize an empty DataFrame to store annotations
        annotations_df = pd.DataFrame(columns=['sample_id', 'sentence', 'emotion', 'confidence', 'comments', 'n_clicks'])

    return annotations_df, *load_example(annotations_df, file_list_df, index), completed, index


def load_example(annotations_df, file_list_df, index):
    """Loads the example in row #index from dataframe file_list. 
    If there are any annotations it will give those values to the annotation dataframe
    
    Parameters:
    * annotations_df: dataframe with current annotations
    * index: current index
    
    
    Returns:
    * sentence: current sentence
    * audio_path: current_audio path
    * ann['emotion']: current emotion
    * ann['confidence']: current confidence
    * ann['comments']: current comments
    * ann['n_clicks']: current number of clicks
    * start: current start
    * end: current end
    * duration: current sentence duration
    
    """
    if index < len(file_list_df):
        row = file_list_df.iloc[index]
        audio_path = os.path.join(storage, 'files_to_annotate', row["sample_id"].split('-')[0], row["sample_id"] + '.wav')
        sentence = row["sentence"]

        # If the user already made an annotation for this example, gradio will return said annotation
        ann = (
            annotations_df.iloc[index].to_dict() if index < len(annotations_df) else {"sample_id": row["sample_id"], "emotion": 'Blank', "confidence": 'Blank',
                                                                                "comments": '', "n_clicks": 0}
        )

        start = row['start']
        end = row['end']
        duration = get_audio_duration(audio_path)

    else:
        index -= 1
        row = file_list_df.iloc[index]
        audio_path = os.path.join(storage, 'files_to_annotate', row["sample_id"].split('-')[0], row["sample_id"] + '.wav')
        sentence = row["sentence"]

        # If the user already made an annotation for this example, gradio will return said annotation
        ann = (
            annotations_df.iloc[index].to_dict() if index < len(annotations_df) else {"sample_id": row["sample_id"], "emotion": 'Blank', "confidence": 'Blank',
                                                                                "comments": '', "n_clicks": 0}
        )

        start = row['start']
        end = row['end']
        duration = get_audio_duration(audio_path)

        gr.Warning("This is the last example, well done!")
    return sentence, audio_path, ann['emotion'], ann['confidence'], ann["comments"], ann['n_clicks'], start, end, duration


def save_annotation(annotations_df, file_list_df, emotions, confidence, comments, n_clicks, participant_id, ann_completed, current_index):
    """Save the annotation for the current example.
    
    Parameters:
    * annotations_df: dataframe with all annotations so far
    * file_list_df: list of files to annotate
    * emotions, confidence, comments, n_clicks: annotations to save
    * participant_id: to indicate where to save the annotations
    * ann_completed: number of annotations completed
    * current_index: current index
    
    Return:
    * annotations_df: updated annotations_df
    * ann_completed: updated number of annotations completed
    """

    row = file_list_df.iloc[current_index]
    sample_id = row["sample_id"]
    sentence = row["sentence"]

    # Update or append annotation
    if sample_id in annotations_df["sample_id"].values:
        annotations_df.loc[annotations_df["sample_id"] == sample_id, ["emotion", "confidence", "comments", "n_clicks"]] = \
            [emotions, confidence, comments, n_clicks]
    else:
        annotations_df.loc[len(annotations_df)] = [sample_id, sentence, emotions, confidence, comments, n_clicks]
        ann_completed += 1
    annotations_df.to_csv(f"{storage}/{participant_id}_annotations.csv", index=False)  # Save to a CSV file

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    annotations_df.to_csv(f"{storage}/temp/{participant_id}_annotations_{timestamp}.csv", index=False)  # Save to a CSV file
    
    return annotations_df, ann_completed

def next_example(annotations_df, file_list_df, emotions, confidence, comments, n_clicks, participant_id, start, end, duration, ann_completed, current_index):
    """Move to the next example.

    Parameters:
    * annotations_df: current annotation dataframe
    * file_list_df: all files to annotate
    * emotions, confidence, comments, n_clicks: annotations to save
    * participant_id: to indicate where to save the annotations
    * ann_completed: number of annotations completed
    * current_index: current index

    Return:
    * annotations_df: updated annotations_df
    
    
    * sentence: current sentence
    * audio_path: current_audio path
    * ann['emotion']: current emotion
    * ann['confidence']: current confidence
    * ann['comments']: current comments
    * ann['n_clicks']: current number of clicks
    * start: current start
    * end: current end
    * duration: current sentence duration

    * ann_completed: updated number of annotations completed
    * current_index: current index

    """

    if emotions == "Blank":
        gr.Warning("Please fill out the emotion section. 'Blank' is not a valid emotion.")
    elif confidence == "Blank":
        gr.Warning("Please fill out the confidence section. 'Blank' is not a valid input.")

    else:  
        annotations_df, ann_completed = save_annotation(annotations_df, file_list_df, emotions, confidence, comments, n_clicks, participant_id, ann_completed, current_index)
        if current_index < len(file_list_df):
            current_index += 1

        else:
           gr.Warning("This is the last example, well done!")

    sentence, audio_path, emotion, confidence, comments, n_clicks, start, end, duration = load_example(annotations_df,
                                                                                                       file_list_df,
                                                                                                       current_index)
    return annotations_df, sentence, audio_path, emotion, confidence, comments, n_clicks, start, end, duration, ann_completed, current_index

def previous_example(annotations_df, file_list_df, emotion, confidence, comments, n_clicks, participant_id,  ann_completed, current_index):

    """Move to the previous example.

    Parameters:
    * annotations_df: current annotation dataframe
    * file_list_df: all files to annotate
    * emotions, confidence, comments, n_clicks: annotations to save
    * participant_id: to indicate where to save the annotations
    * ann_completed: number of annotations completed
    * current_index: current index

    Return:
    * annotations_df: updated annotations_df
    
    
    * sentence: current sentence
    * audio_path: current_audio path
    * ann['emotion']: current emotion
    * ann['confidence']: current confidence
    * ann['comments']: current comments
    * ann['n_clicks']: current number of clicks
    * start: current start
    * end: current end
    * duration: current sentence duration

    * ann_completed: updated number of annotations completed
    * current_index: current index
    """

    if emotion != "Blank":
        annotations_df, ann_completed = save_annotation(annotations_df, file_list_df, emotion, confidence, comments, n_clicks, participant_id,  ann_completed, current_index)
        
    if current_index > 0:
        current_index -= 1

    return annotations_df, *load_example(annotations_df, file_list_df, current_index), ann_completed, current_index


def deactivate_participant_id(annotations_df, file_list_df, total, participant_id, lets_go, previous_button, next_button, sentence_text, audio_player, emotions, confidence, comments, n_clicks, ann_completed, current_index):


    if participant_id in possible_ids.keys():
        file_list_df = pd.read_csv(os.path.join(storage, 'files_to_annotate', f'group_{possible_ids[participant_id]}.csv'), keep_default_na=False)

        total = len(file_list_df)
    

        annotations_df, sentence, audio_player, emotions, confidence, comments, n_clicks, start, end, duration, ann_completed, current_index = load_first_example(annotations_df, file_list_df, participant_id, ann_completed, current_index)
  
        participant_id = gr.Textbox(label='What is your participant ID?', value = participant_id, interactive = False)
        lets_go = gr.Button("Participant selected!", interactive = False)
        
        sentence_text = gr.Textbox(label="Transcription", interactive=False, value = sentence)
        emotions = gr.Radio(["Blank", "Happy", "Sad", "Angry", "Neutral"], label="Predominant Emotion (Check the sidebar for major subclasses)", value =  emotions, visible = True)
        confidence = gr.Radio(["Blank","Very Uncertain", "Somewhat Uncertain", "Neutral", "Somewhat confident", "Very confident"], label="How confident are you that the annotated emotion is present in the recording?", visible = True, value = confidence)
        comments = gr.Textbox(label="Comments", visible =True, value = comments)
        previous_button = gr.Button("Previous Example", visible = True)
        next_button = gr.Button("Next Example",visible = True)
        
        return annotations_df, file_list_df, participant_id, participant_id, lets_go, total, previous_button, next_button, sentence_text, audio_player, emotions, confidence, comments, n_clicks, start, end, duration, ann_completed, current_index

    else:
        raise gr.Error("Please insert a valid participant ID")