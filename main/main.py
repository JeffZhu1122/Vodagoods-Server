#coding:utf-8  
import smtplib  
from email.mime.text import MIMEText
from email.utils import formataddr
import pymysql
import time
import json
from bottle import route, run ,redirect,request,default_app
from beaker.middleware import SessionMiddleware


#设置session参数
session_opts = {
    'session.type':'file',                   # 以文件的方式保存session
    'session.cookei_expires':259200,       # session过期时间为3600秒
    'session.data_dir':'/tmp/sessions',  # session存放路径
    'sessioni.auto':True
    }
	
@route('/iflogin')
def iflogin():
	username = request.query.username[10:-2]
	s = request.environ.get('beaker.session') 
	ausername = s.get(username,username)  
	if not ausername:
		return json.dumps({"Result":"False"})
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	cursor.execute( '''select * from app_user WHERE user_name="{}";'''.format(username))
	data = cursor.fetchone()
	if data==None:
		return json.dumps({"Result":"False"})
	if data[6]!=None:
		groupin=data[6]
		cursor.execute( '''select group_name from app_group WHERE group_id={};'''.format(groupin))
		groupnamein=cursor.fetchone()[0]
	else:
		groupnamein="No Group"
	if data[8]!=None:
		teamin=data[8]
		cursor.execute( '''select team_name from app_team WHERE team_id={};'''.format(teamin))
		teamnamein=cursor.fetchone()[0]
	else:
		teamnamein="No Team"
	db.close()
	rtDic={"Result":"True","id":data[0],"username":data[1],"email":data[3],"phone":data[4],"fight":data[5],"date":str(data[7]),"groupname":groupnamein,"teamname":teamnamein,"wallet":data[9]}
	return json.dumps(rtDic)
	
def mail(my_user,username):
    ret=True
    try:
        my_sender='admin@vodagoods.com'
        msg=MIMEText('''亲爱的{}：\n\n恭喜您成功注册成为sng会员！'''.format(username),'plain','utf-8')
        msg['From']=formataddr(["sng admin",my_sender])   
        msg['To']=formataddr([my_user,my_user])   
        msg['Subject']='注册成功'
        server=smtplib.SMTP("210.9.30.6",25)  
        server.login("admin","admin")    
        server.sendmail(my_sender,my_user,str(msg))   
        server.quit()   
    except Exception:  
        ret=False

@route('/adduser')
def adduser():
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	cursor.execute( '''select * from app_user WHERE user_id>=0;''')
	userId = len(cursor.fetchall())
	username = request.query.username
	cursor.execute( '''select * from app_user WHERE user_name="{}";'''.format(username))
	email = request.query.email
	if len(cursor.fetchall())>0 or "@" not in email:
		return json.dumps({"Result":"False"})
	password = request.query.password	
	phone = request.query.phone
	date= time.strftime("%Y-%m-%d", time.localtime()) 
	sql='''INSERT INTO app_user(
		user_id,user_name,user_passwd,user_email,user_phone,user_fight,submission_date,wallet)
		VALUES(
		{},"{}","{}","{}","{}",{},'{}',{});
		'''.format(userId,username,password,email,phone,0,date,0)
	cursor.execute(sql)
	db.close()
	mail(email,username)
	return  json.dumps({"Result":"True"})

@route('/finduser')
def finduser():
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	username = request.query.username
	password = request.query.password
	cursor.execute( '''select * from app_user WHERE user_name="{}";'''.format(username))
	data = cursor.fetchone()
	if data==None:
		return json.dumps({"Result":"False"})
	if data[6]!=None:
		groupin=data[6]
		cursor.execute( '''select group_name from app_group WHERE group_id={};'''.format(groupin))
		groupnamein=cursor.fetchone()[0]
	else:
		groupnamein="No Group"
	if data[8]!=None:
		teamin=data[8]
		cursor.execute( '''select team_name from app_team WHERE team_id={};'''.format(teamin))
		teamnamein=cursor.fetchone()[0]
	else:
		teamnamein="No Team"
	db.close()
	if password==data[2]:
		rtDic={"Result":"True","id":data[0],"username":data[1],"email":data[3],"phone":data[4],"fight":data[5],"date":str(data[7]),"groupname":groupnamein,"teamname":teamnamein,"wallet":data[9]}
		if rtDic["Result"]=="True":
			s = request.environ.get('beaker.session')  
			s[username] = username
			s.save()
			return json.dumps(rtDic)
	else:
		return json.dumps({"Result":"False"})
	
