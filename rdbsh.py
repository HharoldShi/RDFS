import mysql.connector
import sys
import re
from importdata import connectDB
from mysql.connector import Error


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


# check whether the path current_dir/path_to_dir exists
def is_dir_exist(connection, current_dir, path_to_dir):
    cursor = connection.cursor()
    query = """select count(name) as num from FileInfo where parentdir = %s and name = %s"""

    if path_to_dir.find('/') == -1:
        cursor.execute(query, (current_dir, path_to_dir))
    else:
        bottom_dir = path_to_dir.split('/')[-1]
        parent_dir = current_dir
        for dir in path_to_dir.split('/')[:-1]:
            parent_dir = parent_dir + '/' + dir
        cursor.execute(query, (parent_dir, bottom_dir))

    for num in cursor:
        if int(num[0]) > 0:
            return True

    return False


def cd(connection, current_dir, input):
    re_obj = re.match("^cd (?P<path_to_dir>(.+))", input)
    path_to_dir = re_obj.group("path_to_dir").rstrip('/') # remove '/' at the end of the path if there is any
    if path_to_dir == ".":
        return current_dir
    if path_to_dir == "..":
        if current_dir.split('/')[1] != '':
            for dir in current_dir.split('/')[1:-1]:
                current_dir = '/' + dir
        else:
            current_dir = '/'
    else:
        if is_dir_exist(connection, current_dir, path_to_dir):
            current_dir = current_dir + '/' + path_to_dir
        else:
            print("cd: no such directory: {}").format(path_to_dir)
    return current_dir

def ls():



def shell():
    #root_dir, cd, path, ls, ls -l, find, grep
    root_dir = "/Users/jiahao/Desktop"
    current_dir = root_dir
    #present working directory
    symbol = " $ "

    re_cd = re.compile("^cd ")
    re_find = re.compile("^find ")
    re_grep = re.compile("^grep ")

    connection = connectDB()
    cursor = connection.cursor()
    
    while True:
        fakeshell = current_dir + symbol
        sys.stdout.write(fakeshell)
        try:
            line = sys.stdin.readline()
        except EOFError:
            break

        if re_cd.match(line):
            current_dir = cd(connection, current_dir, line)
                
        elif line == 'ls':
            sql_fetch_son_query = """SELECT `name` FROM FileInfo WHERE `path` LIKE %s"""
            cursor.execute(sql_fetch_son_query, (root_dir+"/%",))
            record = cursor.fetchall()
            #find all records whose path starts with root_dir
            for row in record:
                obj_in_root_dir = "^"+root_dir+"/[^/]$"
                #match objects in the current directory, exclude all subdirectories
                if re.match(obj_in_root_dir, row):                    
                    print(row[0])
                        
        elif line == 'ls -l':
            sql_fetch_son_query = """SELECT * FROM FileInfo WHERE `path` LIKE %s"""
            cursor.execute(sql_fetch_son_query, (root_dir+"/%",))
            record = cursor.fetchall()
            
            for row in record:
                obj_in_root_dir = "^"+root_dir+"/[^/]$"

                if re.match(obj_in_root_dir, row):
                    print(row[0],row[1],row[2],row[3]," ",row[4]," ",row[5]," ",row[6]," ",row[7]," ",row[8]," ",row[9]," ",row[10]," ",row[11])
           
        elif re_find.match(line):
            re_obj = re.match("find (?P<target>(.+))" ,line)
            target = re_obj.group('path').rstrip('/')
            sql_find_query = """SELECT * FROM FileInfo WHERE `path` LIKE %s"""
            cursor.execute(sql_find_query, ("%"+target+"%",))
            record = cursor.fetchall()
            
            for row in record:
                sub_root_dir = "^"+root_dir
                #all files and folders under root_dir
                if re.match(sub_root_dir, row):
                    print(row[0],row[1],row[2],row[3]," ",row[4]," ",row[5]," ",row[6]," ",row[7]," ",row[8]," ",row[9]," ",row[10]," ",(row[12][(len(root_dir)+1):]))
           
        elif re_grep.match(line):
            re_obj = re.match("grep (?P<phrase>([^ ]+) (?P<filepath>(.+)))", line)
            phrase = re_obj.group("phrase")
            path = re_obj.group("filepath").rstrip('/').lstrip('./')
            #support the format ./file
            
            if path.find('/') == -1:
                newpath = (root_dir+'/'+path)

            elif path == '.':
                continue
            elif path == '..':
                root_dir = root_dir.rsplit('/',1)[0]
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