from copy import deepcopy

from django import template
from django.db.models import Count

from ..models import MenuItemOrder

register = template.Library()


class MenuNode:
    def __init__(self, object=None, parent=None, level=0, active_slug=''):
        self.level = level
        self.menu_item = object.menu_item if object else None
        self.parent = parent
        self.is_open = False
        self.is_active = False
        self.children = []

        if self.menu_item and active_slug == self.menu_item.slug:
            self.is_active = True
            self.activate_node()

    @property
    def get_absolute_url(self):
        if self.menu_item:
            return self.menu_item.get_absolute_url

    @property
    def title(self):
        if self.menu_item:
            return self.menu_item.title
        return ""

    def activate_node(self):
        self.is_open = True
        if self.parent:
            self.parent.activate_node()

    def add_child_node(self, child, active_slug):
        new_child = MenuNode(child, self, self.level+1, active_slug)
        self.children.append(new_child)
        return new_child

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title


def create_menu(menu_items, active_menu_item):
    def add_children(parent, index=0):
        while index < total_count:
            item = menu_items[index]
            item_level = item.menu_position.count('-')
            if parent.level == item_level:
                parent.add_child_node(item, active_menu_item)
                index += 1
            elif parent.level > item_level:
                return index
            else:
                index = add_children(parent.children[-1], index)
        return index

    total_count = len(menu_items)
    core_node = MenuNode(level=0, active_slug=active_menu_item)
    add_children(core_node, 0)

    return core_node.children


def get_slug(path):
    if len(path) and path[-1] == '/':
        path = path[:-1]
    return path.split('/')[-1]


@register.inclusion_tag('menu/tags/menu.html', takes_context=True)
def menu(context, menu_name):
    request = context['request']
    active_menu_slug = get_slug(request.path)
    menu_items = MenuItemOrder.objects.filter(
        menu__title=menu_name
    ).select_related(
        'menu_item',
        'parent'
    ).prefetch_related(
        'children'
    )
    menu_nodes = create_menu(menu_items, active_menu_slug)
    return {'menu_items': menu_nodes, 'is_open': True}
