from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('json.html')

@app.route('/validate', methods=['POST'])
def validate():
    return 'Invalid JSON!'

if __name__ == '__main__':
    app.run()
