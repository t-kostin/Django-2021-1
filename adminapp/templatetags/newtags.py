from django import template
from django.conf import settings

register = template.Library()


def add_path_for_product_images(string):
    if not string:
        string = 'product_images/product-placeholder.jpg'
    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='avatar_path')
def add_path_for_avatars(string):
    if not string:
        string = 'user_avatars/avatar-placeholder.jpg'
    return f'{settings.MEDIA_URL}{string}'


register.filter('prod_img_path', add_path_for_product_images)
