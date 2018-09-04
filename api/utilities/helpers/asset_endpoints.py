"""Module for asset endpoints helpers."""
from ..model_serializers.asset import AssetSchema


def create_asset_response(asset_instance, message, handle_many=False):
    """Helper function to create a response after asset operations

    :param asset_instance: An single asset instance or a collection of asset
                           instances in a query object
    :type asset_instance: SQLAlchemy query object
    :param message: Message to be passed with the response
    :type message: string
    :param handle_many: Flag to let the function know whether to handle a
                        single instance or a collection, defaults to False
    :param handle_many: bool, optional
    """

    schema = AssetSchema(
        many=handle_many,
        only=['id', 'tag', 'serial', 'custom_attributes', 'asset_category_id'])

    response = {
        "status": "success",
        "message": message,
        "data": schema.dump(asset_instance).data
    }

    return response
