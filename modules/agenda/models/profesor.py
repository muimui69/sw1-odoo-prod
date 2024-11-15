
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

class Profesor(models.Model):
    _name = 'agenda.profesor'
    _description = 'profesor'

    name = fields.Char(string='Nombre', required=True)
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    direccion = fields.Text(string='Dirección')
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo Electrónico')
    genero = fields.Selection([
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro')
    ], string='Género')
    carnet = fields.Char(string='Carnet', required=True)
    registro = fields.Char(string='Registro Académico')
    user_id = fields.Many2one('res.users', string='Usuario')
    active = fields.Boolean(string='Activo', default=True)
    materia_id=fields.Many2one('agenda.materia', string='Materias')
    curso_ids = fields.Many2many('agenda.curso',  string='Cursos que Imparte')


    @api.model
    def create(self, vals):
        ultimo_registro = self.env['agenda.profesor'].search([], order='id desc', limit=1)



        if ultimo_registro:
            vals['registro'] =int(ultimo_registro.registro) + 1
        else:
            vals['registro'] = 500

        if self.search([('carnet', '=', vals['carnet'])]):
            raise ValidationError('El carnet ya existe')
        
        user_vals = {
            'name': vals['name'],
            'login': vals['registro'],
            'password': vals['carnet'],
            'groups_id': [(4, self.env.ref('agenda.group_profesor').id),
              (4, self.env.ref('base.group_user').id)]
        }

        user = self.env['res.users'].create(user_vals)
        vals['user_id'] = user.id
        return super(Profesor, self).create(vals)

    