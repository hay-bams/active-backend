"""Module for User model."""

from .database import db
from .base.base_model import BaseModel


class User(BaseModel):
    """Class for user db table."""

    __tablename__ = 'users'

    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    image_url = db.Column(db.String)
    center_id = db.Column(db.String, db.ForeignKey('centers.id'))
    role_id = db.Column(db.String, db.ForeignKey('roles.id'), nullable=False)

    def get_child_relationships(self):
        """
        Method to get all child relationships a model has. Overide in the
        subclass if the model has child models.
        """
        return None

    def __repr__(self):
        return f'<User {self.name}>'
