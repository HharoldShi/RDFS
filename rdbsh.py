import mysql.connector
import sys
import re
from mysql.connector import Error


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


def shell():
    #pwd, cd, path, ls, ls -l, find, grep
    pwd = "topdirectory"
    #present working directory
    symbol = " $(:D)$ "
    re_cd = re.compile("^cd ")
    re_find = re.compile("^find ")
    re_grep = re.compile("^grep ")

    
    connection = mysql.connector.connect(host='localhost',
                                         database='project',
                                         user='root',
                                         password='ece651db')
    
    cursor = connection.cursor()
    
    while True:
        fakeshell = pwd+symbol
        sys.stdout.write(fakeshell)
        try:
            line = sys.stdin.readline()
        except EOFError:
            break
    
        if line == 'pwd':
            print(pwd)
            
        elif line == '.' or line == './':
            print(pwd.rsplit('/',1)[1])
            
        elif line == '..' or line == '../':
            print(pwd.rsplit('/',2)[1])
            
        elif re_open_dir.match(line):    
            s
        elif re_cd.match(line):
            re_obj = re.match("cd (?P<path>(.+))" ,line)
            path = re_obj.group('path').rstrip('/')
            
            if path.find('/') == -1:
                newpath = (pwd+'/'+path)

            elif path == '.':
                continue
            elif path == '..':
                pwd = pwd.rsplit('/',1)[0]
                continue
            else:
                newpath = path.rstrip('/')
            
            sql_fetch_path_query = """SELECT `path` FROM FileInfo WHERE `path` = %s AND `type` = 'd'"""
            cursor.execute(sql_fetch_path_query, (newpath,))
            record = cursor.fetchall()
            
            if record:
                pwd = newpath
                
        elif line == 'ls':
            sql_fetch_son_query = """SELECT `name` FROM FileInfo WHERE `path` LIKE %s"""
            cursor.execute(sql_fetch_son_query, (pwd+"/%",))
            record = cursor.fetchall()
            #find all records whose path starts with pwd
            for row in record:
                obj_in_pwd = "^"+pwd+"/[^/]$"
                #match objects in the current directory, exclude all subdirectories
                if re.match(obj_in_pwd, row):                    
                    print(row[0])
                        
        elif line == 'ls -l':
            sql_fetch_son_query = """SELECT * FROM FileInfo WHERE `path` LIKE %s"""
            cursor.execute(sql_fetch_son_query, (pwd+"/%",))
            record = cursor.fetchall()
            
            for row in record:
                obj_in_pwd = "^"+pwd+"/[^/]$"

                if re.match(obj_in_pwd, row):
                    print(row[0],row[1],row[2],row[3]," ",row[4]," ",row[5]," ",row[6]," ",row[7]," ",row[8]," ",row[9]," ",row[10]," ",row[11])
           
        elif re_find.match(line):
            re_obj = re.match("find (?P<target>(.+))" ,line)
            target = re_obj.group('path').rstrip('/')
            sql_find_query = """SELECT * FROM FileInfo WHERE `path` LIKE %s"""
            cursor.execute(sql_find_query, ("%"+target+"%",))
            record = cursor.fetchall()
            
            for row in record:
                sub_pwd = "^"+pwd
                #all files and folders under pwd
                if re.match(sub_pwd, row):
                    print(row[0],row[1],row[2],row[3]," ",row[4]," ",row[5]," ",row[6]," ",row[7]," ",row[8]," ",row[9]," ",row[10]," ",(row[12][(len(pwd)+1):]))
           
        elif re_grep.match(line):
            re_obj = re.match("grep (?P<phrase>([^ ]+) (?P<filepath>(.+)))", line)
            phrase = re_obj.group("phrase")
            path = re_obj.group("filepath").rstrip('/').lstrip('./')
            #support the format ./file
            
            if path.find('/') == -1:
                newpath = (pwd+'/'+path)

            elif path == '.':
                continue
            elif path == '..':
                pwd = pwd.rsplit('/',1)[0]
                continue
            else:
                newpath = path.rstrip('/')
                
            sql_fetch_blob_query = """SELECT `file` FROM FileBlobs where path = %s"""

            cursor.execute(sql_fetch_blob_query, (newpath,))
            record = cursor.fetchall()
            
            if len(record) == 1:
                data = record[0][1]               
                with open(data, "r") as f:
                    linenum = 0
                    found_flag = False
                    while True:
                        try:
                            fline = f.readline()
                            linenum += 1
                            if phrase in fline:
                                print(linenum,"  ",fline)
                                found_flag = True

                        except EOFError:
                            if not found_flag:
                                print("Not found.")
                            break
                    
            else:
                print("Error: Filepath is wrong.")
            
            
        # elif re_open_file.match(line):
        else:
            print("Error: Unknown command.")
            
    if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return
    
    
if __name__ == '__main__':
    shell()