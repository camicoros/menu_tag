from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Menu, MenuItemOrder, MenuItem


class MenuItemOrderInline(admin.TabularInline):
    model = MenuItemOrder
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = (MenuItemOrderInline,)


class MenuItemForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=MenuItem.objects.all(),
        widget=forms.Select,
        required=False,
        blank=True,
    )

    class Meta:
        model = MenuItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = MenuItem.objects.exclude(id=self.instance.id)

    def clean_parent(self):
        def is_recursive(parent, depth):
            max_depth = 10
            if depth > max_depth or (self.instance.id is not None and (parent.id == self.instance.id)):
                return True
            elif parent.parent:
                return is_recursive(parent.parent, depth+1)
            return False

        parent = self.cleaned_data.get('parent')
        if parent and is_recursive(parent, 0):
            raise ValidationError('Change parent! It\'s too recursive!')
        return parent


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )
    form = MenuItemForm

