#!/usr/bin/python
#author: namhb
import re, requests, string
class coreHTTPModule:
	def __init__(self, logger):
		self.logger							=	logger
		
		self.requestCount 					=	0
		self.timeOut 						=	1000
		self.injectPoint 					=	None
		self.stringCollections 				=	string.printable
		self.basicOptions					=	{
				"URL"	:	{
					"currentSetting"		:	None,
					"required"				:	True,
					"description"			:	"URL to exploit"
				},
				"METHOD" : {
					"currentSetting"		:	None,
					"required"				:	False,
					"description"			:	"HTTP Method: get/post/head"
				},
				"USERAGENT" : {
					"currentSetting"		:	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
					"required"				:	False,
					"description"			:	"User Agent to exploit"
				},
				"COOKIE" : {
					"currentSetting"		:	None,
					"required"				:	False,
					"description"			:	"Cookie to exploit, use <cookie_name1>:<cookie_value1>;<cookie_name2>:<cookie_value2>"
				},
				"REFERER" : {
					"currentSetting"		:	"https://www.google.com/",
					"required"				:	False,
					"description"			:	"Referer to exploit"
				},
				"HOST" : {
					"currentSetting"		:	None,
					"required"				:	False,
					"description"			:	"Host to exploit"
				},
				"ACCEPT_ENCODING" : {
					"currentSetting"		:	"gzip, deflate, sdch",
					"required"				:	False,
					"description"			:	"Host to exploit"
				},
				"ACCEPT_LANGUAGE" : {
					"currentSetting"		:	"en,en-US;q=0.8,vi-VN;q=0.6,vi;q=0.4,fr-FR;q=0.2,fr;q=0.2",
					"required"				:	False,
					"description"			:	"Host to exploit"
				},
				"CONNECTION" : {
					"currentSetting"		:	"keep-alive",
					"required"				:	False,
					"description"			:	"Host to exploit"
				},
				"ACCEPT" : {
					"currentSetting"		:	"",
					"required"				:	False,
					"description"			:	"Host to exploit"
				},
				"DBMS" : {
					"currentSetting"		:	"mysql",
					"required"				:	True,
					"description"			:	"Type of DMBS: mysql/mssql/oracle"
				},
				"DATADICT" : {
					"currentSetting"		:	None,
					"required"				:	False,
					"description"			:	"POST Data to exploit, use <data_name1>:<data_value1>;<data_name2>:<data_value2>. Default use this (not DATA)"
				},
			}
		self.options 						=	None					# Input options
		# Help for this module, how to use
		self.help 							=	"" \
			"This is help for module." \
			""
	def optionParse(self):
		for i in range(0, len(self.options)):
			if(self.options[i].find("=") > 0):
				option 						=	self.options[i].split("=")
				key 						=	option[0]
				value 						=	option[1]
			else:
				key 						=	self.options[i]
				value 						=	None
			if(key in self.basicOptions.keys()):
				# Set value
				self.logger.debug("Set {0} to {1}.".format(key,value))
				self.basicOptions[key]["currentSetting"] = value
			else:
				self.logger.debug("Option {0} not found.".format(key))
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
	def printOptions(self):
		print("Basic options")
		print("=============")
		print("")
		print("\t{0:20s}{1:50s}{2:12s}{3}".format("Name","Current Setting","Required","Description"))
		print("\t{0:20s}{1:50s}{2:12s}{3}".format("----","---------------","--------","-----------"))
		print("")
		for key in self.basicOptions.keys():
			option 							= 	self.basicOptions[key]
			requiredString					=	option["required"] and "YES" or "NO"
			# print("\t{0:20s}{1:50s}{2:12s}{3}".format(key,option["currentSetting"],requiredString,option["description"]))
			self.printOptionsLong(key,option["currentSetting"],requiredString,option["description"])
	def standardURL(self):
		url 								=	self.basicOptions["URL"]["currentSetting"]
		if((url[:7] == "http://") or (url[:8] == "https://")):
			self.logger.debug("URL include http/https, don`t need add prefix.")
		else:
			self.basicOptions["URL"]["currentSetting"] = "{0}{1}".format("http://",self.basicOptions["URL"]["currentSetting"])
			self.logger.debug("Add prefix http to: {0}.".format(self.basicOptions["URL"]["currentSetting"]))
	def getHost(self):
		self.standardURL()
		url 								=	self.basicOptions["URL"]["currentSetting"]
		if(url[:7] == "http://"):
			host 							=	url[7:]
		elif(url[:8] == "https://"):
			host 							=	url[8:]
		else:
			host 							=	url
		# Set host
		self.basicOptions["HOST"]["currentSetting"] = host.split("/")[0]
	def checkOptions(self):
		check 								=	True
		for key in self.basicOptions.keys():
			if((self.basicOptions[key]["required"] == True) and (self.basicOptions[key]["currentSetting"]==None)):
				check 						=	False
				self.logger.error("Option {0} need configure.".format(key))
				return check
			# Check URL start with http or https
			if(key == "URL"):
				self.standardURL()
			if(key == "COOKIE"):
				self.cookieParse()
			if(key == "DBMS"):
				# Set default is mysql
				if(self.basicOptions[key]["currentSetting"] == None):
					self.basicOptions[key]["currentSetting"] = "mysql"
				else:
					# Check type of DBMS: mysql/mssql/oracle
					dbms 					=	self.basicOptions[key]["currentSetting"].lower()
					if((dbms=="mysql") or (dbms=="mssql") or (dbms=="oracle")):
						pass
					else:
						check 				=	False
						self.logger.error("DBMS type must in mysql/mssql/oracle only.")
						return check
			if(key == "METHOD"):
				# If DATA or DATADICT, method is POSt
				if(self.basicOptions["DATADICT"]["currentSetting"] != None):
					self.basicOptions[key]["currentSetting"] = "post"
				# Set default is GET
				if(self.basicOptions[key]["currentSetting"] == None):
					self.basicOptions[key]["currentSetting"] = "get"
				else:
					methodType 				=	self.basicOptions[key]["currentSetting"].lower()
					if((methodType == "get") or (methodType == "post") or (methodType == "head")):
						pass
					else:
						check 				=	False
						self.logger.error("METHOD must in get/post/head only.")
						return check
					if(methodType == "post"):
						# Post data is set or not
						if(self.basicOptions["DATADICT"]["currentSetting"] == None):
							check 			=	False
							self.basicOptions["DATADICT"]["required"] = True
							self.logger.error("POST data must set in POST Method.")
			# Check inject point (only one inject point, with * character)
			# Set HOST default is URL
			if(key == "HOST"):
				if((self.basicOptions[key]["currentSetting"] == None) and (self.basicOptions["URL"]["currentSetting"] != None) ):
					self.getHost()
			# Check data dict
			if(key == "DATADICT"):
				if(self.basicOptions["DATADICT"]["currentSetting"] != None):
					self.dataDictParse()
		return check
	def checkInjectPoint(self):
		# Check only one inject point
		# For all parameter manipulation, SQL, XSS, LFI use same
		numberStar							=	0
		for key in self.basicOptions.keys():
			# Check in URL, COOKIE, DATA, USERAGENT, REFERER
			if((key == "URL") or (key == "USERAGENT") or (key == "REFERER")):
				dataString					=	self.basicOptions[key]["currentSetting"]
				if(dataString != None):
					number 					=	len(re.findall("\*",dataString))
					if(number > 0):
						self.logger.debug("Found {0} inject point in {1}".format(number,key))
						if((number == 1) and (self.injectPoint == None)):
							self.injectPoint=	key
							self.logger.debug("Set inject point to: {0}".format(key))
						elif(number > 1):
							self.logger.error("Only one inject point (* character) in {0}.".format(key))
						numberStar			+=	number
			if((key == "COOKIE") and (self.basicOptions["COOKIE"]["currentSetting"] != None)):
				for name in self.basicOptions["COOKIE"]["currentSetting"].keys():
					cookieString 			=	self.basicOptions["COOKIE"]["currentSetting"][name]
					if(cookieString != None):
						number2 				=	len(re.findall("\*",cookieString))
						if(number2 > 0):
							self.logger.debug("Found {0} inject point in {1}".format(number2,key))
							if((number2 == 1) and (self.injectPoint == None)):
								self.injectPoint=	key
								self.logger.debug("Set inject point to: {0}".format(key))
							elif(number2 > 1):
								self.logger.error("Only one inject point (* character) in {0}.".format(key))
							numberStar			+=	number2
			if((key == "DATADICT") and (self.basicOptions["DATADICT"]["currentSetting"] != None)):
				for name in self.basicOptions["DATADICT"]["currentSetting"].keys():
					dataString 					=	self.basicOptions["DATADICT"]["currentSetting"][name]
					if(dataString != None):
						number3 				=	len(re.findall("\*",dataString))
						if(number3 > 0):
							self.logger.debug("Found {0} inject point in {1}".format(number3,key))
							if((number3 == 1) and (self.injectPoint == None)):
								self.injectPoint=	key
								self.logger.debug("Set inject point to: {0}".format(key))
							elif(number3 > 1):
								self.logger.error("Only one inject point (* character) in {0}.".format(key))
							numberStar			+=	number3
		# Sum all					
		if(numberStar == 0):
			self.logger.error("Not found any inject point.")
			return False
		elif(numberStar == 1):
			self.logger.warning("Inject point is ready.")
			return True
		elif(numberStar > 1):
			self.logger.error("Only one inject point (* character).")
			return False
	def cookieParse(self):
		cookieString 						=	self.basicOptions["COOKIE"]["currentSetting"]
		if(cookieString == None):
			return True
		else:
			# Parse string <cookie_name1>:<cookie_value1>;<cookie_name2>:<cookie_value2> to array 
			allCookies 						=	{}
			cookieSplit 					=	cookieString.split(";")
			for cookie in cookieSplit:
				tmp 						=	cookie.split(":")
				if(tmp[0] != cookie):
					cookieName 				=	tmp[0]
					cookieValue 			=	tmp[1]
					allCookies[cookieName]	=	cookieValue
				else:
					self.basicOptions["COOKIE"]["currentSetting"] = None
					self.logger.error("Set COOKIE error in: {0}. Wrong syntax <cookie_name1>:<cookie_value1>.".format(tmp[0]))
					return False
			self.basicOptions["COOKIE"]["currentSetting"] = allCookies			
	def dataDictParse(self):
		dataString 							=	self.basicOptions["DATADICT"]["currentSetting"]
		if(dataString == None):
			return True
		else:
			# Parse string <cookie_name1>:<cookie_value1>;<cookie_name2>:<cookie_value2> to array 
			allData 						=	{}
			dataSplit 						=	dataString.split(";")
			for data in dataSplit:
				tmp 						=	data.split(":")
				if(tmp[0] != data):
					dataName 				=	tmp[0]
					dataValue 				=	tmp[1]
					allData[dataName]		=	dataValue
				else:
					self.basicOptions["DATADICT"]["currentSetting"] = None
					self.logger.error("Set DATADICT error in: {0}. Wrong syntax <data_name1>:<data_value1>.".format(tmp[0]))
					return False
			self.basicOptions["DATADICT"]["currentSetting"] = allData			
	def sendHTTPRequest(self, payload):
		
		# Create http request with your options
		httpMethod 							=	self.basicOptions["METHOD"]["currentSetting"]
		url 								=	self.basicOptions["URL"]["currentSetting"]
		userAgent 							=	self.basicOptions["USERAGENT"]["currentSetting"]
		referer 							=	self.basicOptions["REFERER"]["currentSetting"]
		host 								=	self.basicOptions["HOST"]["currentSetting"]
		dataDict 							=	self.basicOptions["DATADICT"]["currentSetting"]
		cookie 								=	self.basicOptions["COOKIE"]["currentSetting"]
		accept 								=	self.basicOptions["ACCEPT"]["currentSetting"]
		acceptEncoding 						=	self.basicOptions["ACCEPT_ENCODING"]["currentSetting"]
		acceptLanguage 						=	self.basicOptions["ACCEPT_LANGUAGE"]["currentSetting"]
		connection 							=	self.basicOptions["CONNECTION"]["currentSetting"]
		# Add Payload
		if((self.injectPoint != "COOKIE") and (self.injectPoint != "DATADICT")):
			# If string type, too easy
			if(self.injectPoint == "URL"):
				url 						=	self.basicOptions[self.injectPoint]["currentSetting"].replace("*",payload)
			if(self.injectPoint == "USERAGENT"):
				userAgent 					=	self.basicOptions[self.injectPoint]["currentSetting"].replace("*",payload)
			if(self.injectPoint == "REFERER"):
				referer 					=	self.basicOptions[self.injectPoint]["currentSetting"].replace("*",payload)
			if(self.injectPoint == "HOST"):
				host 						=	self.basicOptions[self.injectPoint]["currentSetting"].replace("*",payload)
		else:
			# It is dict, read all items and replace
			if(self.injectPoint == "COOKIE"):
				cookieBackup 				=	self.basicOptions["COOKIE"]["currentSetting"]
				for cookieN in cookieBackup.keys():
					cookieBackup[cookieN] 	= 	cookieBackup[cookieN].replace("*",payload)
				cookie 						=	self.basicOptions["COOKIE"]["currentSetting"]
			elif(self.injectPoint == "DATADICT"):
				dataBackup					=	self.basicOptions["DATADICT"]["currentSetting"]
				for name in dataBackup.keys():
					dataBackup[name] 		= 	dataBackup[name].replace("*",payload)
				data 						=	dataBackup
		# Prepare
		s 									= 	requests.Session()
		header 								=	{
					"USER_AGENT"			:	userAgent,
					"HOST"					:	host,
					"REFERER"				:	referer,
					"ACCEPT"				:	accept,
					"ACCEPT_ENCODING"		:	acceptEncoding,
					"ACCEPT_LANGUAGE"		: 	acceptLanguage,
					"CONNECTION"			:	connection,
					}
		if(httpMethod == "get"):
			# Prepare header
			req 							= 	requests.Request(
				'GET', 
				url,
				cookies 					=	cookie,
				headers 					=	header,
				)
			
		elif(httpMethod == "post"):
			# Post method
			req 							= 	requests.Request(
				'POST', 
				url,
				cookies 					=	cookie,
				headers 					=	header,
				data 						=	dataDict,
				# Converrt
				)
		prepped 							= 	req.prepare()
		self.logger.debug("Send {2} request number {0} to {1}.".format(self.requestCount + 1, host, httpMethod.upper()))
		self.logger.debug("URL: {0}.".format(url))
		self.logger.debug("Cookie: {0}.".format(cookie))
		if(httpMethod == "post"):
			self.logger.debug("Data: {0}.".format(dataDict))
		resp 								= 	s.send(
				prepped,
				# timeout 					=	self.timeOut,
			)
		# Update number request
		self.requestCount					+=	1
		# Return response
		return resp
	def start(self):
		if(self.checkOptions() == False):
			exit()
		if(self.checkInjectPoint() == False):
			exit()
		self.logger.warning("Started Module: {0}.".format(self.name))
	def end(self):
		# Finish
		self.logger.warning("Send {0} request.".format(self.requestCount))