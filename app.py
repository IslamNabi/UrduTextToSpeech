from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import uuid

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ----------------- Frontend Route -----------------
@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    if request.method == "POST":
        text = request.form.get("text")

        if not text:
            return render_template("index.html", audio_file=None, error="Please enter some text.")

        # Generate a unique filename
        filename = f"static/{uuid.uuid4().hex}.mp3"

        # Call OpenAI TTS
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",  # voices: alloy, verse, sage, shimmer
            input=text
        )

        # Save audio file
        with open(filename, "wb") as f:
            f.write(response.content)

        audio_file = filename

    return render_template("index.html", audio_file=audio_file)


# ----------------- REST API Route -----------------
@app.route("/api/tts", methods=["POST"])
def api_tts():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Generate unique filename
    filename = f"static/{uuid.uuid4().hex}.mp3"

    # Call OpenAI TTS
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    # Save file
    with open(filename, "wb") as f:
        f.write(response.content)

    return jsonify({"audio_url": filename})


# ----------------- Run App -----------------
if __name__ == "__main__":
    app.run(debug=True)
