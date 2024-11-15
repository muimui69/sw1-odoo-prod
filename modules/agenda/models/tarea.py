from odoo import models, fields,api
import logging

_logger = logging.getLogger(__name__)
class Tarea(models.Model):
    _name = 'agenda.tarea'
    _description = 'Modelo para gestionar tareas'

    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')
    fecha = fields.Date(string='Fecha')
    fecha_entrega = fields.Date(string='Fecha de Entrega')
    materia_id = fields.Many2one('agenda.materia', string='Materia')
    curso_id = fields.Many2one('agenda.curso', string='Curso')
    profesor_id = fields.Many2one('agenda.profesor', string='Profesor')
    archivo_adjuntos_ids = fields.One2many(
        'agenda.archivo_adjunto', 'tarea_id', string='Archivos Adjuntos'
    )
    estudiantes_ids = fields.Many2many(
        'agenda.estudiante',
        string='Estudiantes',
        compute='_compute_estudiantes_ids',
        store=True
    )
    tarea_enviada_ids = fields.One2many('agenda.tarea_enviada', 'tarea_id', string='Tareas Enviadas')


    @api.model
    def create(self, vals):
        if 'profesor_id' not in vals:
            # Busca el profesor relacionado con el usuario logueado
            profesor = self.env['agenda.profesor'].search([('user_id', '=', self.env.uid)], limit=1)
            if profesor:
                _logger.info("Profesor encontrado para el usuario logueado: %s", profesor)
                vals['profesor_id'] = profesor.id
        return super(Tarea, self).create(vals)
    
    @api.depends('curso_id', 'materia_id')
    def _compute_estudiantes_ids(self):
        for record in self:
            if record.curso_id and record.materia_id:
                estudiantes = self.env['agenda.estudiante'].search([
                    ('curso_id', '=', record.curso_id.id),
                    ('materia_ids', 'in', record.materia_id.id)
                ])
                record.estudiantes_ids = estudiantes
            else:
                record.estudiantes_ids = False
    
   