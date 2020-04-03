import mysql.connector
import subprocess
import sys
import re
from importdata import connectDB, scanDir
from mysql.connector import Error


# check whether the path current_dir/path_to_dir exists
def is_dir_exist(connection, current_dir, path_to_dir):
    cursor = connection.cursor()
    query = """select count(`name`) as num from FileInfo where parentdir = %s and `name` = %s"""

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


def move_dir_up_one_level(path_to_dir):
    dir_arr = path_to_dir.split('/')[1:-1]
    if len(dir_arr) > 0:
        temp_dir = ''
        for dir in dir_arr:
            temp_dir = temp_dir + '/' + dir
    else:
        temp_dir = '/'
    return temp_dir


def pwd(current_dir):
    print(current_dir)


def cd(connection, current_dir, input):
    re_obj = re.match("^cd (?P<path_to_dir>(.+))", input)
    path_to_dir = re_obj.group("path_to_dir").rstrip('/') # remove '/' at the end of the path if there is any
    if path_to_dir == ".":
        return current_dir
    if path_to_dir == "..":
        current_dir = move_dir_up_one_level(current_dir)
    else:
        if is_dir_exist(connection, current_dir, path_to_dir):
            current_dir = current_dir + '/' + path_to_dir
        else:
            # print(path_to_dir)
            print("cd: no such directory: {}".format(path_to_dir))
            return
    return current_dir


def ls(connection, current_dir):
    cursor = connection.cursor()
    query = """select `name` from FileInfo where parentdir = "{}" """.format(current_dir)
    cursor.execute(query)
    for name in cursor:
        print(name[0])
    cursor.close()


def lsl(connection, current_dir):
    cursor = connection.cursor()
    query = """select `type`, `ownerPermission`, `groupUserPermission`, `otherUserPermission`, 
            `numHardLinks`, `owner`, `group`, `size`, `lastModifiedDate`, `lastModifiedtime`, 
            `name` from FileInfo where parentdir = "{}" """.format(current_dir)
    cursor.execute(query)
    for (type, ownerPermission, groupUserPermission, otherUserPermission, numHardLinks, owner, group, size,
         lastModifiedDate, lastModifiedtime, name) in cursor:
        print("{}{}{}{:4} {:>5}  {}  {} {:>8}  {:>3}  {:>2}  {}".format(type, ownerPermission, groupUserPermission,
            otherUserPermission, numHardLinks, owner, group, size, lastModifiedDate, lastModifiedtime, name))
    cursor.close()


def find(connection, path_to_dir, partial_filename, current_dir):
    find_dir = path_to_dir
    if path_to_dir == ".":
        find_dir = current_dir
    elif path_to_dir == "..":
        find_dir = move_dir_up_one_level(current_dir)
    else:
        # the path is under the current dir
        if path_to_dir.find('/') != 0:
            find_dir = current_dir + '/' + path_to_dir

    # if not is_dir_exist(connection, current_dir, find_dir):
    #     print("find: directory not exist: {}".format(find_dir))
    #     return

    dir_pattern = find_dir + "%"
    filename_pattern = partial_filename.replace("*", "%")

    cursor = connection.cursor()
    query = """select `type`, `ownerPermission`, `groupUserPermission`, `otherUserPermission`, 
            `numHardLinks`, `owner`, `group`, `size`, `lastModifiedDate`, `lastModifiedtime`, 
            `parentdir`, `name` from FileInfo where parentdir like "{}" and `name` like "{}" """.format(dir_pattern, filename_pattern)
    cursor.execute(query)

    flag = 0
    for (type, ownerPermission, groupUserPermission, otherUserPermission, numHardLinks, owner, group, size,
         lastModifiedDate, lastModifiedtime, parentdir, name) in cursor:
        flag = 1
        print("{}{}{}{:4} {:>5}  {}  {} {:>8}  {:>3}  {:>2}  {}/{}".format(type, ownerPermission, groupUserPermission,
                                                                        otherUserPermission, numHardLinks, owner, group,
                                                                        size, lastModifiedDate, lastModifiedtime, parentdir, name))
    if flag == 0:
        print("find: file not found. ")
    cursor.close()


