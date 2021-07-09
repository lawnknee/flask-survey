from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

CURRENT_SURVEY = 'selected_survey'
CURRENT_RESPONSES = 'current_responses'

# surveys = {
#     "satisfaction": satisfaction_survey,
#     "personality": personality_quiz,
# }

@app.route('/')
def show_survey_choices():
    """Landing page where user can pick a survey."""

    return render_template("survey_choices.html", surveys=surveys)

@app.route('/', methods=["POST"])
def selected_survey():
    """Renders the selected survey's title and instructions."""

    selected = request.form["selected_survey"]
    survey = surveys[selected]
    
    session[CURRENT_SURVEY] = selected

    return render_template('survey_start.html', survey=survey)

@app.route('/begin', methods=["POST"])
def begin():
    """Start button: Redirects user to questions"""

    session[CURRENT_RESPONSES] = []

    return redirect(f'/question/{len(session[CURRENT_RESPONSES])}')

@app.route('/question/<int:q_id>')
def question_page(q_id):
    """Questions page: Displays current question and choices. Forces user to stay on 
       correct page."""

    responses = session.get(CURRENT_RESPONSES)
    selected = session[CURRENT_SURVEY]
    survey = surveys[selected]

    if (len(responses) == len(survey.questions)):
        flash("hey you're already done")
        return redirect("/complete")

    elif (q_id != len(responses)):
        flash("please stay on your current question")
        return redirect(f'/question/{len(responses)}')

    question = survey.questions[q_id]
    return render_template('question.html', 
        question=question,
        q_id=q_id)

@app.route('/answer/<int:q_id>', methods=["POST"])
def answer(q_id):
    """Answer page: Appends user answer to responses list and takes user to the next question.
       If no more questions, renders the completion page.
    """

    answer = request.form['answer']
    selected = session[CURRENT_SURVEY]
    survey = surveys[selected]

    responses = session[CURRENT_RESPONSES]
    responses.append(answer)
    session[CURRENT_RESPONSES] = responses

    next_q = q_id + 1

    if next_q == len(survey.questions):
        return redirect('/complete')

    return redirect(f"/question/{next_q}")
    
@app.route('/complete')
def complete():
    """Render completion page"""

    return render_template("completion.html")

