# Generated by Django 3.2 on 2024-08-10 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=256, unique=True, verbose_name='Почта'),
        ),
    ]