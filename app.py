from flask import Flask, render_template, request, jsonify
import requests
import pyttsx3
import speech_recognition as sr
from transformers import pipeline
from flask import send_from_directory

app = Flask(__name__)

# GPT-2 model
chatbot = pipeline("text-generation", model="gpt2")

# Text-to-Speech setup
#tts_engine = pyttsx3.init()

# Replace with your API keys
WEATHER_API_KEY = "3c8ee3c1011b4798d44a8030d58fc245"
JOKE_API_URL = "https://official-joke-api.appspot.com/random_joke"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
# this is my account api key you can register on newsapi.org for your  api key
NEWS_API_KEY = "07046e24b5084e4597cfb28e88af454d"



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/weather", methods=["POST"])
def get_weather():
    city = request.args.get('city', 'Unknown')
    
    if not city:
        return jsonify({"error": "City not provided"}), 400

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"
  
    response = requests.get(weather_url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return jsonify({
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        })
    else:
        return jsonify({"error": "Unable to fetch weather"}), 500



@app.route("/joke", methods=["GET"])
def get_joke():
    response = requests.get(JOKE_API_URL)
    print(response)
    if response.status_code == 200:
        data = response.json()
        return jsonify({"setup": data["setup"], "punchline": data["punchline"]})
    else:
        return jsonify({"error": "Unable to fetch joke"}), 500



@app.route('/news', methods=['POST'])
def get_news():
    
    country = request.json.get('message','us')
    print(country)
    news_url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={NEWS_API_KEY}"
    
    response = requests.get(news_url)
    print(response)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return jsonify({'articles': articles})
    else:
        return jsonify({"error": "Unable to fetch news"}), 500


@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({"error": "Input not provided"}), 400
    print(user_input)
    response = chatbot(user_input, max_length=150, num_return_sequences=1)
    return jsonify({"reply": response[0]["generated_text"]})





@app.route("/tts", methods=["POST"])
def text_to_speech():
    text = request.json.get("text")
   
    if not text:
        return jsonify({"error": "Text not provided"}), 400
    
    # Initialize a new instance of the TTS engine
    tts_engine = pyttsx3.init()

    # Configure the TTS engine if needed (optional)
    tts_engine.setProperty('rate', 150)  # Set speaking rate
    tts_engine.setProperty('volume', 1.0)  # Set volume (0.0 to 1.0)

    try:
        # Speak the provided text
        tts_engine.say(text)
        tts_engine.runAndWait()

        # Stop the engine and clean up
        tts_engine.stop()
        return jsonify({"message": "Text spoken successfully"})
    except Exception as e:
        tts_engine.stop()  # Ensure the engine is stopped on error
        return jsonify({"error": str(e)}), 500


@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening for speech...")
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            return jsonify({"text": text})
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand the audio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"API request error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')



if __name__ == '__main__':
    app.run(debug=True)