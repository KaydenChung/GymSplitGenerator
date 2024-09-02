# Library Imports
from flask import Flask, render_template, request
import google.generativeai as genai
import os
import re

# Creating Flask App
app = Flask(__name__)

def parseText(data):
    questions = []
    answers = []
    tempAnswers = []
    for item in data:
        if item.strip() and not item.startswith(' '):
            if tempAnswers:
                answers.append(tempAnswers)
                tempAnswers = []
            questions.append(item)
        elif item.strip() and item.startswith(' '):
            tempAnswers.append(item.strip())
    if tempAnswers:
        answers.append(tempAnswers)
    print("Questions:", questions)
    print("Answers:", answers)

@app.route("/")
def index():
    return render_template('index.html')


#setting up the ai model 
genai.configure(api_key="AIzaSyDG75dqGCZPTR_xDqEltEjkDLntCFNhprs")

# Using `response_mime_type` requires either a Gemini 1.5 Pro or 1.5 Flash model
model = genai.GenerativeModel('gemini-1.5-flash')


# Flask App Handling
@app.route("/form", methods=['GET', 'POST'])

def createForm():
    if request.method == 'POST':
        if 'days' in request.form and 'fitness_level' in request.form:
            days = request.form['days']
            fitness_level = request.form['fitness_level']

 

            prompt = f"""
            Create a gym split for a person who works out {days} days a week with {fitness_level} fitness level.
            Don't return anything besides five questions that will assist in creating this gym split
            After each question provide a list of 3 possible answers for the question.
            Your response should have absolutely no markdown formatting.
            The response should contain no numbers, letters, or dashes infront of the question or answers.
            """

            response = model.generate_content(prompt)
            questions = response.text

            parseText(questions)

            return render_template('form.html', question=questions)
        else:
            # Handle the form submission with answers
            answers = {key: request.form[key] for key in request.form}
            # Process the answers as needed
            return render_template('answers_submitted.html', answers=answers)
                
    
    return render_template('form.html')


# Main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)