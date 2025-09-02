from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os
import uuid

# Load environment variables from .env file
load_dotenv()

# Initialize Flask
app = Flask(__name__)

# Initialize OpenAI client with API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    if request.method == "POST":
        text = request.form["text"]

        # Generate a unique filename
        filename = f"static/{uuid.uuid4().hex}.mp3"

        # Call OpenAI TTS
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",  # you can try: alloy, verse, sage, etc.
            input=text
        )

        # Save audio file
        with open(filename, "wb") as f:
            f.write(response.content)

        audio_file = filename

    return render_template("index.html", audio_file=audio_file)

if __name__ == "__main__":
    app.run(debug=True)
