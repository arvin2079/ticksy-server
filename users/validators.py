import re


def validate_email(value):
    if re.match(r'^([A-Z|a-z|0-9](\.|_){0,1})+[A-Z|a-z|0-9]\@([A-Z|a-z|0-9])+((\.){0,1}[A-Z|a-z|0-9]){2}\.[a-z]{2,3}$',
                value):
        return True
    return False


def validate_identifier_code(value):
    return True


def validate_identifier_image(value):
    return True


def validate_firstname(value):
    return is_persian(value)


def validate_lastname(value):
    return is_persian(value)


def is_persian(value):
    if re.match(r'[۱۲۳۴۵۶۷۸۹۰ آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+', value):
        return True
    return False


def is_english(value):
    if re.match(r'^[a-zA-Z ]+$', value):
        return True
    return False
