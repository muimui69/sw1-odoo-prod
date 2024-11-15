from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class TareaController(http.Controller):

    # Obtener todas las tareas con datos relacionados
    @http.route('/api/tareas', type='json', auth='public', methods=['GET'], csrf=False)
    def get_tareas(self):
        tareas = request.env['agenda.tarea'].sudo().search([])
        data = []
        for tarea in tareas:
            data.append({
                'id': tarea.id,
                'name': tarea.name,
                'descripcion': tarea.descripcion,
                'fecha': tarea.fecha,
                'fecha_entrega': tarea.fecha_entrega,
                'materia': {'id': tarea.materia_id.id, 'name': tarea.materia_id.name} if tarea.materia_id else None,
                'curso': {'id': tarea.curso_id.id, 'name': tarea.curso_id.name} if tarea.curso_id else None,
                'profesor': {'id': tarea.profesor_id.id, 'name': tarea.profesor_id.name} if tarea.profesor_id else None,
                'estudiantes': [{'id': estudiante.id, 'name': estudiante.name} for estudiante in tarea.estudiantes_ids],
                'archivos_adjuntos': [{'id': adjunto.id, 'archivo_nombre': adjunto.archivo_nombre} for adjunto in tarea.archivo_adjuntos_ids],
            })
        return data

    # Obtener una tarea por ID con datos relacionados
    @http.route('/api/tareas/<int:tarea_id>', type='json', auth='public', methods=['GET'], csrf=False)
    def get_tarea(self, tarea_id):
        tarea = request.env['agenda.tarea'].sudo().browse(tarea_id)
        if not tarea.exists():
            return {'error': 'Tarea no encontrada'}
        return {
            'id': tarea.id,
            'name': tarea.name,
            'descripcion': tarea.descripcion,
            'fecha': tarea.fecha,
            'fecha_entrega': tarea.fecha_entrega,
            'materia': {'id': tarea.materia_id.id, 'name': tarea.materia_id.name} if tarea.materia_id else None,
            'curso': {'id': tarea.curso_id.id, 'name': tarea.curso_id.name} if tarea.curso_id else None,
            'profesor': {'id': tarea.profesor_id.id, 'name': tarea.profesor_id.name} if tarea.profesor_id else None,
            'estudiantes': [{'id': estudiante.id, 'name': estudiante.name} for estudiante in tarea.estudiantes_ids],
            'archivos_adjuntos': [{'id': adjunto.id, 'archivo_nombre': adjunto.archivo_nombre} for adjunto in tarea.archivo_adjuntos_ids],
        }

    # Crear una nueva tarea
    @http.route('/api/tareas', type='json', auth='public', methods=['POST'], csrf=False)
    def create_tarea(self, **kwargs):
        try:
            vals = {
                'name': kwargs.get('name'),
                'descripcion': kwargs.get('descripcion'),
                'fecha': kwargs.get('fecha'),
                'fecha_entrega': kwargs.get('fecha_entrega'),
                'materia_id': kwargs.get('materia_id'),
                'curso_id': kwargs.get('curso_id'),
                'archivo_adjuntos_ids': [(0, 0, adjunto) for adjunto in kwargs.get('archivo_adjuntos', [])]
            }
            tarea = request.env['agenda.tarea'].sudo().create(vals)
            return {'id': tarea.id, 'message': 'Tarea creada exitosamente'}
        except Exception as e:
            _logger.error(f"Error al crear tarea: {e}")
            return {'error': str(e)}

    # Actualizar una tarea
    @http.route('/api/tareas/<int:tarea_id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update_tarea(self, tarea_id, **kwargs):
        tarea = request.env['agenda.tarea'].sudo().browse(tarea_id)
        if not tarea.exists():
            return {'error': 'Tarea no encontrada'}
        try:
            tarea.write(kwargs)
            return {'message': 'Tarea actualizada exitosamente'}
        except Exception as e:
            _logger.error(f"Error al actualizar tarea: {e}")
            return {'error': str(e)}

    # Eliminar una tarea
    @http.route('/api/tareas/<int:tarea_id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete_tarea(self, tarea_id):
        tarea = request.env['agenda.tarea'].sudo().browse(tarea_id)
        if not tarea.exists():
            return {'error': 'Tarea no encontrada'}
        try:
            tarea.unlink()
            return {'message': 'Tarea eliminada exitosamente'}
        except Exception as e:
            _logger.error(f"Error al eliminar tarea: {e}")
            return {'error': str(e)}
