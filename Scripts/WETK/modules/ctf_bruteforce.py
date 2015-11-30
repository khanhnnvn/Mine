#!/usr/bin/python
#author: namhb
import sys, os
# Load core module
from libs.coreHTTPModule import coreHTTPModule
class Module(coreHTTPModule):
	def __init__(self, logger):
		coreHTTPModule.__init__(self, logger)
		self.name						=	"CTF Brute Force Module"								# Changed
		self.description 				=	"This is Module for Brute force, file fuzzing"
		self.rank						=	"MEDIUM"												# Exploit level
		self.type						=	"Scan"													# Type: exploit | scanner | support
		self.author						=	"namhb"
		self.version					=	"0.0.1"
		self.fileList 					= 	[
				"robots.txt",
				".htaccess",
				"web.config",
				"login.php",
				"admin.php",
				"phpmyadmin",
				"mysqladmin",
				"backup",
			]
		self.help 						=	"" \
			"This is help for module." \
			""
	def sendHttpGetRequest(self, url):
		if(url[:5] == "https"):
			r 								=	requests.get(url,verify=False)
			r.headers["content-length"]		=	None
		else:
			r 								=	requests.get(url)
		return r
	def run(self):
		# We coding here
		print("Site: {0} result:".format(self.basicOptions["URL"]["currentSetting"]))
		print("==========================")
		print("")
		print("\t{0:50s}{1:10s}{2}".format("Filename","Code","Size"))
		print("\t{0:50s}{1:10s}{2}".format("--------","----","----"))
		print("")
		for fileName in self.fileList:
			r 								=	self.sendHTTPRequest(fileName)
			print("\t{0:50s}{1:10s}{2}".format(fileName,str(r.status_code),r.headers["content-length"]))
# Load control module
execfile(os.path.join(os.getcwd(), "libs", "controlHTTPModule.py"))

