from django.contrib import admin

from .models import Menu, MenuItemOrder, MenuItem
from .forms import MenuItemOrderForm


class MenuItemOrderInline(admin.TabularInline):
    model = MenuItemOrder
    extra = 0
    form = MenuItemOrderForm
    fields = ('level', 'menu_item', 'parent')
    ordering = ('menu_position', )
    readonly_fields = ('level', )

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(MenuItemOrderInline, self).get_formset(request, obj=None, **kwargs)
        if request._obj_ is not None:
            formset.form.base_fields["parent"].queryset = MenuItemOrder.objects.filter(menu=request._obj_)
        return formset

    def level(self, obj):
        return "{}{}".format("----" * obj.menu_position.count('-'), "----|")


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = (MenuItemOrderInline,)

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )

