from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from flaskwebgui import FlaskUI
from lib import *

app = Flask(__name__)
ui = FlaskUI(app)

@app.route('/')
def hello():
    result = ZEN_API_getWorkTimeStatus(emulate='')
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
    # ui.run()