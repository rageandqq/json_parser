from flask import Flask
from flask import render_template
from flask import request

from parser.tokenizer import Tokenizer

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('json.html', data='')

@app.route('/validate', methods=['POST'])
def validate():
    json_to_parse = request.form['data']
    tokenizer = Tokenizer(json_to_parse)

    parsed_token = tokenizer.next()
    return parsed_token.token_value

if __name__ == '__main__':
    app.run(debug=True)
