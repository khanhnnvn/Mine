import shodan, os
from libs.coreScannerModule import coreScannerModule
class Module(coreScannerModule):
	def __init__(self, logger, profile):
		coreScannerModule.__init__(self, logger, profile)
		self.name							=	"Shodan Module"
		self.description 					=	"Shodan Module for Search Enginer"
		self.rank							=	"MEDIUM"					# Exploit level
		self.type							=	"Scanner"					# Type: exploit | scanner | support
		self.author							=	"namhb"
		self.version						=	"0.0.1"
		self.shodanAPI 						=	self.base.getConfig("SHODAN","API_KEY")
		self.api 							= 	shodan.Shodan(self.shodanAPI)
		self.basicOptions["KEYWORD"] 		=	{
					"currentSetting"		:	None,
					"required"				:	True,
					"description"			:	"Key word to search"
		}
	def search(self, keyword):
		try:
			self.logger.debug("Shodan search {0}".format(keyword))
			results 	 					= 	self.api.search(keyword)
			self.logger.info("Found {0} results.".format(results['total']))
			return results
		except shodan.APIError, e:
			self.logger.error(e)
	def run(self):
		keyword 							=	self.basicOptions["KEYWORD"]["currentSetting"]
		self.search(keyword)
# Load control module
execfile(os.path.join(os.getcwd(), "libs", "controlModule.py"))
