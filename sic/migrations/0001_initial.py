# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('text', models.TextField()),
                ('classification', models.CharField(max_length=1, choices=[('p', 'Positive'), ('n', 'Negative'), ('q', 'Question'), ('u', 'Neutral')])),
                ('start_line', models.PositiveIntegerField()),
                ('end_line', models.PositiveIntegerField()),
                ('start_column', models.PositiveIntegerField()),
                ('end_column', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('text', models.TextField()),
                ('name', models.CharField(max_length=128)),
                ('hash', models.CharField(primary_key=True, max_length=128, serialize=False, unique=True)),
                ('under_discussion', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comment',
            name='license',
            field=models.ForeignKey(to='sic.License', related_name='comments'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comments'),
            preserve_default=True,
        ),
    ]
