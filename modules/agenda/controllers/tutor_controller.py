from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class TutorController(http.Controller):

    # Obtener todos los tutores con datos relacionados
    @http.route('/api/tutores', type='json', auth='public', methods=['GET'], csrf=False)
    def get_tutores(self):
        tutores = request.env['agenda.tutor'].sudo().search([])
        data = []
        for tutor in tutores:
            data.append({
                'id': tutor.id,
                'name': tutor.name,
                'fecha_nacimiento': tutor.fecha_nacimiento,
                'direccion': tutor.direccion,
                'telefono': tutor.telefono,
                'email': tutor.email,
                'parentesco': tutor.parentesco,
                'genero': tutor.genero,
                'carnet': tutor.carnet,
                'registro': tutor.registro,
                'user_id': {'id': tutor.user_id.id, 'name': tutor.user_id.name} if tutor.user_id else None,
                'estudiantes': [{'id': estudiante.id, 'name': estudiante.name} for estudiante in tutor.estudiante_ids],
                'active': tutor.active,
            })
        return data

    # Obtener un tutor por ID con datos relacionados
    @http.route('/api/tutores/<int:tutor_id>', type='json', auth='public', methods=['GET'], csrf=False)
    def get_tutor(self, tutor_id):
        tutor = request.env['agenda.tutor'].sudo().browse(tutor_id)
        if not tutor.exists():
            return {'error': 'Tutor no encontrado'}
        return {
            'id': tutor.id,
            'name': tutor.name,
            'fecha_nacimiento': tutor.fecha_nacimiento,
            'direccion': tutor.direccion,
            'telefono': tutor.telefono,
            'email': tutor.email,
            'parentesco': tutor.parentesco,
            'genero': tutor.genero,
            'carnet': tutor.carnet,
            'registro': tutor.registro,
            'user_id': {'id': tutor.user_id.id, 'name': tutor.user_id.name} if tutor.user_id else None,
            'estudiantes': [{'id': estudiante.id, 'name': estudiante.name} for estudiante in tutor.estudiante_ids],
            'active': tutor.active,
        }

    # Crear un tutor
    @http.route('/api/tutores', type='json', auth='public', methods=['POST'], csrf=False)
    def create_tutor(self, **kwargs):
        try:
            vals = {
                'name': kwargs.get('name'),
                'fecha_nacimiento': kwargs.get('fecha_nacimiento'),
                'direccion': kwargs.get('direccion'),
                'telefono': kwargs.get('telefono'),
                'email': kwargs.get('email'),
                'parentesco': kwargs.get('parentesco'),
                'genero': kwargs.get('genero'),
                'carnet': kwargs.get('carnet'),
                'estudiante_ids': [(6, 0, kwargs.get('estudiante_ids', []))]
            }
            tutor = request.env['agenda.tutor'].sudo().create(vals)
            return {'id': tutor.id, 'message': 'Tutor creado exitosamente'}
        except Exception as e:
            _logger.error(f"Error al crear tutor: {e}")
            return {'error': str(e)}

    # Actualizar un tutor
    @http.route('/api/tutores/<int:tutor_id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update_tutor(self, tutor_id, **kwargs):
        tutor = request.env['agenda.tutor'].sudo().browse(tutor_id)
        if not tutor.exists():
            return {'error': 'Tutor no encontrado'}
        try:
            tutor.write(kwargs)
            return {'message': 'Tutor actualizado exitosamente'}
        except Exception as e:
            _logger.error(f"Error al actualizar tutor: {e}")
            return {'error': str(e)}

    # Eliminar un tutor
    @http.route('/api/tutores/<int:tutor_id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete_tutor(self, tutor_id):
        tutor = request.env['agenda.tutor'].sudo().browse(tutor_id)
        if not tutor.exists():
            return {'error': 'Tutor no encontrado'}
        try:
            tutor.unlink()
            return {'message': 'Tutor eliminado exitosamente'}
        except Exception as e:
            _logger.error(f"Error al eliminar tutor: {e}")
            return {'error': str(e)}
