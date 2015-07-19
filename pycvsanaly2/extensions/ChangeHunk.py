#coding:utf-8
import sys
import MySQLdb
import string
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

#连接xyb数据库
try:
    connXyb = MySQLdb.connect(host='localhost',user='root',passwd='xybsnny',db='xyb')
except Exception, e:
    print e
    sys.exit()
#获得xyb的游标
curXyb = connXyb.cursor()
#创建changeHunk表格
sql1='''                        
    create table if not exists changeHunk(
    hunk_id           int(10),
    commit_id         int(10),
    file_id           int(10),
    old_start_line    int(10),
    old_length        int(10),
    new_start_line    int(10),
    new_length        int(10),
    change_content    longtext
    )
'''        
try:
    curXyb.execute(sql1)
except Exception, e:
    print e

sql2="select * from patches"
try:
    curVolde.execute(sql2)
except Exception, e:
    print e
wholeRecord = curVolde.fetchall()    #返回一定数量的记录
hunk_id = 1
for j in range(len(wholeRecord)):
    traPart = wholeRecord[j]             #返回要遍历的字符串
    #print traPart
    print j
    traCommit_id = traPart[1]
    #print traCommit_id
    traFile_id = traPart[2]
    #print traFile_id
    traPart = traPart[3]
    #print traPart
    find = False
    
    for i in range(len(traPart)):      #开始遍历
        old_start_line=0
        old_length=0
        new_start_line=0
        new_length=0
        change_content=""

        if(traPart[i]=='@')and(traPart[i+1]=='@')and(traPart[i+3]=='-')and(str.isdigit(traPart[i+4])==True)and(traPart[i+5]!='.'):
            find = True
            
            haveLeft = False
            haveRight = False
            index1 = i
            index2 = i
            index3 = i
            index4 = i
            while(traPart[index1]!='-'):
                index1 = index1+1   
            #print index1,'@'    
            while(traPart[index2]!='+'):
                index2 = index2+1  
            #print index2,'@@'
            while(index1<index2):
                if(traPart[index1]==','):
                    haveLeft=True
                index1 = index1+1
            #print haveLeft,"haveLeft"
            if(haveLeft==False):
                continue                                #judge -0 +0,3
            
            while(traPart[index3]!='+'):
                index3 = index3+1 
            #print index3,"&"
            index4 = index3
            while(traPart[index4]!='@'):
                index4 = index4+1
            #print index4,"&&"
            while(index3<index4):
                if(traPart[index3]==','):
                    haveRight=True
                index3 = index3+1
            #print haveRight,"haveRight"
            if(haveRight==False):
                continue                                #judge -0,3 +0
            #print "****"
            #print i
            #print traCommit_id
            #print traFile_id
            he=0
            start=0
            end=0
        
            head=i
            while(traPart[head]!='-'):
                head=head+1
            #if(traPart[head+2]!=','):
            #    continue
            start=head+1
            while(traPart[head]!=','):
                head=head+1
            end=head-1
            while(start<=end):
                s=traPart[start]
                he=he*10+ string.atoi(s,10)
                start=start+1
            old_start_line=he                        #获得旧的开始行数
            #print old_start_line
            he=0

            head=end
            start=head+2
            while(traPart[head]!='+'):
                head=head+1
            #if(traPart[head+2]!=','):
            #    continue
            end=head-2
            while(start<=end):
                s=traPart[start]
                he=he*10+ string.atoi(s,10)
                start=start+1
            old_length=he                           #获得旧的行数
            he=0
        
            head=end
            start=head+3
            while(traPart[head]!=','):
                head=head+1
            end=head-1
            while(start<=end):
                s=traPart[start]
                he=he*10+ string.atoi(s,10)
                start=start+1
            new_start_line=he                           #获得新的开始行数
            he=0
        
            head=end
            start=head+2
            while(traPart[head]!='@'):
                head=head+1
            end=head-2
            while(start<=end):
                s=traPart[start]
                he=he*10+ string.atoi(s,10)
                start=start+1
            new_length=he                           #获得新的行数
            he=0
        
            #print traCommit_id
            #print traFile_id
            #print old_start_line
            #print old_length
            #print new_start_line
            #print new_length

            head=end+4
            start=head
            while((traPart[head]!='@')and(head<len(traPart)-1)):
                head=head+1
            end=head
            change_content=traPart[start:end]      #获得修改部分
            #print change_content                 
        
            sql="insert into changeHunk values('%s','%s','%s','%s','%s','%s','%s',"'%s'")"
            try:
                curXyb.execute(sql,[hunk_id,traCommit_id,traFile_id,old_start_line,old_length,new_start_line,new_length,change_content])
                print hunk_id,'*'
                hunk_id = hunk_id +1
                #print change_content
            except Exception, e:
                print e                           #将遍历的数据插入数据库
            #修改提交    
            connXyb.commit()     
    if(find==False):
        continue
                   
#连接关闭
connXyb.close()
connVolde.close()