def grep(connection, pattern, partial_filename, current_dir):
    # filename contains path, which starts with root '/'
    if partial_filename.find('/') == 0:
        grep_dir = move_dir_up_one_level(partial_filename)
        partial_filename = partial_filename.split('/')[-1]
    elif partial_filename.find('/') == -1:
        grep_dir = current_dir
    else:
        grep_dir = move_dir_up_one_level(current_dir + '/' + partial_filename)
        partial_filename = partial_filename.split('/')[-1]

    # if not is_dir_exist(grep_dir):
    #     print("grep: directory not exist: {}".format(grep_dir))
    #     return

    filename_pattern = partial_filename.replace("*", "%")
    pattern_re = re.compile(pattern)

    cursor = connection.cursor()
    query = """ select concat(`parentdir`, '/', `name`) as path, `fileContent` from FileBlobs where parentdir = "{}" and 
            `name` like "{}" """.format(grep_dir, filename_pattern)
    cursor.execute(query)

    flag = 0
    found = False
    for (path, fileContent) in cursor:
        flag = 1
        lines = str(fileContent.decode(encoding='UTF-8')).splitlines()
        line_num = 0
        for line in lines:
            line_num += 1
            if pattern_re.search(line) is not None:
                found = True
                print(path, ":", line_num, " ", line)

    if flag == 0:
        print("grep: file not exist. ")
        return
    if not found:
        print("grep: no match is found. ")
        return


def add_to_PATH(connection, path):
    cursor = connection.cursor()
    query = """ insert into `PATH` (`path`) values ({})""".format(path)
    cursor.execute(query)
    connection.commit()
    cursor.close()


def execute_prog_in_PATH(connection, prog_name):
    cursor = connection.cursor()
    query = """ select `path` from `PATH` """
    cursor.execute(query)
    executed = False
    for path in cursor:
        try:
            path_to_prog = path[0] + "/" + prog_name
            ret_code = subprocess.call([path_to_prog])
            if ret_code == 0:
                executed = True
                cursor.close()
                return 0
        except:
            pass
        #     print(ret_code)
    if not executed:
        print("Error: Unknown command.")
    cursor.close()
    return -1


def show_PATH(connection):
    cursor = connection.cursor()
    query = """ select `path` from `PATH` """
    cursor.execute(query)
    for path in cursor:
        print(path[0])
    cursor.close()


def shell():
    #root_dir, cd, path, ls, ls -l, find, grep
    root_dir = '/Users/jiahao/Desktop'
    current_dir = root_dir
    connection = connectDB()

    while True:
        fakeshell = current_dir + " $ "
        # print(fakeshell)
        sys.stdout.write(fakeshell)
        sys.stdout.flush()
        try:
            line = sys.stdin.readline()
        except EOFError:
            break

        if re.match("^\s*importdata\s*", line):
            scanDir(connection, root_dir)
            print("importdata success!")

        #pwd
        elif re.match("^\s*pwd\s*", line):
            pwd(current_dir)

        # cd
        elif re.match("^\s*cd", line):
            current_dir = cd(connection, current_dir, line)

        # ls
        elif re.match("\s*ls\s*$", line):
            ls(connection, current_dir)

        # ls -l
        elif re.match("\s*ls\s*-l\s*$", line):
            lsl(connection, current_dir)

        # find path_to_dir (partial)filename
        elif re.match("^\s*find \s*(?P<path_to_dir>(.+)) \s*(?P<partial_filename>(.+))", line):
            re_obj = re.match("^\s*find \s*(?P<path_to_dir>(.+)) \s*(?P<partial_filename>(.+))", line)
            path_to_dir = re_obj.group("path_to_dir").rstrip('/')
            partial_filename = re_obj.group("partial_filename")
            find(connection, path_to_dir, partial_filename, current_dir)

        # grep pattern file
        elif re.match("^\s*grep \s*(?P<pattern>(.+)) \s*(?P<partial_filename>(.+))", line):
            re_obj = re.match("^\s*grep \s*(?P<pattern>(.+)) \s*(?P<partial_filename>(.+))", line)
            pattern = re_obj.group("pattern").replace('"','')
            partial_filename = re_obj.group("partial_filename")
            grep(connection, pattern, partial_filename, current_dir)

        # export PATH "path_to_excutable_programs"
        elif re.match("^\s*export \s*PATH \s*(?P<path>(.+))", line):
            re_obj = re.match("\s*export \s*PATH \s*(?P<path>(.+))", line)
            path_to_prog = re_obj.group("path")
            add_to_PATH(connection, path_to_prog)

        # show PATH
        elif re.match("\s*show \s*PATH\s*", line):
            show_PATH(connection)

        elif re.match("^\s*(?P<prog_name>(.+))",line):
            # print("check")
            re_obj = re.match("^\s*(?P<prog_name>(.+))", line)
            prog_name = re_obj.group("prog_name")
            ret_code = execute_prog_in_PATH(connection, prog_name)

        else:
            print("Error: Unknown command.")
            
    if (connection.is_connected()):
            connection.close()
            print("MySQL connection is closed")
    return
    
    
if __name__ == '__main__':
    shell()

# tests

# cd test/test1
# ls
# ls -l
# find . test*
# grep "thi" test.txt
# grep "thissa" test.txt


# To do
# - find dir test; append the dir to the current directory (except dir starts with '/')
# - grep pattern file; if file contains path in it, append the path to curent dir (except when the path starts with '/')