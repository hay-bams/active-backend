"""Module for role model"""

from .base.auditable_model import AuditableBaseModel
from .database import db


class Role(AuditableBaseModel):
    """
    Model for roles
    """

    __tablename__ = 'roles'

    title = db.Column(db.String(60), nullable=False, unique=True) # pylint: disable=E1101
    users = db.relationship( # pylint: disable=E1101
        'User', backref='role', cascade='delete', lazy='dynamic')

    def get_child_relationships(self):
        """
        Method to get all child relationships of this model

        Returns:
             children(tuple): children of this model
        """
        return (self.users,)

    def __repr__(self):
        return f'<Role {self.title}>'
