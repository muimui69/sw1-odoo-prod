from odoo import http
from odoo.http import request, Response
import json

class EstudianteController(http.Controller):

    @http.route('/api/estudiantes', type='json', auth='public', methods=['GET'], csrf=False)
    def get_estudiantes(self):
        estudiantes = request.env['agenda.estudiante'].sudo().search([])
        data = []
        for est in estudiantes:
            data.append({
                'id': est.id,
                'name': est.name,
                'fecha_nacimiento': est.fecha_nacimiento,
                'direccion': est.direccion,
                'telefono': est.telefono,
                'genero': est.genero,
                'carnet': est.carnet,
                'registro': est.registro,
                'curso_id': est.curso_id.id,
                'user_id': est.user_id.id,
                'fecha_ingreso': est.fecha_ingreso,
                'active': est.active
            })
        return data

    @http.route('/api/estudiantes', type='json', auth='public', methods=['POST'], csrf=False)
    def create_estudiante(self, **kwargs):
        vals = {
            'name': kwargs.get('name'),
            'fecha_nacimiento': kwargs.get('fecha_nacimiento'),
            'direccion': kwargs.get('direccion'),
            'telefono': kwargs.get('telefono'),
            'genero': kwargs.get('genero'),
            'carnet': kwargs.get('carnet'),
            'curso_id': kwargs.get('curso_id'),
        }
        try:
            estudiante = request.env['agenda.estudiante'].sudo().create(vals)
            return {'id': estudiante.id, 'message': 'Estudiante creado exitosamente'}
        except Exception as e:
            return {'error': str(e)}

    @http.route('/api/estudiantes/<int:estudiante_id>', type='json', auth='public', methods=['GET'], csrf=False)
    def get_estudiante(self, estudiante_id):
        estudiante = request.env['agenda.estudiante'].sudo().browse(estudiante_id)
        if estudiante.exists():
            return {
                'id': estudiante.id,
                'name': estudiante.name,
                'fecha_nacimiento': estudiante.fecha_nacimiento,
                'direccion': estudiante.direccion,
                'telefono': estudiante.telefono,
                'genero': estudiante.genero,
                'carnet': estudiante.carnet,
                'registro': estudiante.registro,
                'curso_id': estudiante.curso_id.id,
                'user_id': estudiante.user_id.id,
                'fecha_ingreso': estudiante.fecha_ingreso,
                'active': estudiante.active
            }
        return {'error': 'Estudiante no encontrado'}

    @http.route('/api/estudiantes/<int:estudiante_id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update_estudiante(self, estudiante_id, **kwargs):
        estudiante = request.env['agenda.estudiante'].sudo().browse(estudiante_id)
        if not estudiante.exists():
            return {'error': 'Estudiante no encontrado'}
        estudiante.write(kwargs)
        return {'message': 'Estudiante actualizado exitosamente'}

    @http.route('/api/estudiantes/<int:estudiante_id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete_estudiante(self, estudiante_id):
        estudiante = request.env['agenda.estudiante'].sudo().browse(estudiante_id)
        if estudiante.exists():
            estudiante.unlink()
            return {'message': 'Estudiante eliminado exitosamente'}
        return {'error': 'Estudiante no encontrado'}
