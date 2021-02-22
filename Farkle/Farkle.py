from tkinter import Tk, Button, Frame, Label, Menu, Toplevel, Entry
from PIL import Image, ImageTk
import os
import random
import mysql.connector

# populating seed for random number generator
randomG = random
randomG.seed()

# used to keep track of who's turn it is
userTurn = ""
# Game Dice
dice = [0, 0, 0, 0, 0, 0]
rerolledDice = []
# used to keep track of die that the user would like to re-roll
lockedInDie = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False}
# tracked each rounds points
points = 0
allPLastRound = False
newScoringDie = False
gameEnd = 2000

# Will be used to access Farkle Player Object
players = []
names = []

# AI Farkle
aiFarkled = False
fromAI = False

# Global TK Objects
main = Tk()
main.title("Farkle")

# Main program function definitions
# ____________________________________________________


# simulates a die roll by providing a random number
def rollDie():
    return randomG.randrange(6) + 1


# takes a number between 1 and 6 and returns the OS path to the image (in same directory as the script)
def dieImage(dieNumber):
    directory1 = os.path.dirname(os.path.realpath(__file__))
    a = str(dieNumber)
    return os.path.join(directory1, a + '.png')


def checkScoring(fromSelectiveRoll=False):
    dieCount = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    roundPoints = 0
    global dice
    global points
    global allPLastRound
    global lockedInDie
    global newScoringDie
    newScoringDie = False
    # Counting how many of each die exist
    for die in dice:
        dieCount[die] = dieCount[die] + 1

    # Locking in non scoring die
    for die in dieCount:
        if dieCount[die] < 3:
            for x in range(len(dice)):
                if dice[x] == die:
                    if die != 1 and die != 5:
                        lockedInDie[x+1] = True

        # Looking for scoring die and updating global points
        if die == 1 and dieCount[die] > 0:
            if dieCount[die] == 3:
                roundPoints = roundPoints + 1000
            elif 3 < dieCount[die] < 6:
                if dieCount[die] == 4:
                    roundPoints = roundPoints + 1100
                if dieCount[die] == 5:
                    roundPoints = roundPoints + 1200
            elif dieCount == 6:
                roundPoints = roundPoints + 2000
            else:
                roundPoints = roundPoints + (100 * dieCount[die])
        elif die == 5 and dieCount[die] > 0:
            if dieCount[die] == 3:
                roundPoints = roundPoints + 500
            elif 3 < dieCount[die] < 6:
                if dieCount[die] == 4:
                    roundPoints = roundPoints + 550
                if dieCount[die] == 5:
                    roundPoints = roundPoints + 600
            elif dieCount[die] == 6:
                roundPoints = roundPoints + 1000
            else:
                roundPoints = roundPoints + (50 * dieCount[die])
        else:
            if dieCount[die] == 3:
                roundPoints = roundPoints + (die * 100)
            elif 3 < dieCount[die] < 6:
                roundPoints = roundPoints + (die * 100)
                c = 0
                for x in range(6):
                    if dice[x] == die:
                        c = c + 1
                        if c > 3:
                            lockedInDie[x+1] = True
            elif dieCount == 6:
                roundPoints = roundPoints + (die * 200)

    if stateCheck(messages=False):
        allPLastRound = True
        points = roundPoints + points
    elif roundPoints > 0 and allPLastRound:
        points = roundPoints + points
        allPLastRound = False
    elif roundPoints > 0 and fromSelectiveRoll:
        for x in rerolledDice:
            if x == 1 or x == 5:
                newScoringDie = True
            elif dieCount[x] == 3:
                newScoringDie = True

        points = roundPoints
    elif roundPoints > 0:
        points = roundPoints
    else:
        points = 0


# destroys main window and ends program
def endProgram():
    main.destroy()


# resizes windows to default
def setWindowSize(window, x):
    window.geometry(x)


# Discovers all frames associated with a window then removes them
def clearWindow(window):
    children = window.winfo_children()

    for item in children:
        if item.winfo_children():
            children.extend(item.winfo_children())

    for item in children:
        item.pack_forget()


# Draws the title screen after clearing any thing existing in the main window
def drawTitleScreen():
    clearWindow(main)
    setWindowSize(main, "200x100")
    titleScreen.pack()


