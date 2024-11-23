import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# Initialisation
recognizer = sr.Recognizer()

# Interface utilisateur
st.title("Amélioration de l'application de reconnaissance vocale")

# Choix de l'API
api_choice = st.selectbox("Choisissez l'API de reconnaissance vocale :", ["Google", "Sphinx"])

# Choix de la langue
languages = {
    "Français": "fr-FR",
    "Anglais": "en-US",
    "Espagnol": "es-ES",
    "Allemand": "de-DE"
}
language = st.selectbox("Choisissez la langue :", list(languages.keys()))

# Zone de transcription
st.text("Cliquez sur le bouton pour commencer la reconnaissance vocale.")
transcription_output = st.empty()

# Boutons Pause/Reprise
pause = st.button("Pause")
resume = st.button("Reprendre")

# Fonction pour enregistrer l'audio avec sounddevice
def record_audio(duration=5, samplerate=44100):
    st.write("Enregistrement en cours... Parlez maintenant.")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Attend que l'enregistrement se termine
    return samplerate, audio_data

# Fonction de transcription
def transcribe_speech():
    try:
        duration = st.slider("Durée de l'enregistrement (secondes) :", 1, 10, 5)
        samplerate, audio_data = record_audio(duration)
        
        # Sauvegarder temporairement l'audio pour le traitement par SpeechRecognition
        wav_file = "temp_audio.wav"
        write(wav_file, samplerate, audio_data)
        
        # Charger le fichier audio dans SpeechRecognition
        with sr.AudioFile(wav_file) as source:
            audio = recognizer.record(source)
            if api_choice == "Google":
                transcription = recognizer.recognize_google(audio, language=languages[language])
            elif api_choice == "Sphinx":
                transcription = recognizer.recognize_sphinx(audio, language=languages[language])
            else:
                transcription = "API non supportée pour le moment."

            return transcription

    except sr.UnknownValueError:
        return "Erreur : La reconnaissance vocale n'a pas compris l'audio."
    except sr.RequestError as e:
        return f"Erreur de connexion avec l'API : {e}"
    except Exception as e:
        return f"Une erreur inattendue est survenue : {e}"

# Enregistrement de la transcription
def save_transcription(text):
    with open("transcription.txt", "w") as f:
        f.write(text)
    st.success("Transcription enregistrée dans 'transcription.txt'.")

# Gestion Pause/Reprise
if resume:
    st.session_state["paused"] = False
if pause:
    st.session_state["paused"] = True

if "paused" not in st.session_state:
    st.session_state["paused"] = False

if not st.session_state["paused"]:
    if st.button("Commencer la reconnaissance"):
        transcription = transcribe_speech()
        transcription_output.text(transcription)

        if st.button("Enregistrer la transcription"):
            save_transcription(transcription)
