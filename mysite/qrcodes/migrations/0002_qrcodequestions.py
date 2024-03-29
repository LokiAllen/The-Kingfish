# Generated by Django 5.0.2 on 2024-02-17 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrcodes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QrCodeQuestions',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=254)),
                ('answer', models.CharField(max_length=254)),
                ('time', models.IntegerField(default=30)),
                ('reward', models.IntegerField(default=2)),
            ],
            options={
                'db_table': 'qrcodequestions',
            },
        ),
    ]
