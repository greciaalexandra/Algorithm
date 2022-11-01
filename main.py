import os

from flask_cors import cross_origin
from google.cloud import speech
from flask import Flask, redirect, url_for, request
app = Flask(__name__)

import RAKE

stop_dir = "SmartStoplist.txt"
rake_object = RAKE.Rake(stop_dir)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cloud_admin.json'
speech_client = speech.SpeechClient()

@app.route('/speech',methods=['POST'])
@cross_origin()
def usuario():
    media_file_name_mp3 = request.files['file']

    byte_data_mp3 = media_file_name_mp3.read()
    audio_mp3 = speech.RecognitionAudio(content=byte_data_mp3)
    config_mp3 = speech.RecognitionConfig(
        sample_rate_hertz=48000,
        enable_automatic_punctuation=True,
        language_code='es-Es'
    )
    response_standard_mp3 = speech_client.recognize(
        config=config_mp3,
        audio=audio_mp3
    )
    response = response_standard_mp3.results[0].alternatives[0].transcript
    keywords = rake_object.run(response)
    list=[]
    for x in keywords:
        print(x)
        list.append(x[0])
    return {"speech":response,"keywords":list}

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)