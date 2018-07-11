# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 18:40:45 2014

@author: hbq
"""

# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions
import random
def name_to_number(name):
    if name == "rock":
        name = 0
    elif name == "Spock":
        name = 1
    elif name == "paper":
        name = 2
    elif name == "lizard":
        name = 3
    elif name == "scissors":
        name = 4
    else:
        print "please enter a correct choice"
    return name

def number_to_name(number):
    if number == 0:
        number = "rock"
    elif number == 1:
        number = "spock"
    elif number == 2:
        number = "paper"
    elif number == 3:
        number = "lizard"
    elif number == 4:
        number = "scissors"
    return number
    
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    

def rpsls(player_choice): 
    # print a blank line to separate consecutive games
    print "\n"
    # print out the message for the player's choice
    # convert the player's choice to player_number using the function name_to_number()
    print "Playser chooses " + player_choice 
    player_choice = name_to_number(player_choice)
    # compute random guess for comp_number using random.randrange()
    cchoice = random.randrange(0,4)
    # convert comp_number to comp_choice using the function number_to_name()
    computer_choice = number_to_name(cchoice)
    # print out the message for computer's choice
   
    # compute difference of comp_number and player_number modulo five
    result = (cchoice - player_choice) % 5
    # use if/elif/else to determine winner, print winner message
       
    print "Computer chooses " + computer_choice
    if result == 0 :
        print "Computer and Player tie!"
    elif result <=2:
        print "Player wins!"
    elif result >= 3:
        print "Computer wins!"
    
# test your code - LEAVE THESE CALLS IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


