#coding:utf-8  
import pymysql

mf=open("updatestock.txt","r")
nr=mf.readlines()
db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
cursor = db.cursor()
for lines in nr:
	lines=lines.strip().split(",")
	title=lines[0].split("-")[1]
	stock=int(lines[1].split("-")[1])
	sql='''UPDATE app_stock SET stock_number={} WHERE stock_name="{}";'''.format(stock,title)
	cursor.execute(sql)

	