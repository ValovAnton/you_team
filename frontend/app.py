from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BACKEND_URL = "http://backend:8000/register"

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        response = requests.post(BACKEND_URL, json={"email": email, "password": password, "confirm_password": confirm_password,})

        return jsonify(response.json())

    return """
    <form method="post">
        Email: <input type="email" name="email" required><br>
        Password: <input type="password" name="password" required><br>
        Confirm password: <input type="password" name="confirm_password" required><br>
        <input type="submit" value="Register">
    </form>
    """ # регистрация без верстки

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
