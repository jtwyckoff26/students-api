# students-api
API for Schoolytics Interview

This repository has a python API created using the Flask framework and performs crud operations on a SQLite3 database.

## Installation
  - Clone the repository
  - Open terminal and navigate to the path of repo
  - We will first load the database
```bash
$ sqlite3
sqlite> .open "backup.students.db"
sqlite> .save "backup.students.db"
sqlite> .exit
```
  - We will then download the needed python packages
```bash
$ pip install flask
$ pip install flask-restful
$ pip install sqlalchemy
```

## Usage
  - Finally we will run the app.py file
```bash
$ python app.py
```
  - You can then navigate to the browser of your choice and go to localhost (http://127.0.0.1:5000/students)
  - Your options to return the queries are as follows:
     - "?value=<value>" = Returns group by <value> and count completed assignments,Returns group by <value> and average grade, and Returns group by <value> and count assignments created
     - "?value=school" = Returns group by school and find percentage of students with more than 1 assignment completed

### Additional Info

  - I have attatched the CSV Data folder for your review
  - This folder shows the dummy data i created to test the API
