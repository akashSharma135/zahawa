# Generated by Django 3.2.6 on 2021-09-09 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20210907_0637'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CreateCart',
            new_name='CartItem',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='cartID',
            new_name='user',
        ),
    ]
