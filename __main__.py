import base64
import os
import string
import time

import speech_recognition as sr
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from gevent import pywsgi
from openai import OpenAI


class AIAudioReplier:
    def __init__(self, file_path):
        self._file_path = file_path

    def get_file_path(self) -> string:
        return self._file_path

    def read_text_from_audio(self, language) -> string:
        with sr.AudioFile(self._file_path) as source:
            recognizer = sr.Recognizer()
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=language)
            return text

    @staticmethod
    def ask_ai(text):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": os.getenv("OPENAI_CONTENT")
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        return completion.choices[0].message.content


app = Flask(__name__)


@app.route("/answer-to-audio", methods=["POST"])
def _answer_to_audio():
    """
    This function is responsible for handling the POST request to the /answer-to-audio endpoint.
    Input data example: {"data": "base64_encoded_audio_file"}
    :return: A json response containing the extracted text from the audio file and the AI response.
    """
    # Save a timestamp to avoid concurrency issues
    timestamp = str(time.time()).replace(".", "_")
    audio_replier = AIAudioReplier(f"{timestamp}")
    # Start parsing the request
    encoded_bytes = request.get_json()["data"]
    file_data = base64.b64decode(encoded_bytes)
    with open(audio_replier.get_file_path(), "wb") as fw:
        fw.write(file_data)
    # Read the text from the audio file
    audio_language = os.getenv("AUDIO_LANGUAGE")
    extracted_text = audio_replier.read_text_from_audio(audio_language)
    ai_response = audio_replier.ask_ai(extracted_text)
    os.remove(audio_replier.get_file_path())
    return jsonify({"data": extracted_text, "response": ai_response})


if __name__ == "__main__":
    load_dotenv()
    s1 = pywsgi.WSGIServer(("0.0.0.0", 80), app)
    s1.serve_forever()
