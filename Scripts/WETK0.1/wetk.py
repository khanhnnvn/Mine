#!/usr/bin/python
#author: namhb
import sys, time, requests, os, logging, argparse, datetime, platform, pkgutil, imp, re
import libs.coreHTTPModule

'''
How to use:
'''
######---------------------------------------------#####
######-------------- WEToolKit class ---- ---------#####
class WEToolKit:
	def __init__(self):
		#Const
		self.dirPath					=		os.getcwd() 										# relative directory path
		self.filePath					=		os.path.abspath(__file__) 							# absolute file path
		self.fileName					=		os.path.basename(__file__) 							# the file name only
		self.system						=		platform.system()									# check OS
		self.debug						=		False												# default disable debug
		self.version 					=		"0.0.1a"											# TK version
		self.logFolder					=		"logs"												# Log store
		self.modulesFolder				=		"modules"											# Modules folder 
		self.libsFolder 				=		"libs"												# Libs folder
		self.profileFolder 				=		"profiles"											# Profile
		self.moduleFolderPath			= 		os.path.join(self.dirPath,self.modulesFolder) 		# Modules folder Path
		self.libsFolderPath				= 		os.path.join(self.dirPath,self.libsFolder) 			# Libs Path
		self.profileFolderPath			= 		os.path.join(self.dirPath,self.profileFolder) 		# Profiles Path
		self.logPrefix					=		"wetk"												# Log Prefix
		self.moduleExt					=		"py"												# python module extension file
		# Start
		self.run()
	def run(self):
		# Get Argument
		self.getArument()
		# Log config
		self.logConfig()
		# Check Profile file
		if(os.path.isfile(os.path.join(self.profileFolderPath, self.args.profile))):
			# Profile exits
			self.profilePath 			=		os.path.join(self.profileFolderPath, self.args.profile)
		else:
			self.logger.info("Can not load Profile {}".format(self.args.profile))
			exit()
		# Use module
		if(self.args.use != None):
			self.modulePath				=		self.args.use
			self.loadModule(self.modulePath)
			exit()
		if(self.args.list != None):
			self.listModule()
			exit()

	def listModule(self):
		self.logger.info("List Modules")
		print("List Modules")
		print("============")
		print("")
		print("\t{0:100s}{1:10s}{2:10s}{3}".format("Name","Version","Rank","Description"))
		print("\t{0:100s}{1:10s}{2:10s}{3}".format("----","-------","----","-----------"))
		print("")
		prefixLength					=		len(self.moduleFolderPath)
		time 							=		1
		for path, subdirs, files in os.walk(self.moduleFolderPath):
			for name in files:
				if(name[-3:] == ".py"):
					# Is module file
					try:
						# Try to load to get info
						moduleFilePath	=		os.path.join(path, name)
						imp.load_source("wetkModule",moduleFilePath)
						if(time==1):
							import wetkModule
						else:
							del wetkModule
							import wetkModule
						time 			+=1
						wetkModule.init(self.logger, self.profilePath)
						subFolder		=		path[prefixLength:]
						if(len(subFolder)!=0):
							subFolder	=		subFolder[1:]
						# Change \ to /, Windows only
						subFolder		=		subFolder.replace("\\","/")
						name 			=		"{0}/{1}".format(subFolder,name[:-3])
						# Remove / first
						if(name[0] == "/"):
							name 		=		name[1:]
						print("\t{0:100s}{1:10s}{2:10s}{3}".format(name,wetkModule.getVersion(),wetkModule.getRank(),wetkModule.getDescription()))
					except Exception, e:
						raise
					else:
						pass
					finally:
						pass
	def loadModule(self, moduleName):
		modulePath 						=		moduleName.split("/")								# Split by /
		self.logger.info("Try to load: {0}.".format(modulePath[-1]))							# Print module name as last Element
		try:
			moduleFileName				=		"{0}.{1}".format(os.path.join(moduleName),self.moduleExt)
			moduleFilePath				=		os.path.join(self.dirPath,self.modulesFolder,moduleFileName)
			imp.load_source("wetkModule",moduleFilePath)
			import wetkModule
			wetkModule.init(self.logger, self.profilePath)
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
				if(self.args.useoptions != None):
					wetkModule.setOptions(self.args.useoptions)	
				wetkModule.checkOptions()
			else:
				if(self.args.useoptions != None):
					wetkModule.setOptions(self.args.useoptions)
				wetkModule.run()
		finally:
			self.logger.info("Finish load module: {0}.".format(moduleName))
		
	def getArument(self):
		parser 							= 		argparse.ArgumentParser(description="WETK - Web Exploit ToolKit - Version {0}".format(self.version))
		# Enable debug
		parser.add_argument(
			'-d',
			'--debug',
			help 						=		'enable/disable debug',
			default						=		'false',
			action						=		'store_true',
			)
		# Show version
		parser.add_argument(
			'-v',
			'--version',
			help 						=		'WETK version',
			action						=		'store_true',
			)
		# Update Framework
		parser.add_argument(
			'--update',
			help 						=		'Update Framework',
			action						=		'store_true',
			)
		# List Module
		parser.add_argument(
			'-l',
			'--list',
			help 						=		'List all modules',
			action						=		'store_true',
			)
		# Use Module
		parser.add_argument(
			'-u',
			'--use',
			help 						=		'Use module'
			)
		# Show module help
		parser.add_argument(
			'--showhelp',
			help 						=		'Show module Help',
			default						=		'false',
			action						=		'store_true',
			)
		# Show module options
		parser.add_argument(
			'--showoptions',
			help 						=		'Show module Options',
			default						=		'false',
			action						=		'store_true',
			)
		# Check module options
		parser.add_argument(
			'--checkoptions',
			help 						=		'Check module Options',
			default						=		'false',
			action						=		'store_true',
			)
		# Use module options
		parser.add_argument(
			'-o',
			'--useoptions',
			help 						=		'Module Options',
			default						=		None,
			nargs						=		'+',
			)
		# Use profile
		parser.add_argument(
			'-p',
			'--profile',
			help 						=		'Profle Options',
			default						=		"default",
			)
		
		# Set default is show help
		if(len(sys.argv) < 2):
			#Only Filename
			parser.print_help()
			exit(0)
		# Parse and save agrument
		self.args 						= 		parser.parse_args()
		
	def writeErrorLog(self, log):
		self.logger.error(log)
	def logConfig(self):
		self.logger 					= 		logging.getLogger(__name__)					# Logging constructor 
		# Set format
		self.logFormat 					= 		logging.Formatter("%(asctime)-15s %(levelname)-10s %(message)s")				
		# Console Handler
		consoleHandler 					= 		logging.StreamHandler()
		consoleHandler.setFormatter(self.logFormat)
		self.logger.addHandler(consoleHandler)
		# File Handler
		dateTimeNow 					= 		datetime.datetime.now()
		logFileName						=		"{0}_{1}_{2}_{3}.log".format(
												self.logPrefix,
												dateTimeNow.year,
												dateTimeNow.month,
												dateTimeNow.day)
		logFilePath						=		os.path.join(self.dirPath, self.logFolder, logFileName)
		fileHandler 					= 		logging.FileHandler(logFilePath)
		fileHandler.setFormatter(self.logFormat)
		self.logger.addHandler(fileHandler)
		# Get and set debug
		if(self.args.debug == True):
			self.debug 					=		True
			self.logger.setLevel(logging.DEBUG)	
		else:
			self.debug 					=		False
			self.logger.setLevel(logging.INFO)
		self.logger.debug("Set Logging mode is {0}.".format(self.debug))


######---------------------------------------------#####
tk 										=		None
def logKeyboardInterrupt(log):
	print(log)
def main():
	global tk
	tk 									= 		WEToolKit()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		logKeyboardInterrupt("User canncel.")
	else:
		pass
	finally:
		pass


