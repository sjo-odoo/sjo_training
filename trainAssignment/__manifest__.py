{
    'name':'TrainAssignment',
    'version':'1.0',
    'author':'shubhamj',
    'category':'Uncategorized',
    'depends':['base','website'],
    'installable':True,
    'application':True,
    'data':[
        'views/views.xml',
        'demo/demo.xml',
        'demo/template.xml',
        'security/ir.model.access.csv',
        'views/assets.xml'
    ],
    'qweb': [
        'static/src/xml/train_widget.xml',
    ]
}