from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
class TareaEnviada(models.Model):
    _name = 'agenda.tarea_enviada'
    _description = 'Modelo para gestionar tareas enviadas'

    name = fields.Char(string='Nombre', required=True)
    tarea_id = fields.Many2one('agenda.tarea', string='Tarea', required=True, domain="[('estudiantes_ids.user_id', '=', uid)]")
    estudiante_id = fields.Many2one(
        'agenda.estudiante',
        string='Estudiante',
        required=True,
        compute='_compute_estudiante_id',
        store=True,
        readonly=True
    )
    archivo_adjunto_ids = fields.One2many(
        'agenda.archivo_adjunto', 'tarea_enviada_id', string='Archivos Adjuntos'
    )
    estado_envio = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
    ], string='Estado de Envío', default='pendiente')

    @api.model
    def create(self, vals):
        # Obtener el estudiante asociado al usuario logueado
        estudiante = self.env['agenda.estudiante'].search([('user_id', '=', self.env.uid)], limit=1)
        if estudiante:
            vals['estudiante_id'] = estudiante.id
        else:
            raise UserError('No se pudo encontrar un estudiante asociado al usuario actual.')
        
        # Crear el registro con el estudiante asignado
        return super(TareaEnviada, self).create(vals)
    
    @api.onchange('archivo_adjunto_ids')
    def _onchange_archivo_adjunto_ids(self):
        """Marcar la tarea como enviada automáticamente cuando se adjunta un archivo."""
        if self.archivo_adjunto_ids:
            self.estado_envio = 'enviado'
        else:
            self.estado_envio = 'pendiente'
