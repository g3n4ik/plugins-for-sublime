from flask import Flask, request
from transformers import GPT2LMHeadModel

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_prediction():
    context = request.form.get('context')
    context = context + " Misha"
    return context

if __name__ == '__main__':
    app.run(host='localhost', port=5342)