@route('/addgroup')
def addgroup():
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	cursor.execute( '''select * from app_group WHERE group_id>=0;''')
	groupId = len(cursor.fetchall())
	groupname = request.query.groupname[10:-2]
	groupintro=request.query.groupintro[10:-2]
	ownerid = request.query.ownerid	
	cursor.execute( '''select * from app_group WHERE group_name="{}";'''.format(groupname))
	if len(cursor.fetchall())>0 or len(groupname)==0 or len(groupintro)==0:
		return json.dumps({"Result":"False2"})
	date= time.strftime("%Y-%m-%d", time.localtime()) 
	sql='''INSERT INTO app_group(
		group_id,group_name,group_fight,group_owner_id,group_max_mbr,group_now_mbr,group_submission_date,group_intro)
		VALUES(
		{},"{}",{},{},{},{},'{}',"{}");
		'''.format(groupId,groupname,0,ownerid,50,1,date,groupintro)
	cursor.execute(sql)
	cursor.execute('''UPDATE app_user SET user_group={} WHERE user_id={};'''.format(groupId,ownerid))
	db.close()
	return  json.dumps({"Result":"True"})

@route('/addteam')
def addteam():
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	cursor.execute( "select * from app_team WHERE team_id>=0;")
	teamId = len(cursor.fetchall())
	teamname = request.query.teamname[10:-2]
	teamintro=request.query.teamintro[10:-2]
	ownerid = request.query.ownerid	
	cursor.execute( '''select * from app_team WHERE team_name="{}";'''.format(teamname))
	if len(cursor.fetchall())>0 or len(teamname)==0 or len(teamintro)==0:
		return json.dumps({"Result":"False"})
	date= time.strftime("%Y-%m-%d", time.localtime()) 
	sql='''INSERT INTO app_team(
		team_id,team_name,team_type,team_fight,team_owner_id,team_max_mbr,team_now_mbr,team_submission_date,team_intro)
		VALUES(
		{},"{}",{},{},{},{},{},'{}',"{}");
		'''.format(teamId,teamname,0,0,ownerid,5,1,date,teamintro)
	cursor.execute(sql)
	cursor.execute('''UPDATE app_user SET user_team={} WHERE user_id={};'''.format(teamId,ownerid))
	db.close()
	return  json.dumps({"Result":"True"})
	
@route('/groupintro')
def groupintro():
	groupname = request.query.groupname
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	cursor.execute( '''select group_owner_id from app_group WHERE group_name="{}";'''.format(groupname))
	userId=cursor.fetchone()[0]
	cursor.execute( '''select group_intro from app_group WHERE group_name="{}";'''.format(groupname))
	nr=cursor.fetchone()[0]
	cursor.execute( '''select user_name from app_user WHERE user_id={};'''.format(userId))
	owner=cursor.fetchone()[0]
	cursor.execute( '''select group_id from app_group WHERE group_name="{}";'''.format(groupname))
	groupId=cursor.fetchone()[0]
	cursor.execute( '''select user_id from app_user WHERE user_group={};'''.format(groupId))
	allUserId=cursor.fetchall()
	userlist=[]
	for i in allUserId:
		userlist.append(i[0])
	cursor.execute( '''select group_now_mbr from app_group WHERE group_name="{}";'''.format(groupname))
	groupNow=cursor.fetchone()[0]
	cursor.execute( '''select group_max_mbr from app_group WHERE group_name="{}";'''.format(groupname))
	groupMax=cursor.fetchone()[0]
	db.close()
	return json.dumps({"intro":nr,"owner":owner,"member":"{}".format(userlist),"nowmeb":groupNow,"maxmeb":groupMax})

@route('/teamintro')
def teamintro():
	teamname = request.query.teamname
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	cursor.execute( '''select team_owner_id from app_team WHERE team_name="{}";'''.format(teamname))
	userId=cursor.fetchone()[0]
	cursor.execute( '''select team_intro from app_team WHERE team_name="{}";'''.format(teamname))
	nr=cursor.fetchone()[0]
	cursor.execute( '''select user_name from app_user WHERE user_id={};'''.format(userId))
	owner=cursor.fetchone()[0]
	cursor.execute( '''select team_id from app_team WHERE team_name="{}";'''.format(teamname))
	teamId=cursor.fetchone()[0]
	cursor.execute( '''select user_id from app_user WHERE user_team={};'''.format(teamId))
	allUserId=cursor.fetchall()
	userlist=[]
	for i in allUserId:
		userlist.append(i[0])
	cursor.execute( '''select team_now_mbr from app_team WHERE team_name="{}";'''.format(teamname))
	teamNow=cursor.fetchone()[0]
	cursor.execute( '''select team_max_mbr from app_team WHERE team_name="{}";'''.format(teamname))
	teamMax=cursor.fetchone()[0]
	db.close()
	return json.dumps({"intro":nr,"owner":owner,"member":"{}".format(userlist),"nowmeb":teamNow,"maxmeb":teamMax})
	
