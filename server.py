from flask import Flask, request, jsonify
import google.genai as genai
import os

app = Flask(__name__)

# ---------------------------
# Google AI API クライアント設定
# ---------------------------
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# ---------------------------
# 性格診断 API（PythonAnywhere から呼ばれる）
# ---------------------------
@app.route("/personality", methods=["POST"])
def personality():
    data = request.get_json()

    name = data.get("name", "")
    birthday = data.get("birthday", "")
    birthplace = data.get("birthplace", "")
    birthtime = data.get("birthtime", "")
    mbti = data.get("mbti", "")

    prompt = f"""
以下の情報をもとに、四柱推命・ホロスコープ・MBTI の観点を統合して、
その人の特徴、強み、弱み、今後の動き方を優しくまとめてください。

- 名前: {name}
- 生年月日: {birthday}
- 生まれた場所: {birthplace}
- 生まれた時間: {birthtime}
- MBTI: {mbti}

文章は読みやすく、前向きで、安心できるトーンにしてください。
"""

    response = client.models.generate_content(
        model="models/text-bison-001",
        contents=prompt
    )

    return jsonify({"result": response.text})

# ---------------------------
# 動作確認用
# ---------------------------
@app.route("/", methods=["GET"])
def home():
    return "AI Personality Server is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
