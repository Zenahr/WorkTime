from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from flaskwebgui import FlaskUI
from lib import *

app = Flask(__name__)
ui = FlaskUI(app)

@app.template_filter()
def timefy(hoursAndMinutesTuple):
    hours, minutes = hoursAndMinutesTuple
    return str(hours) + ":" + str(minutes) + " hrs"

@app.route('/')
def hello():
    emulate = '' # 'yes' | 'no' | ''
    if emulate == 'yes' or emulate == 'no':
        result = ZEN_API_getWorkTimeStatus(emulate=emulate)
        return render_template('index.html', result=result)
    
    statusInfo = getStatusInfo()

    if ZEN_API_haveIWorkedEnoughThisWeek():
        result = ZEN_API_getWorkTimeStatus(emulate=emulate)
        return render_template('index.html', result=result, statusInfo=statusInfo)
    return render_template('yay.html', statusInfo=statusInfo)

if __name__ == '__main__':
    app.run(debug=True)
    # ui.run()