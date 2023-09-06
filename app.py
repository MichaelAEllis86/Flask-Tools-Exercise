#how to import flask things
from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice 
from surveys import Question, Survey
app=Flask(__name__)
app.config["SECRET_KEY"]="mookster21"
debug=DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses=[]

satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])

@app.route("/")
def show_root():
    # responses=[] may return to this line, intention was to reset responses list upon returning to root page. Change to list is not lasting once questions are reaccessed after survey completion
    questions=satisfaction_survey.questions
    instructions=satisfaction_survey.instructions
    title=satisfaction_survey.title
    print("printing responses", responses, type(responses), len(responses))
    return render_template ("root.html",questions=questions,instructions=instructions,title=title,)

@app.route("/questions/<int:id>")
def find_question(id):
    current_question=satisfaction_survey.questions[id].question
    choices=satisfaction_survey.questions[id].choices
    choice1=satisfaction_survey.questions[id].choices[0]
    choice2=satisfaction_survey.questions[id].choices[1]
    print("printing responses", responses, type(responses), len(responses))

    if (len(responses)==0 and id != 0):
        # in this scenario the user tries to access a question before starting. Take back to root/start
        return redirect("/")
    
    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them but dont let them answer more questions/restart 
        return redirect("/complete")
    
    if (len(responses) != id):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {id}." ,"error")
        return redirect(f"/questions/{len(responses)}")
    
    return render_template("questions.html",current_question=current_question,id=id,choices=choices,choice1=choice1,choice2=choice2)

@app.route("/answers", methods=["POST", "GET"])
def add_survey_answer():
    answer=request.form["answer"]
    responses.append(answer)
    print(answer)
    print(responses)

    if (len(responses) == len(satisfaction_survey.questions)):
        # Then they have answered all questions redirect to finished survery page
        return redirect ("/complete")
    
    else: return redirect (f"/questions/{len(responses)}")


@app.route("/base")
def show_base_template():
    return render_template("base.html")

@app.route("/complete")
def show_complete():
    return render_template ("complete.html")

#  
    # print(satisfaction_survey.questions)
    # print(satisfaction_survey.instructions)
    # print(satisfaction_survey.title)
    # print("SPACE")
    # print(questions)
    # print(instructions)
    # print(title)
    # print("SPACE")

# class Survey:
#     """Questionnaire."""

#     def __init__(self, title, instructions, questions):
#         """Create questionnaire."""

#         self.title = title
#         self.instructions = instructions
#         self.questions = questions


# satisfaction_survey = Survey(
#     "Customer Satisfaction Survey",
#     "Please fill out a survey about your experience with us.",
#     [
#         Question("Have you shopped here before?"),
#         Question("Did someone else shop with you today?"),
#         Question("On average, how much do you spend a month on frisbees?",
#                  ["Less than $10,000", "$10,000 or more"]),
#         Question("Are you likely to shop here again?"),
#     ])