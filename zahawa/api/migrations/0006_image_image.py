# Generated by Django 3.2.6 on 2021-09-02 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_createcart_packages'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, default='media/default.png', null=True, upload_to=None),
        ),
    ]
