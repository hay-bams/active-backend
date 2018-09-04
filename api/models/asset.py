from sqlalchemy.dialects.postgresql import JSON
from .base.auditable_model import AuditableBaseModel
from .database import db


class Asset(AuditableBaseModel):
    """
    Model for assets
    """
    tag = db.Column(db.String(60), nullable=False, unique=True)
    serial = db.Column(db.String(60), nullable=True)
    custom_attributes = db.Column(JSON, nullable=True)
    asset_category_id = db.Column(
        db.String, db.ForeignKey('asset_categories.id'), nullable=False)
    center_id = db.Column(db.String, db.ForeignKey('centers.id'))

    def get_child_relationships(self):
        """
        Method to get all child relationships a model has. Overide in the
        subclass if the model has child models.
        """
        return None

    def __repr__(self):
        return '<Asset {}>'.format(self.tag)
