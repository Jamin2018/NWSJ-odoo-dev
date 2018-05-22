# -*- coding:utf-8 -*-

from odoo import http
from odoo.http import request
# import requests


class Todo(http.Controller):

    @http.route('/helloworld',auth='public')
    def hello_world(self):
        return '''
               <!DOCTYPE html>
               <html>
               <head>
               <meta charset="utf-8">
               <title></title>
               <style type="text/css">
               *{margin:0;padding:0;}
               </style>
               
               </head>
               <body>
               <div style="position:fixed; height:100%; width:100%">
               <iframe src="http://192.168.0.105:8000" style="height:100%;width:100%">
               <p>不支持iframe</p>
               </iframe>
               </div>
               </body>
               </html>
        '''

    @http.route('/hello', auth='public',website=True)
    def hello(self,**kwargs):
        return request.render('todo_website.hello')
    #
    @http.route('/todo', auth='user', website=True)
    def index(self, **kwargs):
        TodoTask = request.env['todo.task']
        tasks = TodoTask.search([])
        return request.render('todo_website.index',{'tasks':tasks})


    @http.route('/todo/<model("todo.task"):task>', website=True)
    def detail(self, task, **kwargs):
        return request.render('todo_website.detail', {'task': task})


    @http.route('/todo/add', website=True)
    def add(self, **kwargs):
        users = request.env['res.users'].search([])
        return request.render('todo_website.add', {'users': users})


    @http.route('/hello1', auth='public',website=True)
    def hello1(self,**kwargs):
        # return request.render('todo_website.hello1')
        return '''
        <h1>1111111111</h1>
        '''
