######---------------------------------------------#####
module 										= 	None
# Init module
def init(logger, profile):
	global module
	module 									=	Module(logger, profile)
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
	module.run()
	module.end()