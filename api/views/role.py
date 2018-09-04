"""Module for role resources"""

from flask_restplus import Resource
from flask import jsonify
from main import api
from api.utilities.model_serializers.role import RoleSchema
from api.middlewares.token_required import token_required
from ..models.role import Role
from ..utilities.messages.success_messages import SUCCESS_MESSAGES


@api.route('/roles')
class RoleResource(Resource):
    """
    Resource class for creating and getting roles
    """

    @token_required
    def get(self):
        """
        Gets list of all roles
        """

        roles = Role._query().all()
        roles_data = RoleSchema(
            many=True,
            only=['id', 'title'],
        ).dump(roles).data

        return jsonify({
            'status': 'success',
            'message': SUCCESS_MESSAGES['fetched'].format('Roles'),
            'data': roles_data,
        })
