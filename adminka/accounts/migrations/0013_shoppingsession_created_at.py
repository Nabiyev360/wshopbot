# Generated by Django 4.1.1 on 2022-09-24 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_shoppingsession_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingsession',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
    ]
