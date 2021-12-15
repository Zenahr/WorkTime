from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from flaskwebgui import FlaskUI
from lib import *

app = Flask(__name__)
ui = FlaskUI(app)

@app.route('/')
def hello():
    emulate = '' # 'yes' | 'no' | ''
    if emulate == 'yes' or emulate == 'no':
        result = ZEN_API_getWorkTimeStatus(emulate=emulate)
        return render_template('index.html', result=result)
        
    if ZEN_API_haveIWorkedEnoughThisWeek():
        result = ZEN_API_getWorkTimeStatus(emulate=emulate)
        return render_template('index.html', result=result)
    return render_template('yay.html')

if __name__ == '__main__':
    app.run(debug=True)
    # ui.run()