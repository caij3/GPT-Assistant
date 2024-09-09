import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
from pydub import AudioSegment
from pydub.playback import play

def play_audio(audio_file):
    audio = AudioSegment.from_file(audio_file)
    play(audio)

load_dotenv()

api_key = os.getenv("API_KEY")
region = os.getenv("REGION")

speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
audio_config = speechsdk.audio.AudioConfig(filename="audio.wav")

speech_synthesis_voice_name = "en-US-AriaNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config, audio_config)

text = "Hello there!".strip()

ssml = f"""<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
            <voice name="en-US-SaraNeural"><prosody rate="+20.00%" pitch="+40.00%">
                {text}
            </prosody></voice></speak>""".format(speech_synthesis_voice_name)
speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml).get()

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")