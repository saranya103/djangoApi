# Generated by Django 4.0.6 on 2022-07-11 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_is_admin_alter_user_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.CharField(max_length=10),
        ),
    ]