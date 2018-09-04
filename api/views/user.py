"""Module for users resource"""

from flask_restplus import Resource

from main import api
from ..models.center import Center
from ..middlewares.base_validator import ValidationError
from ..middlewares.token_required import token_required
from ..utilities.validators.validate_id import validate_id
from ..utilities.messages.error_messages import serialization_errors
from ..utilities.messages.success_messages import SUCCESS_MESSAGES


@api.route('/centers/<string:center_id>/people/<string:person_id>')
class UserResource(Resource):
    """Resource class for users"""

    @token_required
    @validate_id
    def delete(self, center_id, person_id):
        """Delete a user"""

        center = Center.get_or_404(center_id)
        person = center.users.filter_by(id=person_id, deleted=False).first()
        if not person:
            raise ValidationError(
                {
                    'message': serialization_errors['person_not_found']
                }, 404)
        person.delete()

        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['person_deleted'].format(person.name)
        }
