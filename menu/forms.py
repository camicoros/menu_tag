from django import forms
from django.core.exceptions import ValidationError

from .models import MenuItemOrder


class MenuItemOrderForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=MenuItemOrder.objects.all(),
        widget=forms.Select,
        required=False,
        blank=True,
    )

    class Meta:
        model = MenuItemOrder
        fields = '__all__'

    def clean(self):
        def is_recursive(_parent, _item, depth):
            max_depth = 10
            if depth > max_depth or (self.instance.id is not None and (_parent.menu_item == _item)):
                return True
            elif _parent.parent:
                return is_recursive(_parent.parent, _item, depth+1)
            return False

        cleaned_data = super().clean()

        menu_item = self.cleaned_data.get('menu_item')
        parent = self.cleaned_data.get('parent')
        if parent and is_recursive(parent, menu_item, 0):
            raise ValidationError(f'Change parent for {menu_item.title}! It\'s too recursive!')

        return cleaned_data
