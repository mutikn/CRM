# Generated by Django 5.1.7 on 2025-03-11 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='employee',
            new_name='user',
        ),
    ]
