from odoo import models, fields, api

class ArchivoAdjunto(models.Model):
    _name = 'agenda.archivo_adjunto'
    _description = 'Modelo para almacenar archivos adjuntos'

    archivo = fields.Binary(string='Archivo Adjunto', required=True)
    archivo_nombre = fields.Char(string='Nombre del Archivo')
    tarea_id = fields.Many2one('agenda.tarea', string='Tarea', ondelete='cascade')
    tarea_enviada_id = fields.Many2one('agenda.tarea_enviada', string='Tarea Enviada', ondelete='cascade')
    comunicado_id = fields.Many2one('agenda.comunicado', string='Comunicado', ondelete='cascade') 
