class Module:
	def __init__(self, logger):
		self.logger			=	logger
		self.logger.info("Loaded Module")
	
def init(logger):
	module 					=	Module(logger)
# Show help
def showHelp():
	global tmp
	tmp = "bbbbbbbbb"
# Main to start module
def run():
	print("test")