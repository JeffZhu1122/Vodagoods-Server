#coding:utf-8  
import bottle
import time
import os
import tkinter as tk
from tkinter import messagebox
import pymysql
import smtplib  
from email.mime.text import MIMEText
from email.utils import formataddr

@bottle.route('/order')
def order():
	username = bottle.request.query.username[10:-2]
	price = bottle.request.query.price[10:-2]
	orderThing = bottle.request.query.orderthing[10:-2]
	orderNum = bottle.request.query.ordernum[10:-2]
	sitNum = bottle.request.query.sitnum[10:-2]
	ifpaied=bottle.request.query.ifpaied[10:-2]
	paymet=bottle.request.query.paymet[10:-2]
	if paymet=="wxpay":
		pass
	elif paymet=="alipay":
		pass
	ordertime=time.strftime("%Y-%m-%d", time.localtime()) 
	total=float(orderNum)*float(price)
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	ifcard=False
	if orderThing=="网吧充值卡":
		cursor.execute('''select user_email from app_user WHERE user_name="{}";'''.format(username))
		email=cursor.fetchone()[0]
		cursor.execute('''select netkey_number from app_netkey WHERE (netkey_sold is null) and (netkey_price='{}') limit 1;'''.format(price))
		cardnumber=cursor.fetchone()[0]
		sendcard(email,username,cardnumber)
		cursor.execute('''UPDATE app_netkey SET netkey_sold={} WHERE netkey_number="{}";'''.format(1,cardnumber))
		cursor.execute('''UPDATE app_netkey SET netkey_sold_date='{}' WHERE netkey_number="{}";'''.format(ordertime,cardnumber))
		cursor.execute('''UPDATE app_netkey SET netkey_sold_name="{}" WHERE netkey_number="{}";'''.format(username,cardnumber))
		cursor.execute( "select * from app_order WHERE order_id>=0;")
		newId = len(cursor.fetchall())
		cursor.execute('''select stock_number from app_stock WHERE stock_name="{}";'''.format(orderThing))
		inStock=cursor.fetchone()[0]
		cursor.execute('''UPDATE app_stock SET stock_number={} WHERE stock_name="{}";'''.format(int(inStock)-int(orderNum),orderThing))
		cursor.execute( '''select wallet from app_user WHERE user_name="{}";'''.format(username))
		wallet=cursor.fetchone()[0]
		cursor.execute( '''UPDATE app_user SET wallet='{}' WHERE user_name="{}";'''.format(float(wallet)-total,username))
		sql='''INSERT INTO app_order(
		order_id,order_user_name,order_user_seat,order_name,order_number,order_submission_date)
		VALUES(
		{},"{}","{}","{}",{},'{}');
		'''.format(newId,username,sitNum,orderThing,orderNum,ordertime)
		cursor.execute(sql)
	else:
		if ifpaied=="No":
			tkbox=tk.messagebox.askyesno("有新订单！","时间:"+ordertime+"\n座位:"+sitNum+"\n订单物品:"+orderThing+"\n是否需付款:"+ifpaied+"\n数量:"+orderNum+'\n是否送达？')
		else:
			tkbox=tk.messagebox.askyesno("有新订单！","时间:"+ordertime+"\n座位:"+sitNum+"\n订单物品:"+orderThing+"\n是否需付款:"+ifpaied+"\n数量:"+orderNum+"\n总价:"+str(total)+'\n是否送达？')
		if tkbox:
			cursor.execute( "select * from app_order WHERE order_id>=0;")
			newId = len(cursor.fetchall())
			cursor.execute('''select stock_number from app_stock WHERE stock_name="{}";'''.format(orderThing))
			inStock=cursor.fetchone()[0]
			cursor.execute('''UPDATE app_stock SET stock_number={} WHERE stock_name="{}";'''.format(int(inStock)-int(orderNum),orderThing))
			if ifpaied=="No":
				cursor.execute( '''select wallet from app_user WHERE user_name="{}";'''.format(username))
				wallet=cursor.fetchone()[0]
				cursor.execute( '''UPDATE app_user SET wallet='{}' WHERE user_name="{}";'''.format(float(wallet)-total,username))
			sql='''INSERT INTO app_order(
			order_id,order_user_name,order_user_seat,order_name,order_number,order_submission_date)
			VALUES(
			{},"{}","{}","{}",{},'{}');
			'''.format(newId,username,sitNum,orderThing,orderNum,ordertime)
			cursor.execute(sql)
	db.close()
		
def sendcard(my_user,username,number):
    ret=True
    try:
        my_sender='admin@vodagoods.com'
        msg=MIMEText('''亲爱的{}：\n\n感谢您的购买！\n您的充值卡号是  {}'''.format(username,number),'plain','utf-8')
        msg['From']=formataddr(["sng admin",my_sender])   
        msg['To']=formataddr([my_user,my_user])   
        msg['Subject']='购买成功'
        server=smtplib.SMTP("210.9.30.6",25)  
        server.login("admin","admin")    
        server.sendmail(my_sender,my_user,str(msg))   
        server.quit()   
    except Exception:  
        ret=False		
		
bottle.run(host='0.0.0.0', port=9191)