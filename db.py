#coding=utf-8
import sqlite3

class Member:
    def __init__(self, m):  # pid = 0, name = "lazy", phone = '', email = ''
        pid, name, phone, email = m
        self.pid = pid
        self.name = name
        self.phone = phone
        self.email = email

    def getIcon(self):
        iconid = int(self.pid) % 4
        return './head/' + str(iconid) + '.png'


class MemberDB:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cu = self.conn.cursor()
        self.memberList = []
        self.readMember()

    def readMember(self):
        self.memberList = []
        self.cu.execute("select pid, name, phone, email from member")
        for row in self.cu:
            print row
            m = Member(row)
            self.memberList.append(m)

    def addMember(self, member):
        try:
            data = member.pid, member.name, member.phone, member.email
            self.cu.execute("INSERT INTO member (pid,name,phone,email) VALUES (?, ?, ?, ?)", data)
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True

    def delMember(self, pid):
        try:
            self.cu.execute("DELETE FROM member WHERE pid = %d" % (pid))
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True


    def searchMember(self, tags):
        self.memberList = []


"""
conn.execute('''CREATE TABLE member
    (pid int primary key NOT NULL,
    name text NOT NULL,
    phone char(11), email text,
    school text, dept text, stunum char(20),
    field text, skill text,
    trend text, locate text,
    GM text, TM text, MM text, HR text, PM text, OT text);''')
ALTER TABLE table_name ADD column_name datatype
DROP TABLE member;
INSERT INTO member (pid,name,phone,email) VALUES (10003, '王五','12309877890','example@126.com')
UPDATE member set  email = 'example@163.com' where pid=10000

print "Table created successfully"
print "Records created successfully"
print(cursor.fetchall())
conn.commit()
print "Total number of rows updated :", conn.total_changes
print "Operation done successfully"
"""


"""
conn.execute("")
conn.commit()
cursor = conn.execute("SELECT * FROM member ")
for m in cursor:
    print m
"""
conn = sqlite3.connect('test.db')
mdb = MemberDB()
m = Member((10005,"lazy","18877890988","example@tom.com"))
#mdb.addMember(m)
mdb.readMember()


conn.close()