def lockIn(number):
    global die1B
    global die2B
    global die3B
    global die4B
    global die5B
    global die6B

    if 6 >= number > 0:
        if number == 1 and die1B["background"] == "Grey":
            lockedInDie[number] = True
            die1B.config(background="Green")
            gameFrame3.pack()
        elif number == 1 and die1B["background"] == "Green":
            lockedInDie[number] = False
            die1B.config(background="Grey")
            gameFrame3.pack()

        if number == 2 and die2B["background"] == "Grey":
            lockedInDie[number] = True
            die2B.config(background="Green")
            gameFrame3.pack()
        elif number == 2 and die2B["background"] == "Green":
            lockedInDie[number] = False
            die2B.config(background="Grey")
            gameFrame3.pack()

        if number == 3 and die3B["background"] == "Grey":
            lockedInDie[number] = True
            die3B.config(background="Green")
            gameFrame3.pack()
        elif number == 3 and die3B["background"] == "Green":
            lockedInDie[number] = False
            die3B.config(background="Grey")
            gameFrame3.pack()

        if number == 4 and die4B["background"] == "Grey":
            lockedInDie[number] = True
            die4B.config(background="Green")
            gameFrame3.pack()
        elif number == 4 and die4B["background"] == "Green":
            lockedInDie[number] = False
            die4B.config(background="Grey")
            gameFrame3.pack()

        if number == 5 and die5B["background"] == "Grey":
            lockedInDie[number] = True
            die5B.config(background="Green")
            gameFrame3.pack()
        elif number == 5 and die5B["background"] == "Green":
            lockedInDie[number] = False
            die5B.config(background="Grey")
            gameFrame3.pack()

        if number == 6 and die6B["background"] == "Grey":
            lockedInDie[number] = True
            die6B.config(background="Green")
            gameFrame3.pack()
        elif number == 6 and die6B["background"] == "Green":
            lockedInDie[number] = False
            die6B.config(background="Grey")
            gameFrame3.pack()
        stateCheck()
        checkScoring()


