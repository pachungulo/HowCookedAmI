from flask import Flask, render_template, url_for, request, redirect
import processing, gpt

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("input.html")

@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        userInput = request.form['coursesInput']
        selected_semester = request.form.get('semester') #fall or winter
        #userInput = processing.getListOfClasses(userInput)
        #courses = processing.processUserInput(userInput, selected_semester)
        coursesSummary = processing.outputClasses(userInput, selected_semester)
        overallRating = int(processing.passSemesterRating(userInput, selected_semester) * 50)
        imgLink = gpt.generateImage(overallRating)
        if imgLink[-1]=="/":
            imgLink=imgLink[:-1]
        
        print(coursesSummary)
        print(imgLink)
        # courses = [{
        #     "code": "ECSE 324",
        #     "professor": "Dubach",
        #     "overallDifficulty": 80,
        #     "comments": "These are the comments"
        #     }]
        # Process the courses data as needed
        return render_template("summary.html", courses=coursesSummary, image = imgLink, overall = overallRating)
    # if request.method == "POST":
    #     classes = request.form["classes"]
    #     classes = classes.split(",")
    #     return render_template('submit.html', classes=classes)

    else:
        return redirect(url_for("index"))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))
