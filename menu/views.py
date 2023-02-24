from django.shortcuts import render
from .models import Menu




def show_menu(response, name=None, node=None):
    if name:
        root = Menu.objects.get(name=name)
        tree = {'name': name, 'children': build_tree(root, node)}
        print(tree)

        return render(response, 'menu/menu.html', tree)
    else:
        return render(response, 'menu/index.html')

def build_tree(root, node, stop=False):
    res = []
    if root.submenus.all():
        for item in root.submenus.all():
            if node is None:
                res.append({'name': item.name, 'children': None})
            elif item.name == node:
                res.append({'name': item.name, 'children': build_tree(item, None)})
            else:
                res.append({'name': item.name, 'children': build_tree(item, node)})
    return res