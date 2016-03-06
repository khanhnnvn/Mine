#!/usr/bin/python
#author: namhb
import sys, time, requests, os, logging, argparse, datetime, platform, pkgutil, imp, re, importlib

class WetkCore:
	def __init__(self):
		self.logger 					= 		logging.getLogger(__name__)					# Logging constructor 

	def logConfig(self, logPrefix, dirPath, logFolder):		
		# Set format
		self.logFormat 					= 		logging.Formatter("%(asctime)-15s %(levelname)-10s %(message)s")				
		# Console Handler
		consoleHandler 					= 		logging.StreamHandler()
		consoleHandler.setFormatter(self.logFormat)
		self.logger.addHandler(consoleHandler)
		# File Handler
		dateTimeNow 					= 		datetime.datetime.now()
		logFileName						=		"{0}_{1}_{2}_{3}.log".format(
												logPrefix,
												dateTimeNow.year,
												dateTimeNow.month,
												dateTimeNow.day)
		logFilePath						=		os.path.join(dirPath, logFolder, logFileName)
		fileHandler 					= 		logging.FileHandler(logFilePath)
		fileHandler.setFormatter(self.logFormat)
		self.logger.addHandler(fileHandler)
		# # Get and set debug
		if(self.args.debug == True):
			self.debug 					=		True
			self.logger.setLevel(logging.DEBUG)	
		else:
			self.debug 					=		False
			self.logger.setLevel(logging.INFO)
		self.logger.debug("Set Logging mode is {0}.".format("True"))
	def getArument(self, version):
		parser 							= 		argparse.ArgumentParser(description="WETK - Web Exploit ToolKit - Version {0}".format(version))

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
		# -----------------------------------------------------------------------------------------
		# List Module
		parser.add_argument(
			'-l',
			'--list',
			help 						=		'List all modules',
			action						=		'store_true',
			)
		# # -----------------------------------------------------------------------------------------
		# # Use Modules 
		parser.add_argument(
			'-u',
			'--use',
			help 						=		'Use module'
			)
		# Show module help
		parser.add_argument(
			'-sh',
			'--showhelp',
			help 						=		'Show module Help',
			default						=		'false',
			action						=		'store_true',
			)
		# Show module options
		parser.add_argument(
			'-so',
			'--showoptions',
			help 						=		'Show module Options',
			default						=		'false',
			action						=		'store_true',
			)
		# Check module options
		parser.add_argument(
			'-co',
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
		# # -----------------------------------------------------------------------------------------
		# Use profile
		parser.add_argument(
			'-p',
			'--profile',
			help 						=		'Profle Options',
			default						=		"default",
			)
		# Set default is show help
		if(len(sys.argv) < 2):
			parser.print_help()
			exit(0)
		# Parse and save agrument
		self.args 						= 		parser.parse_args()
		return self.args
	def load_class(self,full_class_string):
		"""
		dynamically load a class from a string
		"""

		class_data = full_class_string.split(".")
		module_path = ".".join(class_data[:-1])
		class_str = class_data[-1]

		module = importlib.import_module(module_path)
		# Finally, we retrieve the Class
		return getattr(module, class_str)
	def loadProfile(self, profileFolderPath):
		# Check Profile file
		if(os.path.isfile(os.path.join(profileFolderPath, self.args.profile))):
			# Profile exits
			self.profilePath 			=		os.path.join(profileFolderPath, self.args.profile)
		else:
			self.logger.info("Can not load Profile {}".format(self.args.profile))
			exit()
	def loadModule(self, modulePath, modulesFolder, moduleNameDefault, profileFolderPath):
		self.loadProfile(profileFolderPath)
		# Load module
		classPath 						=		"{0}.{1}.{2}".format(modulesFolder,modulePath, moduleNameDefault)
		try:
			self.logger.info("Try to load: {0}.".format(classPath))
			wetkModule 					=		self.load_class(classPath)(self.logger, self.profilePath)					
		except Exception, e:
			self.logger.debug(e)
			self.logger.error("Error while load module {0}".format(classPath))
		else:
			self.logger.debug("Loading module: {0}".format(classPath))

			if(self.args.showhelp == True):
				print(wetkModule.help)
			elif(self.args.showoptions == True):
				wetkModule.printOptions()
			elif(self.args.checkoptions == True):
				if(self.args.useoptions != None):
					wetkModule.options 	=	self.args.useoptions
					wetkModule.optionParse()
					wetkModule.checkOptions()
			elif(self.args.useoptions != None):
				wetkModule.options 		=	self.args.useoptions
				wetkModule.optionParse()
				wetkModule.start()
				wetkModule.run()
				wetkModule.end()
		finally:
			self.logger.info("Finish load module: {0}".format(classPath))
	def listModule(self, modulesFolder, moduleFolderPath, moduleNameDefault, profileFolderPath):
		self.loadProfile(profileFolderPath)
		self.logger.info("List Modules")
		print("List Modules")
		print("============")
		print("")
		print("\t{4:30s}{0:100s}{1:10s}{2:10s}{3}".format("Name","Version","Rank","Description","Path"))
		print("\t{4:30s}{0:100s}{1:10s}{2:10s}{3}".format("----","-------","----","-----------","----"))
		print("")
		prefixLength					=		len(moduleFolderPath)
		time 							=		1
		splitCharacter 					=		"\\" if (platform.system() == "Windows") else "/"
		# Standard path
		for path, subdirs, files in os.walk(moduleFolderPath):
			for name in files:
				if((name[-3:] == ".py") and (name != "__init__.py")):
					# Is module file
					try:
						if(path == moduleFolderPath):
							classPath 	=		"{0}.{1}.{2}".format(modulesFolder,name[:-3],moduleNameDefault)
						else:
							subPath 	=		path[len(moduleFolderPath)+1:]
							if(subPath.find(splitCharacter) > 0):
								subPaths 	=	subPath.split(splitCharacter)
								classPath 	=		modulesFolder
								for path in subPaths:
									classPath 	=	"{0}.{1}".format(classPath, path)
								classPath	=	"{0}.{1}.{2}".format(classPath,name[:-3],moduleNameDefault)
							else:
								# subfoder 1
								classPath 	=		"{0}.{3}.{1}.{2}".format(modulesFolder,name[:-3],moduleNameDefault,subPath)
						wetkModule 			=		self.load_class(classPath)(self.logger, self.profilePath)
						print("\t{4:30s}{0:100s}{1:10s}{2:10s}{3}".format(wetkModule.name,wetkModule.version,wetkModule.rank,wetkModule.description,classPath[len(modulesFolder)+1:-(len(moduleNameDefault)+1)]))
					except Exception, e:
						raise
					else:
						pass
					finally:
						pass
