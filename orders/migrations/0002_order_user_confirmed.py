# Generated by Django 5.1.4 on 2025-01-16 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