def endTurn():
    global userTurn
    global points
    global players
    global allPLastRound
    global newScoringDie
    global lockedInDie
    global dice
    global rerolledDice
    global aiFarkled

    if players[0].playerNamesAndScores[userTurn] == 0 and points < 999 and not rollAllB["background"] == "Red":
        notificationL.config(text="You have not yet rolled enough points to enter the game, you must keep rolling!")
        notificationLabelFrame.pack()
    else:
        if rollAllB["background"] == "Red":
            # Resetting all things
            rollAllB.config(background="Grey", command=lambda: rollAll(True))
            points = 0
            allPLastRound = False
            newScoringDie = False
            lockedInDie = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False}
            dice = [0, 0, 0, 0, 0, 0]
            rerolledDice = []

            directory1 = os.path.dirname(os.path.realpath(__file__))
            imagePath1 = os.path.join(directory1, "b.png")
            imageBlank = Image.open(str(imagePath1))
            blankP = ImageTk.PhotoImage(imageBlank)

            dieL1 = Label(gameFrame2, image=blankP)
            dieL1.image = blankP
            dieL1.grid(row=0, column=0)

            dieL2 = Label(gameFrame2, image=blankP)
            dieL2.image = blankP
            dieL2.grid(row=0, column=1)

            dieL3 = Label(gameFrame2, image=blankP)
            dieL3.image = blankP
            dieL3.grid(row=0, column=2)

            dieL4 = Label(gameFrame2, image=blankP)
            dieL4.image = blankP
            dieL4.grid(row=0, column=3)

            dieL5 = Label(gameFrame2, image=blankP)
            dieL5.image = blankP
            dieL5.grid(row=0, column=4)

            dieL6 = Label(gameFrame2, image=blankP)
            dieL6.image = blankP
            dieL6.grid(row=0, column=5)

            gameFrame1.pack()
            gameFrame2.pack()
            gameFrame3.pack()
            gameFrame4.pack()
            drawFarkle()
        else:

            players[0].playerNamesAndScores[userTurn] = points + players[0].playerNamesAndScores[userTurn]

            # Resetting all things
            rollAllB.config(background="Grey", command=lambda: rollAll(True))
            points = 0
            allPLastRound = False
            newScoringDie = False

            lockedInDie = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False}
            dice = [0, 0, 0, 0, 0, 0]
            rerolledDice = []

            directory1 = os.path.dirname(os.path.realpath(__file__))
            imagePath1 = os.path.join(directory1, "b.png")
            imageBlank = Image.open(str(imagePath1))
            blankP = ImageTk.PhotoImage(imageBlank)

            dieL1 = Label(gameFrame2, image=blankP)
            dieL1.image = blankP
            dieL1.grid(row=0, column=0)

            dieL2 = Label(gameFrame2, image=blankP)
            dieL2.image = blankP
            dieL2.grid(row=0, column=1)

            dieL3 = Label(gameFrame2, image=blankP)
            dieL3.image = blankP
            dieL3.grid(row=0, column=2)

            dieL4 = Label(gameFrame2, image=blankP)
            dieL4.image = blankP
            dieL4.grid(row=0, column=3)

            dieL5 = Label(gameFrame2, image=blankP)
            dieL5.image = blankP
            dieL5.grid(row=0, column=4)

            dieL6 = Label(gameFrame2, image=blankP)
            dieL6.image = blankP
            dieL6.grid(row=0, column=5)

            gameFrame1.pack()
            gameFrame2.pack()
            gameFrame3.pack()
            gameFrame4.pack()
            drawFarkle()

        # determining winner, displaying to players that the game has ended and updating the winners score in the
        # database.
        if players[0].playerNamesAndScores[userTurn] >= gameEnd:
            displayWinner = Toplevel(main)
            winner = Label(displayWinner, text=userTurn+" has won! with: "+str(players[0].playerNamesAndScores[userTurn]))

            # connecting to local MySQL database where scores are recorded
            databaseNamesWins = {}
            scoresDatabase = mysql.connector.connect(host="127.0.0.1", user="FarkleGame", passwd="ThisPasswordIsWeak1",
                                                     database="farklescores")
            cursor = scoresDatabase.cursor()
            cursor.execute("select * from scores order by winCount desc;")
            for player in cursor:
                line = str(player)
                playerName = ""
                playerWins = ""
                playerName = line[line.find('(\'') + 2:line.find('\',')]
                playerWins = line[line.find('\',') + 3:line.find(')')]
                databaseNamesWins[playerName] = int(playerWins)

            if userTurn in databaseNamesWins:
                databaseNamesWins[userTurn] = int(databaseNamesWins[userTurn]) + 1
                cursor.execute("INSERT INTO scores (uName, winCount) VALUES (\'" + userTurn + "\', "
                               + str(databaseNamesWins[userTurn]) + ") ON DUPLICATE KEY UPDATE winCount = "
                               + str(databaseNamesWins[userTurn]) + ";")
                scoresDatabase.commit()
            else:
                cursor.execute("INSERT INTO scores (uName, winCount) VALUES (\'" + str(userTurn) + "\', 1);")
                scoresDatabase.commit()

            scoresDatabase.disconnect
            resetButton = Button(displayWinner, text="Back to main menu", command=lambda: [displayWinner.destroy(),
                                                                                           drawTitleScreen()])
            resetButton.pack()
            winner.pack()

        userIndex = names.index(userTurn)

        if userIndex != len(names)-1:
            userTurn = names[userIndex + 1]
        else:
            userTurn = names[0]
        turnLabel.config(text=userTurn + "'s Turn")

        if "AI Player" in userTurn:
            AIPlayerTurn(userTurn)
        else:
            Button(gameFrame4, text="End Turn", background = "Red", command=lambda:endTurn()).grid(row=1, column=1)
            gameFrame4.pack()

    allPLastRound = False
    newScoringDie = False
    aiFarkled = False


