# Generated by Django 3.2.6 on 2021-09-07 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20210906_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='packages',
            name='amount',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='packages',
            name='image',
            field=models.ImageField(blank=True, default='media/default.png', null=True, upload_to=''),
        ),
    ]