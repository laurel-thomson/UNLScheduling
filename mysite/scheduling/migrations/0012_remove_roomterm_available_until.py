# Generated by Django 2.0.13 on 2019-07-29 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0011_auto_20190721_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomterm',
            name='available_until',
        ),
    ]
