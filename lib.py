import dotenv
import os
from requests import request
from pprint import pprint as print
import datetime

dotenv.load_dotenv()

TOKEN = os.getenv("TEMPO_API_TOKEN")
weeklyHours = 30 # Change this depending on your minimum weekly work time

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

def getWorkdaysLeftToDistribute():
    today = datetime.datetime.today()
    workdaysLeft = 5 - today.weekday()
    return workdaysLeft


def getHoursandMinutesLeftToWork(seconds):
    hours = weeklyHours
    hoursLeft = hours - convertSecondsToHours(seconds)[0]
    minutesLeft = convertSecondsToHours(seconds)[1]
    return hoursLeft, minutesLeft

def printMessage(haveIWorkedEnoughResult, hoursLeftToWorkResult, workdaysLeftResult):
    if haveIWorkedEnoughResult:
        print("I have worked enough")
    else:
        print("I have not worked enough")
        print(f'of the total hours of {weeklyHours}:')
        print("I have " + str(hoursLeftToWorkResult[0]) + " hours and " + str(hoursLeftToWorkResult[1]) + " minutes left to work")
        print("I have " + str(workdaysLeftResult) + " workdays left to distribute the remaining time")


# main function. determine if I have worked enough or not and return the display message.

# use this to create the display message on the frontend for now.
def main():
    data                       = getData()
    relevantLogs               = getRelevantWorkLogs(data)
    totalWeekWorkTimeInSeconds = getTotalWeekWorkTimeInSeconds(relevantLogs)
    haveIWorkedEnoughResult    = haveIWorkedEnoughPerWeek(totalWeekWorkTimeInSeconds)
    hoursLeftToWorkResult      = getHoursandMinutesLeftToWork(totalWeekWorkTimeInSeconds)
    workdaysLeftResult         = getWorkdaysLeftToDistribute()
    printResult                = printMessage(haveIWorkedEnoughResult, hoursLeftToWorkResult, workdaysLeftResult)
    return printResult

main()