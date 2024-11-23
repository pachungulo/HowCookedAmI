from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("input.html")

@app.route('/result', methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        classes = request.form["classes"]
        classes = classes.split(",")
        return render_template('submit.html', classes=classes)

    else:
        return redirect(url_for("index"))

# @app.route('/submit/<classes>')
# def submit(classes):
#     return render_template("submit.html", classes=classes)
