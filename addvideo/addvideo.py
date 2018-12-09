#coding:utf-8  
import time
import pymysql

mf=open("video.txt","r")
nr=mf.readlines()
db = pymysql.connect("210.9.30.6","app","WEgVsnNuWhlUwVs","app")
cursor = db.cursor()
cursor.execute( "select * from app_video WHERE video_id>=0;")
newId = len(cursor.fetchall())
for lines in nr:
	lines=lines.strip().split(",")
	title=lines[0].split("-")[1]
	url=lines[1].split("-")[1]
	imageurl=lines[2].split("-")[1]
	date=time.strftime("%Y-%m-%d", time.localtime())
	sql='''INSERT INTO app_video(
		video_id,video_name,video_url,video_image_url,video_submission_date)
		VALUES(
		{},"{}","{}","{}",'{}');
		'''.format(newId,title,url,imageurl,date)
	cursor.execute(sql)
	newId+=1

	
