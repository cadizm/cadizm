# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('headspace', '0002_auto_20171006_1950'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='library',
            name='book_id',
        ),
        migrations.RenameField(
            model_name='library',
            old_name='book_id',
            new_name='book',
        ),
        migrations.RenameField(
            model_name='library',
            old_name='username',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='library',
            unique_together=set([('user', 'book')]),
        ),
        migrations.AddIndex(
            model_name='library',
            index=models.Index(fields=['user'], name='book'),
        ),
    ]
