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
    """Landing page: Renders the title and instruction for the survey."""

    title = survey.title
    instructions = survey.instructions

    return render_template('survey_start.html', 
        title=title, # passing parameter by name, not assignment
        instructions=instructions)

@app.route('/begin', methods=["POST"])
def begin():
    """Start button: Redirects user to questions"""

    return redirect('/question/0')

@app.route('/question/<int:q_id>')
def question_page(q_id):
    """Questions page: Displays current question and choices"""

    question = survey.questions[q_id]
    return render_template('question.html', 
        question=question,
        q_id=q_id)

@app.route('/answer/<int:q_id>', methods=["POST"])
def answer(q_id):
    """Answer page: Appends user answer to responses list and take user to the next question.
        If no more questions, renders the completion page.
    """

    responses.append(request.form['answer'])
    next_q = q_id + 1

    if next_q == len(survey.questions):
        return render_template('completion.html')

    return redirect(f"/question/{next_q}")
    

