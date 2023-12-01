import speech_recognition as sr
from pykakasi import kakasi

def transcribe_and_convert_to_romaji(audio_file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="ja-JP")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None

def convert_to_romaji(japanese_text):
    converter = kakasi()
    converter.setMode("H", "a")  # Set to convert to Hepburn romanization
    romaji_text = converter.do(japanese_text)
    return romaji_text

# Example usage
audio_file_path = "audios/koigaoyogimasu.wav"
transcribed_text = transcribe_and_convert_to_romaji(audio_file_path)

if transcribed_text:
    print("Transcription (Romaji):", transcribed_text)
    # You can compare transcribed_text with your expected pronunciation
    # Add your pronunciation assessment logic here
