from django.core.exceptions import ValidationError


def validate_name(value):
    """This method validates whether the name has any number"""

    if any(i.isdigit() for i in value):
        raise ValidationError("Item has number")


def validate_number(value):
    """This method validates whether the price has any character"""

    if any(i.isalpha() for i in str(value)):
        raise ValidationError("Price has character")


def validate_quantity(value):
    """This method validates quantity, should be greater than 0"""
    if value < 1:
        raise ValidationError("Quantity should be greater than 0.")
