import shodan, os, re, time
from libs.coreScannerModule import coreScannerModule
from operator import itemgetter, attrgetter, methodcaller
from selenium import webdriver 												# use selenium to interactive google via phantomjs
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Module(coreScannerModule):
	def __init__(self, logger, profile):
		coreScannerModule.__init__(self, logger, profile)
		self.name							=	"Google Search Subdomain Module"
		self.description 					=	"Google Module for Search Enginer"
		self.rank							=	"MEDIUM"					# Exploit level
		self.type							=	"Scanner"					# Type: exploit | scanner | support
		self.author							=	"namhb"
		self.version						=	"0.0.1"
		self.basicOptions["DOMAIN"] 		=	{
					"currentSetting"		:	None,
					"required"				:	True,
					"description"			:	"Primary domain to search"
		}
		dcap 								= 	dict(DesiredCapabilities.PHANTOMJS)
		dcap["phantomjs.page.settings.customHeaders"] 	= {
			'ACCEPT_LANGUAGE'				:	'en,en-US;q=0.8,vi-VN;q=0.6,vi;q=0.4,fr-FR;q=0.2,fr;q=0.2',
			'ACCEPT_ENCODING'				:	'gzip, deflate, sdch',
			'ACCEPT'						:	'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'USER_AGENT'					:	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
		}
		self.driver 						=	webdriver.PhantomJS(
			executable_path="//usr//bin//phantomjs",
			desired_capabilities=dcap
		)
		self.nextPage 						=	False
		self.nextURL 						=	""
		self.subDomains 					=	[]
		self.startID 						=	0
		self.tmpID 							=	0
		self.foundNew 						=	False
		self.query 							=	""
		self.waitTime 						=	5
		self.pageList						=	[]
	def debugHTML(self):
		text_file = open(os.path.join(os.getcwd(),self.tmpFolder,"debug.html"), "w")
		text_file.write(self.driver.page_source.encode('utf8'))
		text_file.close()
	def addSubDomain(self, linkUrl):
		# Find domain
		m 									= 	re.search("\/\/(.*?)\/", linkUrl)
		domain 								=	m.group(1)
		if((domain != self.domain) and (domain not in self.subDomains)):
			self.logger.info("Found: {0}".format(domain))
			self.subDomains.append(domain)
			# set Found New
			self.foundNew 					=	True
			self.query 						=	"{0} -{1}".format(self.query, domain)
	def getNextPage(self):		
		self.pageList 						=	sorted(self.pageList, key=lambda item:item[0])
		for item in self.pageList:
			if(item[0] > self.startID):
				self.startID 				=	item[0]
				self.nextURL 				=	item[1]
				self.nextPage 				=	True
				break;
	def checkCaptcha(self):
		try:
			self.driver.find_element_by_name("captcha")
		except Exception, e:
			return False
		return True
	def sloveCaptcha(self):
		imgs 								=	self.driver.find_elements_by_tag_name("img")
		for img in imgs:
			print(img.get_attribute("src"))
		self.driver.save_screenshot(os.path.join(os.getcwd(),self.tmpFolder,"captcha.png"))
		captcha 							= 	raw_input('Enter captcha :')
		captchaInput 						=	self.driver.find_element_by_name("captcha")
		captchaInput.clear()
		captchaInput.send_keys(captcha)
		captchaButton 						=	self.driver.find_element_by_name("submit")
		captchaButton.click()
		self.debugHTML()
	def findOnePage(self):
		# Check captcha
		while (self.checkCaptcha()):
			self.logger.error("Captcha found, exit now")
			self.sloveCaptcha()
		# Find all 
		self.debugHTML()
		driver 								=	self.driver
		allATag 							=	driver.find_elements_by_tag_name("a")
		self.pageList						=	[]
		self.nextURL 						=	""
		self.nextPage 						=	False
		for i in range(0, len(allATag)):
			aTag 							=	allATag[i]
			linkUrl 						=	aTag.get_attribute("href")
			if((linkUrl[:32] == "https://www.google.com.vn/url?q=") and (linkUrl[32:70] != "http://webcache.googleusercontent.com/")):
				self.addSubDomain(linkUrl[32:])
			elif((linkUrl[:35] == "https://www.google.com.vn/search?q=") and (linkUrl.find("&start=") > 0)):
				m 							= 	re.search("start=(.*?)&", linkUrl)
				cid 						=	int(m.group(1))
				item 						=	(cid,linkUrl)
				self.pageList.append(item)
		self.getNextPage()

		# # Check new subdomain to sub query, if not, go next page, disable to prevent loop
		# if(self.foundNew == True):
		# 	# Re run first with new query append - new sub domain
		# 	self.logger.debug("Found new subdomain, run new query: {0}".format(self.query))
		# 	time.sleep(self.waitTime)
		# 	self.getFirst(self.query)

		if(self.nextPage == True):
			self.logger.debug("Go to next page {0}".format(self.nextURL))
			self.driver.get(self.nextURL)
			time.sleep(self.waitTime)
			self.findOnePage()
		else:
			# Don`t go to next page
			self.debugHTML()
			self.logger.info("Not found any subdomain, finish now.")
	def getFirst(self, query):
		# Set found new
		self.foundNew 						=	False
		self.startID 						=	0
		self.tmpID 							=	0
		self.nextPage 						=	False
		self.nextElement 					=	None
		# Check domain
		self.logger.debug("First Query: {0}".format(query))
		driver 								=	self.driver
		# Fill query and search
		
		textSearch 							=	driver.find_element_by_name("q") 					# Text box
		textSearch.clear()
		textSearch.send_keys(query)
		clickSearch 						=	driver.find_element_by_name("btnG") 				# click button
		clickSearch.click()
		# Parse to find all link
		self.findOnePage()
	def printResult(self):
		print("Found {0} subdomains:".format(len(self.subDomains)))
		print("=============")
		print("")
		for subdomains in self.subDomains:
			print("\t{0}".format(subdomains))
	def run(self):
		self.domain 						=	self.basicOptions["DOMAIN"]["currentSetting"]
		self.logger.debug("Google Search Sub Domain: {0}".format(self.domain))
		self.driver.get("https://google.com.vn/")
		self.query 							=	"site:{0}".format(self.domain)
		self.getFirst(self.query)
		self.printResult()
# Load control module
execfile(os.path.join(os.getcwd(), "libs", "controlModule.py"))
