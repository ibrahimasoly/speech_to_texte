import streamlit as st
import speech_recognition as sr
import time

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

# Fonction de transcription
def transcribe_speech():
    try:
        with sr.Microphone() as source:
            st.write("En attente de votre voix... Parlez maintenant.")
            recognizer.adjust_for_ambient_noise(source)  # Ajuste le bruit de fond
            audio = recognizer.listen(source)

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

