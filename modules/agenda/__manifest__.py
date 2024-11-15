# -*- coding: utf-8 -*-
{
    'name': "agenda",

    'summary': "preuba 1",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/grupos.xml',
        'security/ir.model.access.csv',
        'views/estudiante_vista.xml',
        'views/profesor_vista.xml',
        'views/tutor_vista.xml',
        'views/curso_vista.xml',
        'views/materia_vista.xml',
        'views/mis_cursos.xml',
        'views/vista_estudiante.xml',
        'views/vista_tutor.xml',
        'views/tarea_vista.xml',
        'views/mis_tareas.xml',
        'views/enviar_tarea.xml',
        'views/comunicados.xml',
        'views/mis_comunicados.xml',
      
      
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

