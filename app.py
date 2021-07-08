from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def homepage():
    """Landing page renders the title and instruction for survey.
    """

    title = survey.title
    instructions = survey.instructions

    return render_template('survey_start.html', 
        title=title, # passing parameter by name, not assignment
        instructions=instructions)

@app.route('/begin', methods=["POST"])
def begin():
    """Start button redirects to questions"""

    return redirect('/question/0')

@app.route('/question/<int:q_id>')
def question_page(q_id):
    """Questions page displays question and choices"""

    question = survey.questions[q_id]
    return render_template('question.html', 
        question=question,
        q_id=q_id)

@app.route('/answer/<int:q_id>', methods=["POST"])
def answer(q_id):
    """appends user answer to responses list
        take user to next question
        if no more questions, render completion page
    """

    responses.append(request.form['answer'])
    next_q = q_id + 1

    if next_q == len(survey.questions):
        return render_template('completion.html')

    return redirect(f"/question/{next_q}")
    

