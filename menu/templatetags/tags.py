from django import template
from menu.models import MenuItem
import pprint


pp = pprint.PrettyPrinter(indent=2)

register = template.Library()

@register.inclusion_tag('menu/results.html', takes_context=True)
def draw_menu(context, name):
    items = MenuItem.objects.filter(menu__name=name).select_related('parent').all()
    menu_names = context['request'].GET
    active_node = menu_names.get(name)
    items_list = build_tree(items)
    pp.pprint(items_list)
    search_item(items_list, active_node)
    return {'items': items_list, 'name': name}

def build_tree(items, parent=None):
    res = []
    for item in items:
        if item.parent == parent:
            res.append({'name': item.name, 'submenus': build_tree(items, item)})
    return res

def search_item(tree, name, found=False):
    for node in tree:
        print(node['name'])
        if node['name'] == name:
            found = True
            return found
        if 'submenus' in node and not found:
            found = search_item(node['submenus'], name, found)
            return found