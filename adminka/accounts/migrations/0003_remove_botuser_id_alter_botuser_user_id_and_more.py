# Generated by Django 4.1.1 on 2022-09-24 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_user_botuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botuser',
            name='id',
        ),
        migrations.AlterField(
            model_name='botuser',
            name='user_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='ShoppingSession',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.IntegerField()),
                ('created_at', models.DateField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.botuser')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('created_at', models.DateField(auto_now=True)),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.shoppingsession')),
            ],
        ),
    ]
