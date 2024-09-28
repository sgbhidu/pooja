from django.utils.text import slugify

import uuid

def generate_slug(description:str )-> str:
    from .models import color_quantity,pooja_products
    description=slugify(description)
    while(color_quantity.objects.filter(slug=description).exists()):
        description= f'{slugify(description)}-{str(uuid.uuid4())[:4]}'

    return description
