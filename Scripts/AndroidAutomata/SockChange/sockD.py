import logging, datetime, os, subprocess, time, requesocks
#!/usr/bin/python
class sockD:
	def __init__(self, db):
		self.db 						=		db
		self.logPrefix					=		"sockD"												# Log Prefix
		self.logFolder					=		"Logs"												# Log store
		self.dirPath 					=		os.getcwd()
		self.sockPort 					=		9991
		self.sockTimeOut 				=		10													# 10
		self.sshCmd 					=		"sshpass -p {0} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no {1}@{2} -D {3} "
		self.netstatCmd 				=		"lsof -i:{0} | tail -n +2 | awk '{{print $2}}' | sort | uniq"
		self.killProcessCmd 			=		"kill -9 {0}"
		self.logSetup()
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
	def checkOpenPort(self):
		cmd 							=		self.netstatCmd.format(self.sockPort)
		re 								= 		os.popen(cmd).read()
		try:
			pid 						=		int(re)
			self.logger.debug("Pid is {0}".format(pid))
			self.pid 					=		pid
			return True
		except Exception, e:
			self.logger.debug("Port is not listen")
			return False
	def closeSock(self):
		if(self.checkOpenPort()):
			# Kill process
			cmd 						=	self.killProcessCmd.format(self.pid)
			os.popen(cmd)
			time.sleep(1)	# delay 2s
			if(self.checkOpenPort()):
				self.logger.error("Can not kill pid {0}".format(self.pid))
				return False
			else:
				self.logger.debug("Killed process {0}".format(self.pid))
				return True
		else:
			return True
	def getSock(self):
		if(self.closeSock()):
			# closeSock ok, open sock
			sockInfo 					=	self.selectSock()
			if(sockInfo is not None):
				self.logger.debug("Goted sock info:")
				self.logger.debug(sockInfo)
				cmd 						=	self.sshCmd.format(sockInfo["password"], sockInfo["username"], sockInfo["ip"], self.sockPort)
				process 					= 	subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				time.sleep(self.sockTimeOut)
				if(self.checkOpenPort()):

					# Open sock ok
					self.logger.info("Open new sock with PID: {0}".format(self.pid))
					
					# Check Internet
					if(self.checkInternet()):
						self.logger.debug("Sock PID {0} access Internet OK".format(self.pid))
						return True
					else:
						self.logger.error("Sock PID {0} can not access Internet".format(self.pid))
						# update sock status is False
						return False
				else:
					self.logger.error("Error, can not open new sock")
					# update sock status is False
					self.updateDieSock(sockInfo["id"])
					# get new sock
					return False
			else:
				self.logger.error("Not found any sock, please add")
				return False
		else:
			# Can not close sock, error, exit
			self.logger.error("Error, can not close sock, exit now!")
			return False
	def checkInternet(self):
		session = requesocks.session()
		session.proxies = {'http': 'socks5://localhost:{0}'.format(self.sockPort), 'https': 'socks5://localhost:{0}'.format(self.sockPort)}
		response = session.get('http://ip.42.pl/raw')
		if(int(response.status_code) == 200):
			return True
		else:
			return False
	def selectSock(self):
		re 								=	self.db.get_one_row("socks","status","True","lastcheck")
		if(len(re) == 1):
			# Found one, ok
			data						=	{}
			row 						=	re[0]
			data["id"]					=	row[0]
			data["ip"]					=	row[1]
			data["username"]			=	row[2]
			data["password"]			=	row[3]
			return data
		else:
			return None
	def updateDieSock(self, id):
		# Update status and last check
		self.db.update_row("socks","id",id,"status","False")
		self.logger.debug("Updated socks id {0} staus to  False".format(id))
		self.db.update_row("socks","id",id,"lastcheck",time.time())