# Generated by Django 4.0.6 on 2022-07-16 14:20

import datetime
import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6, verbose_name='code')),
                ('expire_time_start', models.DateTimeField(default=datetime.datetime.now, verbose_name='start of expire time')),
                ('expire_time_end', models.DateTimeField(default=datetime.timedelta(seconds=300), verbose_name='end of the expire time')),
                ('code_type', models.IntegerField(choices=[(1, 'Signup'), (2, 'Login'), (4, 'sms')], null=True, verbose_name='code type')),
                ('phone_number', models.CharField(max_length=11, verbose_name='phone number')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone_number', models.CharField(max_length=11, unique=True)),
                ('username', models.CharField(blank=True, max_length=250, null=True)),
                ('first_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=250, verbose_name='last name')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
