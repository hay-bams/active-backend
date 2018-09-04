"""Input control enums Module"""

from enum import Enum


class InputControlChoiceEnum(Enum):
    """
    Input controls enums
    """

    TEXTAREA = "textarea"
    TEXT = "text"
    DROPDOWN = "dropdown"
    CHECKBOX = "checkbox"
    RADIOBUTTON = "radio button"
    DATE = "date added"

    @classmethod
    def get_multichoice_fields(cls):
        return [cls.DROPDOWN.value, cls.CHECKBOX.value, cls.RADIOBUTTON.value]
    
    @classmethod
    def get_singlechoice_fields(cls):
        return [cls.TEXTAREA.value, cls.TEXT.value]
    
    @classmethod
    def get_all_choices(cls):
        return cls.get_multichoice_fields() + cls.get_singlechoice_fields()
