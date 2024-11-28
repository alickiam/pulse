import os
from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio_with_speaker_diarization(audio_path, output_file):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./se101finalproject-1a2f5a3e9286.json"

    client = speech.SpeechClient()
    print("Google Cloud credentials loaded successfully.")

    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=10,
    )

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        diarization_config=diarization_config,
    )

    print("Waiting for operation to complete...")
    response = client.recognize(config=config, audio=audio)

    result = response.results[-1]
    words_info = result.alternatives[0].words

    print("Starting to organize the transcribed text file.")
    
    # Prepare a list of tuples (start_time, speaker_tag, word)
    conversation = []
    for word_info in words_info:
        start_time = word_info.start_time.total_seconds()
        speaker_tag = word_info.speaker_tag
        word = word_info.word
        conversation.append((start_time, speaker_tag, word))

    # Sorting the conversation by start time
    conversation.sort(key=lambda x: x[0])

    # Group the conversation by speaker
    formatted_conversation = ""
    current_speaker = None
    speaker_text = []

    for _, speaker_tag, word in conversation:
        if speaker_tag != current_speaker:
            # If switching to a new speaker, append the previous speaker's text
            if current_speaker is not None:
                formatted_conversation += f"Person {current_speaker}: {' '.join(speaker_text)}\n"
            current_speaker = speaker_tag
            speaker_text = []
        speaker_text.append(word)

    # Append the last speaker's text
    if current_speaker is not None:
        formatted_conversation += f"Person {current_speaker}: {' '.join(speaker_text)}\n"

    # Write the formatted conversation to the output file
    with open(output_file, "w") as file:
        file.write(formatted_conversation)

    print(f"Uploaded transcript successfully to {output_file}")
    return result

if __name__ == '__main__':
    audio_path = "audio (1).wav"
    output_file = "transcribed_conversation.txt"
    result = transcribe_audio_with_speaker_diarization(audio_path, output_file)
