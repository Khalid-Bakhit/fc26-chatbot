from flask import Flask, jsonify, request, render_template
from .fc26_bot import answer_question

app = Flask(__name__, template_folder="../templates", static_folder="../static")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_text = data.get("text", "")
    reply = answer_question(user_text)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    # Local dev server
    app.run(host="0.0.0.0", port=5001, debug=True)
