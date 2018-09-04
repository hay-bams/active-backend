"""Module to seed role table"""

from api.models import Role
from api.models.database import db

def seed_roles():
    """
    Seeds sample roles
    """

    titles = [
        'Operations Intern',
        'Operations Coordinator',
        'Operations Assistant',
        'Operations Manager',
    ]

    for title in titles:
        db.session.add(Role(title=title))
    db.session.commit()
