from django import template

from ..models import MenuItemOrder

register = template.Library()


class MenuNode:
    def __init__(self, object, parent=None, active_slug=''):
        self.object = object
        self.menu_item = self.object.menu_item
        self.parent = parent
        self.is_active = False
        self.current_active = False
        self.children = []

        if active_slug == self.menu_item.slug:
            self.current_active = True
            self.activate_node()

    @property
    def get_absolute_url(self):
        return self.menu_item.get_absolute_url

    @property
    def title(self):
        return self.menu_item.title

    def activate_node(self):
        self.is_active = True
        if self.parent:
            self.parent.activate_node()

    def add_child_node(self, child, active_slug):
        new_child = MenuNode(child, self, active_slug)
        self.children.append(new_child)
        return new_child

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title


def create_menu(menu_items, active_menu_item):
    def add_children(c_item, m_items, a_m_item):
        children = m_items.filter(menu_item__parent=c_item.menu_item)
        for child in children:
            new_child = c_item.add_child_node(child, a_m_item)
            add_children(new_child, m_items, a_m_item)

    core_menu = [MenuNode(item, None, active_menu_item) for item in menu_items if not item.menu_item.parent]
    for core_item in core_menu:
        add_children(core_item, menu_items, active_menu_item)

    return core_menu


def get_slug(path):
    if len(path) and path[-1] == '/':
        path = path[:-1]
    return path.split('/')[-1]


@register.inclusion_tag('menu/tags/menu.html', takes_context=True)
def menu(context, menu_name):
    request = context['request']
    active_menu_slug = get_slug(request.path)
    menu_items = MenuItemOrder.objects.filter(menu__title=menu_name).select_related('menu_item', 'menu_item__parent').prefetch_related('menu_item__children')
    menu_nodes = create_menu(menu_items, active_menu_slug)
    return {'menu_items': menu_nodes, 'active': True}
