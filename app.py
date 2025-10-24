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
from load_and_save import *



# ===================
# Gradio Interface
# ===================
with (gr.Blocks(theme=gr.themes.Soft(), css = css) as demo):
    # List of all audio files to annotate

    # Instructions for emotion annotation
    with gr.Sidebar(open = True) as sidebar:
        participant_id = gr.Textbox(label='What is your participant ID?', interactive = True)
        lets_go = gr.Button("Let's go!")
        cheat_sheet = gr.HTML(side_bar_html, padding = False)

    with gr.Tab("Instructions", elem_id = 'instructions'):
        instructions = gr.HTML(intro_html, padding = False)

        with gr.Blocks():
            description = gr.HTML(examples_explanation, padding = False)

            with gr.Accordion(label = "Neutral", open= False):
                neutral_audio = gr.Audio(value=f'{storage}/emotion_examples/neutral.wav', label ="Neutral")

            with gr.Accordion(label = "Happy",  open = False):
                happy_audio = gr.Audio(value=f'{storage}/emotion_examples/happy_low.wav', label ="Happy (Low Intensity)")
                happy_int_audio = gr.Audio(value=f'{storage}/emotion_examples/happy_intense.wav', label ="Happy (High Intensity)")

            with gr.Accordion(label = "Sad",  open = False):
                sad_audio = gr.Audio(value=f'{storage}/emotion_examples/sad_low.wav', label ="Sad (Low Intensity)")
                sad_int_audio = gr.Audio(value=f'{storage}/emotion_examples/sad_intense.wav', label ="Sad (High Intensity)")

            with gr.Accordion(label = "Anger",  open = False):
                angry_audio = gr.Audio(value=f'{storage}/emotion_examples/angry_low.wav', label ="Anger (Low Intensity)")
                angry_int_audio = gr.Audio(value=f'{storage}/emotion_examples/angry_intense.wav', label ="Anger (High Intensity)")

        instructions = gr.HTML(start_annotating, padding = False)
        image = gr.Image(label = "Annotation Interface", value = f"{storage}/instructions_annotation.png", container = False, type ="filepath", show_label = False, show_download_button = False, show_fullscreen_button = False, show_share_button = False)



    with gr.Tab("Annotation Interface") as ann_interface:
        ann_completed = gr.State(0)
        ann_completed_temp = gr.Number(0, visible = False)
        total = gr.State(0)
        total_temp = gr.Number(0, visible = False)
        current_index = gr.State(0)
        current_index_temp = gr.Number(0, visible = False)
        start = gr.State(0.0)
        start_temp = gr.Number(0, visible = False)
        end = gr.State(0.0)
        end_temp = gr.Number(0, visible = False)
        duration = gr.State(0.0)
        duration_temp = gr.Number(0, visible = False)
        n_clicks = gr.State(0)

        part_id = gr.State('')


        annotations = gr.State(pd.DataFrame())
        file_list = gr.State(pd.DataFrame())


        # Row with progress bar

        gr.HTML("""
        <div id="myProgress">
        <div id="myBar">
        <span id="progressText">Press "Let's go!" to start</span> 
        </div>
        </div>
        """, padding = False)

        # Row with audio player
        with gr.Row():
            audio_player = gr.Audio(value= 'blank.mp3', label="Audio", type="filepath", interactive=False, show_download_button = False, show_share_button = False, elem_id = "audio_to_annotate")

        # Hidden row with corresponding sentence
        with gr.Row():
            accordion = gr.Accordion(label="Click to see the sentence", open=False)
            with accordion:
                sentence_text = gr.Textbox(label="Transcription", interactive=False, value = 'This is a sentence.')
        # Row for emotion annotation and confidence
        with gr.Row():
            emotions = gr.Radio(["Blank", "Joy", "Sad", "Angry", "Neutral"], label="Predominant Emotion", value = "Blank", visible = False)

        with gr.Row():
            confidence = gr.Radio(["Blank","Very Uncertain", "Somewhat Uncertain", "Neutral", "Somewhat confident", "Very confident"], label="How confident are you that the annotated emotion is present in the recording?", visible = False)

        with gr.Row():
            # Comment section
            comments = gr.Textbox(label="Comments", visible =False)

        # Next and Previous Buttons
        with gr.Row():
            previous_button = gr.Button("Previous Example", visible = False)
            next_button = gr.Button("Next Example", visible = False)

        # Go back

        previous_button.click(
            previous_example,
            inputs=[annotations, file_list, emotions, confidence, comments, n_clicks, participant_id,  ann_completed , current_index],
            outputs=[annotations, sentence_text, audio_player, emotions, confidence, comments, n_clicks, start, end, duration,
            ann_completed, current_index],).then(state_to_number, [start, end, duration, current_index, ann_completed, total],
            [start_temp, end_temp, duration_temp, current_index_temp, ann_completed_temp, total_temp]).then(None, [],
            [start_temp, end_temp, duration_temp, current_index_temp,
            ann_completed_temp, total_temp], js = js_progress_bar)

        # Go to the next example
        next_button.click(
            next_example,
            inputs=[annotations, file_list,emotions, confidence, comments, n_clicks, participant_id, start, end, duration, ann_completed, current_index],
            outputs=[annotations,sentence_text, audio_player, emotions, confidence, comments, n_clicks, start, end, duration, ann_completed,
            current_index],).then(state_to_number, [start, end, duration, current_index, ann_completed, total],
            [start_temp, end_temp, duration_temp, current_index_temp, ann_completed_temp, total_temp]).then(None, [],
            [start_temp, end_temp, duration_temp, current_index_temp,
            ann_completed_temp, total_temp], js = js_progress_bar)



        buttons = [previous_button, next_button]
        data = [sentence_text, audio_player, emotions, confidence, comments]

        lets_go.click(deactivate_participant_id, [annotations, file_list,  total, participant_id,
        lets_go, *buttons, *data, n_clicks, ann_completed, current_index],
        [annotations, file_list, participant_id, part_id, lets_go, total, *buttons,
        *data, n_clicks, start, end, duration, ann_completed, current_index]).then(state_to_number, [start, end, duration, current_index, ann_completed, total],
        [start_temp, end_temp, duration_temp, current_index_temp, ann_completed_temp, total_temp]).then(None, [],
        [start_temp, end_temp, duration_temp, current_index_temp,
        ann_completed_temp, total_temp], js = js_progress_bar)

        audio_player.play(count_clicks, [n_clicks], [n_clicks])

        sidebar.collapse(state_to_number, [start, end, duration, current_index, ann_completed, total],
        [start_temp, end_temp, duration_temp, current_index_temp, ann_completed_temp, total_temp]).then(None, [], [start_temp, end_temp, duration_temp, current_index_temp, ann_completed_temp, total_temp], js = js_progress_bar)

        sidebar.expand(state_to_number, [start, end, duration, current_index, ann_completed, total],
        [start_temp, end_temp, duration_temp, current_index_temp, ann_completed_temp, total_temp]).then(None, [], [start_temp, end_temp, duration_temp, current_index_temp, ann_completed_temp, total_temp], js = js_progress_bar)

    ann_interface.select(state_to_number, [start, end, duration, current_index, ann_completed, total],
        [start_temp, end_temp, duration_temp, current_index_temp, ann_completed_temp, total_temp]).then(None, [], [start_temp, end_temp, duration_temp, current_index_temp, ann_completed_temp, total_temp], js = js_progress_bar)


    if HUGGINGFACE: # The interface to access files is only necessary when using huggingface.
        # Files are easily accessible when ran locally.
        with gr.Tab("Access Files"):

            with gr.Row():
                password = gr.Textbox(label="Enter Password", type="password")
                get_files_button = gr.Button("Get Files")

            with gr.Column():
                files = gr.File(label="Download Files", file_count="multiple", interactive=True)
                storage_use = gr.Text(label="Total Usage")

            get_files_button.click(fn=get_storage, inputs=[password], outputs=[files, storage_use])



demo.launch(allowed_paths = ['/data'])

