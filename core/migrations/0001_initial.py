# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-08-20 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('isActive', models.BooleanField(default=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('author', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('url', models.URLField()),
                ('urltoimage', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('isActive', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100)),
                ('uid', models.CharField(blank=True, max_length=100, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('url', models.URLField()),
                ('category', models.CharField(choices=[('business', 'business'), ('entertainment', 'entertainment'), ('general', 'general'), ('health', 'health'), ('science', 'science'), ('sports', 'sports'), ('technology', 'technology'), ('more', 'more')], max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]