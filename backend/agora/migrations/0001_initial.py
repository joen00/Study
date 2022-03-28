# Generated by Django 3.2.8 on 2021-11-26 21:58

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ONEUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile')),
                ('fcm_id', models.CharField(blank=True, default='EMPTY', max_length=254, null=True)),
                ('group_joined', models.TextField(blank=True, default=' ')),
                ('user_goal', models.TextField(blank=True, null=True)),
                ('score', models.IntegerField(default=0)),
                ('phone_number', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RoomKeyWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StudyEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('explain', models.TextField()),
                ('attribute', models.SmallIntegerField()),
                ('date_start', models.DateTimeField(blank=True, null=True)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_on', models.BooleanField(blank=True, default=True)),
                ('date_set', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom_pk', models.IntegerField()),
                ('score', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('ratee_pk', models.ForeignKey(on_delete=models.SET('deleted_user'), related_name='ratee_pk', to=settings.AUTH_USER_MODEL)),
                ('rater_pk', models.ForeignKey(on_delete=models.SET('deleted_user'), related_name='rater_pk', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMoney',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_commit', models.DateTimeField(auto_now_add=True)),
                ('payment', models.PositiveIntegerField()),
                ('attribute', models.BooleanField()),
                ('total_money', models.PositiveIntegerField()),
                ('user_pk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserKeyWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword_pk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agora.keyword')),
                ('user_pk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]