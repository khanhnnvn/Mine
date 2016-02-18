from SQLite.sqlite import SQLitedatabase
from SockChange.sockD import sockD
import logging, datetime


class AndroidAutomata(object):
	"""docstring for AndroidAutomata"""
	def __init__(self):
		self.dbConnect()
		self.sockD 	=	sockD(self.db)
		self.sock 	=	self.sockD.getSock()
		# self.sockD.selectSock()
	# Setup database
	def dbConnect(self):
		self.db 	=	SQLitedatabase("appDB")


def main():
	mainClass 		=	AndroidAutomata()

if __name__ == '__main__':
	main()