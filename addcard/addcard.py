#coding:utf-8  
import time
import pymysql

mf=open("card.txt","r")
nr=mf.readlines()[4:-1]
db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
cursor = db.cursor()
cursor.execute( "select * from app_netkey WHERE netkey_id>=0;")
newId = len(cursor.fetchall())
isFirst=True
mf=open("pay_card.txt","w")
for lines in nr:
	if isFirst:
		isFirst=False
	else:
		number=lines.strip().split()[1]
		price=lines.strip().split()[3]
		date=time.strftime("%Y-%m-%d", time.localtime())
		sql='''INSERT INTO app_netkey(
			netkey_id,netkey_number,netkey_price,netkey_submission_date)
			VALUES(
			{},"{}",'{}','{}');
			'''.format(newId,number,price,date)
		cursor.execute(sql)
		mf.write(number+"\n")
		newId+=1