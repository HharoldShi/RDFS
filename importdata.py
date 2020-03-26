import os
import subprocess
import sys
import re
import mysql.connector
from mysql.connector import Error

regf = re.compile("^d[rwx-]{3} [0-9]+ [A-Za-z0-9]+ [A-Za-z0-9]+ [0-9]+ [0-9]+[-][0-9]+[-][0-9]+ [0-9]+[:][0-9]+ [^/]+$")
regdir = re.compile("^d[rwx-]{3} [0-9]+ [A-Za-z0-9]+ [A-Za-z0-9]+ [0-9]+ [0-9]+[-][0-9]+[-][0-9]+ [0-9]+[:][0-9]+ [^/]+[/]$")
regname = re.compile()

# DirTree = dict()

# class Directory:
    # def __init__(self, name='', parent='', dson=[], fson=[], path='')
        # self.parent = parent
        # self.fson = fson
        # self.dson = dson
        # self.name = name
        # self.path = path

       

       
def scanDir():
    for (root,dirs,files) in os.walk(os.getcwd(), topdown=True): 
        result = subprocess.run(['ls', '-lp'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        
        for line in result.split("\n"):
            
            if regf.match(line):           
                ownerp,groupp,otherp,hlink,owner,group,date,time,name = getInfo(line)
                path = root+'/'+name
                insertInfo(ownerp,groupp,otherp,hlink,owner,group,date,time,name,path)
                insertBLOB(path)
                
            elif regdir.match(line):
                ownerp,groupp,otherp,hlink,owner,group,date,time,name = getInfo(line)
                path = root+'/'+name
                insertInfo(ownerp,groupp,otherp,hlink,owner,group,date,time,name,path)
                
            
            else:
                pass

    

def getInfo(line):
    re_obj = re.match("^d(?P<ownerp>([rwx-]{3}))(?P<groupp>([rwx-]{3}))(?P<otherp>([rwx-]{3})) (?P<hlink>([0-9]+)) (?P<owner>([A-Za-z0-9]+)) (?P<group>([A-Za-z0-9]+)) (?P<size>([0-9]+)) (?P<date>([0-9]+[-][0-9]+[-][0-9]+)) (?P<time>([0-9]+[:][0-9]+)) (?P<name>([^/]+))", line)
    ownerp = re_obj.group("ownerp")
    groupp = re_obj.group("groupp")
    otherp = re_obj.group("otherp")
    hlink = re_obj.group("hlink")
    owner = re_obj.group("owner")
    group = re_obj.group("group")
    date = re_obj.group("date")
    time = re_obj.group("time")
    name = re_obj.group("name")   
    
    return ownerp,groupp,otherp,hlink,owner,group,date,time,name
    
    
def insertInfo(ownerp,groupp,otherp,hlink,owner,group,date,time,name,path):
    connection = mysql.connector.connect(host='localhost',
                                         database='project',
                                         user='root',
                                         password='ece651db')
    cursor = connection.cursor()
    sql_insert_info_query = """ INSERT INTO FileInfo
                      (ownerPermission, groupUserPermission, otherUserPermission, numHardLinks,
                      owner, `group`, `size`, lastModified, lastModifiedTime, name, `path`) 
                      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"""
    insert_info_tuple = (ownerp,groupp,otherp,hlink,owner,group,date,time,name,path)
    cursor.execute(sql_insert_info_query, insert_info_tuple)
    connection.commit()
    return

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insertBLOB(path):
    connection = mysql.connector.connect(host='localhost',
                                         database='project',
                                         user='root',
                                         password='ece651db')

    cursor = connection.cursor()
    sql_insert_blob_query = """ INSERT INTO FileBlobs
                          (path, file) VALUES (%s,%s)"""

    buffer = convertToBinaryData(path)

    # Convert data into tuple format
    insert_blob_tuple = (path, buffer)
    result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    connection.commit()
    return


def main():
    scanDir()
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        
if __name__ == '__main__':
    main()