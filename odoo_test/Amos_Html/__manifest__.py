# -*- coding: utf-8 -*-

{
	'name':'数据透视表',
	'description':'Manage your personal To-Do tasks.',
	'author':'Jamin',
	# 'depends':['base','mail'],
	'depends':['base',],
	'application':True,
	'data':[
		'security/ir.model.access.csv',
		# 'security/todo_access_rules.xml',
		'views/amos_html_view.xml',
		'views/pivot_table.xml'
	],
}