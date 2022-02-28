from surveys import Question, Survey, satisfaction_survey, personality_quiz, surveys
from flask import Flask, request, render_template, flash, redirect, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "chickens"

# from flask_debugtoolbar import DebugToolbarExtension
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# debug = DebugToolbarExtension(app)

survey = surveys["satisfaction"]

@app.route("/")
def show_homepage(): 
    """shows homepage"""
    return render_template("homepage.html", survey = survey)

@app.route("/start", methods=["POST"])
def reset_answers() :
    return redirect("/question/0")

@app.route("/collecting_answer", methods=["POST"])
def add_answer():

    choices = survey.questions[len(session['responses'])].choices   

    if request.form.get('choice') :
        choice = request.form['choice']
        session['responses'].append(choices[int(choice)])
        print(f"Session {session}")
        # return render_template("thank_you.html", survey = survey)
        return redirect(f"/question/{len(session['responses'])}")

    elif q_number == len(survey.questions) :
        return redirect("/thank_you")

    else :
        print("no choice found")
        return redirect(f"/question/{len(session['responses'])}")

@app.route("/question/<question_number>", methods=["GET"])
def display_question(question_number):
    """renders the specified question and choices"""
    
    print(type(session['responses']))
    q_number = int(question_number)
    question = survey.questions[q_number].question
    choices = survey.questions[q_number].choices

    if not q_number == len(session['responses']) :
        message = "Do not alter the URL to change your place in the survey!"
        flash(message)
        return redirect(f"/question/{len(session['responses'])}")

    if q_number == len(survey.questions) - 1 :
        return render_template("last_question.html", q_number = q_number, question = question, choices = choices)
    else : 
        return render_template("question.html", q_number = q_number, question = question, choices = choices)

@app.route("/thank_you")
def display_thank_page():
    choices = survey.questions[len(survey.questions) - 1].choices
    return render_template("thank_you.html", survey = survey)