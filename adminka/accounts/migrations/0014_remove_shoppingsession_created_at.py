# Generated by Django 4.1.1 on 2022-09-24 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_shoppingsession_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingsession',
            name='created_at',
        ),
    ]
