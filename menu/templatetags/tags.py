from django import template
from menu.models import Menu


register = template.Library()

@register.inclusion_tag('menu/results.html')
def draw_menu(name):
    subs = Menu.objects.get(name=name).submenus.all()
    return {'submenus': subs}