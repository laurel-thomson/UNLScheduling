# Generated by Django 2.0.13 on 2019-06-11 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0005_auto_20190610_0749'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreferenceOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='schedulepreference',
            name='preference_type',
        ),
        migrations.AddField(
            model_name='schedulepreference',
            name='preference_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='scheduling.PreferenceOption'),
            preserve_default=False,
        ),
    ]
