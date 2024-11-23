from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        classes = request.form["classes"]
        return redirect(url_for('submit', classes=classes))

    else:
        return render_template("input.html")

@app.route('/submit/<classes>')
def submit(classes):
    return render_template("submit.html", classes=classes)
