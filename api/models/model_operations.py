"""Module for generic model operations mixin."""

import re

from flask import request

from .database import db
from api.utilities.dynamic_filter import DynamicFilter
from ..utilities.validators.delete_validator import delete_validator
from ..middlewares.base_validator import ValidationError
from ..utilities.messages.error_messages import database_errors


class ModelOperations(object):
    """Mixin class with generic model operations."""
    def save(self):
        """
        Save a model instance
        """
        db.session.add(self)
        db.session.commit()
        return self

    def _update(self, **kwargs):
        """
        update entries
        """
        for field, value in kwargs.items():
            setattr(self, field, value)
        db.session.commit()

    @classmethod
    def get(cls, id):
        """
        return entries by id
        """
        return cls.query.filter_by(id=id, deleted=False).first()

    @classmethod
    def get_or_404(cls, id):
        """
        return entries by id
        """

        record = cls.query.get(id)

        if not record or record.deleted:
            raise ValidationError({
                'message': f'{re.sub(r"(?<=[a-z])[A-Z]+",lambda x: f" {x.group(0).lower()}" , cls.__name__)} not found'  # noqa
            }, 404)

        return record

    def get_child_relationships(self):
        """
        Method to get all child relationships a model has.
        This is used to ascertain if a model has relationship(s) or
        not when validating delete operation.
        It must be overridden in subclasses and takes no argument.
        :return None if there are no child relationships.
        A tuple of all child relationships eg (self.relationship_field1,
        self.relationship_field2)
        """
        raise NotImplementedError("The get_relationships method must be overridden in all child model classes") #noqa

    def delete(self):
        """
        Soft delete a model instance.
        """
        relationships = self.get_child_relationships()
        if delete_validator(relationships):
            self.deleted = True
            if request.decoded_token:
                self.deleted_by = request.decoded_token['UserInfo']['name']
            db.session.add(self)
            db.session.commit()
        else:
            relationship_names = []
            for relationship in relationships:
                relationship_names.append(f'{relationship.first().__class__.__name__}(s)')
            raise ValidationError(dict(
                message=database_errors['model_delete_children'].format(
                    self.__class__.__name__, ', '.join(relationship_names)
                )), status_code=403)

    @classmethod
    def _query(cls, filter_condition=None):
        """
        Returns filtered database entries. It takes model class and
        filter_condition and returns database entries based on the filter
        condition, eg, User._query('name,like,john'). Apart from 'like', other
        comparators are eq(equal to), ne(not equal to), lt(less than),
        le(less than or equal to) gt(greater than), ge(greater than or equal to)
        :param filter_condition:
        :return: an array of filtered records
        """
        
        if filter_condition:
            dynamic_filter = DynamicFilter(cls)
            return dynamic_filter.filter_query(filter_condition)
        return cls.query.filter_by(deleted=False)


    @classmethod
    def count(cls):
        """
        Returns total entries in the database
        """
        counts = cls.query.count()
        return counts
