# -*- coding:utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError



class Tag(models.Model):
    _name = 'todo.task.tag'
    _description = 'To-do Tag'

    name = fields.Char('Name', 40, translate=True)

    task_ids = fields.Many2many('todo.task', string='Tasks')


class Tags(models.Model):
    _name = 'todo.task.tag'
    _description = 'To-do Tag'
    _parent_store = True


    name = fields.Char('Name')

    parent_id = fields.Many2one('todo.task', 'Parent Tag', ondelete='restrict')
    child_ids = fields.One2many('todo.task.tag', 'parent_id', 'Child Tags')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)



class Stage(models.Model):
    _name = 'todo.task.stage'
    _description = 'To-do Stage'

    _order = 'sequence, name'

    # String fields
    name = fields.Char('Name', 40, translate=True)
    desc = fields.Text('Description')
    state = fields.Selection(
        [('draft','New'),('open','Started'),('done','Closed')],
        'State'
    )
    docs = fields.Html('Documentation')

    # Numeric fields
    sequence = fields.Integer('Sequence')
    perc_complete = fields.Float('% Complete',(3,2))

    # Date fields
    date_effective = fields.Date('Effective Date')
    date_changed = fields.Datetime('Last Changed')

    # Other fields
    fold = fields.Boolean('Folded?')
    image = fields.Binary('Image')


    tasks = fields.One2many('todo.task', 'stage_id', 'Tasks in this stage')

class TodoTask(models.Model):
    _inherits = 'todo.task'
    # 模型约束
    _sql_constraints = [
        ('todo_task_name_uniq',
         'UNIQUE(name,active)',
         'Task title must be unique!')
    ]


    text = fields.Char('测试字段')
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    tag_ids = fields.Many2many('todo.task.tag', string='Tags')

    stage_state = fields.Selection(
        related = 'stage_id.state',
        string='Stage_state'
    )

#     # 不知道会不会报错
    refers_to = fields.Reference('referenceable_models', 'Refers to')

    stage_fold = fields.Boolean('Stage Folded?', compute = '_compute_stage_fold', search='_search_stage_fold', inverse='_write_stage_fold')

    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]

    def _write_stage_fold(self):
        self.stage_id.fold = self.stage_fold


    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        for task in self:
            task.stage_fold = task.stage_id.fold

    # 模型约束
    @api.constrains('name')
    def _check_name_size(self):
        for todo in self:
            if len(todo.name) <5:
                raise ValidationError('Must have 5 chars!')
