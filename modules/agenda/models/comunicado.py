from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class Comunicado(models.Model):
    _name = 'agenda.comunicado'
    _description = 'Modelo para gestionar comunicados'

    titulo = fields.Char(string='Título', required=True)
    mensaje = fields.Text(string='Mensaje', required=True)
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today)
    tipo_destinatario_general = fields.Selection([
        ('todos_profesores', 'Todos los profesores'),
        ('todos_estudiantes', 'Todos los estudiantes'),
        ('todos_tutores', 'Todos los tutores'),
        ('profesores_curso', 'Profesores de cursos específicos'),
        ('estudiantes_curso', 'Estudiantes de cursos específicos'),
        ('tutores_curso', 'Tutores de cursos específicos')
    ], string='Tipo de Destinatario', required=True)
    curso_ids = fields.Many2many('agenda.curso', string='Cursos')
    profesor_ids = fields.Many2many('agenda.profesor', string='Profesores Destinatarios')
    estudiante_ids = fields.Many2many('agenda.estudiante', string='Estudiantes Destinatarios')
    tutor_ids = fields.Many2many('agenda.tutor', string='Tutores Destinatarios')
    adjunto_ids = fields.One2many('agenda.archivo_adjunto', 'comunicado_id', string='Archivos Adjuntos')
    def enviar_comunicado(self):
        """Envía el comunicado a los destinatarios seleccionados."""
        for record in self:
            destinatarios = []

            if record.tipo_destinatario_general == 'todos_profesores':
                destinatarios = self.env['agenda.profesor'].search([])
                record.profesor_ids = destinatarios
            elif record.tipo_destinatario_general == 'todos_estudiantes':
                destinatarios = self.env['agenda.estudiante'].search([])
                record.estudiante_ids = destinatarios
            elif record.tipo_destinatario_general == 'todos_tutores':
                destinatarios = self.env['agenda.tutor'].search([])
                record.tutor_ids = destinatarios
            elif record.tipo_destinatario_general == 'profesores_curso':
                if not record.curso_ids:
                    raise ValidationError("Debe seleccionar al menos un curso.")
                destinatarios = self.env['agenda.profesor'].search([('curso_ids', 'in', record.curso_ids.ids)])
                record.profesor_ids = destinatarios
            elif record.tipo_destinatario_general == 'estudiantes_curso':
                if not record.curso_ids:
                    raise ValidationError("Debe seleccionar al menos un curso.")
                destinatarios = self.env['agenda.estudiante'].search([('curso_id', 'in', record.curso_ids.ids)])
                record.estudiante_ids = destinatarios
            elif record.tipo_destinatario_general == 'tutores_curso':
                if not record.curso_ids:
                    raise ValidationError("Debe seleccionar al menos un curso.")
                estudiantes = self.env['agenda.estudiante'].search([('curso_id', 'in', record.curso_ids.ids)])
                destinatarios = estudiantes.mapped('tutor_id')
                record.tutor_ids = destinatarios

            if not destinatarios:
                raise ValidationError("No se encontraron destinatarios para el tipo seleccionado o cursos específicos.")

            # Se ha eliminado la lógica de envío de notificaciones
            _logger.info(f"Comunicado '{record.titulo}' preparado para {len(destinatarios)} destinatarios.")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Comunicado preparado',
                'message': 'El comunicado ha sido preparado y asociado a los destinatarios.',
                'type': 'success',
                'sticky': False,
            },
        }

    @api.onchange('tipo_destinatario_general')
    def _onchange_tipo_destinatario_general(self):
        # Verificamos que tipo_destinatario_general tenga un valor
        if self.tipo_destinatario_general:
            # Si 'curso' no está en el valor de tipo_destinatario_general, limpiamos curso_ids
            if 'curso' not in self.tipo_destinatario_general:
                self.curso_ids = False
        else:
            # Si tipo_destinatario_general es False o None, también limpiamos curso_ids
            self.curso_ids = False
