# PYTHON with SELENIUM project

## technologies / modules
    python
    html
    unittest
    pymysql
    requests
    time
    requests
    selenium 
    logging
    flask 
    PyDoc
    Jenkins pipeline as code

## read configuration from database
    The application is able to automatically resolve insertion conflict during testing  

## read configuration from database
    The application read url, browser type (to run selenium test) and other data from MySql to be used for testing 

# python project structure

### Rest API : 
    backend exposing POST GET PUT DELETE

### Database : 
    create users and config tables

### Web Interface : 
    expose a single verb GET but return a basic web page as html

### python testing

#### backend testing : 
    confirm that the implementation works via unit testing

#### frontend testing : 
    confirm the data returns via selenium testing

## vulnerabilities :
jaydenassi@Jaydens-iMac ~ % docker scout quickview
INFO New version 1.0.2 available (installed version is 0.20.0)
    ✓ SBOM of image already cached, 84 packages indexed

  Your image  pipelineascode-rest:latest  │    0C     1H     0M     0L   
  Base image  python:3.8-alpine           │    0C     1H     0M     0L   
  Updated base image  python:3.9-alpine   │    0C     1H     0M     0L   
                                          │                              

What's Next?
  Learn more about vulnerabilities → docker scout cves pipelineascode-rest:latest
  Learn more about base image update recommendations → docker scout recommendations pipelineascode-rest:latest

jaydenassi@Jaydens-iMac ~ % docker scout cves pipelineascode-rest:latest
INFO New version 1.0.2 available (installed version is 0.20.0)
    ✓ SBOM of image already cached, 84 packages indexed
    ✗ Detected 1 vulnerable package with 1 vulnerability

   0C     1H     0M     0L  setuptools 57.5.0
pkg:pypi/setuptools@57.5.0

    ✗ HIGH CVE-2022-40897 [Inefficient Regular Expression Complexity]
      https://scout.docker.com/v/CVE-2022-40897
      Affected range : <65.5.1                                       
      Fixed version  : 65.5.1                                        
      CVSS Score     : 7.5                                           
      CVSS Vector    : CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H  
    


1 vulnerability found in 1 package
  LOW       0  
  MEDIUM    0  
  HIGH      1  
  CRITICAL  0  

What's Next?
  Learn more about base image update recommendations → docker scout recommendations pipelineascode-rest:latest


## Python-MySQL :
A quick start using PyMySQL

Inside Pycharm terminal:
$ pip install pymysql
$ pip install cryptography
From your host's terminal:
Mac / Linux users

mkdir mysql && cd mysql
docker run --name mysql -v $(pwd):/var/lib/mysql -e MYSQL_ROOT_PASSWORD=mysql -e MYSQL_DATABASE=mydb -e MYSQL_USER=user -e MYSQL_PASSWORD=password -p 3306:3306 -d mysql:8.0.33
Windows users (CMD)

mkdir mysql && cd mysql
docker run --name mysql -v %cd%:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=mysql -e MYSQL_DATABASE=mydb -e MYSQL_USER=user -e MYSQL_PASSWORD=password -p 3306:3306 -d mysql:8.0.33

## port 5000 in new mac :
port 5000 used by Control Center in new mac, and if you kill it , it will set it back again.
So options are kill control center or change port.
I chose to change port!