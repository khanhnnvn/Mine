#!/usr/bin/python
#author: namhb
import requests
class Module:
	def __init__(self, logger):
		self.logger						=	logger
		self.name						=	"CTF Brute Forcr Module"								# Changed
		self.description 				=	"This is Module for Brute force, file fuzzing"
		self.rank						=	"MEDIUM"												# Exploit level
		self.type						=	"Scan"													# Type: exploit | scanner | support
		self.author						=	"namhb"
		self.version					=	"0.0.1"
		self.basicOptions				=	{
				"URL"	:	{
					"currentSetting"	:	None,
					"required"			:	True,
					"description"		:	"URL to scanner"
				}
			}
		self.fileList 					= 	[
				"robots.txt",
				".htaccess",
				"web.config",
				"login.php",
				"admin.php",

			]
		self.options 					=	None													# Input options
		# Help for this module, how to use
		self.help 						=	"" \
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
		print("\t{0:7s}{1:20s}{2:12s}{3}".format("Name","Current Setting","Required","Description"))
		print("\t{0:7s}{1:20s}{2:12s}{3}".format("----","---------------","--------","-----------"))
		print("")
		for key in self.basicOptions.keys():
			option 							= 	self.basicOptions[key]
			requiredString					=	option["required"] and "YES" or "NO"
			print("\t{0:7s}{1:20s}{2:12s}{3}".format(key,option["currentSetting"],requiredString,option["description"]))
	def checkOptions(self):
		check 								=	True
		for key in self.basicOptions.keys():
			if((self.basicOptions[key]["required"] == True) and (self.basicOptions[key]["currentSetting"]==None)):
				check 						=	False
				self.logger.error("Option {0} need configure.".format(key))
		return check
	def sendHttpGetRequest(self, url):
		if(url[:5] == "https"):
			r 								=	requests.get(url,verify=False)
			r.headers["content-length"]		=	None
		else:
			r 								=	requests.get(url)
		return r
	def start(self):
		if(self.checkOptions() == False):
			exit()
		self.logger.warning("Started Module: {0}.".format(self.name))
		# We coding here
		print("Site: {0} result:".format(self.basicOptions["URL"]["currentSetting"]))
		print("==========================")
		print("")
		print("\t{0:50s}{1:10s}{2}".format("Filename","Code","Size"))
		print("\t{0:50s}{1:10s}{2}".format("--------","----","----"))
		print("")
		for fileName in self.fileList:
			url 							=	"{0}/{1}".format(self.basicOptions["URL"]["currentSetting"],fileName)
			r 								=	self.sendHttpGetRequest(url)
			print("\t{0:50s}{1:10s}{2}".format(fileName,str(r.status_code),r.headers["content-length"]))
######---------------------------------------------#####
module 									= 	None
# Init module
def init(logger):
	global module
	module 								=	Module(logger)
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
	module.printOptions()
	module.checkOptions()
# Set options
def setOptions(options):
	global module
	module.options 						=	options
	module.optionParse()
# Main to start module
def run():
	global module 
	module.start()
