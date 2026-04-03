from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

@app.route("/personality", methods=["POST"])
def personality():
    data = request.get_json()
    text = data.get("text", "")

    prompt = f"""
    次の文章から、ユーザーの性格をやさしく、短く、温かくまとめてください。

    【入力】
    {text}
    """

    response = client.models.generate_content(
        model="models/text-bison-001",
        contents=prompt
    )

    result = response.text
    return jsonify({"result": result})

@app.route("/")
def home():
    return "AI server is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
