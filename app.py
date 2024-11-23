from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("input.html")

@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        
        courses = request.form['coursesInput']
        courses = [{
            "code": "ECSE 324",
            "professor": "Dubach",
            "overallDifficulty": 80,
            "comments": "These are the comments"
            }]
        # Process the courses data as needed
        return render_template("summary.html", courses=courses)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))
