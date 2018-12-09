#coding:utf-8  
import time
import pymysql

mf=open("stock.txt","r")
nr=mf.readlines()
db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
cursor = db.cursor()
cursor.execute( "select * from app_stock WHERE stock_id>=0;")
newId = len(cursor.fetchall())
for lines in nr:
	lines=lines.strip().split(",")
	title=lines[0].split("-")[1]
	imageurl=lines[1].split("-")[1]
	stock=int(lines[2].split("-")[1])
	price=float(lines[3].split("-")[1])
	date=time.strftime("%Y-%m-%d", time.localtime())
	sql='''INSERT INTO app_stock(
		stock_id,stock_name,stock_image_url,stock_price,stock_number,stock_submission_date)
		VALUES(
		{},"{}","{}",'{}',{},'{}');
		'''.format(newId,title,imageurl,price,stock,date)
	cursor.execute(sql)
	newId+=1

	