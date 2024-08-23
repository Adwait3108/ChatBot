from flask import Flask, render_template, request, jsonify, session
import random
import spacy
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

# Load the spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Load intents from the JSON file
with open('intents.json', 'r') as file:
    intents = json.load(file)['intents']

# Fallback AI response
def ai_fallback_response(user_message):
    # Here you could integrate a more sophisticated AI model like OpenAI GPT
    return f"I'm not sure how to respond to '{user_message}', but I'm learning!"

@app.route('/')
def index():
    session['conversation'] = []  # Initialize conversation history
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['message'].lower()
    session['conversation'].append({'user': user_message})

    response = None
    for intent in intents:
        for pattern in intent['patterns']:
            if pattern in user_message:
                response = random.choice(intent['responses'])
                break
        if response:
            break
    
    if not response:
        response = ai_fallback_response(user_message)

    session['conversation'].append({'bot': response})
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
