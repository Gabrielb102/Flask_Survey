from surveys import Question, Survey, satisfaction_survey, personality_quiz, surveys
from flask import Flask, request, render_template, flash, redirect

app = Flask(__name__)

from flask_debugtoolbar import DebugToolbarExtension
app.config["SECRET_KEY"] = "chickens"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

responses = []
survey = surveys["satisfaction"]

@app.route("/")
def show_homepage(): 
    """shows homepage"""
    responses.clear()
    return render_template("surveys.html", survey = survey)

@app.route("/satisfaction_survey")
def load_satisfaction_survey() :
    """shows satisfaction survey on page"""
    return render_template("satisfaction_survey.html")

@app.route("/question/<question_number>")
def display_question(question_number):
    """renders the specified question and choices"""
    
    question = survey.questions[int(question_number)].question
    choices = survey.questions[int(question_number)].choices

    if int(question_number) > 0 :
        if request.args.get("choice") :
            responses.append(choices[int(request.args["choice"])])
    if not int(question_number) == len(responses) :
        message = "Do not alter the URL to change your place in the survey!"
        flash(message)
        return redirect(f"/question/{len(responses)}")
    if int(question_number) == len(survey.questions) - 1 :
        return render_template("last_question.html", q_number = question_number, question = question, choices = choices)
    else : 
        question_number = int(question_number) + 1
        return render_template("question.html", q_number = question_number, question = question, choices = choices)

@app.route("/collecting_answer")
def add_last_answer():
    choices = survey.questions[len(survey.questions) - 1].choices
    responses.append(choices[int(request.args["choice"])])
    return redirect("/thank_you")

@app.route("/thank_you")
def display_thank_page():
    choices = survey.questions[len(survey.questions) - 1].choices
    return render_template("thank_you.html", survey = survey, responses = responses)