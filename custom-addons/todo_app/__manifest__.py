{
	'name':'To-Do Application',
	'description':'Manage your personal To-Do tasks.',
	'author':'Jamin',
	'depends':['base'],
	'application':True,
	'data':[
		'security/ir.model.access.csv',
		'security/todo_access_rules.xml',
		'views/todo_menu.xml',
		'views/todo_view.xml',
	],
}
