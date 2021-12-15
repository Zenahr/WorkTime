import dotenv
import os
from requests import request
from pprint import pprint as print
import datetime

dotenv.load_dotenv()

TOKEN = os.getenv("TEMPO_API_TOKEN")
weeklyHours = int(os.getenv("REQUIRED_WEEKLY_HOURS")) # Change this depending on your minimum weekly work time

def getData():
    r = request('get', "https://api.tempo.io/core/3/worklogs", headers={"Authorization": "Bearer " + TOKEN})
    return r.json()

# check if startDate is in current week
def isInCurrentWeek(startDate):
    # get current week
    today = datetime.datetime.today()
    currentWeek = today.isocalendar()[1]

    # get startDate week
    startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    startDateWeek = startDate.isocalendar()[1]
    return currentWeek == startDateWeek

# convert seconds into hours and minutes
def convertSecondsToHours(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return hours, minutes

def getRelevantWorkLogs(apiResultJson):
    relevantLogs = []
    for e in apiResultJson['results']:
        if isInCurrentWeek(e['startDate']):
            relevantLogs.append(e)
    return relevantLogs

def getTotalWeekWorkTimeInSeconds(relevantWorkLogsResult):
    return sum([x['timeSpentSeconds'] for x in relevantWorkLogsResult])

def haveIWorkedEnoughPerWeek(seconds):
    hours = weeklyHours
    return seconds >= hours * 60 * 60

def isWorkday(date):
    return date.weekday() < 5

def getWorkdaysLeftToDistribute(substractCurrentDay=True):
    today = datetime.datetime.today()
    workdaysLeft = 5 - today.weekday()
    if substractCurrentDay:
        return workdaysLeft - 1
    return workdaysLeft

def getHoursandMinutesLeftToWork(seconds):
    hours = weeklyHours
    hoursLeft = hours - convertSecondsToHours(seconds)[0]
    minutesLeft = convertSecondsToHours(seconds)[1]
    return hoursLeft, minutesLeft

def haveIWorkedEnoughThisWeek():
    data                       = getData()
    relevantLogs               = getRelevantWorkLogs(data)
    totalWeekWorkTimeInSeconds = getTotalWeekWorkTimeInSeconds(relevantLogs)
    return haveIWorkedEnoughPerWeek(totalWeekWorkTimeInSeconds)

def getStatusInfo():
    data = getData()
    relevantLogs = getRelevantWorkLogs(data)
    totalWeekWorkTimeInSeconds = getTotalWeekWorkTimeInSeconds(relevantLogs)
    haveIWorkedEnoughResult = haveIWorkedEnoughPerWeek(totalWeekWorkTimeInSeconds)
    hoursAndMinutesLeftToWork = getHoursandMinutesLeftToWork(totalWeekWorkTimeInSeconds)
    workdaysLeftResult = getWorkdaysLeftToDistribute()
    return {
        "haveIWorkedEnough": haveIWorkedEnoughResult,
        "hoursAndMinutesLeftToWork": hoursAndMinutesLeftToWork,
        "workdaysLeft": workdaysLeftResult
    }


def printMessage(haveIWorkedEnoughResult, hoursAndMinutesLeftToWorkResult=(0, 0), workdaysLeftResult=0):
    if haveIWorkedEnoughResult:
        return 'I have worked enough this week!'
    else:
        return f""" <br>
        I have not worked enough yet. <br>
        of the total hours of {weeklyHours}: <br>
        I have {hoursAndMinutesLeftToWorkResult[0]} hours and {hoursAndMinutesLeftToWorkResult[1]} minutes left to work. <br>
        I have {workdaysLeftResult} workdays left to distribute the time remaining.
        """
# use this to create the display message on the frontend for now.
def getWorkTimeStatus(emulate=''):
    """[summary]

    Args:
        emulate (str, optional): 'yes' | 'no' | ''. Defaults to ''. if 'yes' it will simulate having worked enough regardless of truthiness. With 'no' vice versa.

    Returns:
        [type]: [description]
    """
    data                       = getData()
    relevantLogs               = getRelevantWorkLogs(data)
    totalWeekWorkTimeInSeconds = getTotalWeekWorkTimeInSeconds(relevantLogs)
    haveIWorkedEnoughResult    = haveIWorkedEnoughPerWeek(totalWeekWorkTimeInSeconds)
    hoursAndMinutesLeftToWork      = getHoursandMinutesLeftToWork(totalWeekWorkTimeInSeconds)
    workdaysLeftResult         = getWorkdaysLeftToDistribute()
    printResult                = printMessage(haveIWorkedEnoughResult, hoursAndMinutesLeftToWork, workdaysLeftResult)

    if emulate == 'no':
        return printMessage(False)

    if emulate == 'yes':
        return printMessage(True)

    return printResult

if __name__ == '__main__':
    print(getWorkTimeStatus())