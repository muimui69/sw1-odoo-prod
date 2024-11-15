from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class ProfesorController(http.Controller):

    # Obtener todos los profesores con datos relacionados
    @http.route('/api/profesores', type='json', auth='public', methods=['GET'], csrf=False)
    def get_profesores(self):
        profesores = request.env['agenda.profesor'].sudo().search([])
        data = []
        for prof in profesores:
            data.append({
                'id': prof.id,
                'name': prof.name,
                'fecha_nacimiento': prof.fecha_nacimiento,
                'direccion': prof.direccion,
                'telefono': prof.telefono,
                'email': prof.email,
                'genero': prof.genero,
                'carnet': prof.carnet,
                'registro': prof.registro,
                'user_id': {'id': prof.user_id.id, 'name': prof.user_id.name} if prof.user_id else None,
                'materia': {'id': prof.materia_id.id, 'name': prof.materia_id.name} if prof.materia_id else None,
                'cursos': [{'id': curso.id, 'name': curso.name} for curso in prof.curso_ids],
                'active': prof.active,
            })
        return data

    # Obtener un profesor por ID con datos relacionados
    @http.route('/api/profesores/<int:profesor_id>', type='json', auth='public', methods=['GET'], csrf=False)
    def get_profesor(self, profesor_id):
        profesor = request.env['agenda.profesor'].sudo().browse(profesor_id)
        if not profesor.exists():
            return {'error': 'Profesor no encontrado'}
        return {
            'id': profesor.id,
            'name': profesor.name,
            'fecha_nacimiento': profesor.fecha_nacimiento,
            'direccion': profesor.direccion,
            'telefono': profesor.telefono,
            'email': profesor.email,
            'genero': profesor.genero,
            'carnet': profesor.carnet,
            'registro': profesor.registro,
            'user_id': {'id': profesor.user_id.id, 'name': profesor.user_id.name} if profesor.user_id else None,
            'materia': {'id': profesor.materia_id.id, 'name': profesor.materia_id.name} if profesor.materia_id else None,
            'cursos': [{'id': curso.id, 'name': curso.name} for curso in profesor.curso_ids],
            'active': profesor.active,
        }

    # Crear un profesor
    @http.route('/api/profesores', type='json', auth='public', methods=['POST'], csrf=False)
    def create_profesor(self, **kwargs):
        try:
            vals = {
                'name': kwargs.get('name'),
                'fecha_nacimiento': kwargs.get('fecha_nacimiento'),
                'direccion': kwargs.get('direccion'),
                'telefono': kwargs.get('telefono'),
                'email': kwargs.get('email'),
                'genero': kwargs.get('genero'),
                'carnet': kwargs.get('carnet'),
                'materia_id': kwargs.get('materia_id'),
                'curso_ids': [(6, 0, kwargs.get('curso_ids', []))]
            }
            profesor = request.env['agenda.profesor'].sudo().create(vals)
            return {'id': profesor.id, 'message': 'Profesor creado exitosamente'}
        except Exception as e:
            _logger.error(f"Error al crear profesor: {e}")
            return {'error': str(e)}

    # Actualizar un profesor
    @http.route('/api/profesores/<int:profesor_id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update_profesor(self, profesor_id, **kwargs):
        profesor = request.env['agenda.profesor'].sudo().browse(profesor_id)
        if not profesor.exists():
            return {'error': 'Profesor no encontrado'}
        try:
            profesor.write(kwargs)
            return {'message': 'Profesor actualizado exitosamente'}
        except Exception as e:
            _logger.error(f"Error al actualizar profesor: {e}")
            return {'error': str(e)}

    # Eliminar un profesor
    @http.route('/api/profesores/<int:profesor_id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete_profesor(self, profesor_id):
        profesor = request.env['agenda.profesor'].sudo().browse(profesor_id)
        if not profesor.exists():
            return {'error': 'Profesor no encontrado'}
        try:
            profesor.unlink()
            return {'message': 'Profesor eliminado exitosamente'}
        except Exception as e:
            _logger.error(f"Error al eliminar profesor: {e}")
            return {'error': str(e)}
