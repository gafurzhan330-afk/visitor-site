from flask import Flask, request
from datetime import datetime
from functools import wraps
from secrets import compare_digest
import os

app = Flask(__name__)
visitors = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        visitors.append(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        return "<h1>Спасибо! Посещение зарегистрировано!</h1>"

    return """
    <h1>Мой сайт</h1>
    <p>Нажимая кнопку, вы соглашаетесь
    зарегистрировать время посещения.</p>
    <form method="POST">
    <button type="submit">Согласиться</button>
    </form>
    """

@app.route("/admin")
def admin():
    auth = request.authorization
    password = os.environ.get("ADMIN_PASSWORD", "")

    if not password:
        return "Пароль не настроен", 503

    if not auth or auth.username != "admin" or not compare_digest(
        auth.password or "", password
    ):
        return "Нужен пароль", 401, {
            "WWW-Authenticate": 'Basic realm="Admin"'
        }

    return "<pre>" + "\n".join(visitors) + "</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=int(os.environ.get("PORT", 5000)))
