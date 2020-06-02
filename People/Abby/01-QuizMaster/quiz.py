## Quiz testing knowledge of python builtins
## 2020 June 1

## TODO : Add answer options (1-4, so you type number not copy/paste ans)
##        Actually work in all the built ins, real ans, and fake ans

import random

# Identify all Built-ins
reals = [
         ["Arithmetic Error", "ans"],
         ["AssertionError", "ans"],
         ["AttributeError", "ans"],
        ]

# Load in all fake Built-Ins
fakes = [
         ["Arithmetic Error","A","B","C"],
         ["AssertionError","A","B","C"],
         ["AttributeError","A","B","C"],
        ]

# Do the quiz

## Ask how many questions the quiz will be and initialize grading scheme
numQs = int(input(
         "\nHow many questions would you like to answer? (enter a number):\t"
        ) ) 
numCorrect = 0
numIncorrect = 0

## Actually administer the quiz
for i in range(numQs):
    randomNum = random.randint(0, len(fakes)-1)
    testedBuiltIn = reals[randomNum][0]
    potentialAnswers = [reals[randomNum][1], fakes[randomNum][1],
                        fakes[randomNum][2], fakes[randomNum][3] ]
    random.shuffle(potentialAnswers)
    letters = {"A":0, "B":1, "C":2, "D":3}
    print("Question {0}: What is {1}?".format(i, testedBuiltIn))
    for key, value in letters.items():
        print(f"""\t{key}: {potentialAnswers[value]}""") 
    answer = input("Your Answer? (type the letter)\t").strip().upper()
    if potentialAnswers[letters[answer]] == reals[randomNum][1]:
        numCorrect += 1
    else: 
        numIncorrect += 1
    reals.pop(randomNum)
    fakes.pop(randomNum)

# Output Results
print("\n ~~~~ Quiz Complete ~~~~ \n")
print("You got {0} correct out of {1}".format(numCorrect, numQs))
print("Your final score is {0}%".format(numCorrect/numQs*100))
print("Thanks for playing!\n")
