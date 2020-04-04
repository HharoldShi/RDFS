# RDFS
RDFS is a un*x file system based on the relational database MySQL. 
## Dependences
### Python3
  - mysql-connector
### MySQL
  - user "root"
  - password "ece651db"
  - database "ece656project"
## Run
### MySQL
Create database and tables
```mysql
source ./createTable.sql
```
### Shell
Run the shell
```python
python3 rdnsh.py
```
#### Commands
**pwd**

print working directory
```
pwd
```

**cd**

Change directory
```
cd directory
```

**ls**

list files and directories in the working directory. 
```
ls [-l]
```

**find**

Accept the path to a directory and (partial) name of the file. Search the file in the directory and all its subdirectories to the lowest level. 
```
find path_to_directory (partial)filename
```

**grep**

Accept the (partial) name of the file and seek the relevant pattern (regular expression) in the matching file(s). Output the line number and line for the matching lines.
```
grep pattern (partial)filename
```

**show PATH**

Show all directories in the PATH variable. 
```
show PATH
```

**export PATH**

Add a directory into the PATH variable
```
export PATH path_to_directory
```

**remove PATH**

Remove a directory from the PATH variable
```
remove PATH path_to_directory
```

**run excutable**

Accept the name of the excutable file that is in the PATH variable. 
```
excutable_filename
```
### Running example
```
jiahao@Jiahaos-MacBook-Pro Unix-File-System-Based-on-MYSQL % python3 rdbsh.py 
/Library/Python/3.7 $ importdata
Succeed to import data from directory: /Library/Python/3.7
/Library/Python/3.7 $ ls
.
..
site-packages
test
/Library/Python/3.7 $ ls -l
drwxr-xr-x      4  root     wheel      128   3 Apr  22:41  .
drwxr-xr-x      4  root     wheel      128  29 Mar  22:13  ..
drwxr-xr-x     12  root     wheel      384   4 Apr  13:44  site-packages
drwxr-xr-x      5  jiahao   wheel      160   3 Apr  23:49  test
/Library/Python/3.7 $ cd site-packages
/Library/Python/3.7/site-packages $ ls -l
drwxr-xr-x     12  root   wheel      384   4 Apr  13:44  .
drwxr-xr-x      4  root   wheel      128   3 Apr  22:41  ..
drwxr-xr-x     12  root   wheel      384   1 Feb  14:29  asgiref
drwxr-xr-x      8  root   wheel      256   1 Feb  14:29  asgiref-3.2.3.dist-info
drwxr-xr-x     22  root   wheel      704   1 Feb  14:29  django
drwxr-xr-x     11  root   wheel      352   1 Feb  14:29  Django-3.0.2.dist-info
drwxr-xr-x      7  root   wheel      224   1 Feb  14:29  pip
drwxr-xr-x      9  root   wheel      288   1 Feb  14:29  pip-20.0.2.dist-info
drwxr-xr-x     10  root   wheel      320   1 Feb  14:29  pytz
drwxr-xr-x     11  root   wheel      352   1 Feb  14:29  pytz-2019.3.dist-info
drwxr-xr-x     16  root   wheel      512   1 Feb  14:29  sqlparse
drwxr-xr-x      9  root   wheel      288   1 Feb  14:29  sqlparse-0.3.0.dist-info
/Library/Python/3.7/site-packages $ cd django
/Library/Python/3.7/site-packages/django $ find . test*
drwxr-xr-x     11  root   wheel      352   1 Feb  14:29  /Library/Python/3.7/site-packages/django/test
-rw-r--r--      1  root   wheel       60   1 Feb  14:29  /Library/Python/3.7/site-packages/django/conf/app_template/tests.py-tpl
-rw-r--r--      1  root   wheel     7301   1 Feb  14:29  /Library/Python/3.7/site-packages/django/contrib/admin/tests.py
-rw-r--r--      1  root   wheel     7696   1 Feb  14:29  /Library/Python/3.7/site-packages/django/contrib/admin/__pycache__/tests.cpython-37.pyc
-rw-r--r--      1  root   wheel      463   1 Feb  14:29  /Library/Python/3.7/site-packages/django/contrib/staticfiles/testing.py
-rw-r--r--      1  root   wheel      755   1 Feb  14:29  /Library/Python/3.7/site-packages/django/contrib/staticfiles/__pycache__/testing.cpython-37.pyc
-rw-r--r--      1  root   wheel     2050   1 Feb  14:29  /Library/Python/3.7/site-packages/django/core/management/commands/test.py
-rw-r--r--      1  root   wheel     2117   1 Feb  14:29  /Library/Python/3.7/site-packages/django/core/management/commands/testserver.py
-rw-r--r--      1  root   wheel     2198   1 Feb  14:29  /Library/Python/3.7/site-packages/django/core/management/commands/__pycache__/test.cpython-37.pyc
-rw-r--r--      1  root   wheel     1838   1 Feb  14:29  /Library/Python/3.7/site-packages/django/core/management/commands/__pycache__/testserver.cpython-37.pyc
-rw-r--r--      1  root   wheel    61365   1 Feb  14:29  /Library/Python/3.7/site-packages/django/test/testcases.py
-rw-r--r--      1  root   wheel    49553   1 Feb  14:29  /Library/Python/3.7/site-packages/django/test/__pycache__/testcases.cpython-37.pyc
/Library/Python/3.7/site-packages/django $ grep "test" contrib/admin/tes*    
/Library/Python/3.7/site-packages/django/contrib/admin/tests.py : 1   from django.contrib.staticfiles.testing import StaticLiveServerTestCase
/Library/Python/3.7/site-packages/django/contrib/admin/tests.py : 2   from django.test import modify_settings
/Library/Python/3.7/site-packages/django/contrib/admin/tests.py : 3   from django.test.selenium import SeleniumTestCase
/Library/Python/3.7/site-packages/django/contrib/admin/tests.py : 15   @modify_settings(MIDDLEWARE={'append': 'django.contrib.admin.tests.CSPMiddleware'})
/Library/Python/3.7/site-packages/django/contrib/admin/tests.py : 28           Block the execution of the tests until the specified callback returns a
/Library/Python/3.7/site-packages/django $ pwd
/Library/Python/3.7/site-packages/django
/Library/Python/3.7/site-packages/django $ cd /Library/Python/3.7/test
/Library/Python/3.7/test $ ls -l
drwxr-xr-x      5  jiahao   wheel      160   3 Apr  23:49  .
drwxr-xr-x      4  root     wheel      128   3 Apr  22:41  ..
-rw-r--r--@     1  jiahao   wheel     8196   3 Apr  22:52  .DS_Store
-rw-r--r--@     1  jiahao   wheel     3380   3 Apr  23:49  testfile.txt
drwxr-xr-x      8  jiahao   wheel      256   3 Apr  23:33  test_cpp_project
/Library/Python/3.7/test $ cd test_cpp_project
/Library/Python/3.7/test/test_cpp_project $ ls -l
drwxr-xr-x      8  jiahao   wheel      256   3 Apr  23:33  .
drwxr-xr-x      5  jiahao   wheel      160   3 Apr  23:49  ..
-rw-r--r--@     1  jiahao   wheel     6148   3 Apr  23:47  .DS_Store
drwxr-xr-x      6  jiahao   wheel      192   4 Apr  00:20  .idea
drwxr-xr-x      9  jiahao   wheel      288   3 Apr  23:33  cmake-build-debug
-rw-r--r--@     1  jiahao   wheel      133   3 Apr  22:47  CMakeLists.txt
-rw-r--r--      1  jiahao   wheel      182   3 Apr  23:33  main.cpp
-rwxr-xr-x      1  jiahao   wheel    23032   3 Apr  23:33  test_excutable_file
/Library/Python/3.7/test/test_cpp_project $ show PATH
/Library/Python/3.7/test/test_cpp_project $ export PATH "/Library/Python/3.7/test/test_cpp_project"
/Library/Python/3.7/test/test_cpp_project $ show PATH
/Library/Python/3.7/test/test_cpp_project
/Library/Python/3.7/test/test_cpp_project $ cd ..
/Library/Python/3.7/test $ test_excutable_file
Hello, World!
This is a test executable file for ECE656 project. 
/Library/Python/3.7/test $ 

```