def drawDie(die, fromSelectRoll=False):

    # redrawing die
    if not fromSelectRoll:
        dieI1 = Image.open(dieImage(die[0]))
        photo1 = ImageTk.PhotoImage(dieI1)
        dieL1 = Label(gameFrame2, image=photo1)
        dieL1.image = photo1
        dieL1.grid(row=0, column=0)

        dieI2 = Image.open(dieImage(die[1]))
        photo2 = ImageTk.PhotoImage(dieI2)
        dieL2 = Label(gameFrame2, image=photo2)
        dieL2.image = photo2
        dieL2.grid(row=0, column=1)

        dieI3 = Image.open(dieImage(die[2]))
        photo3 = ImageTk.PhotoImage(dieI3)
        dieL3 = Label(gameFrame2, image=photo3)
        dieL3.image = photo3
        dieL3.grid(row=0, column=2)

        dieI4 = Image.open(dieImage(die[3]))
        photo4 = ImageTk.PhotoImage(dieI4)
        dieL4 = Label(gameFrame2, image=photo4)
        dieL4.image = photo4
        dieL4.grid(row=0, column=3)

        dieI5 = Image.open(dieImage(die[4]))
        photo5 = ImageTk.PhotoImage(dieI5)
        dieL5 = Label(gameFrame2, image=photo5)
        dieL5.image = photo5
        dieL5.grid(row=0, column=4)

        dieI6 = Image.open(dieImage(die[5]))
        photo6 = ImageTk.PhotoImage(dieI6)
        dieL6 = Label(gameFrame2, image=photo6)
        dieL6.image = photo6
        dieL6.grid(row=0, column=5)
    else:
        for x in range(len(die)):
            if x == 1:
                dieI1 = Image.open(dieImage(die[0]))
                photo1 = ImageTk.PhotoImage(dieI1)
                dieL1 = Label(gameFrame2, image=photo1)
                dieL1.image = photo1
                dieL1.grid(row=0, column=0)

            if x == 2:
                dieI2 = Image.open(dieImage(die[1]))
                photo2 = ImageTk.PhotoImage(dieI2)
                dieL2 = Label(gameFrame2, image=photo2)
                dieL2.image = photo2
                dieL2.grid(row=0, column=1)

            if x == 3:
                dieI3 = Image.open(dieImage(die[2]))
                photo3 = ImageTk.PhotoImage(dieI3)
                dieL3 = Label(gameFrame2, image=photo3)
                dieL3.image = photo3
                dieL3.grid(row=0, column=2)

            if x == 4:
                dieI4 = Image.open(dieImage(die[3]))
                photo4 = ImageTk.PhotoImage(dieI4)
                dieL4 = Label(gameFrame2, image=photo4)
                dieL4.image = photo4
                dieL4.grid(row=0, column=3)

            if x ==5:
                dieI5 = Image.open(dieImage(die[4]))
                photo5 = ImageTk.PhotoImage(dieI5)
                dieL5 = Label(gameFrame2, image=photo5)
                dieL5.image = photo5
                dieL5.grid(row=0, column=4)

            if x == 6:
                dieI6 = Image.open(dieImage(die[5]))
                photo6 = ImageTk.PhotoImage(dieI6)
                dieL6 = Label(gameFrame2, image=photo6)
                dieL6.image = photo6
                dieL6.grid(row=0, column=5)

    gameFrame2.pack()


