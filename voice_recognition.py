import speech_recognition as sr

# Name of the audio file generated
FILENAME = "audio/mic.mp3"
RECOGNIZER = sr.Recognizer()

# Set the microphone ID
# MIC_ID = 1

# Set to True to utilize WhisperAI
USE_WHISPER = False

# Use WhisperAI to transcribe text
if USE_WHISPER:
    try:
        import whisper
    except Exception as e:
        print("Whisper library not installed. Please use command: pip install openai-whisper")
    model = whisper.load_model("base")

# Listens to audio
def get_audio():
    mic = sr.Microphone()
    # Use if you are manually setting microphone
    # mic = sr.Microphone(device_index=MIC_ID)
    with mic as source:
        print("listening")
        audio = RECOGNIZER.listen(source)
    return audio

# Transcribe audio to text using either Google or Whiseper AI
def recognize_audio(audio,use_whisper=False):
    if use_whisper:
        return recognize_audio_whisper(audio)
    else:
        return recognize_audio_google(audio)

# Transcribe audio using Google
def recognize_audio_google(audio):
    said = ""
    try:
        said = RECOGNIZER.recognize_google(audio)
        if not said:
            return ""
        print("Input: " + said)
    except Exception as e:
        print(e)
    return said

# Transcribe audio using Whisper AI
def recognize_audio_whisper(audio):
    with open (FILENAME, 'wb') as f:
        f.write(audio.get_wav_data())
    result = model.transcribe(str(FILENAME))
    print("Input: " + result["text"])
    return result["text"]