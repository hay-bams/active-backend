"Module for asset category request data"

valid_asset_category_data = {  # pylint: disable=C0103
    "name":
    "Headset",
    "customAttributes": [{
        "key": "brand",
        "label": "brand",
        "isRequired": True,
        "inputControl": "text",
    }, {
        "key": "color",
        "label": "color",
        "isRequired": True,
        "inputControl": "dropdown",
        "choices": ["blue", "red", "black"]
    }]
}

asset_category_with_two_wrong_input_control = {  # pylint: disable=C0103
    "name":
    "Headdsett",
    "customAttributes": [{
        "key": "brand",
        "label": "brand",
        "isRequired": True,
        "inputControl": "textt",
    }, {
        "key": "color",
        "label": "color",
        "isRequired": True,
        "inputControl": "wrong input control",
        "choices": ["blue", "red", "black"]
    }]
}

asset_category_with_one_wrong_input_control = {  # pylint: disable=C0103
    "name":
    "Headsettt",
    "customAttributes": [{
        "key": "brand",
        "label": "brand",
        "isRequired": True,
        "inputControl": "text",
    }, {
        "key": "color",
        "label": "color",
        "isRequired": True,
        "inputControl": "wrong input control"
    }]
}

asset_category_data_without_choices = {  # pylint: disable=C0103
    "name":
    "Headdset",
    "customAttributes": [{
        "key": 'brand',
        "label": "brand",
        "isRequired": True,
        "inputControl": "text",
    }, {
        "key": 'color',
        "label": "color",
        "isRequired": True,
        "inputControl": "dropdown"
    }]
}

valid_asset_category_data_without_attributes = {"name": "Headset"}  # pylint: disable=C0103

invalid_asset_category_data = {  # pylint: disable=C0103
    "name":
    "Headset",
    "customAttributes": [{
        "labe": "brand",
        "is_required": True,
        "inputControl": "text",
    }, {
        "label": "color",
        "isRequired": True,
        "_key": 'color',
        "inputControl": "dropdown",
        "choices": ["blue", "red", "black"]
    }]
}
