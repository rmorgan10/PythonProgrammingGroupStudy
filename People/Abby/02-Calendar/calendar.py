#Python Calendar

import os 
from datetime import datetime
from datetime import date

def monthMap(month, reverse=False):
    converter =  {'january': 1, 'february': 2, 'march': 3, 'april': 4,
                     'may': 5, 'june': 6, 'july': 7, 'august': 8,
                     'september': 9, 'october': 10, 'november': 11,
                     'december': 12}

    if reverse:
        converter = {v: k for k, v in converter.items()}

    return converter[month]

def weekMap(dayOfWeek, reverse=False):
    converter =  {'monday': 0, 'tuesday': 1,  'wednesday': 2, 'thursday': 3,
                  'friday': 4, 'saturday': 5, 'sunday': 6}

    if reverse:
        converter = {v: k for k, v in converter.items()}

    return converter[dayOfWeek]

def firstOfMonth(month: int, year: int):
    thisDate = date(year, month, 1)
    return datetime.weekday(thisDate)

def datePrint(theDate):
    try: 
        if int(theDate) < 10:
            return " " + str(theDate)
        else:
            return str(theDate)
    except: 
        return theDate
    
def datePrint(theDate):
    try: 
        if int(theDate) < 10:
            return " " + str(theDate)
        else:
            return str(theDate)
    except: 
        return theDate
    
def monthLengths(month, reverse=False, leapyear=False):
    converter =  {'january': 31, 'february': 28, 'march': 31, 'april': 30,
                     'may': 31, 'june': 30, 'july': 31, 'august': 31,
                     'september': 30, 'october': 31, 'november': 30,
                     'december': 31}
    
    if leapyear: 
        converter['february'] = 29

    if reverse:
        converter = {v: k for k, v in converter.items()}
        
    return converter[month]

def printCalendar(today: int, month: int, year: int):
    #Print Header
    os.system("clear")
    thisDate = str(date(year, month, today))
    monthNmbr = int(thisDate[5:7])
    monthName = monthMap(monthNmbr, reverse=True)
    print(f"      {monthNmbr} - {monthName.capitalize()} - {year}\n")
    
    previousMonth = 0
    if month > 1:
        previousMonth = month - 1
    else:
        previousMonth = 12

    printout = [['\033[4;30;49mSu|', ' M|', 'Tu|', ' W|', 'Th|', ' F|', 'Sa\033[0m|'],
               [0]*7, [0]*7, [0]*7, [0]*7]

    #Many Initializations
    lengthOfMonth = monthLengths(monthMap(month, reverse=True))
    fomwd = firstOfMonth(month, year) # int - firstOfMonthWeekDay, Monday is 0
    lml = monthLengths(monthMap(previousMonth, reverse=True))
    startDay = 0 if fomwd == 6 else fomwd + 1
    
    #Initialize Calendar with all 0's
    if fomwd == 5 and lengthOfMonth > 29:
        printout.append([0]*7)
        printout.append([0]*7)
    elif fomwd == 4 and lengthOfMonth == 31:
        printout.append([0]*7)
        printout.append([0]*7)
    elif lengthOfMonth > 28: 
        printout.append([0]*7)
    
    #Set dates from previous month
    if startDay != 0: 
        for i in range(startDay):
            printout[1][i] = "\033[0;97;49m" + datePrint(lml - startDay + i + 1) + "\033[0m" + "|"
            
    #Set dates for current month
    printWeek = 1
    printWeekDay = startDay
    for i in range(1,lengthOfMonth+1):
        if i == today:
            printout[printWeek][printWeekDay] = "\033[1;30;43m" + datePrint(i) + "\033[0m" + "|"
        else: 
            printout[printWeek][printWeekDay] = datePrint(i) + "|"
        if printWeekDay == 6:
            printWeek += 1
            printWeekDay = 0
        else: 
            printWeekDay += 1
    
    #Set dates for next month
    if printWeekDay != 0:
        for i in range(7 - printWeekDay):
            printout[printWeek][i+printWeekDay] = "\033[0;97;49m" + datePrint( i + 1 ) + "\033[0m" + "|"

    printStatement = ""
    for week in printout:
        printStatement += "\t|"
        for day in week:
            printStatement += datePrint(day)
        printStatement += "\n"
    print(printStatement)

printCalendar(30,9,2015)#Python Calendar

