# Generated by Django 4.1.1 on 2022-09-24 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_botuser_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingsession',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='botuser',
            name='created_at',
            field=models.DateField(auto_now=True),
        ),
    ]
