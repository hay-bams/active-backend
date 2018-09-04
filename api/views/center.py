"""Module for center resources"""

import os

import cloudinary

from flask_restplus import Resource
from flask import request

from main import api
from api.middlewares.token_required import token_required
from api.utilities.model_serializers.center import CenterSchema
from api.models.center import Center
from api.models.database import db
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.validators.duplicate_validator import validate_duplicate
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.validators.validate_id import validate_id


@api.route('/centers')
class CenterResource(Resource):
    """
    Resource class for creating and getting centers
    """

    @token_required
    @validate_json_request
    def post(self):
        """
        POST method for creating centers.

        Payload should have the following parameters:
            name(str): name of the center
            image(dict): image meta data
        """

        request_data = request.get_json()

        center_schema = CenterSchema(
            only=['name', 'image', 'created_at', 'updated_at'])
        center_data = center_schema.load_object_into_schema(request_data)
        validate_duplicate(Center, name=request_data['name'].title())

        center = Center(**center_data)
        center.save()

        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['created'].format('Center'),
            'data': center_schema.dump(center).data
        }, 201


@api.route('/centers/<string:id>')
class SingleCenterResource(Resource):
    """Resource class for carrying out operations on a single center"""

    @token_required
    @validate_id
    def delete(self, id):  #pylint: disable=C0103, W0622
        """
        A method for deleting a center
        """
        cloudinary.config.update = ({
            'cloud_name':
            os.environ.get('CLOUDINARY_CLOUD_NAME'),
            'api_key':
            os.environ.get('CLOUDINARY_API_KEY'),
            'api_secret':
            os.environ.get('CLOUDINARY_API_SECRET')
        })
        center = Center.get_or_404(id)
        if not (center.assets.all() or center.users.all()):
            db.session.delete(center)
            db.session.commit()
            message = SUCCESS_MESSAGES['hard_delete'].format(center.name)
        else:
            center._update(
                deleted=True,
                deleted_by=request.decoded_token['UserInfo']['name'])
            message = SUCCESS_MESSAGES['soft_delete'].format(center.name)

        cloudinary.api.delete_resources([center.image["public_id"]])

        return {
            'status': 'success',
            'message': message,
        }, 200
