from .base.base_model import BaseModel
from .database import db


class Attribute(BaseModel):
    """
    Model for attributes
    """

    _key = db.Column(db.String(60), nullable=False)
    label = db.Column(db.String(60), nullable=False)
    is_required = db.Column(db.Boolean, nullable=False)
    input_control = db.Column(db.String(60), nullable=False)
    choices = db.Column(db.String(250), nullable=True)
    asset_category_id = db.Column(db.String,
                                  db.ForeignKey('asset_categories.id'),
                                  nullable=False)

    def get_child_relationships(self):
        """
        Method to get all child relationships a model has. Overide in the
        subclass if the model has child models.
        """
        return None

    def __repr__(self):
        return '<Attribute {}>'.format(self.label)
