# Generated by Django 4.1.1 on 2022-09-24 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_botuser_created_at_cartitem_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]