def stateCheck(messages=True, fromSelectRoll=False):
    global points
    global lockedInDie
    global dice
    global newScoringDie
    # seeing if any dice will 'need' to be rerolled i.e. not scoring die
    # checking to see if all of the die are scoring die, if they are it returns True if not then it returns False
    # this can be used by the game logic to determine next steps.
    allScoring = False
    count = 0
    for die in lockedInDie:
        if not lockedInDie[die] and points == 0:
            count = count + 1
    if count == 6:
        allScoring = True

    # Setting die to selectable for individual reroll
    if not lockedInDie[1]:
        die1B.config(command=lambda: lockIn(number=1), background="Grey")
    else:
        die1B.config(command=lambda: lockIn(number=1), background="Green")
        lockedInDie[1] = True
    if not lockedInDie[2]:
        die2B.config(command=lambda: lockIn(number=2), background="Grey")
    else:
        die2B.config(command=lambda: lockIn(number=2), background="Green")
        lockedInDie[2] = True
    if not lockedInDie[3]:
        die3B.config(command=lambda: lockIn(number=3), background="Grey")
    else:
        die3B.config(command=lambda: lockIn(number=3), background="Green")
        lockedInDie[3] = True
    if not lockedInDie[4]:
        die4B.config(command=lambda: lockIn(number=4), background="Grey")
    else:
        die4B.config(command=lambda: lockIn(number=4), background="Green")
        lockedInDie[4] = True
    if not lockedInDie[5]:
        die5B.config(command=lambda: lockIn(number=5), background="Grey")
    else:
        die5B.config(command=lambda: lockIn(number=5), background="Green")
        lockedInDie[5] = True
    if not lockedInDie[6]:
        die6B.config(command=lambda: lockIn(number=6), background="Grey")
    else:
        die6B.config(command=lambda: lockIn(number=6), background="Green")
        lockedInDie[6] = True
    gameFrame3.pack()
    if messages:
        # dealing with different game states such as Farkle or such
        if not allScoring:
            rollSelectedB.config(command=lambda: rollSelected(unlocked=True), background="Grey")
            gameFrame3.pack()
            notificationL.config(text="")
            notificationLabelFrame.pack()
            if points == 0 or (not newScoringDie and fromSelectRoll):
                newScoringDie = False
                notificationL.config(text="You've Rolled A Farkle!\n"
                                          "No points will be recorded for you this round.")
                rollSelectedB.config(command=lambda: rollSelected(False), background="Red")
                rollAllB.config(background="Red", command=lambda: rollAll(False))
                gameFrame3.pack()
                notificationLabelFrame.pack()
                global fromAI
                if fromAI:
                    global aiFarkled
                    aiFarkled = True
        else:
            rollSelectedB.config(command=lambda: rollSelected(unlocked=False), background="Red")
            die1B.config(background="Red")
            die2B.config(background="Red")
            die3B.config(background="Red")
            die4B.config(background="Red")
            die5B.config(background="Red")
            die6B.config(background="Red")
            gameFrame3.pack()
            if points != 0:
                notificationL.config(text="You've Rolled all Point Die!\n"
                                          "You must roll all dice at least once more before banking.")
            notificationLabelFrame.pack()
        rolledScore.config(text="Current rolled score score is: " + str(points))
        currentScore.config(text="Your running score is: " + str(players[0].playerNamesAndScores[userTurn]))
        gameFrame4.pack()

    return allScoring


def rollAll(unlocked):
    if unlocked:
        newDie = []
        global dice
        global lockedInDie
        lockedInDie = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False}
        for i in range(6):
            newDie.append(rollDie())
        # performing sort, redrawing die and marking required re rolls
        newDie.sort()

        drawDie(newDie)

        # assigning new die to the global dice variable
        dice = newDie
        checkScoring()
        stateCheck(messages=True)


# Rolls the die that the user has selected and have been marked Green
def rollSelected(unlocked, ai=False):
    if unlocked and not ai:
        oldDie = []
        global dice
        global rerolledDice
        global lockedInDie
        rerolledDice.clear()
        for die in lockedInDie:
            if lockedInDie[die]:
                rerolledDice.append(rollDie())
            else:
                oldDie.append(dice[die - 1])

        lockedInDie = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False}
        dice = rerolledDice + oldDie
        dice.sort()
        checkScoring(True)
        stateCheck(messages=True, fromSelectRoll=True)
        drawDie(dice)


# Clears the game state and starts a new game
def farkleStart():
    global userTurn
    global turnLabel
    global names
    f = FarklePlayers()
    # wait for user to enter all needed info
    main.wait_window(f.popup)

    turnLabel.pack()
    players.clear()
    players.append(f)
    names = list(f.playerNamesAndScores.keys())
    userTurn = names[0]
    drawFarkle()
    turnLabel.config(text=userTurn + "'s Turn")

    if len(names) > 0:
        if "AI Player" in userTurn:
            AIPlayerTurn(userTurn)


def drawFarkle():
    global userTurn
    global turnLabel
    clearWindow(main)
    turnLabel.pack()
    setWindowSize(main, "600x600")

    die1B.config(background="Red")
    die2B.config(background="Red")
    die3B.config(background="Red")
    die4B.config(background="Red")
    die5B.config(background="Red")
    die6B.config(background="Red")
    gameFrame1.pack()
    gameFrame2.pack()
    gameFrame3.pack()
    gameFrame4.pack()


