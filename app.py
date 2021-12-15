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
    emulate = request.args.get('emulate')

    statusInfo = lib.getStatusInfo()

    if emulate == 'yes':
        result = lib.getWorkTimeStatus(emulate=emulate)
        return render_template('yay.html', result=result, statusInfo=statusInfo)

    elif emulate == 'no':
        result = lib.getWorkTimeStatus(emulate=emulate)
        return render_template('index.html', result=result)
    

    if lib.haveIWorkedEnoughThisWeek():
        return render_template('yay.html', statusInfo=statusInfo)

    result = lib.getWorkTimeStatus(emulate=emulate)
    return render_template('index.html', result=result, statusInfo=statusInfo)

@app.route('/yes')
def emulate_yes():
    return redirect(url_for('hello', emulate='yes'))

@app.route('/no')
def emulate_no():
    return redirect(url_for('hello', emulate='no'))

if __name__ == '__main__':
    app.run(debug=True)
    # ui.run()