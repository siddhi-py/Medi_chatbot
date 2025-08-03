from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

Client = OpenAI(
    api_key="API_KEY_HERE",  # Replace with your actual API key
    base_url="https://api.groq.com/openai/v1"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    try:
        response = Client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a medical genius chatbot. Only answer questions related to medicine, health, and medical advice."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message.content.strip()
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)