def AIPlayerTurn(aiName):
    global rollSelectedB
    global rollAllB
    global points
    global fromAI
    fromAI = True
    endT = False

    def didAIFarkl():
        global aiFarkled
        if aiFarkled:
            farkleNotification = Toplevel(main)
            aiFarkledFrame1 = Frame(farkleNotification)
            oops = Label(aiFarkledFrame1, text="oops looks like I farkled")
            oops.grid(row=0, column=0)
            closeNote = Button(aiFarkledFrame1, text="Understood", command=lambda: farkleNotification.destroy())
            closeNote.grid(row=1, column=0)
            aiFarkledFrame1.pack()
            main.wait_window(farkleNotification)
            aiFarkled=False
            endTurn()
            return True

    rollSelectedB.config(command=lambda: rollSelected(unlocked=False, ai=True))
    rollAllB.config(command=lambda: rollAll(False))
    AIStepButton = Button(gameFrame4, text="AI Step->", command=lambda: AIPlayerTurn(aiName))
    AIStepButton.grid(row=1, column=1)
    gameFrame3.pack()
    gameFrame4.pack()

    if players[0].playerNamesAndScores[userTurn] == 0 and points == 0:
        rollAll(True)
        drawDie(dice)
        endT = didAIFarkl()
        if endT:
            AIStepButton.destroy()
            endTurnB.config(text="End Turn", background="Red", command=lambda: endTurn())
            gameFrame3.pack()
            gameFrame4.pack()
    elif players[0].playerNamesAndScores[userTurn] == 0 and points < 1000:
        rollSelected(unlocked=True, ai=False)
        drawDie(dice)
        endT = didAIFarkl()
    elif points >= 1000:
        endTurn()
        endT = True

    elif points == 0:
        rollAll(True)
        drawDie(dice)
        endT = didAIFarkl()
    elif points < 300:
        rollSelected(unlocked=True, ai=False)
        drawDie(dice)
        endT = didAIFarkl()
        AIStepButton.destroy()
    elif points >= 300:
        endTurn()
        endT = True
        AIStepButton.destroy()

    fromAI = False


def viewManual():
    fileContent = ""
    with open("FarkleRules.txt") as file:
        fileContent = file.readlines()

    manualPopup = Toplevel(main)
    frame1 = Frame(manualPopup)

    Label(frame1, text="Game Manual", font="bold").pack()

    for line in fileContent:
        Label(frame1, text=line, justify="left").pack()
    frame1.pack()


def viewScores():
    # connecting to local MySQL database where scores are recorded
    scoresDatabase = mysql.connector.connect(host="127.0.0.1", user="FarkleGame", passwd="ThisPasswordIsWeak1",
                                             database="farklescores")
    cursor = scoresDatabase.cursor()

    cursor.execute("select * from scores order by winCount desc;")
    scoresPopup = Toplevel(main)
    setWindowSize(scoresPopup, "300x800")
    frame1 = Frame(scoresPopup)
    Label(frame1, text="Player Names", font='bold').grid(row=0, column=0)
    Label(frame1, text="Socres", font='bold').grid(row=0, column=1)

    # displaying scores
    count = 1
    for player in cursor:
        line = str(player)
        playerName = ""
        playerWins = ""

        playerName = line[line.find('(\'')+2:line.find('\',')]
        playerWins = line[line.find('\',')+3:line.find(')')]

        Label(frame1, text=playerName).grid(row=count, column=0)
        Label(frame1, text=playerWins).grid(row=count, column=1)
        count = count + 1

    frame1.pack()
    scoresDatabase.disconnect()

# Program Classes
# ____________________________________________________


