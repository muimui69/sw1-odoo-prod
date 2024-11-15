from odoo import http
from odoo.http import request
import logging
import json

_logger = logging.getLogger(__name__)

class ComunicadoController(http.Controller):

    # Obtener todos los comunicados con datos relacionados
    @http.route('/api/comunicados', type='json', auth='public', methods=['GET'], csrf=False)
    def get_comunicados(self):
        comunicados = request.env['agenda.comunicado'].sudo().search([])
        data = []
        for com in comunicados:
            data.append({
                'id': com.id,
                'titulo': com.titulo,
                'mensaje': com.mensaje,
                'fecha': com.fecha,
                'tipo_destinatario_general': com.tipo_destinatario_general,
                'cursos': [{'id': curso.id, 'name': curso.name} for curso in com.curso_ids],
                'profesores': [{'id': profesor.id, 'name': profesor.name} for profesor in com.profesor_ids],
                'estudiantes': [{'id': estudiante.id, 'name': estudiante.name} for estudiante in com.estudiante_ids],
                'tutores': [{'id': tutor.id, 'name': tutor.name} for tutor in com.tutor_ids],
                'adjuntos': [{'id': adjunto.id, 'archivo_nombre': adjunto.archivo_nombre} for adjunto in com.adjunto_ids],
            })
        return data

    # Obtener un comunicado por ID con datos relacionados
    @http.route('/api/comunicados/<int:comunicado_id>', type='json', auth='public', methods=['GET'], csrf=False)
    def get_comunicado(self, comunicado_id):
        comunicado = request.env['agenda.comunicado'].sudo().browse(comunicado_id)
        if not comunicado.exists():
            return {'error': 'Comunicado no encontrado'}
        return {
            'id': comunicado.id,
            'titulo': comunicado.titulo,
            'mensaje': comunicado.mensaje,
            'fecha': comunicado.fecha,
            'tipo_destinatario_general': comunicado.tipo_destinatario_general,
            'cursos': [{'id': curso.id, 'name': curso.name} for curso in comunicado.curso_ids],
            'profesores': [{'id': profesor.id, 'name': profesor.name} for profesor in comunicado.profesor_ids],
            'estudiantes': [{'id': estudiante.id, 'name': estudiante.name} for estudiante in comunicado.estudiante_ids],
            'tutores': [{'id': tutor.id, 'name': tutor.name} for tutor in comunicado.tutor_ids],
            'adjuntos': [{'id': adjunto.id, 'archivo_nombre': adjunto.archivo_nombre} for adjunto in comunicado.adjunto_ids],
        }
