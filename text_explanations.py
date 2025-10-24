css = """#myProgress {
  width: 100%;
  background-color: var(--block-border-color);
  border-radius: 2px;
}

  #myBar {
    width: 0%;
    height: 30px;
    background-color: var(--block-title-background-fill);
    border-radius: 2px;
  } 

  #progressText {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%); 
    color: var(--block-title-text-color); 
    font-weight: regular; 
    font-size: 14px;
  }

  h1, h2, h3, h4 {
    padding: var(--block-title-padding);
    color: var(--block-title-text-color);
    border: solid var(--block-title-border-width) var(--block-title-border-color);
    border-radius: var(--block-title-radius);
    background: var(--block-title-background-fill);
    width: fit-content;
    display: inline-block;
  }

  h4 {
    margin: 0px;
    color: var(--block-title-background-fill);
    background: var(--block-title-text-color);
  }

  #instructions {
    max-width: 980px;
    align-self: center;
  }

  .content-box {
    border-color: var(--block-border-color);
    border-radius: var(--block-radius);
    background: var(--block-background-fill);
    padding: var(--block-label-padding);
  }


"""



js_progress_bar = """
    function move(start, end, total_duration, current_index, n_ann, total_ann) {
        var elem = document.getElementById("myBar");
        elem.style.width = n_ann/total_ann * 100 + "%";
        index = current_index + 1
        progressText.innerText = `${index} / ${total_ann} (Completed: ${n_ann})`;
        
        const waveform = document.querySelector('#audio_to_annotate #waveform div');
        const shadowRoot = waveform.shadowRoot;
        const canvases = shadowRoot.querySelector('.wrapper');
        console.log(canvases.offsetWidth)
        const leftOffsetPct = start / total_duration;
        const widthPct = (end - start) / total_duration;
        
        // Get CSS variable for background color
        const blockColor = getComputedStyle(document.documentElement)
            .getPropertyValue('--block-title-background-fill')
            .trim() || 'red'; // Default to red if variable is not found
        // Create a style element for the shadow DOM
        const style = document.createElement('style');
        style.textContent = `
        .wrapper::after {
            content: '';
            position: absolute;
            top: 0;
            left: ${canvases.offsetWidth * leftOffsetPct}px;
            width: ${canvases.offsetWidth * widthPct}px;
            height: 100%;
            background-color: blue;
            z-index: 999;
            opacity: 0.5;
        }
        /* Ensure parent has positioning context */
        .wrapper {
            position: relative;
        }
        `;
        // Append the style to the shadow root
        shadowRoot.appendChild(style);
        console.log(start + ' ' + end + ' ' + total_duration);
        console.log(n_ann + ' ' + total_ann);
    }
    """




intro_html = """

<h1>Emotionality in Speech</h1>
<div class="content-box">

    <p>Spoken language communicates more than just words. Speakers use tone, pitch, and other nonverbal cues to express emotions. In emotional speech, these cues can strengthen or even contradict the meaning of the words—for example, irony can make a positive phrase sound sarcastic. For this research, we will focus on three basic emotions plus neutral:</p>

    <ul>
    <li><h4>Anger</h4></li>
    <li><h4>Happiness</h4></li>
    <li><h4>Sadness</h4></li>
    <li><h4>Neutral</h4></li>
    </ul>

    <p>This may seem like a small set, but it's a great starting point for analyzing emotions in such a large collection— <strong>303 hours of interviews! (That’s 13 days of nonstop listening! &#128558)</strong> </p>
</div>

<h2>The ACT-UP Oral History Project</h2>

<div class="content-box">
    <p>You will be annotating short audio clips extracted from the ACT UP (AIDS Coalition to Unleash Power) Oral History Project developed by Sarah Schulman and Jim Hubbard . 
    This archive features interviews with individuals who were part of ACT UP during the late 1980s and early 1990s, amidst the AIDS epidemic. 
    In each video, the subjects talk about their life before the epidemic, how they were affected by AIDS and their work in ACT UP.</p>
</div>

<h2>What will you be annotating?</h2>
<div class="content-box">
    <p>You will annotate one emotion per short audio clip, based on the following criteria:</p>

    <ul>
        <li>
            <h4>Predominant Emotion:</h4> 
            The emotion expressed with the highest intensity. Emotions can be complex, and multiple emotions may occur at the same time.
        </li>
        
        <li>
            <h4>Perceived Emotion at the Time of Recording:</h4> 
            In Oral History Archives, interviewees discuss their past. However, you should annotate the emotion they appear to feel at the time of recording, NOT what they felt during the event they describe.
        </li>
        
        <li>
            <h4>Speech Emotionality:</h4> 
            Focus on how something is said rather than what is said. For example, if a friend recounts an awful day with humor, the content may be sad, but the delivery is joyful. In this case, linguistic emotionality (content) would be classified as sad, while paralinguistic emotionality (tone and delivery) would be classified as joyful.
        </li>
    </ul>

    <div style="text-align: center; padding: 1.5em 0;">
        <strong>If you're uncertain about which emotion you are hearing, open the sidebar by clicking the arrow in the upper left corner. There, you'll find a list of major emotions grouped under each category!</strong>
    </div>
</div>
"""

examples_explanation = """<h3>Audio examples</h3>
    <div class="content-box">
        <p>Let's check out examples for the four emotions to annotate. Note that all these examples use the same sentence and are acted out, making the emotionality in speech more apparent. In a real-world setting, emotionality is more complex, so you will find a list of additional emotions within each of the three emotion categories (Happy, Sad, and Angry) to assist you during annotation.</p>
    </div>"""
side_bar_html = """
<h3>Major subclasses</h3>
<div class="content-box">
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
        <span>&#128578;</span>
        <h4 style="margin: 0;">Happiness</h4>

    </div>
    
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
        <p>Affection, Goodwill, Joy, Satisfaction, Zest, Acceptance, Pride, Hope, Excitement, Relief, Passion, Caring</p>
    </div>

    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
        <span>&#128577;</span>
        <h4 style="margin: 0;">Sadness</h4>
    </div>
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
        <p>Suffering, Regret, Displeasure, Embarrassment, Sympathy, Depression</p>
    </div>
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
        <span>&#128545;</span>
        <h4 style="margin: 0;">Anger</h4>
    </div>
    <div>
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
        <p>Irritability, Torment, Jealousy, Disgust, Rage, Frustration</p>
        <p></p>
    </div>
</div>

"""

start_annotating = """<h2>How to use the annotation interface?</h2>
<div class="content-box">
    <ol>
        <li>
            Open the sidebar by clicking the arrow in the upper left corner.
        </li>
        <li>
            Enter the participant ID you received via email.
        </li>
        <li>
            Click <strong>"Let's go!"</strong> — this will lock your participant ID.
        </li>
        <li>
            You’ll be directed to the annotation interface. The task will resume where you left off (on the last example you annotated), or start from the first audio if this is your first session.
        </li>
        <li>
            When you finish all annotations, please send an email to <a href="mailto:f.pessanha@uu.nl">f.pessanha@uu.nl</a>.
        </li>
    </ol>
    <p><strong>Note:</strong> You can click on any part of the audio to start playing from that point. Please avoid clicking on the audio while it is playing (pause it first). This will not affect the program, but it will help us understand how you interact with the interface.</p>
    <div style="text-align: center; padding: 1.5em 0;">
        <p><strong>Below you can find an overview of the annotation interface.</strong></p>
    </div>

</div>"""