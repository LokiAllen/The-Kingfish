# Generated by Django 5.0.1 on 2024-03-20 16:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0003_alter_useransweredquestion_unique_together"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="answer",
            name="label",
        ),
    ]