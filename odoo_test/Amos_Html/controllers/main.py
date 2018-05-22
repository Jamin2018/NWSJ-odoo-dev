# -*- coding:utf-8 -*-

from odoo import http
from odoo.http import request
import requests
import json



class Pivot(http.Controller):

    @http.route('/NWSJ/pivot-table', auth='public', website=True)
    def pivot_table(self, **kwargs):
        print '==========================='
        try:date = kwargs['date']
        except:date = '1980-01-01 00:00:00 - 2050-01-01 00:00:00'
        if len(date) == 0:date = '1980-01-01 00:00:00 - 2050-01-01 00:00:00'
        try:account = kwargs['account']
        except:account = '.*'
        if len(account) == 0 :account = '.*'
        try:category = kwargs['category']
        except:category = '.*'
        if len(category) == 0: category = '.*'
        try:style = kwargs['style']
        except:style = '.*'
        if len(style) == 0: style = '.*'
        try:color = kwargs['color']
        except:color = '.*'
        if len(color) == 0 : color = '.*'
        try:size = kwargs['size']
        except:size = '.*'
        if len(size) == 0 : size = '.*'


        datas = request.env['amos.html'].search([])
        url = 'http://192.168.0.102:8000/pivot-table-data?date='+date+'&account='+account+'&category='+category+'&style='+style+'&color='+color+'&size='+size
        print url
        obj = requests.get(url)
        datas = json.loads(obj.text)['data']

        return request.render('Amos_Html.pivot_table', {'datas': datas,
                                                        })
    # self.write({'state': 'cancel'})

    @http.route('/NWSJ/pivot-table-data', auth='public', website=True)
    def pivot_table_data(self):
        obj = requests.get('http://192.168.0.102:8000/pivot-table-data/')
        datas = json.loads(obj.text)['data']

        odoo_datas = request.env['amos.html']
        print '==' * 50
        for data in datas:
            domain = [('type','=',data['type'])]
            if odoo_datas.search(domain):
                print '查到相同type:',data['type']
                odoo_datas.search(domain).write(data)
            else:
                print '创建成功'
                odoo_datas.create(data)
        print '==' * 50
        res = {'code':0,'msg':'ok'}
        return res
