from surveys import Question, Survey, satisfaction_survey, personality_quiz, surveys
from flask import Flask, request, render_template, flash, redirect, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "chickens"

# from flask_debugtoolbar import DebugToolbarExtension
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# debug = DebugToolbarExtension(app)

responses = []
survey = surveys["satisfaction"]

@app.route("/")
def show_homepage(): 
    """shows homepage"""
    return render_template("homepage.html", survey = survey)

@app.route("/start", methods=["POST"])
def reset_answers() :
    responses = []
    session['responses'] = responses
    return redirect("/question/0")

@app.route("/collecting_answer", methods=["POST", "GET"])
def add_answer():

    choices = survey.questions[len(responses)].choices   

    if request.form.get('choice') :
        choice = request.form['choice']
        responses.append(choices[int(choice)])
        session['responses'] = responses
        return redirect(f"/question/{len(responses)}")

    else :
        print("no choice found")
        return redirect(f"/question/{len(responses)}")

@app.route("/question/<question_number>", methods=["GET"])
def display_question(question_number):
    """renders the specified question and choices"""
    
    if len(responses) == len(survey.questions) :
        return redirect("/thank_you")
      
    q_number = int(question_number)  
    question = survey.questions[q_number].question
    choices = survey.questions[q_number].choices

    if not q_number == len(responses) :
        message = "Do not alter the URL to change your place in the survey!"
        flash(message)
        return redirect(f"/question/{len(responses)}")

    if q_number == len(survey.questions) - 1 :
        return render_template("last_question.html", q_number = q_number, question = question, choices = choices, responses = responses)
    else : 
        return render_template("question.html", q_number = q_number, question = question, choices = choices, responses = responses)

@app.route("/thank_you")
def display_thank_page():
    choices = survey.questions[len(survey.questions) - 1].choices
    return render_template("thank_you.html", survey = survey)