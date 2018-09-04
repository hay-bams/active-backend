"""Module for a generalized delete validator."""


def delete_validator(relationships):
    """Check if instance has any children before soft deleting.

    Takes in a tuple of the child model field names with the
    backref and returns true if the parent has no children with the deleted
    flag set to true and returns false otherwise.

    Args:
        relationships: tuple of relationship fields

    Returns:
        bool: True if the instance has no children with the deleted flag,
              False otherwise.
    """

    if not relationships:
        return True

    for relationship in relationships:
        is_deletable = relationship.filter_by(deleted=False).first()
        if is_deletable:
            is_deletable = False
            break
        else:
            is_deletable = True
            continue
    return is_deletable
