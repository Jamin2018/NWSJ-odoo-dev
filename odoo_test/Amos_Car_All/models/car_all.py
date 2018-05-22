# -*- coding:utf-8 -*-

from odoo import models,fields,api
from odoo.exceptions import ValidationError

class car_all(models.Model):
    _name = 'car.all'
    _inherits = {'res.car':'order_id'}

    qty = fields.Integer(string=u'数量', default=0)

    order_id = fields.Many2one('res.car', string=u'name')