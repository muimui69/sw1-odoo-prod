from odoo import models, fields

class Curso(models.Model):
    _name = 'agenda.curso'
    _description = 'Curso'

    name = fields.Char(string='Nombre', required=True)
    nivel=fields.Selection([
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria'),
    ], string='Nivel')
    materia_ids = fields.Many2many('agenda.materia', string='Materias')
    estudiante_ids = fields.One2many('agenda.estudiante', 'curso_id', string='Estudiantes')
    profesor_ids = fields.Many2many('agenda.profesor', string='Profesores')