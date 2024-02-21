#Project for a Python self study class from 2015
#This is an early version, I lost access to the final version
#This version contains the ability to change a locally stored password
#the GUI set up using tkinter, and a broken script for creating a vote and 
#adding positions, because this version was in the middle of switching over to
#a sqlite database, and these functions weren't yet updated to pull those values

#The final version stored all variables and values that could change on the
#sqlite database, and had a working createVote, addPosition, endVote function
#pulling those values from the database as needed

import tkinter
from tkinter import *
import sqlite3
import datetime


# testing purposes only
password = 'test'

# create database file
conn = sqlite3.connect('firefight')
c = conn.cursor()

# create tables
c.execute('''CREATE TABLE IF NOT EXISTS users(
          id int auto_increment primary key, username text, password text, admin boolean)''')
c.execute('''CREATE TABLE IF NOT EXISTS positions(
          position text)''')
c.execute('''CREATE TABLE IF NOT EXISTS current(
          position text, candidate text, votes int)''')
c.execute('''CREATE TABLE IF NOT EXISTS past(
          position text, candidate text, votes int, winner boolean)''')

c.execute('''INSERT INTO users(username, password, admin) 
          VALUES('admin', 'VoteProgram', 'yes')''')


'''
tables:
users:
    username text
    password text
    admin boolean
positions:
    position text
current:
    position text
    candidate text
    votes int
past:
    position text
    candidate text
    votes int
    winner boolean
'''

# define root window
root = tkinter.Tk()
root.minsize(width=800, height = 600)
root.maxsize(width=800, height = 600)

# Admin sign in Label
areAdmin = Label(root, text="Administrator sign in", font=("Arial", 18))
areAdmin.pack()

# password label and password
passwordLabel = Label(root, text="Password: ", font=("Arial", 12))
passwordLabel.place(x=300, y=30)

# password entry
adminPasswordEntry = Entry(root)
adminPasswordEntry.place(x=385, y=32.5)

# function for button
def getEnteredPassword(event):
    enteredPassword = adminPasswordEntry.get()
    if enteredPassword == password:
        # define admin window
        admin = tkinter.Toplevel()
        admin.minsize(width=800, height = 600)
        admin.maxsize(width=800, height = 600)
        # label saying to change password
        changePasswordLabel = Label(admin, text="It is recommended to change your password the first time you log in.",
                                    font=("Arial", 16), wraplength=500)
        changePasswordLabel.pack()
        # old password
        changePassword_OldPasswordLabel = Label(admin, text="Old Password: ", font=("Arial", 12))
        changePassword_OldPasswordLabel.place(x=250, y=50)
        changePassword_OldPassword = Entry(admin)
        changePassword_OldPassword.place(x=365, y=52.5)
        # new password
        changePassword_NewPasswordLabel = Label(admin, text="New Password: ", font=("Arial", 12))
        changePassword_NewPasswordLabel.place(x=250, y=70)
        changePassword_NewPassword = Entry(admin)
        changePassword_NewPassword.place(x=365, y=72.5)
    
        # function to change password
        def passwordChangeCommand():
            global password
            oldPasswordValue = changePassword_OldPassword.get()
            newPasswordValue = changePassword_NewPassword.get()
            if oldPasswordValue == password:
                password = newPasswordValue
            else:
                wrong = tkinter.Toplevel()
                wrong.minsize(width=200, height = 100)
                wrong.maxsize(width=200, height = 100)
                Label(wrong, text="Sorry that password is incorrect!", font=("Arial", 24), anchor=W, wraplength=180,
                      fg="red").pack()
        
        # submit button
        newPasswordSubmit = Button(admin, text="Submit", width=10, command=passwordChangeCommand)
        newPasswordSubmit.place(x=350, y=100)
        
        newVoteLabel = Label(admin, text="Create New Vote", font=("Arial", 16))
        newVoteLabel.place(x=310, y=135)

        # positions drop down
        newVoteChoosePositionLabel = Label(admin, text="Choose the position you are voting for", font=("Arial", 12))
        newVoteChoosePositionLabel.place(x=265, y=170)
        position = StringVar(admin)
        position.set("Chief")
        newVoteOption = OptionMenu(admin, position, "Chief")
        newVoteOption.place(x=355, y=195)

        def addPositions():
            newPositions = addPositionsEntry.get()
            formatted = [x.strip() for x in newPositions.split(',')]
            for x in formatted:
                c.execute("INSERT INTO positions VALUES(?)", x)

        # add positions
        addPositionsLabel = Label(admin, text="Please type any positions you'd like to add below, separated by commas",
                                  font=("Arial", 12), wraplength=200)
        addPositionsLabel.place(x=575, y=135)
        addPositionsEntry = Entry(admin, width=30)
        addPositionsEntry.place(x=575, y=195)
        addPositionsButton = Button(admin, text="Submit", width=10, command=addPositions)
        addPositionsButton.place(x=625, y=220)

        newVoteCandLabel = Label(admin, text="Please enter all candidates names below, separated by commas",
                                 font=("Arial", 12), wraplength=250)
        newVoteCandLabel.place(x=275, y=230)
        newVoteCandEntry = Entry(admin, width=50)
        newVoteCandEntry.place(x=250, y=275)
        newVoteButton = Button(admin, text="Submit", width=10)
        newVoteButton.place(x=355, y=300)

        def newVote():
            today = datetime.date.today()
            votingOn = position.get()
            
            
            

        newVoteCandEntry.bind("<Return>", newVote)
        newVoteButton.bind("<Button-1>", newVote)
        
        
    else:
        wrong = tkinter.Toplevel()
        wrong.minsize(width=200, height = 100)
        wrong.maxsize(width=200, height = 100)
        Label(wrong, text="Sorry that password is incorrect!", font=("Arial", 24), anchor=W, wraplength=180,
              fg="red").pack()

# enter button for password
passwordEnterButton = Button(root, text="Enter", width=10)
passwordEnterButton.place(x=360, y=60)
passwordEnterButton.bind("<Button-1>", getEnteredPassword)
root.bind("<Return>", getEnteredPassword)

# Close database when closing window
def onClose():
    c.close
    root.destroy()
    
root.protocol("WM_DELETE_WINDOW", onClose)
root.mainloop()