# class will be used by the farkle function to perform game logic
class FarklePlayers:
    def __init__(self):
        clearWindow(main)
        # display popup asking for the number of players.
        self.popup = Toplevel(main)
        self.playerCFrame1 = Frame(self.popup)
        self.playerCFrame2 = Frame(self.popup)
        setWindowSize(self.popup, "300x200")
        self.howManyLabel = Label(self.playerCFrame1, text="How Many Players?").grid(row=0, column=0)
        self.enterNumber = Entry(self.playerCFrame1)
        self.enterNumber.select_clear()
        self.enterNumber.insert(0, "2")
        self.enterNumber.grid(row=1, column=0)
        self.submitB = Button(self.playerCFrame2, text="Submit", command=self.setPlayerCount).grid(row=2, column=0)
        self.backB = Button(self.playerCFrame2, text="Back", command=self.back).grid(row=2, column=2)
        self.playerCFrame1.pack()
        self.playerCFrame2.pack()

        # setup popup frames for player names/AI Player.
        self.playerNameFrame1 = Frame(self.popup)
        self.playerNameFrame2 = Frame(self.popup)
        self.playerNameFrame3 = Frame(self.popup)
        self.errorFrame = Frame(self.popup)
        self.nameLabel = Label(self.playerNameFrame1, text="Name ").grid(row=0, column=0)
        self.enterName = Entry(self.playerNameFrame1)
        self.enterName.select_clear()
        self.enterName.grid(row=1, column=0)
        self.backB2 = Button(self.playerNameFrame2, text="Back", command=self.back)
        self.backB2.grid(row=0, column=1)
        self.nextNameB = Button(self.playerNameFrame2)
        self.nextNameB.grid(row=0, column=0)
        self.aiPlayerB = Button(self.playerNameFrame3, text="AI Player?", command=self.addAIPlayer)
        self.aiPlayerB.grid(row=0, column=0)
        self.dupError = Label(self.errorFrame, text="Player Names Must be Unique!").grid(row=0, column=0)

        # Set FarkleInfo Variables, used throughout
        # trace is used to find if a name already exists in the dictionary
        self.trace = False
        self.aiPlayercount = 1
        self.playerCount = 0
        self.playerNamesAndScores = {}

    # Gets the user's entered number of players and checks to make sure that the entered value is a number and is
    # greater then two, if so then it moves on to asking for player names, if not then asks player for valid input.
    def setPlayerCount(self):
        if str(self.enterNumber.get()).isnumeric():
            self.playerCount = int(self.enterNumber.get())
            if self.playerCount < 2:
                clearWindow(self.popup)
                playerCountWarnFrame = Frame(self.popup)
                notifyUser = Label(playerCountWarnFrame,
                                   text="You must enter a number greater then 2 \nIt's no fun playing on your"
                                        " own.")
                notifyUser.pack()
                okB = Button(playerCountWarnFrame, text="OK", command=self.resetPlayerCountPopup)
                okB.pack()
                playerCountWarnFrame.pack()

            else:
                clearWindow(self.popup)
                self.setPlayerNames()

    # Wrapper function that displays a box and button asking for the user to enter the name of each player, when
    # the button is pressed the assignName function is called which gets the data from the entry field, adds it to the
    # dictionary of player names and scores and checks to see if more players need to be added.  If they do then
    # setPlayerNames is called again.
    def setPlayerNames(self):
        if not self.trace:
            clearWindow(self.popup)

        self.nextNameB.config(text="Submit Player " + str(len(self.playerNamesAndScores) + 1), command=self.assignName)
        self.playerNameFrame1.pack()
        self.playerNameFrame2.pack()
        self.playerNameFrame3.pack()
        self.trace = False

    # Assigns entry field data to dictionary does nothing if field is blank.
    def assignName(self):
        # checks if there are any entries in the dictionary and that user in isn't empty
        if self.enterName.get() != '' and len(self.playerNamesAndScores) > 0:

            # looking for duplicate player names
            for player in self.playerNamesAndScores:
                if player == str(self.enterName.get()):
                    self.trace = True

            # assigning non duplicate players
            if not self.trace:
                self.playerNamesAndScores[str(self.enterName.get())] = 0
                self.playerCount = self.playerCount - 1
            else:
                self.dupError = Label(self.errorFrame, text="Player Names Must be Unique!").grid(row=0, column=0)
                self.errorFrame.pack()

        # assigning first player
        else:
            if self.enterName.get() != '':
                self.playerNamesAndScores[str(self.enterName.get())] = 0
                self.playerCount = self.playerCount - 1

        # checking if more player names need to be added if not destroy popup window
        if self.playerCount > 0:
            self.setPlayerNames()
            self.enterName.delete(0, 'end')
        else:
            self.popup.destroy()

    # Adds AI players to the game.
    def addAIPlayer(self):
        for player in self.playerNamesAndScores:
            if player == "AI Player" + str(self.aiPlayercount):
                self.aiPlayercount = self.aiPlayercount + 1
        self.playerNamesAndScores["AI Player"+str(self.aiPlayercount)] = 0
        self.playerCount = self.playerCount - 1
        if self.playerCount > 0:
            self.setPlayerNames()
            self.enterName.delete(0, 'end')
        else:
            self.popup.destroy()

    # Used by playerCount to reset the window (but leaves the message) if the user enters invalid info.
    def resetPlayerCountPopup(self):
        setWindowSize(self.popup, "300x200")
        self.playerCFrame1.pack()
        self.playerCFrame2.pack()

    # sends the user back to the main screen
    def back(self):
        self.popup.destroy()
        self.playerCount = 0
        self.playerNamesAndScores = {}
        drawTitleScreen()


