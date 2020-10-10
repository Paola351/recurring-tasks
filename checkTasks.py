import configparser, sendMail
from datetime import datetime
import logging

logging.basicConfig(level='DEBUG', filename='logs/app.log', filemode='a', format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')

taskTypeList = ["daily", "weekly", "monthly", "weekdayofmonth", "yearly", "free"]
daysOfTheWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
monthsOfTheYear = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                   "November", "December"]
occurrences = ["first", "second", "third", "fourth", "last"]

config = configparser.ConfigParser()
config.read('tasks.ini')

now = datetime.now()
day = now.strftime("%d")
month = now.strftime("%m")

def validate_task_type(tt):
    if tt not in taskTypeList:
        errorMessage = "Sorry, taskType should only be in {}".format(taskTypeList)
        sendMail.sendNotification("Error", errorMessage)
        raise ValueError(errorMessage)

def validate_weekday(wd):
    if wd not in daysOfTheWeek:
        errorMessage = "Sorry, Weekday should only be in {}".format(daysOfTheWeek)
        sendMail.sendNotification("Error", errorMessage)
        raise ValueError(errorMessage)

def validate_month(m):
    if m not in monthsOfTheYear:
        errorMessage = "Sorry, month should only be in  {}".format(monthsOfTheYear)
        sendMail.sendNotification("Error", errorMessage)
        raise ValueError(errorMessage)
        
def validate_occurrence(o):
    if o not in occurrences:
        errorMessage = "Sorry, occurrence should only be in {}".format(occurrences)
        sendMail.sendNotification("Error", errorMessage)
        raise ValueError(errorMessage)

def validate_day(d):
    try:
        d = int(d)
    except:
        errorMessage = "day should be an int"
        sendMail.sendNotification("Error", errorMessage)
        raise ValueError(errorMessage)
    if d < 1 or d > 31:
        errorMessage = "Sorry, day should only be in  [1, 31]"
        sendMail.sendNotification("Error", errorMessage)
        raise ValueError(errorMessage)

def extract_type(section):
    return config.get(section, 'Type')

def extract_message(section):
    return config.get(section, 'Message')

def extract_days(section):
    return config.get(section, 'Day')

def extract_months(section):
    return config.get(section, 'Month')

def extract_weekdays(section):
    return config.get(section, 'Weekday')
  
def extract_occurrences(section):
    return config.get(section, 'Occurrence')

for i in config.sections():

    taskType = extract_type(i)

    validate_task_type(taskType)

    if taskType == 'daily':
        message = extract_message(i)
        logging.info("Notification triggered \"{}\" every day ".format(message))
        sendMail.sendNotification(i, message)

    if taskType == 'weekly':
        for j in extract_weekdays(i).split(','):
            validate_weekday(j)
            if daysOfTheWeek.index(j) == now.weekday():
                message = extract_message(i)
                logging.info("Notification triggered \"{}\" every day ".format(message))
                sendMail.sendNotification(i, message)

    if taskType == 'monthly':
        for j in extract_days(i).split(','):
            validate_day(j)
            if day == j:
                message = extract_message(i)
                logging.info("Notification triggered \"{}\" every {} of the month ".format(message, j))
                sendMail.sendNotification(i, message)
                
    if taskType == 'weekdayofmonth':
        for j in extract_weekdays(i).split(','):
            validate_weekday(j)
            for occurrence in extract_occurrences(i).split(','):
                validate_occurrence(occurrence)
                if daysOfTheWeek.index(j) == now.weekday():
                    message = extract_message(i)
                    if occurrence.lower() == "first" and 1 <= int(day) <= 7:
                        sendMail.sendNotification(i, message)
                        logging.info("Notification triggered \"{}\" every {} {} of the month ".format(message, occurrence, j))
                    elif occurrence.lower() == "second" and 8 <= int(day) <= 14:
                        sendMail.sendNotification(i, message)
                        logging.info("Notification triggered \"{}\" every {} {} of the month ".format(message, occurrence, j))
                    elif occurrence.lower() == "third" and 15 <= int(day) <= 21:
                        sendMail.sendNotification(i, message)
                        logging.info("Notification triggered \"{}\" every {} {} of the month ".format(message, occurrence, j))
                    elif occurrence.lower() == "fourth" and 22 <= int(day) <= 28:
                        sendMail.sendNotification(i, message)
                        logging.info("Notification triggered \"{}\" every {} {} of the month ".format(message, occurrence, j))
                    elif occurrence.lower() == "last" and 25 <= int(day) <= 31:
                        sendMail.sendNotification(i, message)
                        logging.info("Notification triggered \"{}\" every {} {} of the month ".format(message, occurrence, j))
                    else:
                        continue

    if taskType == 'yearly':
        m = extract_months(i)
        d = extract_days(i)
        if len(m.split(',')) > 1 or len(d.split(',')) > 1:
            errorMessage = "Sorry, yearly task should only contain one specific date"
            sendMail.sendNotification("Error", errorMessage)
            raise ValueError(errorMessage)
        validate_day(d)
        validate_month(m)
        if d == day and monthsOfTheYear.index(m) + 1 == int(month):
            message = extract_message(i)
            logging.info(
                "Notification triggered \"{}\" every year, the {} of the month {}".format(message, day,
                                                                                                          month))
            sendMail.sendNotification(i, message)

    if taskType == 'free':
        for j in extract_months(i).split(','):
            validate_month(j)
            if monthsOfTheYear.index(j) + 1 == int(month):
                for k in extract_days(i).split(','):
                    validate_day(k)
                    if day == k:
                        message = extract_message(i)
                        logging.info(
                            "Notification triggered \"{}\" every {} of the months {}".format(message,
                                                                                                             day,
                                                                                                             month))
                        sendMail.sendNotification(i, message)
