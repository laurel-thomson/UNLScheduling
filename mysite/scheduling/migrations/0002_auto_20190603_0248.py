# Generated by Django 2.0.13 on 2019-06-03 02:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoomPrivilege',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privilege_level', models.CharField(max_length=50)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.Room')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoomTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('available_until', models.DateTimeField()),
                ('schedule_completed', models.BooleanField(default=False, verbose_name='Schedule completed')),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.Room')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SchedulePreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=50, verbose_name='Day')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('room_term_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.RoomTerm')),
            ],
        ),
        migrations.AddField(
            model_name='schedulepreference',
            name='time_slot_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.TimeSlot'),
        ),
        migrations.AddField(
            model_name='schedulepreference',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scheduleduser',
            name='time_slot_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.TimeSlot'),
        ),
        migrations.AddField(
            model_name='scheduleduser',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
