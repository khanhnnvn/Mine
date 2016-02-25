from flask import Flask, render_template, request, redirect
import os
from pymongo import MongoClient

app 	=	Flask(__name__)

def connect():
	connection 	=	MongoClient("localhost",27017)
	handle 		=	connection["test"]
	return handle
app 	=	Flask(__name__)
handle	=	connect()	
@app.route("/")
def hello():
	if (request.args.get("id") is not None):
		id = request.args.get("id")
		spec = {'id': 1}
		cursor = handle.test_table.find({"id":id})
		str = ""
		for document in cursor:
			print(document)	
		return str
	else:
		return "Hello"
@app.route("/json",methods=['GET','POST'])
def json():
	data = request.json
	id = (data['id'])
	print(data['id'])
	cursor = handle.test_table.find({'id':id})
	for document in cursor:
		print(document)	
	return "json"
app.run(host="0.0.0.0", port=8080, debug=True)
