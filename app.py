from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# responses = []

@app.route('/')
def homepage():
    """Landing page: Renders the title and instruction for the survey."""

    title = survey.title
    instructions = survey.instructions
    session["responses"] = []
    session["q_id"] = 0

    return render_template('survey_start.html', 
        title=title, # passing parameter by name, not assignment
        instructions=instructions)

@app.route('/begin', methods=["POST"])
def begin():
    """Start button: Redirects user to questions"""

    return redirect(f'/question/{session["q_id"]}')

@app.route('/question/<int:q_id>')
def question_page(q_id):
    """Questions page: Displays current question and choices"""



    if (session["q_id"] == len(survey.questions)):
        flash("hey you're already done")
        return redirect("/complete")

    elif (q_id != session["q_id"]):
        flash("pleaes stay on your current question")
        return redirect(f'/question/{session["q_id"]}')

    question = survey.questions[q_id]
    return render_template('question.html', 
        question=question,
        q_id=q_id)

@app.route('/answer/<int:q_id>', methods=["POST"])
def answer(q_id):
    """Answer page: Appends user answer to responses list and take user to the next question.
        If no more questions, renders the completion page.
    """

    response = request.form['answer']

    responses = session["responses"]
    responses.append(response)
    session["responses"] = responses

    next_q = q_id + 1
    session["q_id"] = next_q

    if next_q == len(survey.questions):
        return redirect('/complete')

    return redirect(f"/question/{next_q}")
    
@app.route('/complete')
def complete():
    return render_template("completion.html")

