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
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GAFUR</title>
<style>
body {
    background: black;
    color: #39ff14;
    font-family: Arial;
    text-align: center;
    padding-top: 100px;
}
h1 {
    font-size: 65px;
    text-shadow: 0 0 10px #39ff14,
                 0 0 30px #39ff14,
                 0 0 60px #39ff14;
}
p {
    color: white;
}
button {
    background: #39ff14;
    color: black;
    border: none;
    padding: 15px 30px;
    border-radius: 10px;
    font-size: 18px;
}
</style>
</head>
<body>
<h1>GAFUR</h1>
<p>Добро пожаловать на мой сайт!</p>
<form method="POST">
<button type="submit">Согласиться</button>
</form>
</body>
</html>
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
