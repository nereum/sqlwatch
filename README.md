# sqlwatch.py

A utility similar to Linux/Unix "watch" to Oracle's SQL queries

## Getting Started

This utility will get  SQL*Plus's script, extract its queries and pick one 
(the last query in the file by default) and run it periodically (every 60 
seconds by default) until the user press Control-C.
We can think it as a version of Linux/Unix command watch with Oracle's 
SQL database in mind.


### Prerequisites

Besides regular C-Python the following modules should be installed:
* cx_Oracle - pip install cx_Oracle
* Tabulate  - pip install tabulate

### Usage

The basic use is very straightforward:

``` shell
$ cat test.sql
select sysdate from dual;

$ ./sqlwatch.py -s test.sql

Every 60s | 2018-10-14 12:12:57

SYSDATE
-------------------
2018-10-14 12:12:57

--- Press CTRL-C to quit ---

^C
Quiting...

``` 

Is possible to define the interval between executions using -n <interval>

``` shell
$ ./sqlwatch.py -n 10 -s test.sql

Every 10s | 2018-10-14 12:13:10

SYSDATE
-------------------
2018-10-14 12:13:10

--- Press CTRL-C to quit ---

Every 10s | 2018-10-14 12:13:20

SYSDATE
-------------------
2018-10-14 12:13:20

--- Press CTRL-C to quit ---

^C
Quiting...
```
## Database credentials

There are three forms to connect to database:
1. Passing username and password as parameters (using -u -and "-p" respectivally);
2. Using a module called "credentials.py" with two str variables: db_user and db_pass;
3. Providing the username and password as a regular login procedure.

## Author

* Nereu Matos - [nereum](https://github.com/nereum/)

## License

This project is licensed under the Creative Commons CC0

## Acknowledgments

* I would like to thanks the author of Tabulate - Sergey Astanin (https://pypi.org/project/tabulate/)

