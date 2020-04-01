import os
import subprocess
import sys
import re
import mysql.connector
from mysql.connector import Error

# reg = re.compile("^[dbclnps-][rwx-]{9} [0-9]+ [A-Za-z0-9]+ [A-Za-z0-9]+ [0-9]+ [A-Za-z]{3} \s?[0-9]+ [0-9]+[:][0-9]+ .+$")
reg = re.compile("^(?P<type>([dbclnps-]))(?P<ownerp>([rwx-]{3}))(?P<groupp>([rwx-]{3}))(?P<otherp>([rwx-]{3}.?)) (?P<hlink>(\s*[0-9]+)) (?P<owner>(\s*[A-Za-z0-9]+)) (?P<group>(\s*[A-Za-z0-9]+)) (?P<size>(\s*[0-9]+)) (?P<date>(\s*[A-Za-z]{3} \s?[0-9]+)) (?P<time>([0-9]+[:][0-9]+)) (?P<name>(.+))$")

# DirTree = dict()
# class Directory:
    # def __init__(self, name='', parent='', dson=[], fson=[], path='')
        # self.parent = parent
        # self.fson = fson
        # self.dson = dson
        # self.name = name
        # self.path = path

       
def scanDir(connection, rootDir):
    for (root,dirs,files) in os.walk(rootDir, topdown=True):
        # print((root,dirs,files))
        result = subprocess.run(['ls', '-la', root], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # print(result)
        # print(result.split("\n")[1:-1])
        for line in result.split("\n")[1:-1]:
            # print(line)
            type, ownerp, groupp, otherp, hlink, owner, group, size, date, time, name = getInfo(line)
            insertInfo(connection, root, name, type, ownerp, groupp, otherp, hlink, owner, group, size, date, time)
            if type != "d":
                insertBLOB(connection, root, name)


def connectDB():
    connection = mysql.connector.connect(host='localhost',
                                         database='ece656project',
                                         user='root',
                                         password='ece651db',
                                         auth_plugin='mysql_native_password')
    return connection


def getInfo(line):
    re_obj = reg.match(line)
    type = re_obj.group("type")
    ownerp = re_obj.group("ownerp")
    groupp = re_obj.group("groupp")
    otherp = re_obj.group("otherp")
    hlink = int(re_obj.group("hlink"))
    owner = re_obj.group("owner")
    group = re_obj.group("group")
    size = int(re_obj.group("size"))
    date = re_obj.group("date")
    time = re_obj.group("time")
    name = re_obj.group("name")
    return type,ownerp,groupp,otherp,hlink,owner,group,size,date,time,name
    
    
def insertInfo(connection,parentdir,name,type,ownerp,groupp,otherp,hlink,owner,group,size,date,time):
    cursor = connection.cursor()
    # print(path)
    sql_insert_info_query = """ INSERT INTO FileInfo
                      (`parentdir`, `name`, `type`, ownerPermission, groupUserPermission, otherUserPermission, 
                      numHardLinks, owner, `group`, `size`, lastModifiedDate, lastModifiedTime) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    insert_info_tuple = (parentdir,name,type,ownerp,groupp,otherp,hlink,owner,group,size,date,time)
    cursor.execute(sql_insert_info_query, insert_info_tuple)
    connection.commit()
    cursor.close()
    return


def convertToBinaryData(path_to_file):
    # Convert digital data to binary format
    with open(path_to_file, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(connection, parentdir, name):
    cursor = connection.cursor()
    sql_insert_blob_query = """ INSERT INTO FileBlobs (`parentdir`, `name`, `fileContent`) VALUES (%s, %s, %s)"""
    path_to_file = parentdir + '/' + name
    buffer = convertToBinaryData(path_to_file)

    # Convert data into tuple format
    insert_blob_tuple = (parentdir, name, buffer)
    result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    connection.commit()
    cursor.close()
    return


# def creatDatabase(connection):
#     cursor = connection.cursor()
#     query = open("./createTable.sql").read()
#     try:
#         cursor.execute(query, multi=True)
#         connection.commit()
#         cursor.close()
#     except mysql.connector.Error as err:
#         print(err)


def main():
    connection = connectDB()
    # creatDatabase(connection)
    scanDir(connection, "/Users/jiahao/Desktop")
    if (connection.is_connected()):
        connection.close()
        # print("MySQL connection is closed")


if __name__ == '__main__':
    main()

