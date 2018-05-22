# -*- coding:utf-8 -*-

from odoo import http
from main import Todo

class TodoExtended(Todo):
    @http.route()
    def hello(self,name=None,**kwargs):
        response = super(TodoExtended,self).hello()
        response.qcontext['name'] = name
        return response


    @http.route('/hellocms/<page>', auth='public')
    def hellocms(self, page, **kwargs):
        return http.request.render(page)