"""Module for center model"""

from sqlalchemy.dialects.postgresql import JSON

from .base.auditable_model import AuditableBaseModel
from .database import db


class Center(AuditableBaseModel):
    """
    Model for centers
    """

    __tablename__ = 'centers'

    name = db.Column(db.String(60), nullable=False, unique=True)
    image = db.Column(JSON, nullable=False)
    assets = db.relationship(
        'Asset', backref='center', cascade='delete', lazy='dynamic')
    users = db.relationship(
        'User', backref='center', cascade='delete', lazy='dynamic')

    def get_child_relationships(self):
        """
        Method to get all child relationships of this model

        Returns:
             children(tuple): children of this model
        """
        return self.assets, self.users

    def __repr__(self):
        return f'<Center {self.name}>'
