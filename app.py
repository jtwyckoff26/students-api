#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 15:10:39 2021

@author: jeffwyckoff
"""
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Date, MetaData
from sqlalchemy.sql import select
from json import dumps

#Create a engine for connecting to SQLite3.
#Assuming backup.students.db is in your app root folder

e = create_engine('sqlite:///backup.students.db')

app = Flask(__name__)
api = Api(app)

class Students_Dynamic(Resource):
    def get(self):
        search_value = request.args.get('value') #retrieve args from query string
        print(search_value)
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        #query = conn.execute("select distinct DEPARTMENT from salaries")
        if (search_value == 'student_id') or (search_value == 'course_id') or (search_value == 'teacher_id') or (search_value == 'course_work_id'):
          query = conn.execute("with big_table as (SELECT student_submissions.*, student.school, course.teacher_id FROM student_submissions JOIN student ON student_submissions.student_id = student.student_id JOIN course ON student_submissions.course_id = course.course_id) SELECT {0}, COUNT(CASE WHEN status = 'TURNED_IN' THEN 1 ELSE NULL END) AS SubmissionCount FROM big_table GROUP BY {0}".format(search_value))
          query2 = conn.execute("with big_table as (SELECT student_submissions.*, student.school, course.teacher_id FROM student_submissions JOIN student ON student_submissions.student_id = student.student_id JOIN course ON student_submissions.course_id = course.course_id) SELECT {0}, AVG(assigned_points) AS AverageGrade FROM big_table GROUP BY {0}".format(search_value))
          query3 = conn.execute("with big_table as (SELECT student_submissions.*, student.school, course.teacher_id FROM student_submissions JOIN student ON student_submissions.student_id = student.student_id JOIN course ON student_submissions.course_id = course.course_id) SELECT {0}, count(distinct course_work_id) AS Assignments FROM big_table GROUP BY {0}".format(search_value))
          result = {'data1': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor], 'data2': [dict(zip(tuple (query2.keys()) ,i)) for i in query2.cursor], 'data3': [dict(zip(tuple (query3.keys()) ,i)) for i in query3.cursor]}
          return result
        elif search_value == 'school':
          query = conn.execute("with big_table as (select a.student_id, b.school, COUNT(CASE WHEN a.status = 'TURNED_IN' THEN 1 ELSE NULL END) AS SubCount from student_submissions a inner join student b on a.student_id = b.student_id group by a.student_id) select {0}, COUNT(CASE WHEN SubCount > 1 THEN 1 ELSE NULL END)/CAST(COUNT(SubCount) as float) as Percentage from big_table group by {0}".format(search_value))
          result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
          return result
        #elif search_value.lower() == 'teacher_id':
        #  query = conn.execute("SELECT C.teacher_id, COUNT(C.course_work_id) AS AssignmentCount FROM (SELECT DISTINCT B.teacher_id, A.course_work_id FROM student_submissions A INNER JOIN course B ON A.course_id = B.course_id) C GROUP BY teacher_id")
        #  result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        #  return result
        #elif search_value.lower() == 'school_id':
        #  query = conn.execute("SELECT C.school, COUNT(CASE WHEN C.SubCount > 1 THEN 1 ELSE NULL END) AS Complete, COUNT(C.SubCount) AS Total, CAST(COUNT(CASE WHEN C.SubCount > 1 THEN 1 ELSE NULL END) AS float)/CAST(COUNT(C.SubCount) AS float) AS Percent FROM (SELECT A.student_id, A.SubCount, B.school FROM (SELECT student_id, COUNT(CASE WHEN status = 'TURNED_IN' THEN 1 ELSE NULL END) AS SubCount FROM student_submissions GROUP BY student_id) A INNER JOIN student B ON A.student_id = #B.student_id) C GROUP BY C.school")
        #  result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        #  return result
        elif search_value is None:
          return {'Schoolytics API!': 'Please add /students?value=student_id, /students?value=course_id, /students?value=teacher_id, or /students?value=school_id to the path after /.'}
        else:
          return {'Error': 'This is not a search option. Please add /students?value=student_id, /students?value=course_id, /students?value=teacher_id, or /students?value=school_id to the path after /.'}

#class Students_Info(Resource):
#    def get(self):
        #Info for dynamic API
#        return {'Schoolytics API!': 'Please add /student_id, /course_id, /teacher_id, or /school_id to the path after /students/.'}


#api.add_resource(Students_Info, '/students/?value=<string:search_value>')
api.add_resource(Students_Dynamic, '/students')


if __name__ == '__main__':
     app.run()
