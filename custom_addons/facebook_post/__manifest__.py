{
    'name': 'OpenAI Facebook Integration',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Module to generate and post messages to Facebook using OpenAI API',
    'description': """
        A module to generate messages and images using OpenAI API and post them to Facebook.
    """,
    'author': 'ozkilic',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
}