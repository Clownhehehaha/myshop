# Generated by Django 5.1.3 on 2024-11-27 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]