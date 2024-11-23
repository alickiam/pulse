from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio_with_speaker_diarization(audio_path, output_file):

    client = speech.SpeechClient()

    speech_file = audio_path

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=10,
    )

    config = speech.RecognitionConfig(
        # must use a compatible audio file
        # encoding: LINEAR16(PCM)
        # sample rate: 8000Hz
        # can use FFmpeg to convert audio files to required formats
        # example: ffmpeg -i input.wav -ar 8000 -ac 1 output.wav
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="en-US",
        diarization_config=diarization_config,
    )

    print("Waiting for operation to complete...")
    response = client.recognize(config=config, audio=audio)

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:
    result = response.results[-1]
    words_info = result.alternatives[0].words

    # group words by speaker tag
    conversation = {}
    for word_info in words_info:
        speaker_tag = word_info.speaker_tag
        if speaker_tag not in conversation:
            conversation[speaker_tag] = []
        conversation[speaker_tag].append(word_info.word)

    formatted_conversation = ""
    for speaker_tag, words in conversation.items():
        speaker_label = f"Person {speaker_tag}"
        transcript = " ".join(words)
        formatted_conversation += f"{speaker_label}: {transcript} \n\n"

    with open(output_file, "w") as file:
        file.write(formatted_conversation)

    print("uploaded transcript successfully to {output_file}")
    
    return result

    # for word_info in words_info:
    #     print(f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}")

if __name__ == '__main__':
    audio_path = "resources/commercial_mono.wav"
    output_file = "transcribed_conversation.txt"
    result = transcribe_audio_with_speaker_diarization(audio_path, output_file)
