#coding:utf-8  
import time
import pymysql

mf=open("key.txt","r")
nr=mf.readlines()
db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
cursor = db.cursor()
cursor.execute( "select * from app_card WHERE card_id>=0;")
newId = len(cursor.fetchall())
price=int(nr[0].strip())
isFirst=True
for lines in nr:
	if isFirst:
		isFirst=False
	else:
		number=lines.strip().split(" ")[0]
		password=lines.strip().split(" ")[1]
		date=time.strftime("%Y-%m-%d", time.localtime())
		sql='''INSERT INTO app_card(
			card_id,card_number,card_passwd,card_price,card_submission_date)
			VALUES(
			{},"{}","{}",{},'{}');
			'''.format(newId,number,password,price,date)
		cursor.execute(sql)
		newId+=1