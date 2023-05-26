from flask import Flask, render_template, request, jsonify
import openai
import base64
app = Flask(__name__)

openai.api_key = "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"
messages = [{"role": "system", "content": 'Respond to all input in  1 point short'}]
transcript=""
@app.route('/')

def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global transcript
    audio = request.form['audioI']
    # audio = request.form
    
    
    data_url=audio
    wav_file = open("temp.wav", "wb")
    
    
    header, encoded_data = data_url.split(',', 1)
    decoded_data = base64.b64decode(encoded_data)
    
    wav_file.write(decoded_data)
    
    wav_file.close()
    audio= 'temp.wav'
    
    audio_file= open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # print(transcript)
    transcript=transcript.text
    # return ret(transcript)
    return jsonify({'response': transcript})



@app.route('/reter', methods=['POST'])
def reter():
    global messages
    transcript= request.form['audioI']
    
    messages.append({"role": "user", "content": transcript})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    system_message = response["choices"][0]["message"]
    messages.append(system_message)

   # subprocess.call(["say", system_message['content']])
    chat_transcript = ""
    chat_transcript +=messages[-1]['content'] + "\n"
    # print(chat_transcript)
    
    
    return jsonify({'response': chat_transcript})

if __name__ == '__main__':
    app.run(debug=True)
    
