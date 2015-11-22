#!/usr/bin/python
#author: namhb
import re, requests, string
class Module:
	def __init__(self, logger):
		self.logger							=	logger
		self.name							=	"Template Module"		# Change it
		self.description 					=	"This is Template Module for develope"
		self.rank							=	"HIGH"					# Exploit level
		self.type							=	"Exploit"				# Type: exploit | scanner | support
		self.author							=	"namhb"
		self.version						=	"0.0.1"
		self.requestCount 					=	0
		self.injectPoint 					=	None
		self.stringCollections 				=	string.printable
		self.basicOptions					=	{
				"URL"	:	{
					"currentSetting"		:	None,
					"required"				:	True,
					"description"			:	"URL to exploit"
				},
				"METHOD" : {
					"currentSetting"		:	None,
					"required"				:	False,
					"description"			:	"HTTP Method: get/post/head"
				},
				"USERAGENT" : {
					"currentSetting"		:	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
					"required"				:	False,
					"description"			:	"User Agent to exploit"
				},
				"COOKIE" : {
					"currentSetting"		:	None,
					"required"				:	False,
					"description"			:	"Cookie to exploit, use <cookie_name1>:<cookie_value1>;<cookie_name2>:<cookie_value2>"
				},
				"REFERER" : {
					"currentSetting"		:	"https://www.google.com/",
					"required"				:	False,
					"description"			:	"Referer to exploit"
				},
				"HOST" : {
					"currentSetting"		:	None,
					"required"				:	False,
					"description"			:	"Host to exploit"
				},
				# "DBMS" : {
				# 	"currentSetting"		:	"mysql",
				# 	"required"				:	True,
				# 	"description"			:	"Type of DMBS: mysql/mssql/oracle"
				# },
				"DATA" : {
					"currentSetting"		:	None,
					"required"				:	False,
					"description"			:	"POST Data to exploit"
				},
			}
		self.options 						=	None					# Input options
		# Help for this module, how to use
		self.help 							=	"" \
			"This is help for module." \
			""
	def optionParse(self):
		for i in range(0, len(self.options)):
			if(self.options[i].find("=") > 0):
				option 						=	self.options[i].split("=")
				key 						=	option[0]
				value 						=	option[1]
			else:
				key 						=	self.options[i]
				value 						=	None
			if(key in self.basicOptions.keys()):
				# Set value
				self.logger.debug("Set {0} to {1}.".format(key,value))
				self.basicOptions[key]["currentSetting"] = value
			else:
				self.logger.debug("Option {0} not found.".format(key))
	def printOptions(self):
		print("Basic options")
		print("=============")
		print("")
		print("\t{0:10s}{1:30s}{2:12s}{3}".format("Name","Current Setting","Required","Description"))
		print("\t{0:10s}{1:30s}{2:12s}{3}".format("----","---------------","--------","-----------"))
		print("")
		for key in self.basicOptions.keys():
			option 							= 	self.basicOptions[key]
			requiredString					=	option["required"] and "YES" or "NO"
			print("\t{0:10s}{1:30s}{2:12s}{3}".format(key,option["currentSetting"],requiredString,option["description"]))
	def checkOptions(self):
		check 								=	True
		for key in self.basicOptions.keys():
			if((self.basicOptions[key]["required"] == True) and (self.basicOptions[key]["currentSetting"]==None)):
				check 						=	False
				self.logger.error("Option {0} need configure.".format(key))
				return check
			# Check URL start with http or https
			if(key == "URL"):
				url 						=	self.basicOptions[key]["currentSetting"]
				if((url[:7] == "http://") or (url[:8] == "https://")):
					self.logger.debug("URL include http/https, don`t need add prefix.")
				else:
					self.basicOptions["URL"]["currentSetting"] = "{0}{1}".format("http://",self.basicOptions["URL"]["currentSetting"])
					self.logger.debug("Add prefix http to: {0}.".format(self.basicOptions["URL"]["currentSetting"]))
			# For SQL injection or DBMS Scanner only
			# if(key == "DBMS"):
			# 	# Set default is mysql
			# 	if(self.basicOptions[key]["currentSetting"] == None):
			# 		self.basicOptions[key]["currentSetting"] = "mysql"
			# 	else:
			# 		# Check type of DBMS: mysql/mssql/oracle
			# 		dbms 					=	self.basicOptions[key]["currentSetting"].lower()
			# 		if((dbms=="mysql") or (dbms=="mssql") or (dbms=="oracle")):
			# 			pass
			# 		else:
			# 			check 				=	False
			# 			self.logger.error("DBMS type must in mysql/mssql/oracle only.")
			# 			return check
			if(key == "METHOD"):
				# Set default is GET
				if(self.basicOptions[key]["currentSetting"] == None):
					self.basicOptions[key]["currentSetting"] = "get"
				else:
					methodType 				=	self.basicOptions[key]["currentSetting"].lower()
					if((methodType == "get") or (methodType == "post") or (methodType == "head")):
						pass
					else:
						check 				=	False
						self.logger.error("METHOD must in get/post/head only.")
						return check
					if(methodType == "post"):
						# Post data is set or not
						if(self.basicOptions["DATA"]["currentSetting"] == None):
							check 			=	False
							self.basicOptions["DATA"]["required"] = True
							self.logger.error("POST data must set in POST Method.")
			# Check inject point (only one inject point, with * character)
			# Set HOST default is URL
			if(key == "HOST"):
				if((self.basicOptions[key]["currentSetting"] == None) and (self.basicOptions["URL"]["currentSetting"] != None) ):
					self.basicOptions[key]["currentSetting"] = self.basicOptions["URL"]["currentSetting"]
		return check
	def checkInjectPoint(self):
		# Check only one inject point
		# For all parameter manipulation, SQL, XSS, LFI use same
		numberStar							=	0
		for key in self.basicOptions.keys():
			# Check in URL, COOKIE, DATA, USERAGENT, REFERER
			if((key == "URL") or (key == "USERAGENT") or (key == "COOKIE") or (key == "REFERER") or (key == "DATA")):
				dataString					=	self.basicOptions[key]["currentSetting"]
				if(dataString != None):
					number 					=	len(re.findall("\*",dataString))
					if(number > 0):
						self.logger.debug("Found {0} inject point in {1}".format(number,key))
						if((number == 1) and (self.injectPoint == None)):
							self.injectPoint=	key
							self.logger.debug("Set inject point to: {0}".format(key))
						elif(number > 1):
							self.logger.error("Only one inject point (* character) in {0}.".format(key))
						numberStar			+=	number
		if(numberStar == 0):
			self.logger.error("Not found any inject point.")
			return False
		elif(numberStar == 1):
			self.logger.warning("Inject point is ready.")
			return True
		elif(numberStar > 1):
			self.logger.error("Only one inject point (* character).")
			return False
	def sendHTTPRequest(self, payload):
		# Create http request with your options

		# Update number request
		self.requestCount					+=	1
	# def getLength(self, query):
	# def getQueryResult(self, query):
	# def checkQuery(self, query):
	def start(self):
		if(self.checkOptions() == False):
			exit()
		if(self.checkInjectPoint() == False):
			exit()
		self.logger.warning("Started Module: {0}.".format(self.name))
		# We coding here

		# Finish
		self.logger.warning("Send {0} request.".format(self.requestCount))
######---------------------------------------------#####
module 										= 	None
# Init module
def init(logger):
	global module
	module 									=	Module(logger)
# Get Name
def getName():
	global module
	return module.name
# Get Type
def getType():
	global module
	return module.type
# Get Rank
def getRank():
	global module
	return module.rank
# Get Version
def getVersion():
	global module
	return module.version
# Get Description
def getDescription():
	global module
	return module.description
# Show help
def showHelp():
	global module
	module.logger.info("Show Module Help")
	print("This is module {0} by {1}.".format(module.name, module.author))
	print(module.help)
# Show options
def showOptions():
	global module
	module.logger.info("Show Module Options")
	module.printOptions()
# Show options
def checkOptions():
	global module
	module.logger.info("Check Module Options")
	module.checkOptions()
	module.printOptions()
# Set options
def setOptions(options):
	global module
	module.options 							=	options
	module.optionParse()
# Main to start module
def run():
	global module 
	module.start()

