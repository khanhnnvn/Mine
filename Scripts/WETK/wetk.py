#!/usr/bin/python
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
		self.dirPath				=		os.getcwd() 										# relative directory path
		self.filePath				=		os.path.abspath(__file__) 							# absolute file path
		self.fileName				=		os.path.basename(__file__) 							# the file name only
		self.system					=		platform.system()									# check OS
		self.debug					=		False												# default disable debug
		self.version 				=		"0.0.1a"											# TK version
		self.logFolder				=		"logs"												# Log store
		self.modulesFolder			=		"modules"											# Modules folder 
		self.moduleFolderPath		= 		os.path.join(self.dirPath,self.modulesFolder) 		# Modules folder Path
		self.logPrefix				=		"wetk"												# Log Prefix
		self.moduleExt				=		"py"												# python module extension file
		# Start
		self.run()
	def run(self):
		# Get Argument
		self.getArument()
		# Log config
		self.logConfig()
		# Set variable
		if(self.args.use != None):
			self.modulePath			=		self.args.use
			self.loadModule(self.modulePath)
	def loadModule(self, moduleName):
		modulePath 					=		moduleName.split("/")								# Split by /
		self.logger.debug("Try to load: {0}.".format(modulePath[-1]))							# Print module name as last Element
		try:
			moduleFileName			=		"{0}.{1}".format(os.path.join(moduleName),self.moduleExt)
			moduleFilePath			=		os.path.join(self.dirPath,self.modulesFolder,moduleFileName)
			imp.load_source("wetkModule",moduleFilePath)
			import wetkModule
			wetkModule.init(self.logger)
		except Exception, e:
			self.logger.debug(e)
			self.logger.error("Error while load module {0}.".format(moduleName))
		else:
			self.logger.debug("Loading module: {0}.".format(moduleName))
			if(self.args.showhelp == True):
				wetkModule.showHelp()
			elif(self.args.showoptions == True):
				wetkModule.showOptions()
			elif(self.args.checkoptions == True):
				wetkModule.setOptions(self.args.options)	
				wetkModule.checkOptions()
			else:
				if(self.args.useoptions == True):
					wetkModule.setOptions(self.args.options)
				wetkModule.run()
		finally:
			self.logger.info("Finish load module: {0}.".format(moduleName))
		
	def getArument(self):
		parser 						= 		argparse.ArgumentParser(description="WETK - Web Exploit ToolKit - Version {0}".format(self.version))
		# URL config
		parser.add_argument(
			'--url',
			help 					=		'URL'
			)
		# Enable debug
		parser.add_argument(
			'-d',
			'--debug',
			help 					=		'enable/disable debug',
			default					=		'false',
			action					=		'store_true',
			)
		# Show version
		parser.add_argument(
			'-v',
			'--version',
			help 					=		'WETK version',
			action					=		'store_true',
			)
		# Update Framework
		parser.add_argument(
			'--update',
			help 					=		'Update Framework',
			action					=		'store_true',
			)
		# List Module
		parser.add_argument(
			'-l',
			'--list',
			help 					=		'List all modules',
			action					=		'store_true',
			)
		# Use Module
		parser.add_argument(
			'-u',
			'--use',
			help 					=		'Use module'
			)
		# Show module help
		parser.add_argument(
			'--showhelp',
			help 					=		'Show module Help',
			default					=		'false',
			action					=		'store_true',
			)
		# Show module options
		parser.add_argument(
			'--showoptions',
			help 					=		'Show module Options',
			default					=		'false',
			action					=		'store_true',
			)
		# Check module options
		parser.add_argument(
			'--checkoptions',
			help 					=		'Check module Options',
			default					=		'false',
			action					=		'store_true',
			)
		# Use module options
		parser.add_argument(
			'-o',
			'--useoptions',
			help 					=		'Use module Options',
			default					=		'false',
			action					=		'store_true',
			)
		# Module Option
		# Check need module options or not
		optionNeed					=		False
		arrayNeed					=		[
					"-o",
					"--useoptions",
					"--checkoptions",
			]
		for i in sys.argv:
			if(i in arrayNeed):
				optionNeed			=		True
				break
		if(optionNeed==True):
			parser.add_argument(
				'options',
				help 					=		'Module Options',
				nargs					=		'+',
				default					=		None
				)
		
		# Set default is show help
		if(len(sys.argv) < 2):
			#Only Filename
			parser.print_help()
			exit(0)
		# Parse and save agrument
		self.args 					= 		parser.parse_args()
		

	def logConfig(self):
		self.logger 				= 		logging.getLogger(__name__)					# Logging constructor 
		# Set format
		self.logFormat 				= 		logging.Formatter("%(asctime)-15s %(levelname)-10s %(message)s")				
		# Console Handler
		consoleHandler 				= 		logging.StreamHandler()
		consoleHandler.setFormatter(self.logFormat)
		self.logger.addHandler(consoleHandler)
		# File Handler
		dateTimeNow 				= 		datetime.datetime.now()
		logFileName					=		"{0}_{1}_{2}_{3}.log".format(
												self.logPrefix,
												dateTimeNow.year,
												dateTimeNow.month,
												dateTimeNow.day)
		logFilePath					=		os.path.join(self.dirPath, self.logFolder, logFileName)
		fileHandler 				= 		logging.FileHandler(logFilePath)
		fileHandler.setFormatter(self.logFormat)
		self.logger.addHandler(fileHandler)
		# Get and set debug
		if(self.args.debug == True):
			self.debug 				=		self.args.debug
			self.logger.setLevel(logging.DEBUG)	
		elif(self.args.debug == False):
			self.debug 				=		False
			self.logger.setLevel(logging.INFO)
		self.logger.debug("Set Logging mode is {0}.".format(self.debug))


######---------------------------------------------#####


def main():
	tk 								= 		WEToolKit()


if __name__ == "__main__":
	main()


