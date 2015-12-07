#!/usr/bin/python
#author: namhb
import ConfigParser, os
class baseModule:
	def __init__(self, logger):
		self.config								= 	ConfigParser.ConfigParser()
	def profileParse(self, profilePath):
		self.config.read(profilePath)
	def getConfig(self, section, option):
		if(section not in self.config.sections()):
			self.logger.error("Not found section {} in Profile".format(section))
			exit()
		else:
			return self.config.get(section,option)
	def printOptionsLong(self, key, currentSetting, requiredString, description):
		if(currentSetting != None):
			blockSize 							=	45
			lineC 								=	int(len(currentSetting) / blockSize) + 1					# Primary
			lineD 								=	int(len(description) / blockSize) + 1
			line 								=	lineC > lineD and lineC or lineD
			for i in range(0,line):
				start 							=	i * blockSize
				end 							=	(i+1) * blockSize
				if(i == 0):
					# First line
					print("\t{0:20s}{1:50s}{2:12s}{3}".format(key,currentSetting[start:end],requiredString,description[start:end]))
				else:
					# Not print key
					print("\t{0:20s}{1:50s}{2:12s}{3}".format("",currentSetting[start:end],"",description[start:end]))
		else:
			# Split by desciptions
			blockSize 							=	50
			lineD 								=	int(len(description) / blockSize) + 1
			for i in range(0,lineD):
				start 							=	i * blockSize
				end 							=	(i+1) * blockSize
				if(i == 0):
					# First line
					print("\t{0:20s}{1:50s}{2:12s}{3}".format(key,currentSetting,requiredString,description[start:end]))
				else:
					# Not print key
					print("\t{0:20s}{1:50s}{2:12s}{3}".format("","","",description[start:end]))
	def printOptions(self, basicOptions):
		print("Basic options")
		print("=============")
		print("")
		print("\t{0:20s}{1:50s}{2:12s}{3}".format("Name","Current Setting","Required","Description"))
		print("\t{0:20s}{1:50s}{2:12s}{3}".format("----","---------------","--------","-----------"))
		print("")
		for key in basicOptions.keys():
			option 							= 	basicOptions[key]
			requiredString					=	option["required"] and "YES" or "NO"
			# print("\t{0:20s}{1:50s}{2:12s}{3}".format(key,option["currentSetting"],requiredString,option["description"]))
			self.printOptionsLong(key,option["currentSetting"],requiredString,option["description"])