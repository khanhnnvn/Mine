#!/usr/bin/python
import logging, datetime, os, subprocess, time
from appium import webdriver
class appiumAuto:
	def __init__(self, appName, activityName, adButtonID, deviceName, platformVersion, appiumURL, logger, sockD):
		self.appName 					=		appName
		self.activityName 				=		activityName
		self.adButtonID 				=		adButtonID
		self.deviceName 				=		deviceName
		self.platformVersion 			=		platformVersion
		self.appiumURL 					=		appiumURL
		self.logger 					=		logger
		self.sockD 						=		sockD
		self.clickAble 					=		0
		# Setup for PlayStore
		# com.android.vending/com.google.android.finsky.activities.MainActivity
		self.PsAppName 					=		"com.android.vending"
		self.PsActivityName 			=		"com.google.android.finsky.activities.MainActivity"
		self.PsHomeText 				=		"Play Store"
		# Setup for proxyDroid
		# org.proxydroid/org.proxydroid.ProxyDroid
		self.PxAppName 					=		"org.proxydroid"
		self.PxActivityName 			=		"org.proxydroid.ProxyDroid"
		self.PxSwitchID 				=		"android:id/switchWidget"
		self.PxHomeText 				=		"ProxyDroid"

		# Setup for Chome
		self.ChHomeText 				=		"Chrome"
	# Setup appium 
	def setUpAppium(self):
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
		# desired_caps['appPackage'] 			=	self.PxAppName
		# desired_caps['appActivity'] 			=	self.PxActivityName
		self.driver = webdriver.Remote(self.appiumURL, desired_caps)
	def goToHome(self, callback):
		try:
			self.driver.background_app(5)
			self.driver.keyevent(3)
			if(callback == 1):
				self.callProxyDroid()
			if(callback == 2):
				self.callPlayStore()
			
		except Exception, e:
			self.logger.error("Go Home Error")
			self.logger.error(e)
	def checkHome(self):
		try:
			homeButton 								=	self.driver.find_element_by_xpath("//android.widget.TextView[@text='{0}']".format(self.PxHomeText))
			self.logger.debug("This is Home Desktop")
			return True
		except Exception, e:
			self.logger.debug("Not Home, try again")
			return False
	def callProxyDroid(self):
		# Send Home button code:3
		try:
			if(self.checkHome()):
				homeButton 								=	self.driver.find_element_by_xpath("//android.widget.TextView[@text='{0}']".format(self.PxHomeText))
				homeButton.click()
				self.logger.error("Called Proxy Droid")
			else:
				self.goToHome(1)
		except Exception, e:
			self.logger.error("Call ProxyDroid Error")
			self.logger.error(e)
	def callPlayStore(self):
		# Send Home button code:3
		try:
			if(self.checkHome()):
				homeButton 								=	self.driver.find_element_by_xpath("//android.widget.TextView[@text='{0}']".format(self.PsHomeText))
				homeButton.click()
				self.logger.error("Called PlayStore")
				# Please wait
				time.sleep(2)
			else:
				self.goToHome(2)
		except Exception, e:
			self.logger.error("Call PlayStore Error")
			self.logger.error(e)

	# Function process startApp adversi
	def mainStartScript(self):
		if(self.sockD.checkOpenPort() is True):
			self.appiumStartAppScript()
		else:
			self.logger.debug("Wait For new Sock")
			time.sleep(10)
			self.appiumStartAppScript()
	def appiumStartAppScript(self):
		# Count click
		element = self.driver.find_element_by_id(self.adButtonID)
		self.proxyDroidProcess(True)
		self.driver.start_activity(self.appName,self.activityName)
		waitTime = 0
		while (True):
			try:
				if(self.sockD.checkOpenPort() is True):
					element.click()
					self.clickAble 					+=	1
					if(self.clickAble == 50):
						# Change sock
						self.sockD.getSock()
				else:
					self.logger.debug("Wait For new Sock {0}".format(waitTime))
					time.sleep(30)
					# Select to hold
					try:
						self.el = self.driver.find_element_by_class_name("android.webkit.WebView")
					except:
						pass
					waitTime += 1
					
			except Exception, e:
				waitTime 						=	0
				activityN	   					=   self.driver.current_activity
				self.clickAble 					=	0
				self.logger.debug(activityN)
				# Click one time
				if(self.checkPopUpChrome()):
					# Click Chrome 
					# Find android:id/alwaysUse
					self.choseChromePopup()
				if(activityN == "com.startapp.android.publish.OverlayActivity"):
					# 1, webview: thank
					if(self.findImageView()):
						self.el.click()
						self.logger.debug("Cliked {0}".format("ImageView"))
					# 2, images
					if(self.findImage()):
						self.el.click()
						self.logger.debug("Cliked {0}".format("Image"))
					# 3, view like Full
					if(self.findView()):
						self.el.click()
						self.logger.debug("Cliked {0}".format("View"))
					if(self.findWebView()):
						self.el.click()
						self.logger.debug("Cliked {0}".format("WebView"))
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
					# Chrome, wait close
					time.sleep(10)
					self.driver.start_activity(self.appName,self.activityName)
				elif((activityN == "com.google.android.apps.chrome.ChromeTabbedActivity") or (activityN == "org.chromium.chrome.browser.ChromeTabbedActivity")):
					# Install app if not found
					time.sleep(10)
					self.driver.start_activity(self.appName,self.activityName)
				elif(activityN == "com.google.android.finsky.activities.MainActivity"):
					# Install app if not found
					self.logger.debug("Go to PlayStore")
					self.installApp()
					# Demo on time wait new code for playstore
					self.driver.start_activity(self.appName,self.activityName)
				elif(activityN == "com.google.android.finsky.activities.ScreenshotsActivity"):
					# Back to mainapp
					self.driver.start_activity(self.appName,self.activityName)
				else:
					# Back to app
					time.sleep(10)
					self.driver.start_activity(self.appName,self.activityName)
					# Out app
		# Quit
		self.driver.quit()
	def choseChromePopup(self):
		try:
			checkBox = self.driver.find_element_by_id("android:id/alwaysUse")
			if(checkBox.get_attribute("true") == "true"):
				self.logger.debug("Checked alwaysUse, don`t need click")
			else:
				checkBox.click()
			# Chose chrome
			button = self.driver.find_element_by_id("android:id/allow_button")
			button.click()
		except Exception, e:
			self.logger.error("Select Chrome error")
			self.logger.error(e)
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
		self.driver.start_activity(self.appName,self.activityName)
		count = 0
		# Start 
		self.proxyDroidProcess(False)
		self.driver.start_activity(self.appName,self.activityName)
		self.callPlayStore()
		if(self.checkPlayStoreHome()):
			# Return Hakme
			self.logger.debug("Play Store Home, don`t need install")
		elif(self.checkPlayStoreNotAllowApp()):
			self.logger.debug("App not allow installed")
		elif(self.checkPlayStoreLoading()):
			self.logger.debug("Kill playstore")
			self.driver.start_activity(self.appName,self.activityName)
			self.driver.start_activity(self.PsAppName, self.PsActivityName)
		else:
			for i in range(30):
				try:
					self.logger.debug("Wait time to load PlayStore {0}".format(count))
					time.sleep(1)
					# Install button id
					installButton 							= self.driver.find_element_by_id("com.android.vending:id/buy_button")
					installButton.click()
					continueButton 							= self.driver.find_element_by_id("com.android.vending:id/continue_button")
					# Accept
					continueButton.click()
					count 									+= 1
					# Check app installed
					time.sleep(5)
					while (self.checkPlayStoreInstalled() == False):
						self.logger.debug("Wait app installed")
						time.sleep(10)
					if(self.checkPlayStoreInstalled()):
						# self.lauchInstalledApp()
						break
					# Launch app
					
				except Exception, e:
					# Install error, may be time out
					count 		+= 1
				if(count > 29 ):
					self.logger.error("Can not install from PlayStore, back to main app")
					self.driver.start_activity(self.appName,self.activityName)
					self.driver.start_activity(self.PsAppName, self.PsActivityName)
					self.logger.debug("Killed playstore")
		# On Proxy
		self.driver.start_activity(self.appName,self.activityName)
		self.proxyDroidProcess(True)
		self.driver.start_activity(self.appName,self.activityName)
	def checkPlayStoreNotAllowApp(self):
		# com.android.vending:id/warning_message_module
		try:
			checkButton 						=	self.driver.find_element_by_id("com.android.vending:id/warning_message_module")
			return True
		except Exception, e:
			return False
	def lauchInstalledApp(self):
		# com.android.vending:id/launch_button
		try:
			checkButton 						=	self.driver.find_element_by_id("com.android.vending:id/launch_button")
			checkButton.click()
			time.sleep(15)
		except Exception, e:
			self.logger.debug("Can not lauch app")
	def checkPlayStoreInstalled(self):
		# com.android.vending:id/launch_button
		try:
			checkButton 						=	self.driver.find_element_by_id("com.android.vending:id/launch_button")
			self.logger.debug("App installed OK")
			return True
		except Exception, e:
			return False
	def checkPlayStoreHome(self):
		# com.android.vending:id/li_title
		try:
			homeButton 						=	self.driver.find_element_by_id("com.android.vending:id/li_title")
			self.logger.debug("PlayStore is Home")
			return True
		except Exception, e:
			self.logger.debug("PlayStore is not ready")
			return False
	def checkPlayStoreRetry(self):
		# com.android.vending:id/retry_button
		try:
			processBar 						=	self.driver.find_element_by_id("com.android.vending:id/retry_button")
			self.logger.debug("PlayStore is retry")
			return True
		except Exception, e:
			self.logger.debug("PlayStore is not ready")
			return False
	def checkPlayStoreLoading(self):
		# Find android.widget.ProgressBar
		try:
			processBar 						=	self.driver.find_element_by_class_name("Find android.widget.ProgressBar")
			self.logger.debug("PlayStore is loading")
			return True
		except Exception, e:
			self.logger.debug("PlayStore is ready")
			return False
	def checkProxyOnOff(self):
		try:
			switchButton 					=	self.driver.find_element_by_id("android:id/switchWidget")
			if(switchButton.get_attribute("checked") == "true"):
				self.logger.debug("Proxy is ON")
				return True
			else:
				self.logger.debug("Proxy is OFF")
				return False
		except Exception, e:
			self.logger.error("Not found ProxyDroid Switch")
			return False
	def proxyDroidProcess(self, action=True):
		if(action == True):
			self.callProxyDroid()
			# On off now
			switchButton 					=	self.driver.find_element_by_id("android:id/switchWidget")
			if(self.checkProxyOnOff()):
				# Proxy is on
				if(action):
					# On, dont need on
					self.logger.debug("Proxy is on, don`t need on")
				else:
					# Off
					switchButton.click()
					self.logger.debug("Turn off Proxy")
			else:
				if(action):
					# On
					switchButton.click()
					self.logger.debug("Turn on Proxy")
				else:
					# Off, don`t need off
					self.logger.debug("Proxy is off, don`t need off")
		else:
			self.driver.start_activity(self.PxAppName, self.PxActivityName)
	def checkPopUpChrome(self):
		try:
			Chome 								=	self.driver.find_element_by_xpath("//android.widget.TextView[@text='Chrome']")
			CheckBox 							=	self.driver.find_element_by_class_name("android.widget.CheckBox")
			self.logger.debug("Chrome chose default browser popup")
			return True 					
		except Exception, e:
			return False