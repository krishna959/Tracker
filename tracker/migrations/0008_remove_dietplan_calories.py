# Generated by Django 5.1.6 on 2025-02-25 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_alter_dietplan_calories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dietplan',
            name='calories',
        ),
    ]
