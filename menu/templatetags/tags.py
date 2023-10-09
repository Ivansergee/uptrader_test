from django import template
from menu.models import MenuItem


register = template.Library()

@register.inclusion_tag('menu/results.html', takes_context=True)
def draw_menu(context, name):
    items = MenuItem.objects.filter(menu__name=name).select_related('parent').all()
    menu_names = context['request'].GET
    active_node = menu_names.get(name, name)
    items_dict = {'name': name, 'submenus': build_tree(items)}
    filtered = [search_item(items_dict, active_node)[0]]
    return {'menu_name': name, 'items': filtered}

def build_tree(items, parent=None):
    res = []
    for item in items:
        if item.parent == parent:
            res.append({'name': item.name, 'submenus': build_tree(items, item)})
    return res


def search_item(structure, stop_name):
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
        result, found = search_item(submenu, stop_name)
        res['submenus'].append(result)
        if found:
            return (res, True)

    return (res, False)