from django.core.exceptions import ValidationError

import re


def number_validator(value):
    regex = re.compile('[0-9]')
    if regex.search(value) == None:
        raise ValidationError(
                "Value must include number",
                code="value_must_include_number"
                )

def letter_validator(value):
    regex = re.compile('[a-zA-Z]')
    if regex.search(value) == None:
        raise ValidationError(
                "Value must include letter",
                code="value_must_include_letter"
                )

def special_char_exist_validator(value):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(value) == None:
        raise ValidationError(
                "Value must include special char",
                code="value_must_include_special_char"
                )


def special_char_not_exist_validator(value):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(value) != None:
        raise ValidationError(
                "Value must not include special char",
                code="value_must_not_include_special_char"
                )
                