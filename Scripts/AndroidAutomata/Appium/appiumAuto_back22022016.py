#!/usr/bin/python
import logging, datetime, os, subprocess, time
from appium import webdriver
class appiumAuto:
	def __init__(self, appName, activityName, adButtonID, deviceName, platformVersion, timePerSock, appiumURL, logger, sockD):
		self.appName 					=		appName
		self.activityName 				=		activityName
		self.adButtonID 				=		adButtonID
		self.deviceName 				=		deviceName
		self.platformVersion 			=		platformVersion
		self.timePerSock 				=		timePerSock
		self.appiumURL 					=		appiumURL
		self.logger 					=		logger
		self.sockD						=		sockD
		# Setup for PlayStore
		# com.android.vending/com.google.android.finsky.activities.MainActivity
		self.PsAppName 					=		"com.android.vending"
		self.PsActivityName 			=		"com.google.android.finsky.activities.MainActivity"
		# Setup for proxyDroid
		# org.proxydroid/org.proxydroid.ProxyDroid
		self.PxAppName 					=		"org.proxydroid"
		self.PxActivityName 			=		"org.proxydroid.ProxyDroid"
		self.PxSwitchID 				=		"android:id/switchWidget"

	# get sock
	def getSock(self):
		while ((self.sockD.getSock()) == False):
			self.logger.debug("Sock is not good, changed status. go to next sock")
	# Setup appium 
	def setUpAppium(self):
		self.getSock()
		"Setup for the click"
		desired_caps = {}
		desired_caps['platformName'] 			= 	'Android'
		desired_caps['platformVersion'] 		= 	self.platformVersion
		# desired_caps['deviceName'] = '02c4b753091ce5ec' # Nexus
		desired_caps['deviceName'] 				=	self.deviceName 
		# Returns abs path relative to this file and not cwd
		# desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__),'app-release.apk'))
		# Main
		desired_caps['appPackage'] 				=	self.appName
		desired_caps['appActivity'] 			=	self.activityName
		# For test
		# desired_caps['appPackage'] 				=	self.PxAppName
		# desired_caps['appActivity'] 			=	self.PxActivityName
		self.driver = webdriver.Remote(self.appiumURL, desired_caps)
	# Function process startApp adversi
	def appiumStartAppScript(self):
		element = self.driver.find_element_by_id(self.adButtonID)
		countSockTime 							=	0
		while (True):
			time.sleep(5)
			try:
				element.click()
			except Exception, e:
				activityN	   					=   self.driver.current_activity
				self.logger.debug(activityN)
				# Click one time
				clicked 						=	False
				if(activityN == "com.startapp.android.publish.OverlayActivity"):
					# 1, webview: thank
					if(self.findImageView() (clicked == False)):
						self.el.click()
						self.logger.debug("Cliked {0}".format("ImageView"))
						clicked 				=	True
					# 2, images
					if((self.findImage() and (clicked == False) )):
						self.el.click()
						self.logger.debug("Cliked {0}".format("Image"))
						clicked 				=	True
					# 3, view like Full
					if(self.findView() and (clicked == False)):
						self.el.click()
						self.logger.debug("Cliked {0}".format("View"))
						clicked 				=	True
					if(self.findWebView() and (clicked == False)):
						self.el.click()
						self.logger.debug("Cliked {0}".format("WebView"))
						clicked 				=	True
					if(clicked == False):
						self.logger.error("Check uiviewer")
				elif(activityN == "com.startapp.android.publish.list3d.List3DActivity"):
					if(self.findRelativeLayout() and (clicked == False)):
						self.el.click()
						self.logger.debug("Cliked {0}".format("RelativeLayout"))
						clicked 				=	True
					if(self.findImageView() and (clicked == False)):
						self.el.click()
						self.logger.debug("Cliked {0}".format("ImageView"))
						clicked 				=	True
					if(clicked == False):
						self.logger.error("Check uiviewer")
				elif(activityN == "com.startapp.android.publish.FullScreenActivity"):
					# View full
					if(self.findView()):
						self.el.click()
						self.logger.debug("Cliked {0}".format("View"))
						clicked 				=	True
					if(clicked == False):
						self.logger.error("Check uiviewer")
				elif(activityN == "org.chromium.chrome.browser.document.DocumentActivity"):
					# Chrome, wait close
					time.sleep(5)
					self.driver.start_activity(self.appName,self.activityName)
				elif(activityN == "com.google.android.apps.chrome.ChromeTabbedActivity"):
					# Install app if not found
					time.sleep(5)
					self.driver.start_activity(self.appName,self.activityName)
				elif(activityN == "com.google.android.finsky.activities.MainActivity"):
					# Install app if not found
					# Add more 5 to prevent change sock
					
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
			if(countSockTime == self.timePerSock):
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
		count = 0
		time.sleep(5)
		for i in range(15):
			try:
				self.logger.debug("Wait time to load PlayStore".format(count))
				time.sleep(1)
				# Install button id
				installButton = self.driver.find_element_by_id("com.android.vending:id/buy_button")
				installButton.click()
				time.sleep(1)
				# Accept
				installButton.click()
				break
			except Exception, e:
				# Install error, may be time out
				count 		+= 1
			if(count == 30 ):
				self.logger.error("Can not install from PlayStore, back to main app")
	
	def checkProxyOnOff(self):
		try:
			switchButton 					=	self.driver.find_element_by_id("android:id/switchWidget")
			if(switchButton.get_attribute("checked") == "true"):
				return True
			else:
				return False
		except Exception, e:
			self.logger.error("Not found ProxyDroid Switch")
			return False
	def proxyDroidProcess(self, action=True):
		print(self.driver.contexts)
		# self.driver.start_activity(self.PxAppName, self.PxActivityName)
		# switchButton 					=	self.driver.find_element_by_id("android:id/switchWidget")
		# if(self.checkProxyOnOff()):
		# 	# Proxy is on
		# 	if(action):
		# 		# On, dont need on
		# 		self.logger.debug("Proxy is on, don`t need on")
		# 	else:
		# 		# Off
		# 		switchButton.click()
		# 		self.logger.debug("Turn off Proxy")
		# else:
		# 	if(action):
		# 		# On
		# 		switchButton.click()
		# 		self.logger.debug("Turn on Proxy")
		# 	else:
		# 		# Off, don`t need off
		# 		self.logger.debug("Proxy is off, don`t need off")
	def playStoreProcess(self):
		pass