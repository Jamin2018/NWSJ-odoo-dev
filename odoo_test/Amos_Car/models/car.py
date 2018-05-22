# -*- coding:utf-8 -*-

from odoo import models,fields,api
from odoo.exceptions import ValidationError,UserError

class Res_Car(models.Model):
    _name = 'res.car'
    _description = 'car'

    name = fields.Char(string=u'车辆名称', size=12, translate=True)
    code = fields.Char(string=u'单据编号', size =64, default='New')
    instructor = fields.Boolean(u'是否停产')
    active = fields.Boolean(u'是否有效?',default=True)
    count = fields.Integer(string=u'数量')
    price = fields.Float(string=u'优惠', default=0.0)   # digits=(16,5)限制长度和保留5位小数,可改为前端限制

    note = fields.Text(u'备注')
    content = fields.Html(u'正文', strip_style=True)

    date = fields.Date(string=u'日期',default=fields.Date.context_today)
    date_order = fields.Datetime(string=u'长日期',copy=False,default=fields.Date.context_today)

    sex = fields.Selection([(0,u'不限'),(1,u'男'),(2,u'女')], string=u'性别')

    # user_id = fields.Many2one('res.users',string=u'业务员',default=lambda self:self.env.user)
    # 关联字段
    user_id = fields.Many2one('res.users',string=u'业务员',)
    func = fields.Char(related='user_id.partner_id.function', string=u'职位')

    lines = fields.One2many('res.car.line', 'order_id', string=u'维修日志')

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


    total = fields.Float(compute='_compute_total',string=u'合计')  # store默认为False,数据裤中不会生成total记录，True会生成 / 报错了，odoo10好像默认会生成记录


    # 自定义 odoo 创建方法
    @api.model
    def create(self, vals):


        print '-----------create----------------'
        '''
        添加操作
        '''
        print vals.get('code')
        if vals.get('code') == 'New':
            print 1234567
        result = super(Res_Car, self).create(vals)
        return result


    # 自定义 odoo 修改方法
    @api.multi
    def write(self, vals):
        print '-----------write---------------'
        '''
        添加操作
        '''
        result = super(Res_Car, self).write(vals)
        return result


    # 自定义 odoo 删除方法
    @api.multi
    def unlink(self):
        print '-----------unlink---------------'
        '''
        添加操作，判断谁可以删除
        '''
        for order in self:
            if order.state != 'draft':
                raise UserError(u'只能删除草稿单据')


        result = super(Res_Car, self).unlink()
        return result



    # 自定义 odoo 浏览方法
    @api.multi
    def read(self, fields = None, load='_classic_read'):
        print '-----------read---------------'
        '''
        添加操作,这里可以设置不同权限的人看不同数据
        '''
        print fields
        fields = [u'name', u'instructor', u'active', u'count']
        result = super(Res_Car, self).read(fields = fields, load = load)
        return result




    @api.depends('lines.price','price')   # 依赖上面的lines对象
    def _compute_total(self):
        acc = 0.00
        for record in self.lines:
            # record.total = record.value + record.value * record.tax
            acc += record.price
        self.total = acc - self.price

    # image = fields.Binary('icon')
    # discount = fields.Float(string=u'折扣(%)',default=0.0)


    @api.multi
    def action_draft(self):
        self.write({'state':'draft'})

    @api.multi
    def action_review(self):
        self.write({'state':'review'})

    @api.multi
    def action_done(self):
        self.write({'state':'done'})

    @api.multi
    def action_cancel(self):
        self.write({'state':'cancel'})

    # 模型 ORM 查询操作
    @api.multi
    def action_amos(self):



        # obj = self.env['res.car'].browse([13,14])   # id查询操作
        # for o in obj:
        #     print o.price



        # obj = self.env['res.car'].search([('name' ,'=','jamin')])
        # values = {
        #     'price':999999,
        #     'state':'done'
        # }
        # obj.write(values)   # 修改操作



        # values = {
        #     'name':'jamin'
        # }
        # self.env['res.car'].create(values)    # 创建操作
        #



        # obj  = self.env['ir.model'].search([])  # 条件查询操作

        # for num in obj:
        #     print num.name
        #     print num.id
        print '----------------------------------------------'
        # print obj._ids
        # self.write({'state':'cancel'})




class Res_Car_Line(models.Model):
    _name = 'res.car.line'
    _description = u'日志'

    name = fields.Char(string=u'备注')

    # 跟上面的lines对应
    order_id = fields.Many2one('res.car', string=u'车辆信息', ondelete='cascade', index=True, copy=False)

    sequence = fields.Integer(string=u'排序', default=10, help = '.')

    # 动态合计,跟上面total对应
    price = fields.Float(string=u'价格', defalut=0.0)

    # _log_access = False # 不自动创建默认字段