#!/usr/bin/python
import sqlite3, sys
class SQLitedatabase:
	'Database sqlite3 class'
	def __init__(self, name):
		self.name = name
		self.create_database()
	def create_database(self):
		self.conn = sqlite3.connect(self.name)
		self.c = self.conn.cursor()
	def query(self, query):
		try:   
			r = self.c.execute(query)
			self.conn.commit()
			return r
		except sqlite3.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)
	def query2(self, query):
		try:   
			self.c.execute(query)
			r = self.c.fetchall()
			return r
		except sqlite3.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)
	def check_database_exits(self,table_name):
		re = self.query2("SELECT name FROM sqlite_master WHERE type='table' AND name='"+table_name+"'")
		if (len(re) > 0):
			return True
		else:
			return False
	def insert_table(self,table_name,data):
		sql = "INSERT into "+table_name+" values ("		   
		for item in data:
			if type(item) == int:
				sql = sql + str(item) + ","
			else:
				if type(item) == str:
					sql = sql + "'" + item + "'"+ ","
		sql = sql[:-1] + ")"
		self.query(sql)
	def insert_table_spec(self,table_name,data):
		str1 	=	table_name+" ("
		str2 	=	""
		for key in data.keys():
			item = data[key]
			str1 = str1 + key + ","
			if type(item) == int:
				str2 = str2 + str(item) + ","
			elif type(item) == str:
				str2 = str2 + "'" + item + "'"+ ","
			elif type(item) == bool:
				str2 = str2 + "'" + str(item) + "'"  + ","
			else:
				str2 = str2 + "'" + str(item) + "'"+ ","
		str1 = str1[:-1] + ")"
		str2 = str2[:-1] + ")"
		sql = "INSERT into "+str1+" values (" + str2
		self.query(sql)
	def get_row(self,table_name,key,value):
		if type(value) == int:
			sql = "SELECT * FROM "+table_name + " WHERE "+key+"="+str(value)
		else:
			if type(value) == str:
				sql = "SELECT * FROM "+table_name + " WHERE "+key+"='"+value+"'"
		re = self.query2(sql)
		return re
	def get_row2(self,table_name,data):
		sql = "SELECT * FROM "+table_name + " WHERE 1=1 "
		for key in data.keys():
			item = data[key]
			if type(item) == int:
				sql = sql+" AND "+ key+"="+str(item)+" "
			else:
				if type(item) == str:
					sql = sql+" AND "+key+"='"+item+"'" +" "
		re = self.query2(sql)
		return re
	def get_one_row(self,table_name,key,value,order):
		if type(value) == int:
			sql = "SELECT * FROM "+table_name + " WHERE "+key+"="+str(value)
		else:
			if type(value) == str:
				sql = "SELECT * FROM "+table_name + " WHERE "+key+"='"+value+"'"
		sql = sql + " order by "+order+" limit 0,1"
		re = self.query2(sql)
		return re
	def delete_row(self,table_name,key,value):
		if type(value) == int:
			sql = "DELETE FROM "+table_name + " WHERE "+key+"="+str(value)
		else:
			if type(value) == str:
				sql = "DELETE FROM "+table_name + " WHERE "+key+"='"+value+"'"
		db.query(sql)
	def update_row(self,table_name,key,kvalue,nkey, nvalue):
		if type(nvalue) == int:
			sql = "UPDATE "+table_name + " SET " + nkey + "=" + str(nvalue)
			if type(kvalue) == int:
				sql = sql + " WHERE " + key + "=" + str(kvalue)
			else:
				if type(kvalue) == str:
					sql = sql + " WHERE " + key + "='" + kvalue + "'"
		elif type(nvalue) == str:
			sql = "UPDATE "+table_name + " SET " + nkey + "='" + nvalue + "'"
			if type(kvalue) == int:
				sql = sql + " WHERE " + key + "=" + str(kvalue)
			if type(kvalue) == str:
				sql = sql + " WHERE " + key + "='" + kvalue + "'"
		else:
			print(type(nvalue))
		self.query(sql)

