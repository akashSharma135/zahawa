# Generated by Django 3.2.6 on 2021-09-16 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='loyalty_program',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]