#!/usr/bin/python
#author: namhb
import os, platform
from libs.WetkCore import WetkCore

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
		self.version 					=		"0.0.2a"											# TK version
		self.logFolder					=		"logs"												# Log store
		self.modulesFolder				=		"modules"											# Modules folder 
		self.libsFolder 				=		"libs"												# Libs folder
		self.moduleFolderPath			= 		os.path.join(self.dirPath,self.modulesFolder) 		# Modules folder Path
		self.moduleNameDefault 			=		"module"
		self.libsFolderPath				= 		os.path.join(self.dirPath,self.libsFolder) 			# Modules folder Path
		self.logPrefix					=		"wetk"												# Log Prefix
		self.moduleExt					=		"py"												# python module extension file
		self.profileFolder 				=		"profiles"											# Profile
		self.profileFolderPath			= 		os.path.join(self.dirPath,self.profileFolder) 		# Profiles Path
		# Start
		self.run()
	def run(self):
		self.wetk 						=		WetkCore()
		self.args 						=		self.wetk.getArument(
				self.version
			)
		self.wetk.logConfig(
				self.logPrefix,
				self.dirPath,
				self.logFolder,
			)

		# Use module
		if(self.args.use != None):
			self.wetk.loadModule(
				self.args.use,
				self.modulesFolder,
				self.moduleNameDefault,
				self.profileFolderPath,
				)
			exit()
		if(self.args.list != None):
			self.wetk.listModule(
				self.modulesFolder,
				self.moduleFolderPath,
				self.moduleNameDefault,
				self.profileFolderPath,
				)
			exit()
	


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