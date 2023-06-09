# Generated by Django 4.1.7 on 2023-03-23 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItemOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_position', models.CharField(editable=False, max_length=150)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_menu_items', to='menu.menu')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_order', to='menu.menuitem')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='menu.menuitemorder')),
            ],
            options={
                'ordering': ('menu_position',),
                'unique_together': {('menu', 'menu_item')},
            },
        ),
        migrations.AddField(
            model_name='menu',
            name='menu_items',
            field=models.ManyToManyField(related_name='menus', through='menu.MenuItemOrder', to='menu.menuitem'),
        ),
    ]
