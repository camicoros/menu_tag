from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class MenuItem(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('menu:item', args=(self.slug,))

    def __str__(self):
        return self.title


class Menu(models.Model):
    title = models.CharField(max_length=100, unique=True)
    menu_items = models.ManyToManyField(MenuItem, related_name='menus', through='MenuItemOrder')

    def __str__(self):
        return self.title


class MenuItemOrder(models.Model):
    order = models.PositiveSmallIntegerField(default=0)
    menu_item = models.ForeignKey(MenuItem, related_name='menu_order', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, related_name='ordered_menu_items', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order}"

    class Meta:
        ordering = ('order', )








