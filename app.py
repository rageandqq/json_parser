from flask import Flask
from flask import render_template
from flask import request

from parser.lexer import Lexer

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('json.html', data='')

@app.route('/validate', methods=['POST'])
def validate():
    json_to_parse = request.form['data']
    tokenizer = Lexer(json_to_parse)
    tokens = []
    while tokenizer.has_next():
        tokens.append(tokenizer.next())

    # Note: Flask renders this strangely.
    return ','.join([token.token_value for token in tokens])

if __name__ == '__main__':
    app.run(debug=True)
