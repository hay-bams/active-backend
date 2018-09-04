"""Module to seed asset-category and attribute tables"""

from api.models import AssetCategory, Attribute


def seed_asset_category():
    # Create apple tv asset category and its attributes
    apple_tv = AssetCategory(name='Apple TV')
    apple_tv_attributes_data = [
        {
            '_key': 'warranty',
            'label': 'Warranty',
            'is_required': False,
            'input_control': 'text'
        },
        {
            '_key': 'size',
            'label': 'Size',
            'is_required': False,
            'input_control': 'dropdown',
            'choices': 'multiple choices'
        }
    ]

    apple_tv_attributes = [
        Attribute(
            _key=data['_key'], label=data['label'], is_required=data[
                'is_required'], input_control=data['input_control'],
            choices=data.get('choices')
        ) for data in apple_tv_attributes_data
    ]

    for attribute in apple_tv_attributes:
        apple_tv.attributes.append(attribute)

    apple_tv.save()

    # Create laptops asset category and its attributes
    laptops = AssetCategory(name='Laptops')
    laptops_attribute_data = [
        {
            '_key': 'color',
            'label': 'Color',
            'is_required': False,
            'input_control': 'dropdown',
            'choices': 'multiple choices'
        },
        {
            '_key': 'length',
            'label': 'Length',
            'is_required': False,
            'input_control': 'text'
        }
    ]

    laptops_attribute = [
        Attribute(
            _key=data['_key'], label=data['label'], is_required=data[
                'is_required'], input_control=data['input_control'],
            choices=data.get('choices')
        ) for data in laptops_attribute_data
    ]

    for attribute in laptops_attribute:
        laptops.attributes.append(attribute)

    laptops.save()

    # Create USB dongles asset category and its attributes
    usb_dongles = AssetCategory(name='USB Dongles')
    usb_dongles_attributes_data = [
        {
            '_key': 'color',
            'label': 'Color',
            'is_required': False,
            'input_control': 'dropdown',
            'choices': 'multiple choices'
        },
        {
            '_key': 'length',
            'label': 'Length',
            'is_required': False,
            'input_control': 'text-area'
        }
    ]

    usb_dongles_attributes = [
        Attribute(
            _key=data['_key'], label=data['label'], is_required=data[
                'is_required'], input_control=data['input_control'],
            choices=data.get('choices')
        ) for data in usb_dongles_attributes_data
    ]

    for attribute in usb_dongles_attributes:
        usb_dongles.attributes.append(attribute)

    usb_dongles.save()

    # Create chromebooks asset category and its attributes
    chromebooks = AssetCategory(name='ChromeBooks')
    chromebooks_attributes_data = [
        {
            '_key': 'color',
            'label': 'Color',
            'is_required': True,
            'input_control': 'text-area',
            'choices': 'multiple choices'
        },
        {
            '_key': 'screenSize',
            'label': 'Screen size',
            'is_required': True,
            'input_control': 'text'
        }
    ]

    chromebooks_attributes = [
        Attribute(
            _key=data['_key'], label=data['label'], is_required=data[
                'is_required'], input_control=data['input_control'],
            choices=data.get('choices')
        ) for data in chromebooks_attributes_data
    ]

    for attribute in chromebooks_attributes:
        chromebooks.attributes.append(attribute)

    chromebooks.save()

    # Create chairs asset category and its attributes
    chairs = AssetCategory(name='Chairs')
    chairs_attributes_data = [
        {
            '_key': 'type',
            'label': 'Type',
            'is_required': True,
            'input_control': 'radio button',
            'choices': 'multiple choices'
        }
    ]

    chairs_attributes = [
        Attribute(
            _key=data['_key'], label=data['label'], is_required=data[
                'is_required'], input_control=data['input_control'],
            choices=data.get('choices')
        ) for data in chairs_attributes_data
    ]

    for attribute in chairs_attributes:
        chairs.attributes.append(attribute)

    chairs.save()
