from flask import Flask, render_template, request, redirect
import os
from pymongo import MongoClient

app 	=	Flask(__name__)
@app.route("/")
def hello():
	return "Hello"

if __name__ == "main":
	app.run()
