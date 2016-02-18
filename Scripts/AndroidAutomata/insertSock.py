from SQLite.sqlite import SQLitedatabase
import geoip2.database
import logging, time

# Setup log
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(filename='insertSock.log',level=logging.DEBUG, format=FORMAT)
# Connect geoIP
reader = geoip2.database.Reader('/home/namhb/Downloads/GeoLite2-City.mmdb')
# Connect
db 		=		SQLitedatabase("appDB")

# Check exits
def checkIPExits(db, ip, username, password):
	condition		=	{}
	condition["ip"] =	ip
	condition["username"] =	username
	condition["password"] =	password
	re 				=	db.get_row2("socks",condition)
	if(len(re) > 0):
		return True
	else:
		return False
# Insert
def insertSock(db, ip, username, password, port=22):
	data			=	{}
	if(checkIPExits(db, ip, username, password)):
		logging.error("IP {0} is exits".format(ip))
	else:
		data["ip"] 		=	ip
		data["username"]=	username
		data["password"]=	password
		data["port"]	=	port
		data["status"]	=	True # Default is true
		data["lastcheck"] = 0 
		try:
			response = reader.city(data["ip"])
			data["country"]	=	response.country.iso_code
			data["city"] 	=	response.city.name
		except Exception, e:
			logging.error("Error while insert sock")
		if(data.has_key("country")):	
			logging.debug("Insert to database:")
			logging.debug(data)
			# Start insert
			db.insert_table_spec("socks",data)

with open('sock1.txt') as f:
	lines 				= 	f.readlines()
for line in lines:
	item 				= 	line.split("|")
	ip 					= 	item[0]
	username 			= 	item[1]
	password			= 	item[2]
	insertSock(db, ip, username, password)