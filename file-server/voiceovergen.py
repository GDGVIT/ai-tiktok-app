from gtts import gTTS
import os
async def generate_voiceover(text, output_file="output_voiceover.mp3"):
    """
    Generate a voiceover from text and save it as an audio file.

    Args:
        text (str): The text to convert to speech.
        output_file (str): The name of the output audio file (default: "output_voiceover.mp3").
    """
    # Initialize the TTS object
    tts = gTTS(text)

    # Save the speech as an audio file
    tts.save(output_file)

    # Play the generated audio (optional)
    os.system(f"mpg321 {output_file}")  # You can use other audio players if needed
