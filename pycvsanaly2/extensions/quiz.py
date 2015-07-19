#coding:utf-8
import os
import sys
import MySQLdb
# 进入Mysql,在数据库voldemort中,表格pathces中,属性patch中的数据进行分割
# 设置变量对遍历的数据进行计数
# 将计算的数据存入mysql中    python基础教程Ｐ237 

#连接voldemort数据库
try:
    connVolde = MySQLdb.connect(host='localhost',user='root',passwd='xybsnny',db='voldemort')
except Exception, e:
    print e
    sys.exit()
#获得voldemort的游标
curVolde=connVolde.cursor()

#连接Mysql
try:
    connXyb = MySQLdb.connect(host='localhost',user='root',passwd='xybsnny',db='xyb')
except Exception, e:
    print e
    sys.exit()
#获得xyb的游标
curXyb = connXyb.cursor()

sql3="create table if not exists quiz(id int(10), name varchar(50))"
try:
    curXyb.execute(sql3)
except Exception, e:
    print e
    
InFileId = input("Please input your file_id: ")          
InCommitId = input("Please input your commit_id: ")
print InFileId,InCommitId
sql4="insert into quiz values(1,'zhangsan')"
sql5="insert into quiz values(2,'lisi')"
try:
    curXyb.execute(sql4)
    curXyb.execute(sql5)
except Exception, e:
    print e
print 3
curXyb.execute("select * from quiz limit 5")
wholeRecord = curXyb.fetchall()    #返回一定数量的记录
print len(wholeRecord)
curXyb.execute("delete from quiz where id=1")
#curXyb.execute("alter table quiz add column age int(10)")
curXyb.execute("update quiz set age=21 where id = 2")
wholeRecord=curXyb.fetchall() 
#for whole in wholeRecord:
#    print whole
#whole = wholeRecord[2]
#whole = whole[1]
#myString = "ang"
#hasString = False
#t= False
#if myString in whole:
#    hasString = True
#    t=True
#if ((hasString == True)
#    and(t==True)):
#    print "hasTheString"
#else:
#    print "notHasTheString"

#sql1="set @i=1"
#sql2="delete from quiz where id=@i"
#try:
#    curXyb.execute(sql1)
#    curXyb.execute(sql2)
#except Exception, e:
#    print e
#向hunk_blames中添加属性hunk_id
sql1="alter table hunk_blames add column search_id int(10)"
try:
    curVolde.execute(sql1)
except Exception,e:
    print e
connVolde.commit()       
#修改提交    
connXyb.commit()
#连接关闭
connXyb.close()
connVolde.close()