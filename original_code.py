#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 15:10:39 2021

@author: jeffwyckoff
"""
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

#Create a engine for connecting to SQLite3.
#Assuming backup.students.db is in your app root folder

e = create_engine('sqlite:///backup.students.db')

app = Flask(__name__)
api = Api(app)

class Students_Dynamic(Resource):
    def get(self,search_value='default'):
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        #query = conn.execute("select distinct DEPARTMENT from salaries")
        if search_value.lower() == 'student_id':
          query = conn.execute("SELECT student_id, COUNT(CASE WHEN status = 'TURNED_IN' THEN 1 ELSE NULL END) AS SubmissionCount FROM student_submissions GROUP BY student_id")
          result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
          return result
        elif search_value.lower() == 'course_id':
          query = conn.execute("SELECT course_id, AVG(assigned_points) AS AverageGrade FROM student_submissions GROUP BY course_id")
          result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
          return result
        elif search_value.lower() == 'teacher_id':
          query = conn.execute("SELECT C.teacher_id, COUNT(C.course_work_id) AS AssignmentCount FROM (SELECT DISTINCT B.teacher_id, A.course_work_id FROM student_submissions A INNER JOIN course B ON A.course_id = B.course_id) C GROUP BY teacher_id")
          result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
          return result
        elif search_value.lower() == 'school_id':
          query = conn.execute("SELECT C.school, COUNT(CASE WHEN C.SubCount > 1 THEN 1 ELSE NULL END) AS Complete, COUNT(C.SubCount) AS Total, CAST(COUNT(CASE WHEN C.SubCount > 1 THEN 1 ELSE NULL END) AS float)/CAST(COUNT(C.SubCount) AS float) AS Percent FROM (SELECT A.student_id, A.SubCount, B.school FROM (SELECT student_id, COUNT(CASE WHEN status = 'TURNED_IN' THEN 1 ELSE NULL END) AS SubCount FROM student_submissions GROUP BY student_id) A INNER JOIN student B ON A.student_id = B.student_id) C GROUP BY C.school")
          result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
          return result
        elif search_value.lower() == 'default':
          return {'Schoolytics API!': 'Please add /student_id, /course_id, /teacher_id, or /school_id to the path after /students/.'}
        else:
          return {'Error': 'This is not a search option. Please add /student_id, /course_id, /teacher_id, or /school_id to the path after /students/.'}

class Students_Info(Resource):
    def get(self):
        #Info for dynamic API
        return {'Schoolytics API!': 'Please add /student_id, /course_id, /teacher_id, or /school_id to the path after /students/.'}


api.add_resource(Students_Info, '/students/')
api.add_resource(Students_Dynamic, '/students/<string:search_value>')


if __name__ == '__main__':
     app.run()