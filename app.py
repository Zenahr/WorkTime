from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from flaskwebgui import FlaskUI
import lib

app = Flask(__name__)
ui = FlaskUI(app)

@app.template_filter()
def timefy(hoursAndMinutesTuple):
    hours, minutes = hoursAndMinutesTuple
    if hours <= 0:
        return "+" + str(hours * -1) + ":" + str(minutes) + " hrs"
    return str(hours) + ":" + str(minutes) + " hrs"

@app.route('/')
def hello():
    emulate = '' # 'yes' | 'no' | ''
    if emulate == 'yes' or emulate == 'no':
        result = lib.getWorkTimeStatus(emulate=emulate)
        return render_template('index.html', result=result)
    
    statusInfo = lib.getStatusInfo()

    if lib.haveIWorkedEnoughThisWeek():
        return render_template('yay.html', statusInfo=statusInfo)

    result = lib.getWorkTimeStatus(emulate=emulate)
    return render_template('index.html', result=result, statusInfo=statusInfo)

if __name__ == '__main__':
    app.run(debug=True)
    # ui.run()