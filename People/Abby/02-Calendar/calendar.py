import os 
from datetime import datetime
from datetime import date
import csv

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### Some converters
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

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
#Returns the weekday of the first of the month
def firstOfMonth(month: int, year: int):
    thisDate = date(year, month, 1)
    return datetime.weekday(thisDate)

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### Some Print Formatters
def datePrint(theDate):
    try: 
        if int(theDate) < 10:
            return "0" + str(theDate)
        else:
            return str(theDate)
    except: 
        return theDate

def timePrint(time: str):
    hour = int(time[:2])                                            
    minute = int(time[2:])
    if minute == 0: 
        minute = "00"
    elif minute < 10: 
        minute = "0" + str(minute)
    else: 
        minute = str(minute)
    printout = "hh:mm ap"
    if hour > 12:
        return f"{hour-12}:{minute} PM"
    elif hour == 12: 
        return f"{hour}:{minute} PM"
    else: 
        return f"{hour}:{minute} AM"

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
###Prints the calendar
def printCalendar(year: int, month: int, today: int):
    #print("~~~~~~~~~~~~~~~~~~~ clear screen ~~~~~~~~~~~~~~~~~~~")
    os.system("clear")
    #Print Header
    thisDate = str(date(year, month, today))
    monthNmbr = int(thisDate[5:7])
    monthName = monthMap(monthNmbr, reverse=True)
    print(f"      {monthNmbr} - {monthName.capitalize()} - {year}\n")
    
    previousMonth = 0
    if month > 1:
        previousMonth = month - 1
    else:
        previousMonth = 12

    printout = [['\033[4;30;49mSu|', 
                 ' M|', 'Tu|', ' W|', 'Th|', ' F|', 
                 'Sa\033[0m|'],
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
            printout[1][i] = ("\033[0;97;49m" + 
                              datePrint(lml - startDay + i + 1) + 
                              "\033[0m" + "|"
                             )
            
    #Set dates for current month
    printWeek = 1
    printWeekDay = startDay
    try: 
        eventDates = events[year][month].keys()
    except: 
        eventDates = []
    for i in range(1,lengthOfMonth+1):
        #Printing the Day
        if (i == today) and (i in eventDates):
            printout[printWeek][printWeekDay] = ("\033[1;31;43m" + 
                                                 datePrint(i) + 
                                                 "\033[0m" + "|"
                                                )
        elif i == today: 
            printout[printWeek][printWeekDay] = ("\033[1;30;43m" + 
                                                 datePrint(i) + 
                                                 "\033[0m" + "|"
                                                )
        elif i in eventDates:
            printout[printWeek][printWeekDay] = ("\033[1;31;49m" + 
                                                 datePrint(i) + 
                                                 "\033[0m" + "|"
                                                )
        else: 
            printout[printWeek][printWeekDay] = datePrint(i) + "|"
            
        #Setting up the next iteration
        if printWeekDay == 6:
            printWeek += 1
            printWeekDay = 0
        else: 
            printWeekDay += 1
    
    #Set dates for next month
    if printWeekDay != 0:
        for i in range(7 - printWeekDay):
            printout[printWeek][i+printWeekDay] = ("\033[0;97;49m" + 
                                                   datePrint( i + 1 ) + 
                                                   "\033[0m" + "|"
                                                  )

    printStatement = ""
    for week in printout:
        printStatement += "\t|"
        for day in week:
            printStatement += day
        printStatement += "\n"
    print(printStatement)
    
    try: 
        todaysEvents = events[year][month][today]
        if todaysEvents == []: 
            print("No events this day.")
    except: 
        print("No events this day.")
    else: 
        print("Events this day:")
        for i, event in enumerate(todaysEvents):
            print(f'\t{i+1}: {event.name}')

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### Some user input functions
def askForDate():
    try: 
        request = input('Pick a date ("MMDDYYYY" or ' +
                        '"done" to close calendar): \n').lower().strip()
    except: 
        print("I don't know what that means? Try again please.")

    print('\n')
    return request

def askForCommand():
    try: 
        command = input('\nWhat would you like to do?\n' + 
                        '(type "h" for help or '+
                        '"done" to finish editing/viewing this day) \n'
                       ).lower().strip()
    except: 
        print("I don't know what that means? Try again please.")

    #print('\n')
    return command

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### Calendar interaction functions  
def receiveCommands(year, month, day):
    #request = input("What would you like to do")
    #while input != done: 
    command = askForCommand()
    
    #TODO: Ask someone how to make this more robust
    while command != "done":
        if   command == possibleCommands[0][0]: 
            printHelp(0)
        elif command == possibleCommands[1][0]:
            addAnEvent(1)
        elif command == possibleCommands[2][0]:
            deleteAnEvent(2, year, month, day)
        elif command == possibleCommands[3][0]:
            viewAnEvent(3, events[year][month][day])
        elif command == possibleCommands[4][0]:
            printCalendar(year, month, day)
        else:
            print("Not an option. Please try again.")
        
        command = askForCommand()
        
def printHelp(index):
    print(f"\n\033[1m{possibleCommands[index][1]}:\033[0m")
    
    print("\033[4;30;49m Input\t| Name\t| Definition\033[0m")
    for action in possibleCommands: 
        print(f"{action[0]}\t|{action[1]}\t|{action[2]}")
    
def addAnEvent(index):
    print(f"\n\033[1m{possibleCommands[index][1]}:\033[0m")
    
    name = input("What is the event?\n")
    thisDate = input("What day will it take place? (MMDDYYYY)\n")
    year = int(thisDate[4:])
    month = int(thisDate[:2])
    day = int(thisDate[2:4])
    thisDate = date(year, month, day)
    start = input("When will it begin? (hhmm, military time)\n")
    end = input("When will it end? (hhmm, military time)\n")
    
    if year not in events.keys(): 
        events[year] = {month: {day: [event(name, thisDate, start, end)]}}
    elif month not in events[year].keys():
        events[year][month] = {day: [event(name, thisDate, start, end)]}
    elif day not in events[year][month].keys():
        events[year][month][day] = [event(name, thisDate, start, end)]
    else: 
        events[year][month][day].append(event(name, thisDate, start, end))
    print(f"{name} added.")
    
def deleteAnEvent(index, year, month, day):
    print(f"\n\033[1m{possibleCommands[index][1]}:\033[0m")
    
    eventNum = -1 + int(
            input('Which event would you like to delete? ' +
                  '(give the number)\n'))
    daysEvents = events[year][month][day]
    name = daysEvents[eventNum].name
    check = input(f'Deleting {name}. ' +
                  'Are you sure? (yes or no)\n').lower().strip()
    if check == "no": 
        return
    #try: 
    if eventNum in range(len(daysEvents)):
        newDay = []
        for i in range(len(daysEvents)):
            if i != eventNum: 
                newDay.append(daysEvents[i])
        events[year][month][day] = newDay
        print(f"{name} deleted.")
    else: 
        print("That date doesn't exist.")
    #except: 
    #    print("I don't understand what that means.")
    
def viewAnEvent(index, day):
    print(f"\n\033[1m{possibleCommands[index][1]}:\033[0m")
    
    eventNum = -1 + int(
            input("Which event would you like to view? (give the number)\n"))
    print('\n')
    
    if day == []: 
        print("No events this day.")
    elif eventNum in range(len(day)):
        printEvent(day[eventNum])
        print("\n")
    else: 
        print("That date doesn't exist.")

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### Some Event things        
class event():
    def __init__(self, name, date, start, end):
        self.name = name
        self.date = date
        self.start = start
        self.end = end
        
    def store(self): 
        return f"{self.name};{datePrint(self.date)};{self.start};{self.end}"
    
    def read(self, string):
        string = string.split(";")
        self.name = string[0]
        self.date = string[1]
        self.start = string[2]
        self.end = string[3]
        
def printEvent(event): 
    print(event.name)
    
    #TODO: Make the date print nicer
    print(f'{datePrint(event.date)}:' + 
          f' {timePrint(event.start)} - {timePrint(event.end)}')


### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
#Actual Program   

possibleCommands = [
        ["h","Help", "Prints all possible, valid commands."],
        ["a", "Add", "Add an event."],
        ["d", "Delete", "Delete an event."],
        ["v", "View", "View an event"],
        ["c", "Clear", "Clear the screen and show the calendar."]
    ]

events = {
    2020: {
        1: {
            7: [
                event("Forrest's Birthday", date(2020, 1, 7), "0000", "2359"),
                event("Class", date(2020, 1, 7), "1000", "1100")
                ],
            30: [event("Someone's Birthday", date(2020, 1, 30), "0000", "2359")],
            27: [event("Someone Else's Birthday", date(2020, 1, 27), "0000", "2359")]
            }
        ,
        5: {
            30: [event("Mama's Birthday", date(2020, 5, 30), "0000", "2359")]
            }
        }
        ,
    2019: {
        8: {
            28: [event("Sarah's Birthday", date(2019, 8, 28), "0000", "2359")]
        }
    }
}

os.system("clear")
request = askForDate()

while request != "done":
    try: 
        month = int(request[:2])
        day   = int(request[2:4])
        year  = int(request[4:])
        printCalendar(year, month, day)
    except: 
        if len(request) != 8:
            print("Format for entry not obeyed. Please try again.")
        else: 
            print("Date does not exist. Please try again.")
        request = askForDate()
    else: 
        receiveCommands(year, month, day)
    request = askForDate()
