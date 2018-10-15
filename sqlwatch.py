#!/usr/bin/env python
#
# utilitario que executa uma query periodicamente ate se pressionar CTRL-C
# Inspirado no comando watch
#
# 2018-10-11 Nereu Started
# 2018-10-12 Nereu regexp SQL*Plus commands, DCLs and DMLs
# 2018-10-13 Nereu Adding flag -l/--sqllist
# 2018-10-14 Nereu Using git hub

import argparse
import getpass
import re
import sys
import time
from datetime import datetime as dt

import cx_Oracle as DB
from tabulate import tabulate

parser=argparse.ArgumentParser()

parser.add_argument('-u','--db_user',help='Database user name',default='')
parser.add_argument('-p','--db_pass',help='Database user\'s password',default='')
parser.add_argument('-l','--sqllist',help='Only list queries in sqlfile',action='store_true', default=False)
parser.add_argument('-n','--interval',help='Specify update interval',type=int,default=60)
parser.add_argument('-q','--sqlnum',help='Query position in script file: 0,1,2, .. , -1',type=int,default=-1)
parser.add_argument('-s','--sqlfile',help='SQL*Plus script file',type=argparse.FileType('r'),required=True)

args=parser.parse_args()

db_user=args.db_user
db_pass=args.db_pass

if db_user == '' or db_pass == '':
  try:
    import credentials

    if db_user == '':
      db_user=credentials.db_user

    if db_pass == '':
      db_pass=credentials.db_pass

  except ImportError as error:
     if db_user == '':
       db_user=raw_input("Enter user-name: ")

     if db_pass == '':
       db_pass=getpass.getpass(prompt='Enter password: ',stream=sys.stderr)

sqlplus_cmds_regexp=r'(^(@|\/|\--|#|accept|alter|analyze|append|archive|attribute|audit|begin|break|btitle|call|change|clear|column|comment|commit|compute|connect|copy|create|define|del|delete|describe|disconnect|drop|edit|end|execute|exit|explain|flash|get|grant|help|host|input|insert|list|lock|merge|noaudit|password|pause|print|prompt|purge|quit|recover|remark|repfooter|repheader|replace|rename|revoke|rollback|run|save|set|show|shutdown|spool|start|startup|store|timing|truncate|ttitle|undefine|update|variable|whenever)|(^$))'

sqlfile_entries=''

for row in args.sqlfile:
  if not re.search(sqlplus_cmds_regexp,row.strip(),re.IGNORECASE):
    sqlfile_entries += row

sql_list=[]

for entry in sqlfile_entries.split(';'):
  if entry.strip() != '':
    sql_list.append(entry)

if args.sqlnum >= len(sql_list):
  print('SQL out of range, use option -l to check the sqlfile!')
  exit(3)

if args.sqllist:
  print('')
  print('SQL file : [%s]' % (args.sqlfile.name) )
  print('SQL num  : %d' % (args.sqlnum,) )
  print('SQL list :')
  for i in range(len(sql_list)):
    print('[%d]=[%s]' % (i, sql_list[i][0:76].replace('\n',' ')) )
  print('\nSQL      :\n%s\n' % (sql_list[args.sqlnum],) )
  exit(0)
  
try:

  db=DB.connect(db_user,db_pass)

  c=db.cursor()

  while True:
    c.execute(sql_list[args.sqlnum])

    print('\nEvery %ds | %s\n' % (args.interval, dt.now().strftime('%Y-%m-%d %H:%M:%S')) )

    print(tabulate(c,headers=[i[0] for i in c.description]))

    print('\n--- Press CTRL-C to quit ---\n')

    time.sleep(args.interval)

except DB.DatabaseError as exc:
  error, = exc.args
  print('\n%s\n' % error.message )

except KeyboardInterrupt:
  print('\nQuiting...')
  c.close()
  db.close()
  exit(0)

