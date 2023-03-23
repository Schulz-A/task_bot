def name_validate(name):
    if type(name) != str or len(name) > 40:
        raise ValueError("Название не должно быть больше 40 символов")
    return name


def descr_validate(descr):
    if len(descr) > 850:
        raise ValueError("Описание слишком длинное. Не должно привышать 850 символов")
    return descr


def quantity_validate(quantity: str):
    if not quantity.isdigit():
        raise ValueError("Значение должно быть числом")
    return int(quantity)


validators = {
    "name": name_validate,
    "descr": descr_validate,
    "quantity": quantity_validate,
    "price": quantity_validate
}