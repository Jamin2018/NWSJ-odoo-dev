# -*- coding:utf-8 -*-

from odoo import models,fields,api
from odoo.exceptions import ValidationError

class car(models.Model):
    _inherit = 'res.car'

    note_p = fields.Text(u'补充说明')