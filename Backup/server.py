from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from datetime import datetime
import json_parser, time
app = Flask(__name__)
ask = Ask(app,"/")

@ask.launch
def launch():
	speech_output = "What do you want to do? Say stuff like get balance, expenditure, or add an expense to your mint account"
	return question(speech_output)

@ask.intent('HelloIntent')
def hello():
    return statement("Hello world from flask")


@ask.intent('TestIntent')
def TestIntent():
	return question("What category?").reprompt("Which category do you want expenditures for?")

@ask.intent('TestIntentAns',convert = {'category' : 'TestCategory'})
def TestIntentAns(category):
	data = json_parser(category)
	return statement("Your expenditure for " + category + " is " + str(data) + " dollars")

@ask.intent('GetBalance')
def GetBalance():
	data = json_parser.getBalance()
	return statement("Your balance is " + str(data) + " dollars.")

@ask.intent('GetBudget',mapping = {'category':'CATEGORY'}, default = {'category' : 'all'})
def GetBudget(category):
	data = json_parser.getBudget(category)
	return statement("Your budget for " + category + " is " + str(data) + " dollars")

@ask.intent('SetBudget',mapping = {'category' : 'CATEGORY', 'amount' : 'NUMBER'})
def SetBudget(category,amount):
	json_parser.setBudget(amount,category)
	return statement("Your budget has been successfully set. ")

@ask.intent('GetExpenditure',mapping = {'category' : 'CATEGORY', 'days' : 'DAYS'})
def GetExpenditure(category="all",days=9999):
	print category
	print days
	if category == None:
		category1 = "all"
	else :
		category1 = ''.join(category.split(' '))
	if days==None:
		data = json_parser.getExpenditure(category1)
	else:
		data = json_parser.getExpenditure(category1, int(days))
	print category
	if category == None:
		return statement("Your expenditure is " + str(data) + " dollars ")
	else:
		return statement("Your expenditure on " + category + " is " + str(data) + " dollars ")

@ask.intent('SetExpenditure',mapping = {'category' : 'CATEGORY', 'AMOUNT' : 'AMOUNT'})
def SetExpenditure(amount,category):
	today = time.strftime("%m/%d/%Y")
	json_parser.setExpenditure(today,"HAHA",False,amount,category)
	return statement("Alright. Expense added!")
@ask.intent('InsertEntry',mapping={'firstname': 'NUMBER'})
def insertEntry(firstname):
	#a = 10
	#a = a + int(firstname)
	#firstname = str(a)
	text = render_template('hello', firstname=firstname)
	return statement(text).simple_card('Hello', text)

if __name__ == '__main__':
    app.run(debug=True)	