@route('/intogroup')
def intogroup():
	groupname = request.query.groupname[10:-2]
	username = request.query.username[9:-1]
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	cursor.execute( '''select group_now_mbr from app_group WHERE group_name="{}";'''.format(groupname))
	groupNow=cursor.fetchone()[0]
	cursor.execute( '''select group_max_mbr from app_group WHERE group_name="{}";'''.format(groupname))
	groupMax=cursor.fetchone()[0]
	if groupNow>=groupMax :
		return json.dumps({"Result":"False"})
	cursor.execute( '''select group_id from app_group WHERE group_name="{}";'''.format(groupname))
	groupId=cursor.fetchone()[0]
	cursor.execute('''UPDATE app_user SET user_group={} WHERE user_name="{}";'''.format(groupId,username))
	cursor.execute('''UPDATE app_group SET group_now_mbr={} WHERE group_name="{}";'''.format(groupNow+1,groupname))
	return  json.dumps({"Result":"True"})
	
@route('/intoteam')
def intoteam():
	teamname = request.query.teamname[10:-2]
	username = request.query.username[9:-1]
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	cursor.execute( '''select team_now_mbr from app_team WHERE team_name="{}";'''.format(teamname))
	teamNow=cursor.fetchone()[0]
	cursor.execute( '''select team_max_mbr from app_team WHERE team_name="{}";'''.format(teamname))
	teamMax=cursor.fetchone()[0]
	if groupNow>=groupMax :
		return json.dumps({"Result":"False"})
	cursor.execute( '''select team_id from app_team WHERE team_name="{}";'''.format(teamname))
	teamId=cursor.fetchone()[0]
	cursor.execute('''UPDATE app_user SET user_team={} WHERE user_name="{}";'''.format(teamId,username))
	cursor.execute('''UPDATE app_team SET team_now_mbr={} WHERE team_name="{}";'''.format(teamNow+1,teamname))
	return  json.dumps({"Result":"True"})

@route('/getvideo')
def videoUrl():	
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	cursor.execute( '''select * from app_video WHERE video_id>=0;''')
	allVideo=cursor.fetchall() 
	allBin=[]
	for i in range (len(allVideo)):
		allBin.append({})
		allBin[i]["title"]=allVideo[i][1]
		allBin[i]["url"]=allVideo[i][2]
		allBin[i]["thumbnail_pic_s"]=allVideo[i][3]
	return json.dumps({"result":{"data":allBin}})

@route('/getshop')
def shopUrl():
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	cursor.execute( '''select * from app_stock WHERE stock_id>=0;''')
	allStock=cursor.fetchall()
	allBin=[]
	for i in range (len(allStock)):
		allBin.append({})
		allBin[i]["title"]=allStock[i][1]
		allBin[i]["imageurl"]=allStock[i][2]
		allBin[i]["price"]=allStock[i][3]
		allBin[i]["stock"]=allStock[i][4]
	return json.dumps({"result":{"data":allBin}})
	
@route('/topup')
def topup():
	username = request.query.username[10:-2]
	password = request.query.password[10:-2]
	number = request.query.number[10:-2]
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	cursor.execute( '''select * from app_card WHERE card_number="{}";'''.format(number))
	data = cursor.fetchone()
	if data==None:
		return json.dumps({"Result":"False"})
	if password==data[2] and data[-1]==None:
		cursor.execute( '''select wallet from app_user WHERE user_name="{}";'''.format(username))
		wallet=cursor.fetchone()[0]
		cursor.execute('''UPDATE app_card SET card_used={} WHERE card_number="{}";'''.format(1,number))
		date= time.strftime("%Y-%m-%d", time.localtime()) 
		cursor.execute('''UPDATE app_card SET card_use_date='{}' WHERE card_number="{}";'''.format(date,number))
		cursor.execute('''UPDATE app_card SET card_user_name="{}" WHERE card_number="{}";'''.format(username,number))
		cursor.execute('''UPDATE app_user SET wallet={} WHERE user_name="{}";'''.format(wallet+int(data[3]),username))
		return json.dumps({"Result":"True","Price":data[3]})
	else:
		return json.dumps({"Result":"False"})
		
@route('/myorder')
def myorder():
	username = request.query.username[10:-2]
	db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
	cursor = db.cursor()
	cursor.execute( '''select * from app_order WHERE order_user_name="{}";'''.format(username))
	allStock=cursor.fetchall()
	allBin=[]
	for i in range (len(allStock)):
		allBin.append({})
		allBin[i]["title"]=allStock[i][3]
		allBin[i]["number"]=allStock[i][4]
		cursor.execute( '''select stock_price from app_stock WHERE stock_name="{}";'''.format(allStock[i][3]))
		price=cursor.fetchone()[0]
		allBin[i]["price"]=price
		allBin[i]["totalprice"]=str(int(price)*int(allStock[i][4]))
		allBin[i]["date"]=str(allStock[i][5])
	return json.dumps({"result":{"data":allBin}})
	
app = default_app()
app = SessionMiddleware(app, session_opts)
run(app=app,host='0.0.0.0', port=9090,debug=True)
