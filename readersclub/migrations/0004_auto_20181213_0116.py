# Generated by Django 2.0.8 on 2018-12-13 01:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readersclub', '0003_create_group_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='picture_url',
            field=models.CharField(default='../../static/readersclub/harry-potter-clipart-black-and-white-638462-2576998.jpg', max_length=200),
        ),
        migrations.AddField(
            model_name='book',
            name='picture_url',
            field=models.CharField(default='../../static/readersclub/logo.png', max_length=200),
        ),
        migrations.AlterField(
            model_name='book',
            name='rate',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]