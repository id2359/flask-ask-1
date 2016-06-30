import json,datetime, time
from datetime import datetime
def setExpenditure(date,description,add_to_budget,amount,category):
	f = open("data.json","r")
	data = json.load(f)
	x = { "inserted_at" : date, "description" : description, "add_to_budget" : add_to_budget, "amount" : int(amount) , "category" : category}
	data[0]["budgeting"]["transactions"].append(x)
	if add_to_budget == True:
		data[0]["budgeting"]["budget"][category] += int(amount)   
	else :
		data[0]["budgeting"]["expenditure"][category] += int(amount)
		data[0]["budgeting"]["balance"] -= int(amount)
	f.close()
	f1 = open("data.json","w")
	json.dump(data,f1)
def getExpenditure(category = "all", duration=9999):
	print category
	f = open("data.json","r")
	data = json.load(f)
	f.close()
	if duration == 9999:
		return data[0]["budgeting"]["expenditure"][category]
	trans_by_category = []
	if category == "all":
		trans_by_category = data[0]["budgeting"]["transactions"]
	else:
		for x in data[0]["budgeting"]["transactions"]:
			if x["category"] == category:
				trans_by_category.append(x)
	trans_by_category_exp = []
	for x in trans_by_category:
		if str(x["addToBudget"]) == "false":
			trans_by_category_exp.append(x)
	print (trans_by_category_exp)
	date_format = "%m/%d/%Y"
	expenditure_display = 0
	today = time.strftime("%m/%d/%Y")
	today = datetime.strptime(today,date_format)
	for x in trans_by_category_exp:
		a = datetime.strptime(str(x["insertedAt"]), date_format)
		if (int((today-a).days)) <= duration:
			expenditure_display += int(x["amount"])
	return expenditure_display	
def getBudget(category="all"):
	f = open("data.json","r")
	data = json.load(f)
	if category == "all":
		budget = data[0]["budgeting"]["budget"]["total"]
	else:
		budget = data[0]["budgeting"]["budget"][category]
	f.close()
	return budget

def setBudget(amount,category="all"):
	f = open("data.json","r")
	data = json.load(f)
	f.close()
	if category == "all":
		data[0]["budgeting"]["budget"]["total"] = int(amount)
		data[0]["budgeting"]["budget"]["miscellaneous"] = int(amount)
	else:
		data[0]["budgeting"]["budget"]["total"] = int(amount)
		data[0]["budgeting"]["budget"][category] =  int(amount)
	f1 = open("data.json","w")
	json.dump(data,f1)
	f1.close()
def getBalance():
	f = open("data.json","r")
	data = json.load(f)
	f.close()
	return data[0]["budgeting"]["balance"]