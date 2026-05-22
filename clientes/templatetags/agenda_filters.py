import re
from django import template

register = template.Library()


@register.filter
def guaranies(value):
    try:
        return f"{int(value):,}".replace(',', '.') + " Gs"
    except (ValueError, TypeError):
        return "0 Gs"


@register.filter
def whatsapp_url(telefono):
    """Convierte un número de teléfono al formato wa.me/595XXXXXXXXX."""
    if not telefono:
        return ''
    digits = re.sub(r'\D', '', str(telefono))
    if digits.startswith('595'):
        numero = digits
    elif digits.startswith('0'):
        numero = '595' + digits[1:]
    else:
        numero = '595' + digits
    return f'https://wa.me/{numero}'
