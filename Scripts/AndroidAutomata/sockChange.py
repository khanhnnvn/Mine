from SQLite.sqlite import SQLitedatabase
from SockChange.sockD import sockD
import logging, datetime, os, subprocess, time, requesocks, sys, signal
from time import sleep

class SockAutomata(object):
	def __init__(self):
		self.timeForSock				=		300 													# 15 ph/sock 900
		# Logger
		self.logPrefix					=		"sockD"													# Log Prefix
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
		
		self.start()
		# self.checkAllSock()
		# self.sockD.closeSock()
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
		# Only run first add sock
	def checkAllSock(self):
		for i in range(0,260):
			self.sockD.getSock()
	# Start auto
	# get sock
	def getSock(self):
		while ((self.sockD.getSock()) == False):
			self.logger.debug("Sock is not good, changed status. go to next sock")
	def start(self):
		# self.checkAllSock()
		while (True):
			self.logger.debug("Change new sock")
			self.getSock()
			time.sleep(self.timeForSock)

# Main control
def main():
	mainClass 							=	SockAutomata()
if __name__ == '__main__':
	main()