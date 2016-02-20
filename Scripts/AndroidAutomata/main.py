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
		self.timePerSock 				=		15
		self.dirPath 					=		os.getcwd()
		self.logSetup()
		self.dbConnect()
		self.sockD 						=		sockD(self.db)
		self.getSock()
		self.start()
		# self.checkAllSock()
		# self.sockD.closeSock()
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
		self.appName 					=		"com.hbn.hakmeshop"
		self.activityName 				=		".MainActivity"
		self.deviceName 				=		"604ae633"
		fileHandler.setFormatter(self.logFormat)
		self.logger.addHandler(fileHandler)
		self.logger.setLevel(logging.DEBUG)
	def checkAllSock(self):
		for i in range(0,260):
			self.sockD.getSock()
	# Start auto
	def start(self):
		
		try:
			self.setUpAppium()
		except Exception, e:
			self.logger.error("Can not start Appium")
			# Wait and re run
			time.sleep(5)
			self.start()
			# Set max to restart appium
		if(self.sockD.checkOpenPort() is True):
			# Start run
			self.logger.info("Start run new appium instance")
			self.appiumScript()
		else:
			pass
	# Setup appium
	def setUpAppium(self):
		"Setup for the click"
		desired_caps = {}
		desired_caps['platformName'] 			= 	'Android'
		desired_caps['platformVersion'] 		= 	'4.4.2'
		# desired_caps['deviceName'] = '02c4b753091ce5ec' # Nexus
		desired_caps['deviceName'] 				=	self.deviceName 
		# Returns abs path relative to this file and not cwd
		# desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__),'app-release.apk'))
		desired_caps['appPackage'] 				=	self.appName
		desired_caps['appActivity'] 			=	self.appActivity
		self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
	def appiumScript(self):
		element = self.driver.find_element_by_id("com.hbn.hakmeshop:id/hakmeShopButton")
		countSockTime 			=	0
		while (True):
			time.sleep(5)
			try:
				element.click()
			except Exception, e:
				activityN	   =   self.driver.current_activity
				self.logger.debug(activityN)
				if(activityN == "com.startapp.android.publish.OverlayActivity"):
					# 1, webview: thank
					if(self.findWebView()):
						self.el.click()
						self.logger.debug("Cliked {0}".format("WebView"))
					# 2, images
					elif(self.findImage()):
						self.el.click()
						self.logger.debug("Cliked {0}".format("Image"))
					# 3, view like Full
					elif(self.findView()):
						self.el.click()
						self.logger.debug("Cliked {0}".format("View"))
					elif(self.findImageView()):
						self.el.click()
						self.logger.debug("Cliked {0}".format("ImageView"))
					else:
						self.logger.error("Check uiviewer")
				elif(activityN == "com.startapp.android.publish.list3d.List3DActivity"):
					if(self.findRelativeLayout()):
						self.el.click()
						self.logger.debug("Cliked {0}".format("RelativeLayout"))
					if(self.findImageView()):
						self.el.click()
						self.logger.debug("Cliked {0}".format("ImageView"))
				elif(activityN == "com.startapp.android.publish.FullScreenActivity"):
					# View full
					if(self.findView()):
						self.el.click()
						self.logger.debug("Cliked {0}".format("View"))
				elif(activityN == "org.chromium.chrome.browser.document.DocumentActivity"):
					# Chrome, close
					self.driver.start_activity(self.appName,self.activityName)
				elif(activityN == "com.google.android.apps.chrome.ChromeTabbedActivity"):
					# Install app if not found
					self.driver.start_activity(self.appName,self.activityName)
				elif(activityN == "com.google.android.finsky.activities.MainActivity"):
					# Install app if not found
					self.installApp()
					# Demo on time wait new code for playstore
					self.driver.start_activity(self.appName,self.activityName)
				elif(activityN == "com.google.android.finsky.activities.ScreenshotsActivity"):
					# Back to mainapp
					self.driver.start_activity(self.appName,self.activityName)
				else:
					# Back to app
					self.driver.start_activity(self.appName,self.activityName)
					# Out app
					# close app
			countSockTime += 1
			if(countSockTime == 10):
				countSockTime = 0
				# Update new sock
				self.logger.debug("Start change new Sock")
				self.getSock()
		# Quit
		self.driver.quit()
	def findRelativeLayout(self):
		try:
			self.el = self.driver.find_element_by_class_name("android.widget.RelativeLayout")
			return True
		except Exception, e:
			return False
	def findWebView(self):
		try:
			self.el = self.driver.find_element_by_class_name("android.webkit.WebView")
			return True
		except Exception, e:
			return False
	def findImage(self):
		try:
			self.el = self.driver.find_element_by_class_name("android.widget.Image")
			return True
		except Exception, e:
			return False
	def findImageView(self):
		try:
			self.el = self.driver.find_element_by_class_name("android.widget.ImageView")
			return True
		except Exception, e:
			return False
	def findView(self):
		try:
			self.el = self.driver.find_element_by_class_name("android.view.View")
			return True
		except Exception, e:
			return False
	def installApp(self):
		# Find install button
		try:
			installButton = self.driver.find_element_by_class_name("android.widget.Button")
			installButton.click()
			time.sleep(2)
			# Accept
			installButton.click()
		except Exception, e:
			# Install error, may be time out
			self.logger.error("Can not install from PlayStore, back to main app")
		
def main():
	mainClass 		=	AndroidAutomata()

if __name__ == '__main__':
	main()