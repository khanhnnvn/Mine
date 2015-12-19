#!/usr/bin/python
#author: namhb
import re, requests, urllib2, string, time
from baseModule import baseModule
class coreScannerModule:
	def __init__(self, logger, profile):
		self.logger							=	logger
		self.profile 						=	profile
		self.base 							=	baseModule(self.logger)
		self.tmpFolder 						=	"tmp"
		self.config 						=	self.base.profileParse(self.profile)
		self.basicOptions					=	{
			}
		self.option 						=	None
		# Help for this module, how to use
		self.help 							=	"" \
			"This is help for module." \
			""
	def optionParse(self):
		for i in range(0, len(self.options)):
			if(self.options[i].find("=") > 0):
				option 						=	self.options[i].split("=")
				key 						=	option[0]
				value 						=	"=".join(option[1:])
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
		self.base.printOptions(self.basicOptions)
	def start(self):
		if(self.base.checkOptions(self.basicOptions) == False):
			exit()
		self.logger.warning("Started Module: {0}.".format(self.name))

		# Code here
	def end(self):
		# Finish
		try:
			self.driver.quit()
		except Exception, e:
			pass
