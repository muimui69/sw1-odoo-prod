
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Estudiante(models.Model):
    _name = 'agenda.estudiante'
    _description = 'Estudiante'

    name = fields.Char(string='Nombre', required=True)
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    direccion = fields.Text(string='Dirección')
    telefono = fields.Char(string='Teléfono')
    genero = fields.Selection([
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro')
    ], string='Género')
    carnet = fields.Char(string='Carnet', required=True)
    tutor_id = fields.Many2one('agenda.tutor', string='Tutor')
    registro = fields.Char(string='Registro Académico')
    curso_id = fields.Many2one('agenda.curso', string='curso')
    user_id = fields.Many2one('res.users', string='Usuario')
    materia_ids = fields.Many2many('agenda.materia', string='Materias', compute='_compute_materias', store=True)
    fecha_ingreso = fields.Datetime(string='Fecha de Ingreso', default=fields.Datetime.now)
    active = fields.Boolean(string='Activo', default=True)
    
    @api.depends('curso_id')
    def _compute_materias(self):
        for estudiante in self:
            estudiante.materia_ids = estudiante.curso_id.materia_ids

    @api.model
    def create(self, vals):
        ultimo_registro = self.env['agenda.estudiante'].search([], order='id desc', limit=1)
        if ultimo_registro:
            vals['registro'] =int(ultimo_registro.registro) + 1
        else:
            vals['registro'] = 1001

        if self.search([('carnet', '=', vals['carnet'])]):
            raise ValidationError('El carnet ya existe')
        
        user_vals = {
            'name': vals['name'],
            'login': vals['registro'],
            'password': vals['carnet'],
            'groups_id': [(4, self.env.ref('agenda.group_estudiante').id),
              (4, self.env.ref('base.group_user').id)]
        }

        user = self.env['res.users'].create(user_vals)
        vals['user_id'] = user.id
        return super(Estudiante, self).create(vals)

    