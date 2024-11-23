from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        result = request.form
        classes = result["classes"]
        classes = classes.split(",")
        return render_template("submit.html", classes=classes)
