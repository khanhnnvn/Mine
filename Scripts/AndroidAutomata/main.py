from SQLite.sqlite import SQLitedatabase
from SockChange.sockD import sockD
from Appium.appiumAuto import appiumAuto
import logging, datetime, os, subprocess, time, requesocks, sys, signal
from time import sleep

class AndroidAutomata(object):
	"""docstring for AndroidAutomata"""
	def __init__(self):
		self.appName 					=		"com.hbn.hakmeshop"
		self.activityName 				=		".MainActivity"
		self.adButtonID 				=		"com.hbn.hakmeshop:id/hakmeShopButton"
		self.deviceName 				=		"604ae633"
		# self.deviceName 				=		"02c4b753091ce5ec"
		self.platformVersion			=		"4.4.2"
		self.timePerSock 				=		15
		self.appiumURL 					=		"http://localhost:4723/wd/hub"
		# Logger
		self.logPrefix					=		"appium"												# Log Prefix
		self.logFolder					=		"Logs"													# Log store
		self.dirPath 					=		os.getcwd()
		self.logSetup()
		self.db 						=		SQLitedatabase("appDB")									# Setup database
		# Sock config
		self.sockPort					=		9991
		self.sockD 						=		sockD(
													self.db,
													self.logger,
													self.sockPort)
		self.appium 					=		appiumAuto(
													self.appName, 
													self.activityName, 
													self.adButtonID, 
													self.deviceName, 
													self.platformVersion, 
													# self.timePerSock, 
													self.appiumURL,
													self.logger,
													self.sockD,
													)
		
		self.start()
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
	def start(self):
		try:
			self.appium.setUpAppium()
			# self.test()
		except Exception, e:
			self.logger.error(e)
			self.logger.error("Can not start Appium")
			# Wait and re run
			time.sleep(5)
			self.start()
			# Set max to restart appium
		if(self.sockD.checkOpenPort() is True):
			# Start run
			self.logger.info("Start run new appium instance")
			self.appium.appiumStartAppScript()
		else:
			pass
	def finish(self):
		self.appium.driver.quit()	
	def test(self):
		el = self.appium.driver.find_element_by_id(self.adButtonID)
		self.appium.proxyDroidProcess()
		self.appium.driver.quit()
# Main control
def main():
	mainClass 							=	AndroidAutomata()
if __name__ == '__main__':
	main()
	