

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Tutor(models.Model):
    _name = 'agenda.tutor'
    _description = 'tutor de estudiantes'

    name = fields.Char(string='Nombre', required=True)
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    direccion = fields.Text(string='Dirección')
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo Electrónico')
    parentesco = fields.Char(string='Parentesco')
    genero = fields.Selection([
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro')
    ], string='Género')
    carnet = fields.Char(string='Carnet', required=True)
    registro = fields.Char(string='Registro Académico')
    user_id = fields.Many2one('res.users', string='Usuario')
    active = fields.Boolean(string='Activo', default=True)
    estudiante_ids = fields.One2many('agenda.estudiante', 'tutor_id', string='Estudiantes')

   
    @api.model
    def create(self, vals):
        ultimo_registro = self.env['agenda.tutor'].search([], order='id desc', limit=1)
        if ultimo_registro:
            vals['registro'] =int(ultimo_registro.registro) + 1
        else:
            vals['registro'] = 1

        if self.search([('carnet', '=', vals['carnet'])]):
            raise ValidationError('El carnet ya existe')
        
        user_vals = {
            'name': vals['name'],
            'login': vals['registro'],
            'password': vals['carnet'],
            'groups_id': [(4, self.env.ref('agenda.group_tutor').id),
              (4, self.env.ref('base.group_user').id)]
        }

        user = self.env['res.users'].create(user_vals)
        vals['user_id'] = user.id
        return super(Tutor, self).create(vals)

    