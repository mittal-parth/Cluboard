# Generated by Django 3.2.3 on 2021-05-20 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_delete_info'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='name',
            new_name='item_name',
        ),
    ]
