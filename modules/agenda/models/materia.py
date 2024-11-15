from odoo import models, fields

class Materia(models.Model):
    _name = 'agenda.materia'
    _description = 'Materia'

    name = fields.Char(string='Nombre', required=True)
    descripcion=fields.Text(string='Descripción')
    profesor_ids = fields.One2many('agenda.profesor', 'materia_id', string='Profesores')
    curso_ids = fields.Many2many('agenda.curso', string='Cursos')
    estudiante_ids = fields.Many2many('agenda.estudiante', string='Estudiantes')