# -*- coding:utf-8 -*-

from odoo import models,fields,api
from odoo.exceptions import ValidationError
import requests
from odoo import http
from odoo.http import request
import json


class amos_html(models.Model):
    _name = 'amos.html'
    _description = u'模板'

    # _inherit = ['mail.thread', 'ir.needactiion_mixin']

    type=fields.Char(string=u'类型')
    order_number=fields.Char(string=u'订单数量')
    order_amount=fields.Char(string=u'订单金额')
    refund_number=fields.Char(string=u'退款数量')
    refund_amount=fields.Char(string=u'退款金额')
    refund_rate=fields.Char(string=u'退款率')
    freight_cost=fields.Char(string=u'运费成本')
    active = fields.Boolean(string=u'有效？', default=True)
    N = fields.Char(string=u'缺失',default='None')

    state = fields.Selection([
        ('draft',u'草稿'),
        ('review',u'等待审核'),
        ('done',u'已完成'),
        ('cancel',u'取消')
    ],string='Status', index=True, readonly=True,default='draft',
    track_visibility='onchange', copy=False,
    help=u"* 'Draft' 制单.\n "
         u"* 'review' 制单完成后提交审核.\n"
         u"* 'done' 主管部门审核.\n"
         u"* 'cancel' 取消单据")

    @api.multi
    def action_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def action_review(self):
        self.write({'state': 'review'})

    @api.multi
    def action_done(self):
        self.write({'state': 'done'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def action_amos(self):
        obj = requests.get('http://192.168.0.105:8000/pivot-table-data/')
        datas = json.loads(obj.text)['data']
        print '==' * 50
        for data in datas:
            domain = [('type','=',data['type'])]
            if self.search(domain):
                print '查到相同type:',data['type']
                self.search(domain).write(data)
            else:
                print '创建成功'
                self.create(data)
        print '==' * 50


    # # 自定义 odoo 浏览方法
    # @api.multi
    # def read(self, fields = None, load='_classic_read'):
    #     print '-----------read---------------'
    #     '''
    #     添加操作,这里可以设置不同权限的人看不同数据
    #     '''
    #     fields = [ u'order_number', u'refund_number',u'type',u'N']
    #     result = super(amos_html, self).read(fields = fields, load = load)
    #     return result