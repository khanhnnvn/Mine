#!/usr/bin/python
import logging, datetime, os, subprocess, time, requesocks
class sockD:
	def __init__(self, db, logger, sockPort):
		self.db 						=		db
		self.logger 					=		logger
		self.sockPort 					=		sockPort
		self.sockTimeOut 				=		10													# 10
		self.closePort 					=		True
		self.lastIPSock 				=		""
		self.sshCmd 					=		"sshpass -p {0} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no {1}@{2} -D 0.0.0.0:{3} "
		self.netstatCmd 				=		"netstat -luntp 2>/dev/null | grep 0.0.0.0:{0} | awk '{{print $7}}' | cut -d/ -f1"
		self.netstatCmdCount 			=		"netstat -luntp 2>/dev/null | grep 0.0.0.0:{0} | awk '{{print $7}}' | cut -d/ -f1 | wc -l"
		self.killProcessCmd 			=		"kill -9 {0}"
	def checkOpenPort(self):
		# First, count 
		cmd 							=		self.netstatCmdCount.format(self.sockPort)
		count							= 		os.popen(cmd).read()
		try:
			countN 						=		int(count)
			if(countN > 0):
				# Port open
				cmd 					=		self.netstatCmd.format(self.sockPort)
				re 						= 		os.popen(cmd).read()
				try:
					pid 				=		int(re)
					self.logger.debug("Pid is {0}".format(pid))
					self.pid 			=		pid
				except Exception, e:
					self.logger.debug("Can not get PID, may be port listen by root")
					# self.closePort 			=	False
				return True
			else:
				# Port close
				# self.logger.debug("Port is not listen")
				return False
		except Exception, e:
			self.logger.debug("Unknow Exception, please check")
	def closeSock(self):
		if(self.checkOpenPort()):
			# Check port close
			if(self.closePort == False):
				# True is can not close
				self.logger.debug("Can not close port")
				return False
			else:
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
			self.logger.debug("Port {0} is not listen, don`t need close".format(self.sockPort))
			return True
	def getSock(self):
		if(self.closeSock()):
			# closeSock ok, open sock
			sockInfo 					=	self.selectSock()
			if(sockInfo is not None):
				self.logger.debug("Goted sock info:")
				self.logger.debug(sockInfo)
				cmd 						=	self.sshCmd.format(sockInfo["password"], sockInfo["username"], sockInfo["ip"], self.sockPort)
				devnull 					= 	open(os.devnull, 'wb') 
				process 					= 	subprocess.Popen(cmd, shell=True, stdout=devnull, stderr=devnull)
				#time.sleep(self.sockTimeOut)
				#Edit to count per second
				for i in range(0, self.sockTimeOut):
					time.sleep(1)
					if(self.checkOpenPort()):
						break	
				if(self.checkOpenPort()):

					# Open sock ok
					self.logger.info("Open new sock with PID: {0}".format(self.pid))
					
					# Check Internet
					if(self.checkInternet(sockInfo["id"])):
						self.logger.debug("Sock PID {0} access Internet OK".format(self.pid))
						# update lastcheck
						timeNow 						=	time.time()
						self.db.update_row("socks","id",sockInfo["id"],"lastcheck",timeNow)
						self.logger.debug("Updated socks id {0} lastcheck to  {1}".format(sockInfo["id"],timeNow))
						return True
					else:
						self.logger.error("Sock PID {0} can not access Internet".format(self.pid))
						# update sock status is False
						self.updateDieSock(sockInfo["id"])
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
	def checkInternet(self, id):
		session = requesocks.session()
		session.proxies = {'http': 'socks5://localhost:{0}'.format(self.sockPort), 'https': 'socks5://localhost:{0}'.format(self.sockPort)}
		try:
			startTime					=	time.time()
			response = session.get('http://ip.42.pl/raw')
			if(int(response.status_code) == 200):
				if(self.lastIPSock 		!=	response.text):
					# New sock
					self.lastIPSock 		=	response.text
					doneTime 				=	time.time()
					# Update response time
					time2response 			=	doneTime - startTime
					self.db.update_row("socks","id",id,"time2response",time2response)
					self.logger.debug("Request time of id {0} :  {1}".format(id,time2response))
					return True
				else:
					self.logger.error("Sock not change")
					return False
			else:
				return False
		except Exception, e:
			return False
		
	def selectSock(self):
		re 								=	self.db.get_one_row("socks","status","True","lastcheck")
		# re 								=	self.db.get_one_row("socks","id",95,"lastcheck")
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
		timeNow 						=	time.time()
		self.db.update_row("socks","id",id,"lastcheck",timeNow)
		self.logger.debug("Updated socks id {0} lastcheck to  {1}".format(id,timeNow))
