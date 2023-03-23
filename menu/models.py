from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


class MenuItem(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

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
    menu_item = models.ForeignKey(MenuItem, related_name='menu_order', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, related_name='ordered_menu_items', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, blank=True, null=True)
    menu_position = models.CharField(max_length=150, editable=False)

    def __str__(self):
        return f"{self.menu_item.title}"

    @property
    def formatted_id(self):
        if self.id:
            return f"{self.id:03}"
        elif self._meta.model.objects.count() > 0:
            obj = self._meta.model.objects.latest('id')
            return f"{obj.id+1:03}"
        else:
            return f"{1:03}"

    def update_position(self):
        if self.parent:
            self.menu_position = "-".join((self.parent.menu_position, self.formatted_id))
        else:
            self.menu_position = self.formatted_id

    def save(self, started=None, *args, **kwargs):
        self.update_position()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('menu_position', )
        unique_together = (['menu', 'menu_item'],)


@receiver(post_save, sender=MenuItemOrder, dispatch_uid="update_menu_position")
def update_position(sender, instance, **kwargs):
    for child in instance.children.all():
        try:
            child.save()
        except Exception as e:
            print(e)








