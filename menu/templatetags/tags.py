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
    if not active_node:
        items_dict = {'name': name, 'submenus': []}
        return {'items': items_dict, 'name': name}
    items_dict = {'name': name, 'submenus': build_tree(items)}
    # pp.pprint(items_dict)
    pp.pprint(depth_first_search(items_dict, active_node)[0])
    return {'items': items_dict, 'name': name}

def build_tree(items, parent=None):
    res = []
    for item in items:
        if item.parent == parent:
            res.append({'name': item.name, 'submenus': build_tree(items, item)})
    return res


def depth_first_search(structure, stop_name):
    current_name = structure['name']
    res = {'name': current_name, 'submenus': []}

    if current_name == stop_name:
        if structure['submenus']:
            for submenu in structure['submenus']:
                res['submenus'].append({'name': submenu['name'], 'submenus': []})
            return (res, True)
        return (res, True)

    if not structure['submenus']:
        return (res, False)
    
    for submenu in structure['submenus']:
        result, found = depth_first_search(submenu, stop_name)
        res['submenus'].append(result)
        if found:
            return (res, True)

    return (res, False)