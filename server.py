from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from datetime import datetime
import json_parser, time, webbrowser
app = Flask(__name__)
ask = Ask(app,"/")
setExpendituresession = False
getExpendituresession =False
setBudgetsession =False
getBudgetsession =False
RemainingExpendituresession = False
gdays = 0
gamount = 0

@ask.launch
def launch():
	speech_output = "What do you want to do? Say stuff like get balance, expenditure, or add an expense to your mint account"
	return question(speech_output)

@ask.intent('HelloIntent')
def hello():
	return statement("Hello world from flask")


@ask.intent('TestIntentAns',mapping = {'category' : 'CATEGORY'})
def TestIntentAns(category):
	print category
	getBudgetsession = session.attributes.get('GetBudgetsession')
	setBudgetsession = session.attributes.get('setBudgetsession')
	getExpendituresession = session.attributes.get('GetExpendituresession')
	setExpendituresession = session.attributes.get('setExpendituresession')
	RemainingExpendituresession = session.attributes.get('RemainingExpendituresession')
	print RemainingExpendituresession
	gamount = int(session.attributes.get('Gamount'))
	gdays =   int(session.attributes.get('Gdays'))
	if getExpendituresession :
		return GetExpenditure(category,gdays)
	elif setExpendituresession :
		return SetExpenditure(gamount,category)
	elif setBudgetsession :
		return SetBudget(category,gamount)
	elif getBudgetsession :
		return GetBudget(category)
	elif RemainingExpendituresession:
		return RemainingBudget(category)
	else :
		return launch() 

@ask.intent('GetBalance')
def GetBalance():
	data = json_parser.getBalance()
	# webbrowser.open('http://localhost:3000/display')
	return statement("Your balance is " + str(data) + " dollars.")

@ask.intent('GetBudget',mapping = {'category':'CATEGORY'})
def GetBudget(category):
	if category == None:
		session.attributes['GetBudgetsession'] = True
		session.attributes['setBudgetsession'] = False
		session.attributes['setExpendituresession'] = False
		session.attributes['GetExpendituresession'] = False
		session.attributes['RemainingExpendituresession'] = False
		session.attributes['Gamount'] = 0
		session.attributes['Gdays'] = 0	
		return question("What category?").reprompt("Which category do you want get Budget for?") 
	else :
		category1 = ''.join(category.split(' '))
	data = json_parser.getBudget(category1)
	getBudgetsession = False
	return statement("Your budget for " + category + " is " + str(data) + " dollars")

@ask.intent('SetBudget',mapping = {'category' : 'CATEGORY', 'amount' : 'NUMBER'})
def SetBudget(category,amount):
	if category == None:
		session.attributes['GetBudgetsession'] = False
		session.attributes['setBudgetsession'] = True
		session.attributes['setExpendituresession'] = False
		session.attributes['GetExpendituresession'] = False
		session.attributes['RemainingExpendituresession'] = False
		session.attributes['Gamount'] = amount
		session.attributes['Gdays'] = 0
		print amount 
		print session.attributes['Gamount']
		return question("What category?").reprompt("Which category do you want set Budget for?") 
	else :
		category1 = ''.join(category.split(' '))
	json_parser.setBudget(amount,category)
	setBudgetsession = False
	return statement("Your budget has been successfully set. ")

@ask.intent('RemainingBudget',mapping={'category' : 'CATEGORY'}, default={'category' : 'all'})
def RemainingBudget(category=all):
	if category == None:
		session.attributes['GetBudgetsession'] = False
		session.attributes['setBudgetsession'] = False
		session.attributes['setExpendituresession'] = False
		session.attributes['GetExpendituresession'] = False
		session.attributes['Gamount'] = 0
		session.attributes['Gdays'] = 0	
		session.attributes['RemainingExpendituresession'] = True
		return question("For which category?").reprompt("For which category do you wanna know your remaining cash?")
	else:
		category1 = ''.join(category.split(' '))
	rem = json_parser.RemainingBudget(category)
	RemainingExpendituresession = False
	if rem>0:
		return statement("You can still spend " + str(rem) + " dollars on " + category)
	else:
		return statement("You've exceeded your budget already by " + str(rem) + " dollars for " +category)

@ask.intent('GetExpenditure',mapping = {'category' : 'CATEGORY', 'days' : 'DAYS'}, default = {'category' : 'all'})
def GetExpenditure(category="all",days=9999):
	if category == None:
		session.attributes['GetBudgetsession'] = False
		session.attributes['setBudgetsession'] = False
		session.attributes['setExpendituresession'] = False
		session.attributes['GetExpendituresession'] = True
		session.attributes['RemainingExpendituresession'] = False
		session.attributes['Gamount'] = 0
		session.attributes['Gdays'] = days
		return question("What category?").reprompt("Which category do you want expenditures for?") 
	else :
		category1 = ''.join(category.split(' '))
	if days==None:
		data = json_parser.getExpenditure(category1)
	else:
		data = json_parser.getExpenditure(category1, int(days))
	print category
	getExpendituresession =False
	if category == None:
		return statement("Your expenditure is " + str(data) + " dollars ")
	else:
		if days != None:
			return statement("Your expenditure on " + category + " is " + str(data) + " dollars over the last "+str(days)+" days")
		else:
			return statement("Your expenditure on " + category + " is " + str(data) + " dollars")
@ask.intent('SetExpenditure',mapping = {'category' : 'CATEGORY', 'amount' : 'AMOUNT'})
def SetExpenditure(amount,category):
	if category == None:
		session.attributes['GetBudgetsession'] = False
		session.attributes['setBudgetsession'] = False
		session.attributes['setExpendituresession'] = True
		session.attributes['GetExpendituresession'] = False
		session.attributes['RemainingExpendituresession'] = False
		session.attributes['Gamount'] = amount
		session.attributes['Gdays'] = 0
		
		return question("What category?").reprompt("Which category do you want to set expenditures for?") 
	else :
		category1 = ''.join(category.split(' '))
	today = time.strftime("%m/%d/%Y")
	json_parser.setExpenditure(today,"HAHA","false",amount,category1)
	setExpendituresession =False
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