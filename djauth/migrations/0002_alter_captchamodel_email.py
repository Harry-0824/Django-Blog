# Generated by Django 5.0.3 on 2024-08-07 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='captchamodel',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
