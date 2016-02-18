from SQLite.sqlite import SQLitedatabase
from SockChange.sockD import sockD
import logging, datetime, os, subprocess, time, requesocks
from appium import webdriver
from time import sleep
class AndroidAutomata(object):
	"""docstring for AndroidAutomata"""
	def __init__(self):
		self.logPrefix					=		"appium"												# Log Prefix
		self.logFolder					=		"Logs"												# Log store
		self.dirPath 					=		os.getcwd()
		self.logSetup()
		self.dbConnect()
		self.sockD 						=		sockD(self.db)
		self.start()
	# get sock
	def getSock(self):
		while ((self.sockD.getSock()) == False):
			self.logger.debug("Sock is not good, changed status. go to next sock")
	# Setup database
	def dbConnect(self):
		self.db 	=	SQLitedatabase("appDB")
	# Log setup
	def logSetup(self):
		self.logger 					= 		logging.getLogger(__name__)							# Logging constructor 
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
		self.logger.setLevel(logging.DEBUG)
	# Start auto
	def start(self):
		self.getSock()
		self.setUpAppium()
		if(self.sockD.checkOpenPort() is False):
			# Start run
			self.logger.info("Start run new appium instance")
			self.clickAdd1()
		else:
			pass
	# Setup appium
	def setUpAppium(self):
		"Setup for the click"
		desired_caps = {}
		desired_caps['platformName'] = 'Android'
		desired_caps['platformVersion'] = '5.0'
		desired_caps['deviceName'] = '02c4b753091ce5ec'
		desired_caps['noReset'] = True
		# Returns abs path relative to this file and not cwd
		desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__),'app-release.apk'))
		desired_caps['appPackage'] = 'com.hbn.hakmebankdemo'
		desired_caps['appActivity'] = '.LoginActivity'
		self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
	def clickAdd1(self):
		for i in range(0,10):
			time.sleep(5)
			element = self.driver.find_element_by_name("Sign in or register")
			element.click()
def main():
	mainClass 		=	AndroidAutomata()

if __name__ == '__main__':
	main()