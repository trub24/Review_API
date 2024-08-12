# Generated by Django 3.2 on 2024-08-08 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'админ'), ('moderator', 'модератор'), ('user', 'юзер')], default='user', max_length=16, verbose_name='Роль'),
        ),
    ]