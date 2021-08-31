# Generated by Django 3.2.6 on 2021-08-31 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('captain', models.CharField(blank=True, max_length=100, null=True)),
                ('vice_captain', models.CharField(blank=True, max_length=100, null=True)),
                ('create', models.DateTimeField(auto_now=True, max_length=100, null=True)),
                ('members', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('subscribers', models.JSONField(blank=True, default=[], max_length=400, null=True)),
                ('room_type', models.CharField(choices=[('users', 'users'), ('groups', 'groups'), ('team', 'team'), ('game', 'game'), ('tournament', 'tournament'), ('streaming', 'streaming')], max_length=20, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, default='media/None/default.png', null=True, upload_to='')),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, max_length=400, null=True)),
                ('is_favorite', models.BooleanField(blank=True, default=False, null=True)),
                ('package_type', models.CharField(blank=True, max_length=100, null=True)),
                ('product_name', models.CharField(blank=True, max_length=100, null=True)),
                ('prodcut_amount', models.PositiveIntegerField(default=0)),
                ('item_quantity', models.PositiveIntegerField(default=0)),
                ('previous_work_Description', models.TextField(blank=True, max_length=400, null=True)),
                ('ratings', models.IntegerField(blank=True, max_length=100, null=True)),
                ('reviews', models.CharField(blank=True, max_length=100, null=True)),
                ('project_gallery', models.ForeignKey(blank=True, default='media/None/default.png', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.image')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumb', models.ImageField(blank=True, default='media/None/default.png', null=True, upload_to=None)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('rank', models.PositiveIntegerField(blank=True, default=0)),
                ('created', models.DateTimeField(auto_now=True)),
                ('members', models.ManyToManyField(to='api.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(blank=True, max_length=100, null=True)),
                ('service_image', models.ImageField(blank=True, null=True, upload_to=None)),
                ('service_minAmount', models.PositiveIntegerField(default=0)),
                ('service_maxAmount', models.PositiveIntegerField(default=0)),
                ('rating', models.IntegerField(blank=True, default=0)),
                ('review', models.TextField(blank=True, null=True)),
                ('vendor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.vendors')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_Type', models.CharField(choices=[('Active', 'Active'), ('Completed', 'Completed')], max_length=20, null=True)),
                ('order_status', models.CharField(choices=[('Order_Placed', 'Order_Placed'), ('Confirmed', 'Confirmed'), ('On Process', 'On Process'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], max_length=20, null=True)),
                ('order_datetime', models.DateTimeField(blank=True, max_length=100, null=True)),
                ('event_title', models.CharField(blank=True, max_length=100, null=True)),
                ('event_type', models.CharField(blank=True, max_length=100, null=True)),
                ('event_date', models.DateField(blank=True, max_length=100, null=True)),
                ('event_time', models.TimeField()),
                ('event_location', models.CharField(blank=True, max_length=100, null=True)),
                ('delivery_address', models.CharField(blank=True, max_length=100, null=True)),
                ('total_amount', models.PositiveIntegerField(blank=True, default=0)),
                ('taxes', models.PositiveIntegerField(blank=True, default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_message', models.CharField(blank=True, max_length=100, null=True)),
                ('last_messageDate', models.DateField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.vendors')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_createdDate', models.DateField(blank=True, max_length=100, null=True)),
                ('cart_createdTime', models.TimeField()),
                ('cartID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
