# Generated by Django 5.0.2 on 2024-02-23 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_userinfo_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfriends',
            name='user',
            field=models.IntegerField(),
        ),
    ]
