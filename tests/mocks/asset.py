"""
A set of mock asset data for testing asset creation
"""
ASSET_TWO = {
    "tag": "Fred Macbook",
    "serial": "sbgdvt4528j8gg",
    "customAttributes": {}
}
ASSET_THREE = {
    "tag": "King Macbook",
    "serial": "sbgdvt4528j8gg",
}
ASSET_FOUR = {
    "tag": "Kingg Macbook",
    "serial": "sbgdvt4528j8gg",
    "custom_attributes": {
        "waranty": "10 yr"
    }
}
ASSET_FIVE = {"tag": "Kinngg Macbook", "serial": "sbgdvt4528j8gg"}

ASSET_NO_CUSTOM_ATTRS = {"tag": "Fred\'s Macbook", "serial": "sbgdvt4528j8gg"}

ASSET_EMPTY_CUSTOM_ATTRS = {
    "tag": "Fred\'s Macbook",
    "serial": "sbgdvt4528j8gg",
    "customAttributes": {}
}

ASSET_NO_TAG = {"serial": "sbgdvt4528j8hg"}

ASSET_NO_SERIAL = {"tag": "Jude\'s Macbook"}

ASSET_NONEXISTENT_CATEGORY = {
    "tag": "Fred\'s Macbook",
    "serial": "sbgdvt4528j8gg",
    "assetCategoryId": "-LEiS7lgOu3VmeEBg5cUtt"
}

ASSET_INVALID_CATEGORY_ID = {
    "tag": "Fred\'s Macbook",
    "serial": "sbgdvt4528j8gg",
    "assetCategoryId": "-%LEiS7lgOu3VmeEBg5cU"
}

ASSET_VALID_CUSTOM_ATTRS = {
    'tag': 'abcd1234',
    'serial': '5432A2',
    'custom_attributes': {
        'waranty': '9876A',
        'length': '12cm'
    }
}

ASSET_DATA_EDITS = {'serial': 'EditedSerial123', 'tag': 'EditedTag123'}
