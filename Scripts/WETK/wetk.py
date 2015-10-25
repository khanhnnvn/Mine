#author: namhb
import sys, time, requests, os, logging, argparse

'''
How to use:
'''
######---------------------------------------------#####
######-------------- WEToolKit class ---- ---------#####
class WEToolKit:
	def __init__(self):
		#Const
		self.dirPath		=		os.path.dirname(__file__) 					# relative directory path
		self.filePath		=		os.path.abspath(__file__) 					# absolute file path
		self.fileName		=		os.path.basename(__file__) 					# the file name only
		self.debug			=		False										# default disable debug
		self.version 		=		"0.0.1a"									# TK version
		#Variables
		self.getArument()
		#Preparing, (Get all agrument, log config)

		#Print info, include: flleName
	def printHelp(self):
		print("Start")
	def getArument(self):
		parser 				= 		argparse.ArgumentParser(description="WETK - Web Exploit ToolKit - Version {0}".format(self.version))
		#Enable debug
		parser.add_argument(
			'-d',
			'--debug',
			help 			=		'enable/disable debug'
			)
		#Show version
		parser.add_argument(
			'-v',
			'--version',
			help 			=		'WETK version',
			action			=		'store_true'
			)

		self.args = parser.parse_args()
	def logConfig(self):
		print("Start")




######---------------------------------------------#####


def main():
	tk = WEToolKit()


if __name__ == "__main__":
	main()


