#author: namhb
import sys, time, requests, os, logging, argparse, datetime, platform, pkgutil, imp

'''
How to use:
'''
######---------------------------------------------#####
######-------------- WEToolKit class ---- ---------#####
class WEToolKit:
	def __init__(self):
		#Const
		self.dirPath		=		os.getcwd() 								# relative directory path
		self.filePath		=		os.path.abspath(__file__) 					# absolute file path
		self.fileName		=		os.path.basename(__file__) 					# the file name only
		self.system			=		platform.system()							# check OS
		self.debug			=		False										# default disable debug
		self.version 		=		"0.0.1a"									# TK version
		self.logFolder		=		"logs"										# Log store
		self.modulesFolder	=		"modules"									# Modules folder 
		self.moduleFolderPath= 		os.path.join(self.dirPath,self.modulesFolder) # Modules folder Path
		self.logPrefix		=		"wetk"										# Log Prefix
		#Variables
		self.getArument()
		#Print info, include: flleName
	def loadModule(self, moduleName):
		self.logger.debug("Try to load: {0}.".format(moduleName))
		imp.load_source("wetkModule",self.dirPath+"/a.py")
		import wetkModule
		wetkModule.init(self.logger)
	def getArument(self):
		parser 				= 		argparse.ArgumentParser(description="WETK - Web Exploit ToolKit - Version {0}".format(self.version))
		#Enable debug
		parser.add_argument(
			'-d',
			'--debug',
			help 			=		'enable/disable debug',
			default			=		'false'
			)
		#Show version
		parser.add_argument(
			'-v',
			'--version',
			help 			=		'WETK version',
			action			=		'store_true',
			)
		#List Module
		parser.add_argument(
			'-l',
			'--list',
			help 			=		'List all modules',
			action			=		'store_true',
			)
		#Use Module
		parser.add_argument(
			'-u',
			'--use',
			help 			=		'Use module'
			)
		#Update Framework
		parser.add_argument(
			'--update',
			help 			=		'Update Framework',
			action			=		'store_true',
			)		
		#Set default is show help
		if(len(sys.argv) < 2):
			#Only Filename
			parser.print_help()
			exit(0)
		self.args 			= 		parser.parse_args()
		#Log config
		self.logConfig()
		# Set variable
		if(self.args.use != ""):
			self.modulePath	=		self.args.use
			self.loadModule(self.modulePath)

	def logConfig(self):
		self.logger 		= 		logging.getLogger(__name__)					# Logging constructor
		# Set format
		self.logFormat 		= 		logging.Formatter("%(asctime)-15s %(message)s")				
		# Console Handler
		consoleHandler 		= 		logging.StreamHandler()
		consoleHandler.setFormatter(self.logFormat)
		self.logger.addHandler(consoleHandler)
		# File Handler
		dateTimeNow 		= 		datetime.datetime.now()
		logFileName			=		"{0}_{1}_{2}_{3}.log".format(
										self.logPrefix,
										dateTimeNow.year,
										dateTimeNow.month,
										dateTimeNow.day)
		logFilePath			=		os.path.join(self.dirPath, self.logFolder, logFileName)
		fileHandler 		= 		logging.FileHandler(logFilePath)
		fileHandler.setFormatter(self.logFormat)
		self.logger.addHandler(fileHandler)
		# Get and set debug
		debugString			=		self.args.debug.lower()
		if(debugString == "true"):
			self.debug 		=		True
			self.logger.setLevel(logging.DEBUG)	
		elif(debugString == "false"):
			self.debug 		=		False
			self.logger.setLevel(logging.INFO)
		else:
			self.debug 		=		None
		if(self.debug==None):
			self.logger.error("Debug Argument is True/False only. Exit now!")
			exit(0)
		self.logger.debug("Set Logging mode is {0}.".format(self.debug))


######---------------------------------------------#####


def main():
	tk 						= 		WEToolKit()


if __name__ == "__main__":
	main()


