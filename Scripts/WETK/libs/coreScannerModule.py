#!/usr/bin/python
#author: namhb
import re, requests, urllib2, string, time
from baseModule import baseModule
class coreScannerModule:
	def __init__(self, logger, profile):
		self.logger							=	logger
		self.profile 						=	profile
		self.base 							=	baseModule(self.logger)
		self.config 						=	self.base.profileParse(self.profile)
		self.basicOptions					=	{
			}
		# Help for this module, how to use
		self.help 							=	"" \
			"This is help for module." \
			""
	
	def printOptions(self):
		self.base.printOptions(self.basicOptions)
	def start(self):
		self.logger.warning("Started Module: {0}.".format(self.name))

		# Code here
	def end(self):
		# Finish
		pass