#coding:utf-8
import sys
import MySQLdb
import string
import datetime
#连接voldemort数据库
try:
    connVolde = MySQLdb.connect(host='localhost',user='root',passwd='xybsnny',db='test')
except Exception, e:
    print e
    sys.exit()
#获得voldemort的游标
curVolde=connVolde.cursor()

#连接xyb数据库
try:
    connXyb = MySQLdb.connect(host='localhost',user='root',passwd='xybsnny',db='xyb2')
except Exception, e:
    print e
    sys.exit()
#获得xyb的游标
curXyb = connXyb.cursor()

#向hunk_blames中添加属性hunk_id
sql1="alter table hunk_blames add column search_id int(10)"
try:
    curVolde.execute(sql1)
except Exception,e:
    print e
connVolde.commit()    

#输入要查找的InFieldId和InCommitId 
#LeftTime = input("Please input the bug's start time: ")          
#RightTime = input("Please input the bug's end time: ")
LeftTime = "2015-05-19 10:13:45"
RightTime = "2015-05-19 10:13:45"
datetime.datetime.strptime(LeftTime, "%Y-%m-%d %H:%M:%S").date()
datetime.datetime.strptime(RightTime, "%Y-%m-%d %H:%M:%S").date()


sql2="select * from scmlog where commit_date between "'%s'" and "'%s'""
try:
    curVolde.execute(sql2,[LeftTime,RightTime])
except Exception,e:
    print e
scmlogWholeRecord = curVolde.fetchall() 
for scmlogOneRecord in scmlogWholeRecord:
    #print scmlogOneRecord
    scmlogId = scmlogOneRecord[0]
    sql3="select * from hunks where commit_id = '%s'"
    try:
        curVolde.execute(sql3,scmlogId)
    except Exception,e:
        print e
    hunksWholeRecord = curVolde.fetchall()
    for hunksOneRecord in hunksWholeRecord:                          #hunks中id等于hunk_blames中hunk_id
        print hunksOneRecord
        find = False                                                 #在hunk_blame中搜索出匹配的id                            
        hunksId = hunksOneRecord[0]
        sql4="select * from hunk_blames"
        try:
            curVolde.execute(sql4)
        except Exception,e:
            print e
        hunk_blamesWholeRecord = curVolde.fetchall()
        for hunk_blamesOneRecord in hunk_blamesWholeRecord:
            if(hunksId==hunk_blamesOneRecord[1]):
                bug_commit_id = hunk_blamesOneRecord[2]
                find = True
                break
        if(find==False):                                           #本次记录找不到，跳过
            continue
    
        sql5="select * from changeHunk where commit_id = '%s' and file_id = '%s'"       #找出changeHunk中对应的hunk_id
        try:
            curXyb.execute(sql5,[bug_commit_id,hunksOneRecord[1]])
        except Exception,e:
            print e
        changeHunkWholeRecord = curXyb.fetchall()
        SearchProgramLine = hunksOneRecord[3]                            #需要查找的缺陷代码行数
        SearchResultHunkId = False
        for changeHunkOneRecord in changeHunkWholeRecord:
            if( (SearchProgramLine>changeHunkOneRecord[5])
                and(SearchProgramLine<changeHunkOneRecord[5]+changeHunkOneRecord[6])):
                    SearchResultBool = True                                  #找到缺陷代码行的hunk_id
            if(SearchResultBool == True): 
                    SearchResultHunkId = changeHunkOneRecord[0]             
                    print "已搜索出缺陷代码引入的hunk_id: ",SearchResultHunkId
                    break
            
        SearchHunkBlamesHunkId = hunk_blamesOneRecord[1]                     #将搜索出的hunk_id添加入hunk_blames表中
        sql6="update hunk_blames set search_id='%s' where hunk_id='%s'"
        try:
            curVolde.execute(sql6,[SearchResultHunkId,SearchHunkBlamesHunkId])
        except Exception,e:
            print e 
        connVolde.commit()
    
        sql7="select * from hunk_blames where hunk_id = '%s'"               #输出结果的记录
        try:
            curVolde.execute(sql7,[SearchHunkBlamesHunkId])
        except Exception,e:
            print e
        Result = curVolde.fetchall()
        print "hunk_blames中对应的记录为:",Result  
        print  
print "查找结束"  
#连接关闭
connXyb.close()
connVolde.close()            
