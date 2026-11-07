from flask import Flask, request from datetime import datetime, timezone, timedelta
from datetime import datetime
from functools import wraps
from secrets import compare_digest
import os

app = Flask(__name__)
visitors = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        device = request.user_agent.platform or "Неизвестно"
browser = request.user_agent.browser or "Неизвестно"

visitors.append(
    f"Дата: (datetime.now(timezone.utc) + timedelta(hours=5)).strftime("%d.%m.%Y %H:%M:%S") | "
    f"Устройство: {device} | Браузер: {browser}"
)
        return "<h1>Спасибо! Посещение зарегистрировано!</h1>"

    return """
<style>
body {
    background: black;
    color: #39ff14;
    font-family: Arial;
    padding: 20px;
}
h1 {
    font-size: 35px;
    text-shadow: 0 0 15px #39ff14;
}
div {
    font-size: 22px;
    margin: 15px 0;
    padding: 12px;
    border: 1px solid #39ff14;
    border-radius: 10px;
}
</style>
<h1>GAFUR ADMIN</h1>
""" + "".join(
    "<div>" + escape(v) + "</div>" for v in visitors
)
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

    from markupsafe import escape

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=int(os.environ.get("PORT", 5000)))