# Kicks the program off by drawing the title screen
# ---------------------------------------#
titleScreen = Frame(main)
startGameB = Button(titleScreen, text="Start", command=farkleStart).grid(row=0, column=0)
viewManualB = Button(titleScreen, text="Manual", command=viewManual).grid(row=1, column=0)
viewScoresB = Button(titleScreen, text="Scores", command=viewScores).grid(row=2, column=0)
drawTitleScreen()

# Adding menu bar which will persist throughout the program
menuBar = Menu(main)
fileMenu = Menu(main, tearoff=0)
fileMenu.add_command(label="View Manual", command=viewManual)
fileMenu.add_command(label="View Scores", command=viewScores)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=endProgram)
menuBar.add_cascade(label="File", menu=fileMenu)
main.config(menu=menuBar)

# setting up the Farkle game widgets
# ---------------------------------------#

# populating blank board image details
directory = os.path.dirname(os.path.realpath(__file__))
imagePath = os.path.join(directory, "b.png")
image = Image.open(str(imagePath))
photo = ImageTk.PhotoImage(image)

# Game Frames contain info that needs to be presented throughout the Farkle game
gameFrame1 = Frame(main)
gameFrame2 = Frame(main)
gameFrame3 = Frame(main)
gameFrame4 = Frame(main)

turnLabel = Label(gameFrame1, text=userTurn)
turnLabel.grid(row=0, column=0)

# Inserting board area
dieSpace1 = Label(gameFrame2, image=photo)
dieSpace2 = Label(gameFrame2, image=photo)
dieSpace3 = Label(gameFrame2, image=photo)
dieSpace4 = Label(gameFrame2, image=photo)
dieSpace5 = Label(gameFrame2, image=photo)
dieSpace6 = Label(gameFrame2, image=photo)
dieSpace1.image = photo
dieSpace2.image = photo
dieSpace3.image = photo
dieSpace4.image = photo
dieSpace5.image = photo
dieSpace6.image = photo
dieSpace1.grid(row=0, column=0)
dieSpace2.grid(row=0, column=1)
dieSpace3.grid(row=0, column=2)
dieSpace4.grid(row=0, column=3)
dieSpace5.grid(row=0, column=4)
dieSpace6.grid(row=0, column=5)

# setting up Die Buttons
die1B = Button(gameFrame3, text="Roll Die 1", background="Red")
die2B = Button(gameFrame3, text="Roll Die 2", background="Red")
die3B = Button(gameFrame3, text="Roll Die 3", background="Red")
die4B = Button(gameFrame3, text="Roll Die 4", background="Red")
die5B = Button(gameFrame3, text="Roll Die 5", background="Red")
die6B = Button(gameFrame3, text="Roll Die 6", background="Red")
die1B.grid(row=0, column=0)
die2B.grid(row=0, column=1)
die3B.grid(row=0, column=2)
die4B.grid(row=0, column=3)
die5B.grid(row=0, column=4)
die6B.grid(row=0, column=5)

# setting up roll All and Roll Selected Buttons
rollSelectedB = Button(gameFrame3, text="Roll", background="Red", command=lambda: rollSelected(unlocked=False))
rollAllB = Button(gameFrame3, text="Roll All", background="Grey", command=lambda: rollAll(True))
rollSelectedB.grid(row=2, column=2)
rollAllB.grid(row=2, column=3)

# Adding End Turn Button
endTurnB = Button(gameFrame4, text="End Turn", background="Red", command=lambda: endTurn())
rolledScore = Label(gameFrame4, text="Current rolled score score is: " + str(points))
rolledScore.grid(row=0, column=0)
currentScore = Label(gameFrame4)
currentScore.grid(row=1, column=0)
endTurnB.grid(row=1, column=1)

# Adding notification labels
notificationLabelFrame = Frame(main)
notificationL = Label(notificationLabelFrame)
notificationL.grid(row=0, column=0)

# main loop loops through the game code.
main.mainloop()
