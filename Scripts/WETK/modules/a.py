#!/usr/bin/python
#author: namhb
class Module:
	def __init__(self, logger):
		self.logger						=	logger
		self.name						=	"Template Module"		# Change it
		self.author						=	"namhb"
		self.version					=	"0.0.1"
		self.basicOptions				=	{
				"URL"	:	{
					"currentSetting"	:	None,
					"required"			:	True,
					"description"		:	"URL to exploit"
				}
			}
		self.options 					=	None					# Input options
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
		print("Basic options:")
		print("\t{0:7s}{1:20s}{2:12s}{3}".format("Name","Current Setting","Required","Description"))
		print("\t{0:7s}{1:20s}{2:12s}{3}".format("----","---------------","--------","-----------"))
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
	def sendHTTPRequest(self):
		print("test")
	def start(self):
		self.logger.info("Loaded Module: {0}.".format(self.name))
		if(self.checkOptions() != False):
			exit()
		# We coding here

######---------------------------------------------#####
module 									= 	None
# Init module
def init(logger):
	global module
	module 								=	Module(logger)
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